import requests
import Config
from datetime import date, timedelta, datetime
import os

def _parse_location(command):
    """A dedicated helper function to reliably parse the city name from a command."""
    all_words_to_remove = set(
        Config.weather_trigger +
        Config.rain_trigger +
        Config.weather_junk +
        Config.rain_most_significant +
        Config.weather_full_report +
        Config.weather_temperature +
        Config.weather_wind
    )
    command_words = command.split()
    location_words = [word for word in command_words if word not in all_words_to_remove]
    location = " ".join(location_words)
    return location

def _format_date_hindi(date_str):
    """Converts a 'YYYY-MM-DD' string to a readable Hindi format like '15 August'."""
    try:
        hindi_months = {
            1: "जनवरी", 2: "फरवरी", 3: "मार्च", 4: "अप्रैल", 5: "मई", 6: "जून",
            7: "जुलाई", 8: "अगस्त", 9: "सितंबर", 10: "अक्टूबर", 11: "नवंबर", 12: "दिसंबर"
        }
        dt_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return f"{dt_obj.day} {hindi_months[dt_obj.month]}"
    except Exception:
        return date_str # Fallback if there's an error

def get_rain_forecast(command, city, bolo_func):
    """Fetches and reports daily rain forecasts with specific, formatted dates."""
    try:
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={os.getenv('WEATHER_API_KEY')}"
        geo_response = requests.get(geo_url)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if not geo_data:
            bolo_func(f"माफ़ कीजिए, मुझे '{city}' नाम की जगह नहीं मिली।")
            return
        
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']

        forecast_url = (f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
                        f"&daily=precipitation_probability_mean&timezone=auto&forecast_days=7")
        forecast_response = requests.get(forecast_url)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
        
        daily_forecasts = forecast_data.get('daily', {})
        time_list = daily_forecasts.get('time', [])
        prob_list = daily_forecasts.get('precipitation_probability_mean', [])

        if not time_list or not prob_list:
            bolo_func("माफ़ कीजिए, मैं बारिश का पूर्वानुमान नहीं ला सका।")
            return
        
        today_str = date.today().strftime("%Y-%m-%d")
        today_formatted = _format_date_hindi(today_str)
        tomorrow_str = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        tomorrow_formatted = _format_date_hindi(tomorrow_str)

        if any(phrase in command for phrase in Config.rain_most_significant):
            if len(prob_list) > 1:
                future_probs = prob_list[1:] # Check from tomorrow onwards
                max_prob = max(future_probs)
                
                if max_prob > 50:
                    max_prob_index = future_probs.index(max_prob) + 1
                    rainy_date_str = time_list[max_prob_index]
                    rainy_date_formatted = _format_date_hindi(rainy_date_str)
                    bolo_func(f"अगले कुछ दिनों में, सबसे ज़्यादा बारिश की संभावना {rainy_date_formatted} को है, जो कि {max_prob} प्रतिशत है।")
                else:
                    bolo_func(f"{city} में अगले हफ्ते तक किसी भी दिन भारी बारिश की कोई खास संभावना नहीं है।")
            else:
                bolo_func("मेरे पास भविष्य के पूर्वानुमान की पूरी जानकारी नहीं है।")

        elif any(phrase in command for phrase in Config.rain_today):
            if today_str in time_list:
                idx = time_list.index(today_str)
                pop = prob_list[idx]
                if pop > 45:
                    bolo_func(f"हाँ, आज, यानी {today_formatted} को, {city} में बारिश की {pop} प्रतिशत संभावना है।")
                else:
                    bolo_func(f"नहीं, आज, यानी {today_formatted} को, {city} में बारिश की संभावना बहुत कम है, केवल {pop} प्रतिशत।")
            else:
                bolo_func(f"{city} के लिए आज ({today_formatted}) की बारिश की जानकारी नहीं मिल सकी।")

        elif any(phrase in command for phrase in Config.rain_tomorrow):
            if tomorrow_str in time_list:
                idx = time_list.index(tomorrow_str)
                pop = prob_list[idx]
                if pop > 45:
                     bolo_func(f"हाँ, कल, यानी {tomorrow_formatted} को, {city} में बारिश होने की {pop} प्रतिशत संभावना है।")
                else:
                    bolo_func(f"नहीं, कल, यानी {tomorrow_formatted} को, {city} में बारिश की संभावना काफी कम है।")
            else:
                 bolo_func(f"{city} के लिए कल ({tomorrow_formatted}) की बारिश की जानकारी नहीं मिल सकी।")

        else: # General "kab hogi" query
            found_rain = False
            for i in range(1, len(time_list)):
                if prob_list[i] > 50:
                    day_map = {1: "कल", 2: "परसों"}
                    day_name = day_map.get(i, f"{i} दिन बाद")
                    date_str = time_list[i]
                    date_formatted = _format_date_hindi(date_str)
                    pop_percent = prob_list[i]
                    bolo_func(f"{city} में अगली बारिश की संभावना {day_name}, यानी {date_formatted} को है, जो कि {pop_percent} प्रतिशत है।")
                    found_rain = True
                    break
            
            if not found_rain:
                bolo_func(f"{city} में अगले हफ्ते तक बारिश की कोई खास संभावना नहीं दिख रही है।")
    
    except Exception as e:
        print(f"Rain forecast error: {e}")
        bolo_func("बारिश का पूर्वानुमान लेते समय एक अप्रत्याशित त्रुटि हुई।")

# Weather.py में

def get_general_weather(command, city_to_check, bolo_func):
    """Provides general weather details."""
    try:
        url = (f"http://api.openweathermap.org/data/2.5/weather?"
               f"q={city_to_check}&appid={os.getenv('WEATHER_API_KEY')}&units=metric&lang=hi")
        
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        
        if 'main' in weather_data and 'weather' in weather_data and 'wind' in weather_data:
            temp = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            wind_speed_ms = weather_data['wind']['speed']
            wind_speed_kph = wind_speed_ms * 3.6

            if any(phrase in command for phrase in Config.weather_full_report):
                response_string = (f"{city_to_check} में, तापमान {temp:.1f} डिग्री सेल्सियस है, नमी {humidity} प्रतिशत है, "
                                   f"हवा की गति {wind_speed_kph:.1f} किलोमीटर प्रति घंटा है और "
                                   f"आसमान में {description} की उम्मीद है।")
            elif any(phrase in command for phrase in Config.weather_temperature):
                response_string = (f"{city_to_check} में अभी का तापमान {temp:.1f} डिग्री सेल्सियस है "
                                   f"और हवा में नमी {humidity} प्रतिशत है।")
            elif any(phrase in command for phrase in Config.weather_wind):
                response_string = f"{city_to_check} में हवा की गति {wind_speed_kph:.1f} किलोमीटर प्रति घंटा है।"
            else:
                response_string = (f"{city_to_check} में आज आसमान में {description} की उम्मीद है "
                                   f"और तापमान लगभग {temp:.1f} डिग्री सेल्सियस है।")
            print(response_string)
            bolo_func(response_string)
        else:
            bolo_func("माफ़ कीजिए, मैं मौसम का विवरण प्राप्त नहीं कर सका।")
    except Exception as e:
        print(f"General weather error: {e}")
        bolo_func("मौसम की जानकारी लेते समय एक त्रुटि हुई।")


def get_weather(command, bolo_func):
    """Finds the location, then routes to the correct weather/rain function."""
    location = _parse_location(command)
    city_to_check = location if location else "Lucknow"
    
    if not location and ("मौसम" in command or "बारिश" in command):
        bolo_func(f"आपने शहर का नाम नहीं बताया, इसलिए मैं लखनऊ की जानकारी दे रहा हूँ।")
    
    if any(phrase in command for phrase in Config.rain_trigger) or any(phrase in command for phrase in Config.rain_most_significant):
        get_rain_forecast(command, city_to_check, bolo_func)
    else:
        get_general_weather(command, city_to_check, bolo_func)