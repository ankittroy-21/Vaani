"""
Enhanced News Service for Illiterate Users (SDG Goal 1)
Makes news consumption easier for users with limited or no literacy
"""

import requests
from vaani.core import config as Config
import os
import random
import time
import hashlib
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='news_service.log'
)

logger = logging.getLogger('news_service')

# Cache for offline news access
NEWS_CACHE_FILE = "data/offline_cache/news_cache.json"
NEWS_CACHE_EXPIRY = 3600  # Cache news for 1 hour

class NewsService:
    def __init__(self):
        """Initialize the news service with cache support"""
        self.ensure_cache_dir()
        self.cache = self.load_cache()
        self.news_triggers = set(Config.news_trigger)
        self.news_junk = set(Config.news_junk if hasattr(Config, 'news_junk') else [])
        self.number_words = {
            "पहली": 0, "एक": 0, "1": 0, "पहला": 0, "फर्स्ट": 0,
            "दूसरी": 1, "दो": 1, "2": 1, "दूसरा": 1, "सेकंड": 1,
            "तीसरी": 2, "तीन": 2, "3": 2, "तीसरा": 2, "थर्ड": 2,
            "चौथी": 3, "चार": 3, "4": 3, "चौथा": 3, "फोर्थ": 3,
            "पांचवी": 4, "पांच": 4, "5": 4, "पांचवां": 4, "फिफ्थ": 4
        }
        self.repetition_counter = 0
        self.last_query = ""
    
    def ensure_cache_dir(self):
        """Ensure the cache directory exists"""
        cache_dir = os.path.dirname(NEWS_CACHE_FILE)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def load_cache(self):
        """Load news cache"""
        if os.path.exists(NEWS_CACHE_FILE):
            try:
                import json
                with open(NEWS_CACHE_FILE, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                return cache
            except Exception as e:
                logger.error(f"Error loading news cache: {str(e)}")
                return {}
        return {}
    
    def save_cache(self, cache_data):
        """Save news to cache"""
        try:
            import json
            with open(NEWS_CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            logger.info("News cache updated")
            return True
        except Exception as e:
            logger.error(f"Error saving news cache: {str(e)}")
            return False
    
    def is_cache_valid(self, cache_key):
        """Check if cached news is still valid"""
        if cache_key in self.cache:
            cache_time = self.cache[cache_key].get("timestamp", 0)
            current_time = time.time()
            return (current_time - cache_time) < NEWS_CACHE_EXPIRY
        return False
    
    def get_news(self, command, bolo_func):
        """Get news based on user command with cache support"""
        # Extract query from command
        query = self.extract_query(command)
        
        # Generate cache key
        cache_key = hashlib.md5((query or "top_news").encode()).hexdigest()
        
        # Check if we have valid cached news
        if self.is_cache_valid(cache_key):
            logger.info(f"Using cached news for query: {query or 'top_news'}")
            cached_news = self.cache[cache_key]
            articles = cached_news["articles"]
            
            # Announce the news source
            source = "कैश से" if query else "कैश से आज के शीर्षक"
            bolo_func(f"{source} समाचार सुनिए")
            
            # Read out cached news summaries
            self.announce_news_headlines(articles, bolo_func)
            
            # Prompt for selection
            self.prompt_for_selection(bolo_func)
            
            return articles
        
        # If not in cache or expired, fetch from API
        try:
            api_key = os.getenv('GNEWS_API_KEY')
            if not api_key:
                # No API key, try using any cached news even if expired
                if cache_key in self.cache:
                    old_news = self.cache[cache_key]
                    bolo_func("पुराने समाचार सुनिए, इंटरनेट कनेक्शन नहीं है")
                    self.announce_news_headlines(old_news["articles"], bolo_func)
                    self.prompt_for_selection(bolo_func)
                    return old_news["articles"]
                else:
                    # No cache at all
                    bolo_func("माफ़ कीजिए, समाचार प्राप्त करने में त्रुटि हुई। इंटरनेट कनेक्शन जांचें।")
                    return []
            
            # Build API URL
            if query:
                url = f"https://gnews.io/api/v4/search?q={query}&lang=hi&country=in&max=5&apikey={api_key}"
            else:
                url = f"https://gnews.io/api/v4/top-headlines?category=general&lang=hi&country=in&max=5&apikey={api_key}"
            
            # Make API request
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            news_data = response.json()
            articles = news_data.get("articles", [])
            
            if articles:
                # Cache the news
                self.cache[cache_key] = {
                    "query": query,
                    "articles": articles,
                    "timestamp": time.time()
                }
                self.save_cache(self.cache)
                
                # Announce news
                display_topic = query if query else "आज"
                summary_intro = random.choice(Config.news_summary_responses).format(display_topic)
                bolo_func(summary_intro)
                
                # Read out news headlines
                self.announce_news_headlines(articles, bolo_func)
                
                # Prompt for selection
                self.prompt_for_selection(bolo_func)
                
                return articles
            else:
                bolo_func(f"माफ़ कीजिए, मुझे '{query if query else 'आज'}' विषय पर कोई ताज़ा खबर नहीं मिली।")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching news: {str(e)}")
            # Try using expired cache in case of error
            if cache_key in self.cache:
                old_news = self.cache[cache_key]
                bolo_func("इंटरनेट त्रुटि के कारण पुराने समाचार सुनिए")
                self.announce_news_headlines(old_news["articles"], bolo_func)
                self.prompt_for_selection(bolo_func)
                return old_news["articles"]
            else:
                bolo_func("माफ़ कीजिए, समाचार प्राप्त करने में त्रुटि हुई। इंटरनेट कनेक्शन जांचें।")
                return []
    
    def extract_query(self, command):
        """Extract news query from command"""
        # Filter out junk words and news trigger words
        words = command.lower().split()
        query_words = [word for word in words 
                      if word not in self.news_triggers 
                      and word not in self.news_junk]
        
        # Join filtered words to form query
        return " ".join(query_words)
    
    def announce_news_headlines(self, articles, bolo_func):
        """Announce news headlines in a simple format for illiterate users"""
        hindi_numbers = ["पहली खबर", "दूसरी खबर", "तीसरी खबर", "चौथी खबर", "पांचवी खबर"]
        
        for i, article in enumerate(articles[:5]):
            # Get title and clean it
            title = article.get('title', '')
            # Remove source name after dash if present
            if ' - ' in title:
                title = title.split(' - ')[0]
            
            # Announce with number
            announcement = f"{hindi_numbers[i]}: {title}"
            bolo_func(announcement)
            
            # Small pause between headlines for better comprehension
            time.sleep(0.5)
    
    def prompt_for_selection(self, bolo_func):
        """Prompt user to select a news item in simple language"""
        prompts = [
            "कौन सी खबर के बारे में और जानना चाहेंगे? बस नंबर बोलिए - एक, दो, तीन, चार या पांच।",
            "किस खबर की पूरी जानकारी चाहिए? नंबर बोलें, जैसे 'पहली', 'दूसरी'।",
            "कौन सी खबर अच्छी लगी? उसका नंबर बताइए।",
            "किस खबर के बारे में विस्तार से सुनेंगे? नंबर बोलें।"
        ]
        bolo_func(random.choice(prompts))
    
    def get_article_number(self, command):
        """Extract article number from user command"""
        words = command.lower().split()
        
        # First check for direct number matches
        for word in words:
            if word in self.number_words:
                return self.number_words[word] + 1  # +1 because index is 0-based but we speak 1-based
        
        # If not found, check for word sequences like "पहली खबर"
        for i, word in enumerate(words):
            if i < len(words) - 1 and word in self.number_words:
                next_word = words[i+1]
                if next_word in ["खबर", "समाचार", "न्यूज़", "नंबर"]:
                    return self.number_words[word] + 1
        
        # Fallback: see if any number word appears in the command
        for number_word in self.number_words:
            if number_word in command.lower():
                return self.number_words[number_word] + 1
        
        return None
    
    def process_news_selection(self, command, bolo_func, context):
        """Process user's news selection with fallback mechanisms"""
        # Store command for repetition tracking
        if command.lower() == self.last_query.lower():
            self.repetition_counter += 1
        else:
            self.repetition_counter = 0
            self.last_query = command
        
        # If user repeats the same command 2+ times, try harder to understand
        if self.repetition_counter >= 2:
            # User seems stuck, try all available numbers
            for i in range(1, 6):
                try:
                    self.explain_news_detail(i, bolo_func, context)
                    self.repetition_counter = 0
                    return False  # Keep context active
                except:
                    continue
            
            # If nothing worked, exit news mode
            bolo_func("माफ़ कीजिए, आपका प्रश्न समझ नहीं आया। समाचार सत्र समाप्त करते हैं।")
            return True  # Exit news mode
        
        # Check for exit commands first
        exit_triggers = Config.goodbye_triggers + getattr(Config, 'news_exit_triggers', ['बंद करो', 'बंद', 'कोई नहीं', 'समाप्त'])
        if any(phrase in command.lower() for phrase in exit_triggers):
            bolo_func("ठीक है, समाचार सत्र समाप्त हुआ।")
            return True  # Exit news mode
        
        # Try to extract article number
        article_number = self.get_article_number(command)
        
        if article_number:
            try:
                self.explain_news_detail(article_number, bolo_func, context)
                # Ask if user wants to hear another news item
                follow_up = [
                    "क्या कोई और खबर सुनना चाहेंगे?",
                    "क्या दूसरी खबर भी सुनेंगे?",
                    "किसी अन्य खबर के बारे में जानेंगे?"
                ]
                bolo_func(random.choice(follow_up))
                return False  # Keep news context active
            except Exception as e:
                logger.error(f"Error explaining news: {str(e)}")
                bolo_func("माफ़ कीजिए, इस खबर के विवरण में समस्या आई है। कोई अन्य नंबर बताइए।")
                return False  # Keep news context active
        
        # Try keywords for specific news if number not found
        articles = context.data.get('articles', [])
        for i, article in enumerate(articles):
            title = article.get('title', '').lower()
            if any(word in title for word in command.lower().split()):
                self.explain_news_detail(i+1, bolo_func, context)
                bolo_func("क्या कोई और खबर सुनना चाहेंगे?")
                return False  # Keep context active
        
        # If nothing matched, guide the user
        help_messages = [
            f"कृपया सिर्फ नंबर बताएं, जैसे 'पहली', 'दूसरी' या बस '1', '2'।",
            f"खबर का नंबर बताइए, जैसे 'पहली खबर' या 'खबर नंबर 3'।",
            f"मैं समझ नहीं पाया। बस नंबर बोलिए - एक, दो, तीन, चार या पांच।"
        ]
        bolo_func(random.choice(help_messages))
        return False  # Keep context active
    
    def explain_news_detail(self, number, bolo_func, context):
        """Explains the news details for the selected article with simplification"""
        articles = context.data.get('articles', [])
        
        try:
            # Adjust for 1-based numbering to 0-based index
            index = number - 1
            if index < 0 or index >= len(articles):
                bolo_func("माफ़ कीजिए, यह नंबर गलत है। 1 से 5 के बीच नंबर बताएं।")
                return
            
            article = articles[index]
            
            # Get title
            title = article.get('title', '')
            if ' - ' in title:  # Remove source name if present
                title = title.split(' - ')[0]
            
            # Get article details
            detail = article.get('description') or article.get('content') or "इस खबर के बारे में अधिक जानकारी उपलब्ध नहीं है।"
            
            # Cleanup detail text (remove HTML and excessive whitespace)
            import re
            detail = re.sub(r'<[^>]+>', '', detail)  # Remove HTML tags
            detail = re.sub(r'\s+', ' ', detail)     # Normalize whitespace
            
            # Simplify language for illiterate users
            detail = self.simplify_news_language(detail)
            
            # Add source and date information
            source = article.get('source', {}).get('name', 'अज्ञात स्रोत')
            
            # Format date in Hindi for easier understanding
            published_date = article.get('publishedAt', '')
            date_str = ""
            if published_date:
                try:
                    date = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
                    now = datetime.now()
                    delta = now - date
                    
                    if delta.days == 0:
                        hours = delta.seconds // 3600
                        if hours < 1:
                            date_str = "कुछ मिनट पहले"
                        elif hours == 1:
                            date_str = "एक घंटा पहले"
                        else:
                            date_str = f"{hours} घंटे पहले"
                    elif delta.days == 1:
                        date_str = "कल"
                    else:
                        date_str = f"{delta.days} दिन पहले"
                except:
                    date_str = ""
            
            # Construct response with title repetition for context
            response = f"{title}। {detail} यह खबर {source} से {date_str} प्रकाशित हुई।"
            
            # Speak the news
            bolo_func(response)
            
            # If article has URL, mention it's available
            if article.get('url'):
                bolo_func("इस खबर का लिंक उपलब्ध है, आप अधिक जानकारी के लिए पूछ सकते हैं।")
            
        except Exception as e:
            logger.error(f"Error in explain_news_detail: {str(e)}")
            bolo_func("माफ़ कीजिए, इस खबर के विवरण बताने में समस्या आई है।")
    
    def simplify_news_language(self, text):
        """Simplify complex news language for easier understanding by illiterate users"""
        # Replace complex words with simpler alternatives
        simplifications = {
            'अनुसंधान': 'खोज',
            'आकलन': 'अंदाज़ा',
            'अभिव्यक्ति': 'बात',
            'प्रतिक्रिया': 'जवाब',
            'आंदोलन': 'विरोध',
            'घोषणा': 'ऐलान',
            'कार्यान्वयन': 'लागू करना',
            'अधिकारी': 'अफसर',
            'परिणाम': 'नतीजा',
            'स्थिति': 'हालात',
            'उल्लेखनीय': 'खास',
            'हस्तक्षेप': 'दखल',
            'प्रतिनिधि': 'प्रतिनिधि',
            'विशिष्ट': 'खास',
            'नीति': 'नियम',
            'कार्यक्रम': 'योजना',
            'प्रकरण': 'मामला',
            'अवसर': 'मौका',
            'क्षमता': 'ताकत',
            'संशोधन': 'बदलाव'
        }
        
        for complex_word, simple_word in simplifications.items():
            text = text.replace(complex_word, simple_word)
        
        return text

# Simplified interface for main.py integration
def get_news(command, bolo_func):
    """Get news based on command"""
    service = NewsService()
    return service.get_news(command, bolo_func)

def process_news_selection(command, bolo_func, context):
    """Process news selection based on command"""
    service = NewsService()
    return service.process_news_selection(command, bolo_func, context)