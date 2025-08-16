import time
import Config
import requests
import random
from datetime import datetime
from Voice_tool import bolo, listen_command
from Time import current_time
from Weather import get_weather
from News import get_news
from Wikipedia import search_wikipedia

def log_unprocessed_query_remote(query):
    """Sends the unprocessed query and a secret auth key to a remote Google Form."""
    try:
        form_url = f"https://docs.google.com/forms/d/e/{Config.GFORM_ID}/formResponse"
        form_data = {
            Config.GFORM_ENTRY_ID: query,
            Config.GFORM_AUTH_KEY_ENTRY_ID: Config.GFORM_SECRET_KEY
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

def handle_positive_feedback(command):
    """Process positive feedback with regional variations."""
    # Check for exact matches first
    if command.lower() in Config.POSITIVE_FEEDBACK_SET:
        return True
    
    # Check for partial matches (feedback within longer sentences)
    for feedback in Config.POSITIVE_FEEDBACK_SET:
        if feedback in command:
            return True
    return False

def main():
    print("नमस्ते, मैं आपकी कैसे मदद कर सकता हूँ?")
    bolo("नमस्ते, मैं आपकी कैसे मदद कर सकता हूँ?", lang='hi')

    all_weather_triggers = Config.weather_trigger + Config.rain_trigger + Config.rain_most_significant
    
    while True:
        command = listen_command()
        
        if not command:
            continue

        # 1. First check for exit commands
        if "बंद करो" in command or "अलविदा" in command:
            bolo("फिर मिलेंगे! अपना ध्यान रखना।")
            break
            
        # 2. Handle positive feedback (new block)
        if handle_positive_feedback(command):
            responses = [
                "धन्यवाद! मैं और कैसे मदद कर सकता हूँ?",
                "आपकी प्रशंसा मुझे प्रेरित करती है!",
                "मैं और बेहतर सेवा देने का प्रयास करूँगा",
                "शुक्रिया! क्या मैं आपके लिए और कुछ कर सकता हूँ?"
            ]
            bolo(random.choice(responses))
            continue
            
        # 3. Existing command processing
        elif any(phrase in command for phrase in Config.timedekh):
            current_time(bolo)
        elif any(word in command for word in all_weather_triggers):
            get_weather(command, bolo)
        elif "खबरें" in command or "समाचार" in command:
            get_news(command, bolo)
        elif "विकिपीडिया पर" in command:
            search_wikipedia(command, bolo)
        elif "नमस्ते" in command or "हेलो" in command:
            bolo("नमस्ते! क्या हाल है?")
        else:
            bolo("मैं यह समझ नहीं पाया, कृपया फिर से कहें।")
            log_unprocessed_query_remote(command)
        
        time.sleep(1)

if __name__ == "__main__":
    # Initialize feedback set for faster lookups
    Config.POSITIVE_FEEDBACK_SET = set(Config.POSITIVE_FEEDBACK)
    main()
