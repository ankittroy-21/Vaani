import requests
import Config

def get_weather(command, bolo_func):
    """
    Parses a command to find a city, fetches weather data, and uses the provided
    speaking function to announce the result.
    """
    trigger_words = ["मौसम", "वेदर", "तापमान"]
    junk_words = ["का", "में", "शहर", "आज", "कैसा", "है", "बताओ"]
    
    location = ""
    command_words = command.split()

    # Logic to find the location in the command
    for i, word in enumerate(command_words):
        if word in trigger_words:
            # Assume the location is mentioned before the trigger word
            location_words = command_words[:i]
            cleaned_location_words = [w for w in location_words if w not in junk_words]
            location = " ".join(cleaned_location_words).strip()
            break

    if location:
        city_to_check = location
        bolo_func(f"{city_to_check} का मौसम बता रहा हूँ।")
    else:
        # If no location is found, default to Lucknow as per our original setup
        city_to_check = "Lucknow"
        bolo_func(f"लखनऊ का मौसम बता रहा हूँ।")

    try:
        # Use the API key from the config file
        url = (f"http://api.openweathermap.org/data/2.5/weather?"
               f"q={city_to_check}&appid={Config.WEATHER_API_KEY}&units=metric&lang=hi")
        
        response = requests.get(url)
        response.raise_for_status()  # This will raise an error for bad responses (4xx or 5xx)
        weather_data = response.json()
        
        if 'main' in weather_data and 'weather' in weather_data and 'wind' in weather_data:
            temp = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            wind_speed_ms = weather_data['wind']['speed']
            wind_speed_kph = wind_speed_ms * 3.6

            response_string = (f"तापमान {temp:.1f} डिग्री सेल्सियस है, "
                               f"नमी {humidity} प्रतिशत है, "
                               f"हवा की गति {wind_speed_kph:.1f} किलोमीटर प्रति घंटा है और "
                               f"{description} की उम्मीद है।")
            bolo_func(response_string)
            
        else:
            bolo_func("माफ़ कीजिए, मैं मौसम का विवरण प्राप्त नहीं कर सका।")
            
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            bolo_func(f"माफ़ कीजिए, मुझे '{city_to_check}' नाम की जगह नहीं मिली।")
        else:
            bolo_func("मौसम की जानकारी लेते समय एक त्रुटि हुई।")
    except Exception as e:
        print(f"Weather error: {e}")
        bolo_func("मौसम की जानकारी लेते समय एक अप्रत्याशित त्रुटि हुई।")