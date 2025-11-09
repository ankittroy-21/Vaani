import time
from vaani.core import config as Config
import os
from dotenv import load_dotenv
from vaani.core import api_key_manager
import random
from datetime import datetime
import sys
import io

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
from vaani.core.voice_tool import bolo_stream as bolo, listen_command
from vaani.core.context_manager import BaseContext, NewsContext, AgriculturalContext, SchemeContext
from vaani.services.time.time_service import current_time, get_date_of_day_in_week, get_day_summary
from vaani.services.weather.weather_service import get_weather
# Use enhanced news service instead of the old one
from vaani.services.news.news_service import get_news, process_news_selection
from vaani.services.knowledge.wikipedia_service import search_wikipedia
from vaani.services.agriculture.agri_command_processor import process_agriculture_command
from vaani.services.social.social_scheme_service import handle_social_schemes_query
from vaani.services.knowledge.general_knowledge_service import handle_general_knowledge_query
from vaani.core.language_manager import get_language_manager, handle_language_command
from vaani.services.finance.financial_literacy_service import handle_financial_query
from vaani.services.finance.simple_calculator_service import handle_calculation_query
from vaani.services.social.emergency_assistance_service import handle_emergency_query
# New SDG Goal 1 services (No Poverty)
from vaani.core.offline_mode import OfflineMode
from vaani.services.finance.expense_tracker_service import process_expense_command
# Import SMS integration if enabled in config
SMS_INTEGRATION_ENABLED = getattr(Config, 'SMS_INTEGRATION_ENABLED', False)
if SMS_INTEGRATION_ENABLED:
    # sms_integration will be imported lazily where needed to avoid startup import errors
    try:
        from vaani.services.communication import sms_integration
        print("SMS/USSD integration available")
    except ImportError:
        print("SMS/USSD integration not available")
        SMS_INTEGRATION_ENABLED = False

# --- Initial Setup ---
api_key_manager.setup_api_keys()
load_dotenv()

# Initialize language manager
lang_manager = get_language_manager()

# Initialize offline mode
offline_mgr = OfflineMode()

# Check if running in offline mode
def is_online():
    return offline_mgr.is_online()

print(f"Internet connection: {'Available' if is_online() else 'Not available (OFFLINE MODE)'}")

# Create required directories
for directory in ["data/expense_data", "data/offline_cache"]:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

# Set user ID (basic implementation - would be improved in production)
import hashlib
USER_ID = hashlib.md5(("default_user" + str(datetime.now().date())).encode()).hexdigest()[:8]

# --- Logging functions ---
def log_unprocessed_query(query):
    """Log unprocessed queries to a local file."""
    try:
        with open("unprocessed_queries.txt", "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] - Query: {query}\n")
    except Exception as e:
        print(f"Error: Could not write to log file. Reason: {e}")

# Simple context storage for news articles
current_articles = []

def main():
    global current_articles
    
    # Get greeting in current language
    startup_message = lang_manager.get_phrase('greeting')[0] + "! " + random.choice(Config.startup_responses)
    print(startup_message)
    bolo(startup_message, lang=lang_manager.get_tts_code())

    all_weather_triggers = Config.weather_trigger + Config.rain_trigger + Config.rain_most_significant
    is_waiting_for_news_selection = False

    while True:
        # Listen with current language's STT code
        prompt_text = lang_manager.get_phrase('listening')
        command = listen_command(
            lang_code=lang_manager.get_stt_code(),
            prompt_text=prompt_text
        )
        if not command:
            continue

        # Store original command for logging
        original_command = command
        command_lower = command.lower()

        # PRIORITY 1: Emergency - Handle FIRST and FAST
        if handle_emergency_query(command, bolo):
            continue
        
        # PRIORITY 2: Language switching
        is_lang_switch, new_lang = handle_language_command(command)
        if is_lang_switch:
            lang_manager.set_language(new_lang)
            lang_name = lang_manager.get_language_name(new_lang)
            response = f"{lang_manager.get_phrase('greeting', new_lang)[0]}! {lang_name} {lang_manager.get_phrase('listening', new_lang)}"
            print(response)
            bolo(response, lang=lang_manager.get_tts_code(new_lang))
            continue

        if is_waiting_for_news_selection:
            # Use unified context for news processing
            context = NewsContext(current_articles)
            if process_news_selection(command, bolo, context):
                is_waiting_for_news_selection = False
                current_articles = []
            continue

        # Priority order: Most specific triggers first to avoid conflicts
        
        # 1. Goodbye (highest priority)
        if any(phrase in command for phrase in Config.goodbye_triggers):
            bolo(random.choice(Config.goodbye_responses))
            break

        # 2. Time requests (very specific)
        elif any(phrase in command for phrase in Config.timedekh):
            current_time(bolo)

        # 3. Date requests (specific)
        elif any(phrase in command for phrase in Config.date_trigger):
            get_date_of_day_in_week(command, bolo)

        # 4. Weather (before agriculture to avoid conflicts)
        elif any(word in command for word in all_weather_triggers):
            get_weather(command, bolo)

        # 5. News (specific)
        elif any(phrase in command for phrase in Config.news_trigger):
            articles = get_news(command, bolo)
            if articles:
                current_articles = articles
                is_waiting_for_news_selection = True

        # 6. Wikipedia (specific)
        elif any(phrase in command for phrase in Config.wikipedia_trigger):
            search_wikipedia(command, bolo)

        # 7. Financial Literacy (for illiterate users - SDG Goal 1)
        elif handle_financial_query(command, bolo):
            pass  # Already handled

        # 8. Simple Calculator (for daily math needs)
        elif handle_calculation_query(command, bolo):
            pass  # Already handled
            
        # 9. Expense Tracker (NEW - for financial tracking)
        elif any(word in command_lower for word in ["खर्च", "खर्चा", "expense", "पैसा", "रुपये", "हिसाब"]):
            response = process_expense_command(command, USER_ID)
            bolo(response)

        # 10. Agriculture-related (check for specific agriculture context)
        elif (any(word in command_lower for word in Config.agri_trigger) or 
              any(crop in command_lower for crop in Config.agri_commodities) or
              any(market in command_lower for market in Config.agri_markets)):
            
            # Use unified context for agriculture processing
            context = AgriculturalContext()
            process_agriculture_command(command, bolo, {}, context)

        # 10. Social scheme triggers (specific schemes only)
        elif any(phrase in command_lower for phrase in Config.social_scheme_trigger):
            # Use unified context for social schemes
            context = SchemeContext()
            handle_social_schemes_query(command, bolo, context)

        # 11. Historical date (now more specific, less likely to conflict)
        elif any(phrase in command for phrase in Config.historical_date_trigger):
            get_day_summary(command, bolo)

        # 12. Greeting (low priority)
        elif any(phrase in command for phrase in Config.greeting_triggers):
            bolo(random.choice(Config.greeting_responses))

        # 13. General Knowledge Questions (before unrecognized)
        # Check if it's a curiosity/general knowledge question
        elif (any(trigger in command_lower for trigger in Config.general_knowledge_triggers) or 
              any(topic in command_lower for topic in Config.child_curiosity_topics) or
              '?' in command or '।' in command):
            # Try to handle as general knowledge question
            if not handle_general_knowledge_query(command, bolo):
                # If not handled, fall through to unrecognized
                error_msg = lang_manager.get_phrase('error')
                print(error_msg)
                bolo(error_msg, lang=lang_manager.get_tts_code())
                log_unprocessed_query(original_command)

        # 14. Unrecognized command
        else:
            error_msg = lang_manager.get_phrase('error')
            print(error_msg)
            bolo(error_msg, lang=lang_manager.get_tts_code())
            log_unprocessed_query(original_command)
        
        time.sleep(1)

if __name__ == "__main__":
    main()