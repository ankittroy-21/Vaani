import requests
import Config
from deep_translator import GoogleTranslator
import random

def get_news(command, bolo_func):
    words_to_remove = set(Config.news_junk + Config.news_trigger)
    command_words = command.split()
    query_words = [word for word in command_words if word not in words_to_remove]
    query = " ".join(query_words)
        
    try:
        if query:
            search_message = random.choice(Config.news_search_responses).format(query)
            print(search_message)
            url = (f"https://gnews.io/api/v4/search?q={query}&lang=hi&country=in&apikey={Config.GNEWS_API_KEY}")
        else:
            search_message = random.choice(Config.news_top_headlines_responses)
            print(search_message)
            bolo_func(search_message)
            url = (f"https://gnews.io/api/v4/top-headlines?category=general&lang=hi&country=in&apikey={Config.GNEWS_API_KEY}")

        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()
        articles = news_data.get("articles", [])
        
        if articles:
            display_topic = query if query else "आज" 
            summary_intro = random.choice(Config.news_summary_responses).format(display_topic)
            print(summary_intro)
            bolo_func(summary_intro)
            
            for article in articles[:3]:
               original_title = article['title']
               try:
                    translator = GoogleTranslator(source='auto', target='hi')
                    translated_title = translator.translate(original_title)
                    print(f"Headline: {translated_title}")
               except Exception as e:
                    print(f"Could not translate: {e}")
                    translated_title = original_title
                    print(f"Headline: {translated_title}")
               bolo_func(translated_title)
        else:
            bolo_func(f"माफ़ कीजिए, मुझे '{query}' विषय पर कोई ताज़ा खबर नहीं मिली।")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.json()}")
        bolo_func("माफ़ कीजिए, समाचार सेवा से संपर्क नहीं हो पा रहा है।")
    except Exception as e:
        print(f"An unexpected news error occurred: {e}")
        bolo_func("खबरें प्राप्त करते समय एक अप्रत्याशित त्रुटि हुई।")