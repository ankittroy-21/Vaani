import time
import Config
import requests
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import api_key_manager
import random
from datetime import datetime

# --- Enhanced Imports ---
from nlu_engine import process_nlu
from context_manager import Context
from nlu_preprocessor import normalize_query # <<< NEW: Import the normalizer function

# --- Original Function Imports ---
from Voice_tool import bolo, listen_command
from Time import current_time, get_date_of_day_in_week, get_day_summary
from Weather import get_weather
from News import get_news, process_news_selection
from Wikipedia import search_wikipedia
from agri_command_processor import process_agriculture_command
from social_scheme_service import handle_social_schemes_query, handle_scheme_selection

# --- Initial Setup ---
api_key_manager.setup_api_keys()
load_dotenv()

# --- Logging functions (Unchanged) ---
def log_unprocessed_query_remote(query):
    try:
        cipher_suite = Fernet(Config.KEY)
        gform_id = cipher_suite.decrypt(Config.GFORM_ID).decode()
        entry_id = cipher_suite.decrypt(Config.ENTRY_ID).decode()
        auth_key_entry_id = cipher_suite.decrypt(Config.AUTH_KEY_ENTRY_ID).decode()
        secret_key = cipher_suite.decrypt(Config.SECRET_KEY).decode()
        form_url = f"https://docs.google.com/forms/d/e/{gform_id}/formResponse"
        form_data = {entry_id: query, auth_key_entry_id: secret_key}
        requests.post(form_url, data=form_data, timeout=5)
        print(f"Successfully logged remote query: {query}")
    except Exception as e:
        print(f"An error occurred during remote logging: {e}")
        log_unprocessed_query_local(query)

def log_unprocessed_query_local(query):
    try:
        with open("unprocessed_queries_fallback.txt", "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] - Query: {query}\n")
    except Exception as e:
        print(f"Critical Error: Could not write to fallback log file. Reason: {e}")

# --- Interrupting Intents (Unchanged) ---
INTERRUPTING_INTENTS = {"get_time", "get_weather", "get_wikipedia"}

def main():
    startup_message = random.choice(Config.startup_responses)
    print(startup_message)
    bolo(startup_message, lang='hi')

    context = Context()

    while True:
        command = listen_command()
        if not command:
            continue

        # --- ENHANCEMENT: Normalize the command before processing it ---
        original_command = command # Keep a copy for logging if needed
        command = normalize_query(command)
        print(f"Normalized Command: '{command}' (from Original: '{original_command}')")
        # --- END OF ENHANCEMENT ---

        # Rule-based override for simple, critical commands
        if command in ["समय", "टाइम"]:
            current_time(bolo)
            continue

        intent, score, entities = process_nlu(command)
        print(f"Intent: {intent} (Score: {score:.2f}), Entities: {entities}")

        is_in_context = context.state is not None
        is_interrupt = intent in INTERRUPTING_INTENTS and is_in_context

        if is_interrupt:
            print("--- INTERRUPTION DETECTED ---")
            if intent == "get_time": current_time(bolo)
            elif intent == "get_weather": get_weather(command, bolo)
            elif intent == "get_wikipedia": search_wikipedia(command, bolo)
            time.sleep(1)
            # Restore context prompt after interruption
            if context.state == 'awaiting_news_selection':
                 bolo("चलिए वापस आते हैं। " + "आप किस खबर के बारे में विस्तार से जानना चाहेंगे?")
            elif context.state == 'awaiting_agri_response':
                 bolo("चलिए कृषि संबंधी विषय पर वापस आते हैं। आप क्या पूछ रहे थे?")
            elif context.state == 'awaiting_scheme_selection':
                 bolo("चलिए सरकारी योजनाओं के विषय पर वापस आते हैं। आप किस योजना के बारे में जानना चाहते हैं?")
            continue

        # Context Handling Logic
        if is_in_context:
            if context.state == 'awaiting_news_selection':
                if process_news_selection(command, bolo, context) != 'NOT_HANDLED': continue
            elif context.state == 'awaiting_agri_response':
                process_agriculture_command(command, bolo, entities, context, force_intent="get_agri_scheme")
                context.clear(); continue
            elif context.state == 'awaiting_scheme_selection':
                handle_scheme_selection(command, bolo, context); continue

        # Main Dispatcher
        if intent == "goodbye":
            bolo(random.choice(Config.goodbye_responses)); break
        elif intent == "greet":
            bolo(random.choice(Config.greeting_responses))
        elif intent == "get_time":
            current_time(bolo)
        elif intent == "get_weather":
            get_weather(command, bolo)
        elif intent == "get_news":
            articles = get_news(command, bolo)
            if articles: context.set(topic='news', state='awaiting_news_selection', data={'articles': articles})
        elif intent == "get_wikipedia":
            search_wikipedia(command, bolo)
        elif intent == "get_historical_date":
            get_day_summary(command, bolo)
        elif intent == "get_social_schemes":
            handle_social_schemes_query(command, bolo, context)
        elif intent in ["get_agri_price", "get_agri_scheme", "get_agri_advice"]:
            process_agriculture_command(command, bolo, entities, context,force_intent=intent)
        else:
            if is_in_context:
                bolo("मैं समझी नहीं, कृपया अपेक्षित जवाब दें या कोई दूसरा कमांड बोलें।")
            else:
                bolo(random.choice(Config.unrecognized_command_responses))
                log_unprocessed_query_remote(original_command) # Log the original, unprocessed command

        time.sleep(1)

if __name__ == "__main__":
    main()