import time
import Config
from Voice_tool import bolo, listen_command
from Time import current_time
from Weather import get_weather
from News import get_news
from Wikipedia import search_wikipedia

def main():
    print("नमस्ते, मैं आपकी कैसे मदद कर सकता हूँ?")
    bolo("नमस्ते, मैं आपकी कैसे मदद कर सकता हूँ?", lang='hi')

    # Combine all weather and rain triggers from Config.py into a single list
    all_weather_triggers = Config.weather_trigger + Config.rain_trigger
    
    while True:
        command = listen_command()
        
        if not command:
            continue

        if "बंद करो" in command or "अलविदा" in command:
            bolo("फिर मिलेंगे! अपना ध्यान रखना।")
            break
        
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
        
        time.sleep(1)

if __name__ == "__main__":
    main()