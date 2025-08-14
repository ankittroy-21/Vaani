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
    
    while True:
        command = listen_command()
        
        if not command:
            continue

        if "बंद करो" in command or "अलविदा" in command:
            bolo("फिर मिलेंगे! अपना ध्यान रखना।")
            break
        elif any(phrase in command for phrase in Config.timedekh):
            current_time(bolo)
        elif "मौसम" in command or "वेदर" in command:
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
