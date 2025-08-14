import requests
import Config
from deep_translator import GoogleTranslator

def get_news(command, bolo_func):
    """Fetches and translates news headlines."""
    junk_words = ["की", "के", "बारे", "में", "से", "ताज़ा", "बताओ", "सुनाओ", "न्यूज़", "खबरें", "समाचार"]
    query = command
    for word in junk_words:
        query = query.replace(word, "").strip()
        
    try:
        if query:
            print(f"ठीक है, {query} के बारे में GNews से खबरें खोज रहा हूँ।")
            bolo_func(f"ठीक है, {query} के बारे में GNews से खबरें खोज रहा हूँ।")
            url = (f"https://gnews.io/api/v4/search?q={query}&lang=hi&country=in&apikey={Config.GNEWS_API_KEY}")
        else:
            print("ठीक है, भारत से आज की ताज़ा खबरें सुना रहा हूँ।")
            bolo_func("ठीक है, भारत से आज की ताज़ा खबरें सुना रहा हूँ।")
            url = (f"https://gnews.io/api/v4/top-headlines?category=general&lang=hi&country=in&apikey={Config.GNEWS_API_KEY}")

        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()
        articles = news_data.get("articles", [])
        
        if articles:
            print(f"ये हैं {query} की कुछ प्रमुख खबरें:")
            bolo_func(f"ये हैं {query} की कुछ प्रमुख खबरें:")
            for article in articles[:3]:
               original_title = article['title']
               try:
                    translator = GoogleTranslator(source='auto', target='hi')
                    translated_title = translator.translate(original_title)
                    print(f"artcle about {query} : {translated_title}")
               except Exception as e:
                    print(f"Could not translate: {e}")
                    translated_title = original_title
                    print(f"article about {query}: {translated_title}")
               bolo_func(translated_title)
        else:
            print("माफ़ कीजिए, मुझे इस विषय पर कोई ताज़ा खबर नहीं मिली।")
            bolo_func("माफ़ कीजिए, मुझे इस विषय पर कोई ताज़ा खबर नहीं मिली।")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.json()}")
        bolo_func("माफ़ कीजिए, समाचार सेवा से संपर्क नहीं हो पा रहा है।")
    except Exception as e:
        print(f"An unexpected news error occurred: {e}")
        bolo_func("खबरें प्राप्त करते समय एक अप्रत्याशित त्रुटि हुई।")
  