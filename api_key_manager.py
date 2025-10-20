# api_key_manager.py (OPTIONAL enhancement)
import os

def setup_api_keys():
    if os.path.exists('.env'):
        return

    print("--- API Key Setup ---")
    print("Your API keys were not found. Please enter them now.")
    print("They will be saved locally in a .env file ")
    
    print("\n" + "-"*50)
    weather_key = input(" Enter your OpenWeatherMap API Key: ")
    print("-"*50)

    print("\n" + "-"*50)
    gnews_key = input(" Enter your GNews API Key: ")
    print("-"*50)
    
    print("\n" + "-"*50)
    agmarknet_key = input(" Enter your Agmarknet API Key (from data.gov.in): ")
    print("-"*50)
    
    print("\n" + "-"*50)
    print(" Gemini API Key (Optional - for general knowledge questions)")
    print(" Get it from: https://makersuite.google.com/app/apikey")
    gemini_key = input(" Enter your Gemini API Key (or press Enter to skip): ")
    print("-"*50)

    with open('.env', 'w') as f:
        f.write(f'WEATHER_API_KEY="{weather_key}"\n')
        f.write(f'GNEWS_API_KEY="{gnews_key}"\n')
        f.write(f'AGMARKNET_API_KEY="{agmarknet_key}"\n')
        if gemini_key and gemini_key.strip():
            f.write(f'GEMINI_API_KEY="{gemini_key}"\n')

    print("\nAPI keys saved successfully to .env file!")
    print("You will not be asked for them again.\n")
    if gemini_key and gemini_key.strip():
        print("✅ Gemini API enabled - General knowledge questions will be answered!")
    else:
        print("⚠️  Gemini API skipped - General knowledge feature will be disabled.")