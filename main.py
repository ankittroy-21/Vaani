import time
import Config
import requests
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import api_key_manager
import random
from datetime import datetime
from Voice_tool import bolo, listen_command
from Time import current_time, get_date_of_day_in_week, get_day_summary
from Weather import get_weather
from News import get_news, process_news_selection
from Wikipedia import search_wikipedia
from agri_command_processor import process_agriculture_command
from agri_advisory_service import get_farming_advisory

api_key_manager.setup_api_keys()
load_dotenv()

def log_unprocessed_query_remote(query):
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
    try:
        with open("unprocessed_queries_fallback.txt", "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] - Query: {query}\n")
    except Exception as e:
        print(f"Critical Error: Could not write to fallback log file. Reason: {e}")

def main():
    startup_message = random.choice(Config.startup_responses)
    print(startup_message)
    bolo(startup_message, lang='hi')

    all_weather_triggers = Config.weather_trigger + Config.rain_trigger + Config.rain_most_significant

    is_waiting_for_news_selection = False
    is_waiting_for_wiki_confirm = False
    pending_wiki_query = ""

    while True:
        command = listen_command()

        if not command:
            continue

        if is_waiting_for_wiki_confirm:
            if any(word in command for word in ["हाँ", "हां", "yes", "ज़रूर", "खोजो"]):
                bolo(f"ठीक है, विकिपीडिया पर {pending_wiki_query} खोज रही हूँ।")
                search_wikipedia(pending_wiki_query, bolo)
                log_unprocessed_query_remote(pending_wiki_query)
            else:
                bolo("ठीक है। कोई और जानकारी चाहिए तो बताइए।")
                log_unprocessed_query_remote(pending_wiki_query)

            is_waiting_for_wiki_confirm = False
            pending_wiki_query = ""
            continue

        if is_waiting_for_news_selection:
            if process_news_selection(command, bolo):
                is_waiting_for_news_selection = False
            continue

        agri_status = process_agriculture_command(command, bolo)

        if agri_status == "HANDLED":
            time.sleep(1)
            continue

        elif agri_status == "SCHEME_NOT_FOUND":
            unprocessed_query = command
            bolo("मुझे इससे जुड़ी कोई भी योजना नहीं मिली, क्या आप इसे विकिपीडिया पर खोजना चाहेंगे?")
            is_waiting_for_wiki_confirm = True
            pending_wiki_query = unprocessed_query
            continue

        if any(phrase in command for phrase in Config.goodbye_triggers):
            bolo(random.choice(Config.goodbye_responses))
            break

        elif any(phrase in command for phrase in Config.timedekh):
            current_time(bolo)

        elif any(phrase in command for phrase in Config.date_trigger):
            get_date_of_day_in_week(command, bolo)

        elif any(word in command for word in all_weather_triggers):
            get_weather(command, bolo)

        elif any(phrase in command for phrase in Config.news_trigger):
            if get_news(command, bolo):
                is_waiting_for_news_selection = True

        elif any(phrase in command for phrase in Config.wikipedia_trigger):
            search_wikipedia(command, bolo)

        elif any(phrase in command for phrase in Config.greeting_triggers):
            bolo(random.choice(Config.greeting_responses))

        elif any(phrase in command for phrase in Config.historical_date_trigger):
            get_day_summary(command, bolo)

        else:
            response = random.choice(Config.unrecognized_command_responses)
            print(response)
            bolo(response)
            log_unprocessed_query_remote(command)

        time.sleep(1)

if __name__ == "__main__":
    main()