import speech_recognition as sr
from gtts import gTTS
import os
import time
import datetime
from playsound import playsound
import requests
import wikipedia

WEATHER_API_KEY = "d8d27914ed689d6db6b7cfaaa81b03af"
GNEWS_API_KEY = "176a4e62933fed171ad078e1c9f4476a"

def bolo(text, lang='hi'):
    try:
        tts = gTTS(text=text, lang=lang)
        audio_file = "temp_audio.mp3"
        tts.save(audio_file)
        playsound(audio_file)
        os.remove(audio_file)
    except ImportError:
        print("The 'playsound' library is not installed. Please run: pip install playsound")
        print("As a fallback, using os.system. This might not work on all systems.")
        tts = gTTS(text=text, lang=lang)
        audio_file = "temp_audio.mp3"
        tts.save(audio_file)
        if os.name == 'nt':
            os.system(f"start {audio_file}")
        else:
            os.system(f"afplay {audio_file}")
        time.sleep(max(2, len(text) / 15))
    except Exception as e:
        print(f"Error in bolo function: {e}")

def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language='hi-IN')
        print(f"आपने कहा: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("क्षमा करें, मैं आपकी बात समझ नहीं पाया।")
        bolo("क्षमा करें, मैं आपकी बात समझ नहीं पाया।")
        return ""
    except sr.RequestError as e:
        print(f"Google Speech Recognition सेवा से कनेक्ट नहीं हो सका; {e}")
        bolo("Google Speech Recognition सेवा से कनेक्ट नहीं हो सका।")
        return ""

def current_time():
   now=datetime.datetime.now()
   if 4 <= now.hour < 12:
    time_of_day = "सुबह"
   elif 12 <= now.hour < 16:
    time_of_day = "दोपहर"
   elif 16 <= now.hour < 20:
    time_of_day = "शाम"
   else:
    time_of_day = "रात"
   bolo(
        f"अभी {now.strftime('%I:%M')} {time_of_day} के हैं।"
    )

def get_weather(command):
    trigger_words = ["मौसम", "वेदर", "तापमान"]
    junk_words = ["का", "में", "शहर", "आज", "कैसा", "है", "बताओ"]
    
    location = ""
    command_words = command.split()

    for i, word in enumerate(command_words):
        if word in trigger_words:
            location_words = command_words[:i]
            cleaned_location_words = [w for w in location_words if w not in junk_words]
            location = " ".join(cleaned_location_words).strip()
            break

    if location:
        city_to_check = location
        bolo(f"{city_to_check} का मौसम बता रहा हूँ।")
    else:
        bolo("आप किस शहर का मौसम जानना चाहते हैं?")
        return

    try:
        url = (f"http://api.openweathermap.org/data/2.5/weather?"
               f"q={city_to_check}&appid={WEATHER_API_KEY}&units=metric&lang=hi")
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        
        if 'main' in weather_data and 'weather' in weather_data and 'wind' in weather_data:
            temp = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            wind_speed_ms = weather_data['wind']['speed']
            wind_speed_kph = wind_speed_ms * 3.6
            print(f"तापमान {temp:.1f} डिग्री सेल्सियस है, "
                  f"नमी {humidity} प्रतिशत है, "
                  f"हवा की गति {wind_speed_kph:.1f} किलोमीटर प्रति घंटा है और "
                  f"{description} की उम्मीद है।")
            response_string = (f"तापमान {temp:.1f} डिग्री सेल्सियस है, "
                               f"नमी {humidity} प्रतिशत है, "
                               f"हवा की गति {wind_speed_kph:.1f} किलोमीटर प्रति घंटा है और "
                               f"{description} की उम्मीद है।")
            bolo(response_string)
            
        else:
            bolo("माफ़ कीजिए, मैं मौसम का विवरण प्राप्त नहीं कर सका।")
            
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            bolo(f"माफ़ कीजिए, मुझे '{city_to_check}' नाम की जगह नहीं मिली।")
        else:
            bolo("मौसम की जानकारी लेते समय एक त्रुटि हुई।")
    except Exception as e:
        print(f"Weather error: {e}")
        bolo("मौसम की जानकारी लेते समय एक अप्रत्याशित त्रुटि हुई।")

def get_news(command):
    junk_words = ["की", "के", "बारे", "में", "से", "ताज़ा", "बताओ", "सुनाओ", "खबरें", "समाचार"]
    query = command
    for word in junk_words:
        query = query.replace(word, "").strip()
        
    try:
        if query:
            print(f"ठीक है, {query} के बारे में GNews से खबरें खोज रहा हूँ।")
            bolo(f"ठीक है, {query} के बारे में GNews से खबरें खोज रहा हूँ।")
            url = (f"https://gnews.io/api/v4/search?q={query}&lang=hi&country=in&apikey={GNEWS_API_KEY}")
        else:
            print("ठीक है, भारत से आज की ताज़ा खबरें सुना रहा हूँ।")
            bolo("ठीक है, भारत से आज की ताज़ा खबरें सुना रहा हूँ।")
            url = (f"https://gnews.io/api/v4/top-headlines?category=general&lang=hi&country=in&apikey={GNEWS_API_KEY}")

        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()
        articles = news_data.get("articles", [])
        
        if articles:
            print("ये हैं आज की कुछ प्रमुख खबरें:")
            bolo("ये हैं आज की कुछ प्रमुख खबरें:")
            for article in articles[:3]:
                print(article['title'])
                bolo(article['title'])
        else:
            print("माफ़ कीजिए, मुझे इस विषय पर कोई ताज़ा खबर नहीं मिली।")
            bolo("माफ़ कीजिए, मुझे इस विषय पर कोई ताज़ा खबर नहीं मिली।")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.json()}")
        bolo("माफ़ कीजिए, समाचार सेवा से संपर्क नहीं हो पा रहा है।")
    except Exception as e:
        print(f"An unexpected news error occurred: {e}")
        bolo("खबरें प्राप्त करते समय एक अप्रत्याशित त्रुटि हुई।")

def search_wikipedia(command):
    query = command.replace("विकिपीडिया पर", "").replace("खोजो", "").strip()
    
    if not query:
        bolo("आप विकिपीडिया पर क्या खोजना चाहते हैं?")
        return

    bolo(f"ठीक है, विकिपीडिया पर {query} खोज रहा हूँ...")

    try:
        wikipedia.set_lang("hi")
        full_summary = wikipedia.summary(query, sentences=3)
        bolo("विकिपीडिया के अनुसार,")
        bolo(full_summary)

    except wikipedia.exceptions.DisambiguationError as e:
        bolo(f"इस विषय पर एक से ज़्यादा परिणाम हैं। आप इनमें से क्या मतलब रखते हैं? {', '.join(e.options[:3])}")
    except wikipedia.exceptions.PageError:
        bolo(f"माफ़ कीजिए, मुझे '{query}' के लिए कोई विकिपीडिया पेज नहीं मिला।")
    except Exception as e:
        print(f"An unexpected Wikipedia error occurred: {e}")
        bolo("माफ़ कीजिए, विकिपीडिया पर खोजते समय एक त्रुटि हुई।")

def main():
    print("नमस्ते, मैं आपकी कैसे मदद कर सकता हूँ?")
    bolo("नमस्ते, मैं आपकी कैसे मदद कर सकता हूँ?", lang='hi')
    print("कृपया बोलिए :")
    while True:
        command = listen_command()
        
        if not command:
            continue

        if "बंद करो" in command or "अलविदा" in command:
            bolo("फिर मिलेंगे! अपना ध्यान रखना।")
            break
        elif "समय" in command or "टाइम" in command:
            current_time()
        elif "मौसम" in command or "वेदर" in command:
            get_weather(command)
        elif "खबरें" in command or "समाचार" in command:
            get_news(command)
        elif "विकिपीडिया पर" in command:
            search_wikipedia(command)
        elif "नमस्ते" in command or "हेलो" in command:
            bolo("नमस्ते! क्या हाल है?")
        else:
            bolo("मैं यह समझ नहीं पाया, कृपया फिर से कहें।")
        
        time.sleep(1)

if __name__ == "__main__":
    main()

