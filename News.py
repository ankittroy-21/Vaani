import requests
import Config
import os
from deep_translator import GoogleTranslator
import random

# The global articles_cache is no longer needed!

def get_news(command, bolo_func):
    words_to_remove = set(Config.news_junk + Config.news_trigger)
    command_words = command.split()
    query_words = [word for word in command_words if word not in words_to_remove]
    query = " ".join(query_words)
        
    try:
        # ... (rest of your URL and request logic is fine)
        if query:
            #...
            url = f"https://gnews.io/api/v4/search?q={query}&lang=hi&country=in&max=5&apikey={os.getenv('GNEWS_API_KEY')}"
        else:
            #...
            url = f"https://gnews.io/api/v4/top-headlines?category=general&lang=hi&country=in&max=5&apikey={os.getenv('GNEWS_API_KEY')}"

        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()
        articles = news_data.get("articles", [])
        
        if articles:
            display_topic = query if query else "आज" 
            summary_intro = random.choice(Config.news_summary_responses).format(display_topic)
            bolo_func(summary_intro)
            
            hindi_numbers = [" पहली खबर", " दूसरी खबर", " तीसरी खबर", " चौथी खबर", " पांचवी खबर"]

            for i, article in enumerate(articles):
               # ... (your translation and speaking logic is fine)
               translated_title = article['title'] # Simplified for example
               announcement = f"{hindi_numbers[i]} है: {translated_title}"
               bolo_func(announcement)
            
            bolo_func("आप किस खबर के बारे में विस्तार से जानना चाहेंगे? कृपया 1 से 5 के बीच का नंबर बताएं, या 'बंद करो' कहें।")
            return articles  # <<-- IMPORTANT: Return articles for context
        else:
            bolo_func(f"माफ़ कीजिए, मुझे '{query}' विषय पर कोई ताज़ा खबर नहीं मिली।")
            return [] # <<-- IMPORTANT: Return empty list on failure

    except Exception as e:
        print(f"An unexpected news error occurred: {e}")
        bolo_func("खबरें प्राप्त करते समय एक अप्रत्याशित त्रुटि हुई।")
        return [] # <<-- IMPORTANT: Return empty list on error

def explain_news_detail(number, bolo_func, context):
    """Explains the news details for the selected article from the context."""
    articles = context.data.get('articles', [])
    try:
        article = articles[number - 1]
        detail = article.get('description') or article.get('content') or "इस खबर के बारे में अधिक जानकारी उपलब्ध नहीं है।"
        
        # ... (your translation logic is fine)
        translated_detail = detail

        bolo_func(f"ठीक है, सुनिए: {translated_detail}")
    
    except IndexError:
        bolo_func("माफ़ कीजिए, यह एक अमान्य नंबर है। कृपया 1 से 5 के बीच का नंबर चुनें।")
    except Exception as e:
        print(f"Error explaining news detail: {e}")
        bolo_func("विवरण बताते समय एक त्रुटि हुई।")

def process_news_selection(command, bolo_func, context):
    """Handles user's choice of news headline using the context object."""
    hindi_to_int = { "एक": 1, "पहला": 1, "1": 1, "दो": 2, "दूसरा": 2, "2": 2, # etc.
                     "तीन": 3, "तीसरा": 3, "3": 3, "चार": 4, "चौथा": 4, "4": 4, "पांच": 5, "पांचवा": 5, "5": 5 }
    
    for word, number in hindi_to_int.items():
        if word in command:
            explain_news_detail(number, bolo_func, context)
            bolo_func("क्या आप किसी और खबर के बारे में जानना चाहेंगे?")
            return False # Keep the context active

    exit_triggers = Config.goodbye_triggers + Config.news_exit_triggers
    if any(phrase in command for phrase in exit_triggers):
        bolo_func("ठीक है, खबरों का सत्र समाप्त हुआ।")
        return True # Signal to main to clear the context
        
    # If the command is not a number or an exit command
    bolo_func("मैं समझी नहीं, कृपया 1 से 5 के बीच का कोई नंबर बताएं या 'बंद करो' कहें।")
    return False # Keep the context active