# main.py

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

# --- Original Function Imports ---
from Voice_tool import bolo, listen_command
from Time import current_time, get_date_of_day_in_week, get_day_summary
from Weather import get_weather
from News import get_news, process_news_selection
from Wikipedia import search_wikipedia
from agri_command_processor import process_agriculture_command


# --- Initial Setup ---
api_key_manager.setup_api_keys()
load_dotenv()


# --- Logging functions (Restored) ---
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
    except Exception as e:
        print(f"An error occurred during remote logging: {e}")
        log_unprocessed_query_local(query)

def log_unprocessed_query_local(query):
    """Fallback to log the query to a local file if remote logging fails."""
    try:
        with open("unprocessed_queries_fallback.txt", "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] - Query: {query}\n")
    except Exception as e:
        print(f"Critical Error: Could not write to fallback log file. Reason: {e}")


# A set of intents that can temporarily interrupt a conversation
INTERRUPTING_INTENTS = {"get_time", "get_weather", "get_wikipedia"}


# --- Main Application Logic (with intelligent interruption handling) ---
def main():
    startup_message = random.choice(Config.startup_responses)
    print(startup_message)
    bolo(startup_message, lang='hi')

    context = Context()

    while True:
        command = listen_command()
        if not command:
            continue

        intent, score, entities = process_nlu(command)
        print(f"Intent: {intent} (Score: {score:.2f}), Entities: {entities}")

        is_in_context = context.state is not None
        is_interrupt = intent in INTERRUPTING_INTENTS and is_in_context

        if is_interrupt:
            print("--- INTERRUPTION DETECTED ---")
            if intent == "get_time":
                current_time(bolo)
            elif intent == "get_weather":
                get_weather(command, bolo)
            elif intent == "get_wikipedia":
                search_wikipedia(command, bolo)

            time.sleep(1)
            if context.state == 'awaiting_news_selection':
                 bolo("चलिए वापस आते हैं। " + "आप किस खबर के बारे में विस्तार से जानना चाहेंगे?")
            elif context.state == 'awaiting_agri_response':
                 bolo("चलिए कृषि संबंधी विषय पर वापस आते हैं। आप क्या पूछ रहे थे?")
            continue

        # --- NEW: CONTEXT HANDLING LOGIC ---
        if is_in_context:
            if context.state == 'awaiting_news_selection':
                status = process_news_selection(command, bolo, context)
                if status == 'SESSION_ENDED':
                    context.clear()
                if status != 'NOT_HANDLED':
                    continue
            # If context is waiting for an agricultural response, route directly
            elif context.state == 'awaiting_agri_response':
                print("--- CONTEXT: Awaiting Agri Response ---")
                # Force intent to agri_scheme to handle single-word replies like "गेहूं"
                process_agriculture_command(command, bolo, entities, context, force_intent="get_agri_scheme")
                context.clear() # Clear context after handling
                continue

        # --- Main Dispatcher for New Commands ---
        if intent == "goodbye":
            bolo(random.choice(Config.goodbye_responses))
            break
        elif intent == "greet":
            bolo(random.choice(Config.greeting_responses))
        elif intent == "get_time":
            current_time(bolo)
        elif intent == "get_weather":
            get_weather(command, bolo)
        elif intent == "get_news":
            articles = get_news(command, bolo)
            if articles:
                context.set(topic='news', state='awaiting_news_selection', data={'articles': articles})
        elif intent == "get_wikipedia":
            search_wikipedia(command, bolo)
        elif intent == "get_historical_date":
            get_day_summary(command, bolo)
        elif intent in ["get_agri_price", "get_agri_scheme", "get_agri_advice"]:
            process_agriculture_command(command, bolo, entities, context)
        else:
            if is_in_context:
                bolo("मैं समझी नहीं, कृपया अपेक्षित जवाब दें या कोई दूसरा कमांड बोलें।")
            else:
                bolo(random.choice(Config.unrecognized_command_responses))
                log_unprocessed_query_remote(command)

        time.sleep(1)


if __name__ == "__main__":
    main()