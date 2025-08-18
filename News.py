import requests
import Config
from deep_translator import GoogleTranslator
import random

articles_cache = []

def get_news(command, bolo_func):
    """
    Fetches up to 5 news headlines, presents them as a numbered list,
    and returns them to be cached for further explanation.
    """
    words_to_remove = set(Config.news_junk + Config.news_trigger)
    command_words = command.split()
    query_words = [word for word in command_words if word not in words_to_remove]
    query = " ".join(query_words)
        
    try:
        if query:
            search_message = random.choice(Config.news_search_responses).format(query)
            print(search_message)
            url = f"https://gnews.io/api/v4/search?q={query}&lang=hi&country=in&max=5&apikey={Config.GNEWS_API_KEY}"
        else:
            search_message = random.choice(Config.news_top_headlines_responses)
            print(search_message)
            bolo_func(search_message)
            url = f"https://gnews.io/api/v4/top-headlines?category=general&lang=hi&country=in&max=5&apikey={Config.GNEWS_API_KEY}"

        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()
        articles = news_data.get("articles", [])
        
        if articles:
            global articles_cache
            articles_cache = articles

            display_topic = query if query else "आज" 
            summary_intro = random.choice(Config.news_summary_responses).format(display_topic)
            print(summary_intro)
            bolo_func(summary_intro)
            
            hindi_numbers = [" पहली खबर", " दूसरी खबर", " तीसरी खबर", " चौथी खबर", " पांचवी खबर"]

            for i, article in enumerate(articles_cache):
               original_title = article['title']
               try:
                    translator = GoogleTranslator(source='auto', target='hi')
                    translated_title = translator.translate(original_title)
               except Exception as e:
                    print(f"Could not translate title: {e}")
                    translated_title = original_title
               
               announcement = f"{hindi_numbers[i]} है: {translated_title}"
               print(announcement)
               bolo_func(announcement)
            
            bolo_func("आप किस खबर के बारे में विस्तार से जानना चाहेंगे? कृपया 1 से 5 के बीच का नंबर बताएं, या 'बंद करो' कहें।")
            return True
        else:
            bolo_func(f"माफ़ कीजिए, मुझे '{query}' विषय पर कोई ताज़ा खबर नहीं मिली।")
            return False

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.json()}")
        bolo_func("माफ़ कीजिए, समाचार सेवा से संपर्क नहीं हो पा रहा है।")
        return False
    except Exception as e:
        print(f"An unexpected news error occurred: {e}")
        bolo_func("खबरें प्राप्त करते समय एक अप्रत्याशित त्रुटि हुई।")
        return False

def explain_news_detail(number, bolo_func):
    """
    Explains the news details for the selected article and then asks the user if they want to hear another.
    """
    global articles_cache
    try:
        article = articles_cache[number - 1]
        detail = article.get('description') or article.get('content') or "इस खबर के बारे में अधिक जानकारी उपलब्ध नहीं है।"
        
        try:
            translator = GoogleTranslator(source='auto', target='hi')
            translated_detail = translator.translate(detail)
        except Exception as e:
            print(f"Could not translate detail: {e}")
            translated_detail = detail

        bolo_func(f"ठीक है, सुनिए: {translated_detail}")
        bolo_func("क्या आप कोई और खबर विस्तार से सुनना चाहेंगे?")
    
    except IndexError:
        bolo_func("माफ़ कीजिए, यह एक अमान्य नंबर है। कृपया फिर से प्रयास करें।")
    except Exception as e:
        print(f"Error explaining news detail: {e}")
        bolo_func("विवरण बताते समय एक त्रुटि हुई।")


def process_news_selection(command, bolo_func):
    """
    Handles user's choice of news headline. Allows for multiple selections
    and exits when a specific exit command is given.
    """
    hindi_to_int = {
        "एक": 1, "१": 1, "1": 1,"नंबर एक": 1, 
    "पहला": 1, "पहली": 1, "पहिले": 1, "पहिलौ": 1,
    "इक": 1, "इक्का": 1, "इकाई": 1, "एको": 1,
    "वन": 1, "फर्स्ट": 1, "फस्ट": 1,

    "दो": 2, "२": 2, "2": 2,"नंबर दो": 2,
    "दूसरा": 2, "दूसरी": 2, "दुसरा": 2, "दुसरी": 2,
    "दू": 2, "दुई": 2, "दु": 2,
    "जुड़वा": 2, "डबल": 2,
    "टू": 2,  "सेकंड": 2, "सिकंड": 2,

    "तीन": 3, "३": 3, "3": 3, "नंबर तीन": 3,
    "तीसरा": 3, "तीसरी": 3, "तिसरा": 3, "तिसरी": 3,
    "तिन": 3, "त्रि": 3, "त्रिक": 3, "तेइसरा": 3,
    "थ्री": 3, "थर्ड": 3, "थरड": 3,

    "चार": 4, "४": 4, "4": 4,
    "चौथा": 4, "चौथी": 4,"नंबर चार": 4,
    "चारी": 4, "चौती": 4, "चौति": 4, "चौर": 4, "चौह": 4,
    "फोर": 4, "फोर्थ": 4, "फोरथ": 4, "क्वाड": 4,

    "पांच": 5, "५": 5, "5": 5, "पाँच": 5, "नंबर पांच": 5,
    "पांचवा": 5, "पाँचवा": 5, "पांचवीं": 5,
    "पांचे": 5, "पांचो": 5, "पंच": 5, "पंचम": 5,
    "फाइव": 5,  "फिफ्थ": 5, "फिफट": 5,
    }
    
    for word, number in hindi_to_int.items():
        if word in command:
            explain_news_detail(number, bolo_func)
            return False 

    exit_triggers = Config.goodbye_triggers + Config.news_exit_triggers
    if any(phrase in command for phrase in exit_triggers):
        bolo_func("ठीक है, खबरों का सत्र समाप्त हुआ।")
        global articles_cache
        articles_cache = [] 
        return True 
        
   
    return False