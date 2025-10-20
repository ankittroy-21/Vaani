import time
import Config
import requests
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import api_key_manager
import random
from datetime import datetime
from Voice_tool import bolo_stream as bolo, listen_command
from Time import current_time, get_date_of_day_in_week, get_day_summary
from Weather import get_weather
from News import get_news, process_news_selection
from Wikipedia import search_wikipedia
from agri_command_processor import process_agriculture_command
from social_scheme_service import handle_social_schemes_query

# --- Initial Setup ---
api_key_manager.setup_api_keys()
load_dotenv()

# --- Logging functions ---
def log_unprocessed_query_remote(query):
    """Sends the unprocessed query and a secret auth key to a remote Google Form."""
    try:
        cipher_suite = Fernet(Config.KEY)
        gform_id = cipher_suite.decrypt(Config.GFORM_ID).decode()
        entry_id = cipher_suite.decrypt(Config.ENTRY_ID).decode()
        auth_key_entry_id = cipher_suite.decrypt(Config.AUTH_KEY_ENTRY_ID).decode()
        secret_key = cipher_suite.decrypt(Config.SECRET_KEY).decode()

        form_url = f"https://docs.google.com/forms/d/e/{gform_id}/formResponse"
        form_data = {
            entry_id: query,
            auth_key_entry_id: secret_key
        }
        requests.post(form_url, data=form_data, timeout=5)
        print(f"Successfully logged remote query: {query}")
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not log query remotely. Reason: {e}")
        log_unprocessed_query_local(query)
    except Exception as e:
        print(f"An unexpected error occurred during remote logging: {e}")
        log_unprocessed_query_local(query)

def log_unprocessed_query_local(query):
    """Fallback to log the query to a local file if remote logging fails."""
    try:
        with open("unprocessed_queries_fallback.txt", "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] - Query: {query}\n")
    except Exception as e:
        print(f"Critical Error: Could not write to fallback log file. Reason: {e}")

# Simple context storage for news articles
current_articles = []

def main():
    global current_articles
    startup_message = random.choice(Config.startup_responses)
    print(startup_message)
    bolo(startup_message, lang='hi')

    all_weather_triggers = Config.weather_trigger + Config.rain_trigger + Config.rain_most_significant
    is_waiting_for_news_selection = False

    while True:
        command = listen_command()
        if not command:
            continue

        # Store original command for logging
        original_command = command
        command_lower = command.lower()

        if is_waiting_for_news_selection:
            # Create a simple context object for news processing
            class SimpleContext:
                def __init__(self, articles):
                    self.data = {'articles': articles}
            
            context = SimpleContext(current_articles)
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

        # 7. Agriculture-related (check for specific agriculture context)
        elif (any(word in command_lower for word in Config.agri_trigger) or 
              any(crop in command_lower for crop in Config.agri_commodities) or
              any(market in command_lower for market in Config.agri_markets)):
            
            # Create a simple context for agriculture processing
            class SimpleAgriContext:
                def __init__(self):
                    self.state = None
                    self.data = {}
                    
                def set(self, **kwargs):
                    for key, value in kwargs.items():
                        setattr(self, key, value)
                        if key != 'state':
                            self.data[key] = value
            
            context = SimpleAgriContext()
            process_agriculture_command(command, bolo, {}, context)

        # 8. Social scheme triggers (specific schemes only)
        elif any(phrase in command_lower for phrase in Config.social_scheme_trigger):
            # Create a simple context for social schemes
            class SimpleSchemeContext:
                def __init__(self):
                    self.state = None
                    self.data = {}
                    
                def set(self, **kwargs):
                    for key, value in kwargs.items():
                        setattr(self, key, value)
                        if key != 'state':
                            self.data[key] = value
            
            context = SimpleSchemeContext()
            handle_social_schemes_query(command, bolo, context)

        # 9. Historical date (now more specific, less likely to conflict)
        elif any(phrase in command for phrase in Config.historical_date_trigger):
            get_day_summary(command, bolo)

        # 10. Greeting (low priority)
        elif any(phrase in command for phrase in Config.greeting_triggers):
            bolo(random.choice(Config.greeting_responses))

        # 11. Unrecognized command
        else:
            print("मैं यह समझ नहीं पाई, कृपया फिर से कहें।")
            bolo("मैं यह समझ नहीं पाई, कृपया फिर से कहें।")
            log_unprocessed_query_remote(original_command)
        
        time.sleep(1)

if __name__ == "__main__":
    main()