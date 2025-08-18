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


    with open('.env', 'w') as f:
        f.write(f'WEATHER_API_KEY="{weather_key}"\n')
        f.write(f'GNEWS_API_KEY="{gnews_key}"\n')

    print("\nAPI keys saved successfully to .env file!")
    print("You will not be asked for them again.\n")