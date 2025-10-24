"""
Offline Mode Support for Vaani
Ensures essential functionality works without internet connection
"""

import os
import json
import hashlib
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='offline_mode.log'
)

logger = logging.getLogger('offline_mode')

class OfflineMode:
    def __init__(self, cache_dir="offline_cache"):
        """Initialize the offline mode manager with cache directory"""
        self.cache_dir = cache_dir
        self.ensure_cache_dir()
        self.services = {
            "financial": self.get_financial_cache_file(),
            "emergency": self.get_emergency_cache_file(),
            "agriculture": self.get_agriculture_cache_file(),
            "schemes": self.get_schemes_cache_file(),
            "calculator": self.get_calculator_cache_file()
        }
        
    def ensure_cache_dir(self):
        """Ensure the cache directory exists"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
            logger.info(f"Created cache directory: {self.cache_dir}")
    
    def is_online(self):
        """Check if internet connection is available"""
        try:
            # Try to connect to Google DNS to check internet
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False
    
    def get_cache_path(self, service):
        """Get the cache file path for a specific service"""
        return os.path.join(self.cache_dir, f"{service}_cache.json")
    
    def load_cache(self, service):
        """Load cached data for a service"""
        cache_path = self.get_cache_path(service)
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.error(f"Error decoding cache file: {cache_path}")
                return {}
        return {}
    
    def save_cache(self, service, data):
        """Save data to cache for a service"""
        cache_path = self.get_cache_path(service)
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Updated cache for {service}")
            return True
        except Exception as e:
            logger.error(f"Error saving cache for {service}: {str(e)}")
            return False
    
    def get_response(self, service, query, online_function=None):
        """
        Get response from cache or online function
        
        Args:
            service: Service type (financial, emergency, etc)
            query: The user's query
            online_function: Function to call if online
            
        Returns:
            Response text and whether it came from cache
        """
        # First check if we're online and can use the online function
        if self.is_online() and online_function:
            try:
                response = online_function(query)
                
                # Save successful response to cache
                if response:
                    cache = self.load_cache(service)
                    query_hash = hashlib.md5(query.encode()).hexdigest()
                    
                    cache[query_hash] = {
                        "query": query,
                        "response": response,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    # Find similar queries to link together
                    for existing_hash, data in list(cache.items()):
                        if self.query_similarity(query, data["query"]) > 0.7:
                            cache[existing_hash]["similar_to"] = query_hash
                    
                    self.save_cache(service, cache)
                    return response, False  # False = not from cache
                
            except Exception as e:
                logger.error(f"Error with online function: {str(e)}")
                # Fall back to cache on error
        
        # If offline or online function failed, try to find in cache
        cache = self.load_cache(service)
        if not cache:
            return self.get_fallback_response(service, query), True
        
        # Try exact match first
        query_hash = hashlib.md5(query.encode()).hexdigest()
        if query_hash in cache:
            return cache[query_hash]["response"], True
        
        # Try similarity matching
        best_match = None
        best_score = 0.6  # Minimum similarity threshold
        
        for item_hash, data in cache.items():
            similarity = self.query_similarity(query, data["query"])
            if similarity > best_score:
                best_match = item_hash
                best_score = similarity
        
        if best_match:
            return cache[best_match]["response"], True
            
        # No match found, return fallback response
        return self.get_fallback_response(service, query), True
    
    def query_similarity(self, query1, query2):
        """Calculate simple similarity between two queries"""
        # Simple implementation using set similarity
        # For production, use a more sophisticated algorithm
        words1 = set(query1.lower().split())
        words2 = set(query2.lower().split())
        
        if not words1 or not words2:
            return 0.0
            
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def get_fallback_response(self, service, query):
        """Get a fallback response when no cache is available"""
        fallbacks = {
            "financial": "मुझे खेद है, इस प्रश्न का उत्तर ऑफलाइन मोड में उपलब्ध नहीं है। कृपया इंटरनेट कनेक्शन होने पर पुनः प्रयास करें।",
            "emergency": "आपातकालीन नंबर: पुलिस: 100, एम्बुलेंस: 108, आग: 101, महिला हेल्पलाइन: 1091",
            "agriculture": "मुझे खेद है, फसल संबंधी जानकारी ऑफलाइन मोड में उपलब्ध नहीं है। कृपया इंटरनेट कनेक्शन होने पर पुनः प्रयास करें।",
            "schemes": "मुझे खेद है, योजना संबंधी जानकारी ऑफलाइन मोड में उपलब्ध नहीं है। कृपया इंटरनेट कनेक्शन होने पर पुनः प्रयास करें।",
            "calculator": "मुझे खेद है, इस गणना का उत्तर ऑफलाइन मोड में उपलब्ध नहीं है।"
        }
        return fallbacks.get(service, "इंटरनेट कनेक्शन न होने के कारण जानकारी उपलब्ध नहीं है।")
    
    # Pre-cached content files
    def get_financial_cache_file(self):
        """Get or create financial literacy cache file"""
        cache_path = self.get_cache_path("financial")
        if not os.path.exists(cache_path):
            basic_financial = {
                hashlib.md5("बैंक में खाता कैसे खोलें".encode()).hexdigest(): {
                    "query": "बैंक में खाता कैसे खोलें",
                    "response": """बैंक में खाता खोलना बहुत आसान है।
पहला कदम: बैंक में जाना और पूछना
पहले क्या करें: अपने घर के पास किसी बैंक में जाओ। बैंक की पहचान है कि वहां लोग पैसे जमा करते और निकालते हैं।
फिर क्या करें: बैंक के बाहर या अंदर तुम्हें कोई वर्दी वाला आदमी (गार्ड) या कोई बैंक का कर्मचारी मिलेगा। उससे हाथ जोड़कर कहो, "नमस्ते! मुझे अपना पैसा रखने के लिए एक खाता खुलवाना है।"
आखिर में क्या होगा: वो तुम्हें किसी अधिकारी या कर्मचारी के पास भेज देंगे, जो खाता खोलने में मदद करेगा।

दूसरा कदम: खाता खोलने वाला कागज़ (फ़ॉर्म) लेना और मदद मांगना
पहले क्या करें: जिस अधिकारी के पास तुम्हें भेजा गया है, उससे कहो, "मुझे खाता खोलने वाला एक कागज़ चाहिए।"
फिर क्या करें: अगर तुम्हें पढ़ना-लिखना नहीं आता, तो घबराना नहीं। उसी अधिकारी से या किसी और भरोसेमंद बैंक कर्मचारी से कहो, "भैया/बहनजी, मुझे यह कागज़ भरना नहीं आता, क्या आप मेरी मदद कर सकते हैं?"
आखिर में क्या होगा: बैंक कर्मचारी तुम्हारी बातों को सुनकर वह कागज़ भर देंगे।

तीसरा कदम: अपनी पहचान के कागज़ देना
पहले क्या करें: कागज़ भरते समय, वे तुमसे तुम्हारी पहचान का कोई कागज़ (जैसे आधार कार्ड, वोटर आईडी) और तुम्हारे घर के पते का कोई कागज़ मांगेंगे। ये कागज़ उनके पास जमा करवाओ।
फिर क्या करें: वे तुम्हारे हस्ताक्षर (अगर तुम अंगूठा लगाते हो, तो अंगूठे का निशान) लेंगे। बैंक कर्मचारी तुम्हें बताएँगे कि कहाँ निशान लगाना है।
आखिर में क्या होगा: बैंक के पास तुम्हारी पहचान और पते की जानकारी पहुँच जाएगी।

चौथा कदम: अपने खाते में पैसे जमा करना
पहले क्या करें: अब तुम्हें अपने नए खाते में पहली बार कुछ पैसे जमा करने होंगे। ये पैसे तुम्हारे अपने हैं। तुम ₹100 या जितने भी पैसे चाहो, जमा कर सकते हो।
फिर क्या करें: बैंक तुम्हें एक छोटी सी किताब देंगे जिसे 'पासबुक' कहते हैं। इसमें तुम्हारे जमा किए गए पैसे और निकाले गए पैसों का हिसाब लिखा होगा।
आखिर में क्या होगा: तुम्हारे पैसे बैंक में सुरक्षित जमा हो जाएँगे और तुम्हें उनकी पासबुक में एंट्री मिल जाएगी।

पांचवां कदम: तुम्हारा खाता खुल गया!
आखिर में क्या होगा: बस! अब तुम्हारा बैंक में खाता खुल गया है। तुम कभी भी बैंक आकर अपने पैसे जमा कर सकते हो और जब ज़रूरत हो, तब निकाल सकते हो। बैंक तुम्हारे पैसों का ध्यान रखेगा। यह लो, तुम्हारा बैंक खाता खुल गया! बधाई हो!""",
                    "timestamp": datetime.now().isoformat()
                },
                hashlib.md5("ATM से पैसे कैसे निकालें".encode()).hexdigest(): {
                    "query": "ATM से पैसे कैसे निकालें",
                    "response": """ATM से पैसे निकालना बहुत आसान है।
पहला कदम: ATM ढूंढना
पहले क्या करें: अपने बैंक का ATM ढूंढें। ये एक छोटे कमरे जैसा होता है, जिसमें एक मशीन लगी होती है।
फिर क्या करें: ATM के अंदर जाएं। अकेले जाना सबसे सुरक्षित है।
आखिर में क्या होगा: आप ATM मशीन के सामने खड़े हो जाएंगे।

दूसरा कदम: अपना कार्ड डालना
पहले क्या करें: अपना ATM कार्ड निकालें।
फिर क्या करें: ATM मशीन में एक छोटा सा छिद्र दिखेगा जहां तीर का निशान बना होगा, वहां अपना कार्ड डालें।
आखिर में क्या होगा: मशीन आपका कार्ड अंदर खींच लेगी।

तीसरा कदम: पिन नंबर डालना
पहले क्या करें: मशीन पर लिखा आएगा "कृपया अपना पिन नंबर डालें"।
फिर क्या करें: अपना 4 अंक का गुप्त नंबर (पिन) डालें। ध्यान रखें, इसे किसी को न दिखाएं।
आखिर में क्या होगा: मशीन आपको अगले स्क्रीन पर ले जाएगी जहां विकल्प दिखेंगे।

चौथा कदम: "पैसे निकालें" का विकल्प चुनना
पहले क्या करें: स्क्रीन पर कई बटन या विकल्प दिखेंगे।
फिर क्या करें: "पैसे निकालें" या "Cash Withdrawal" वाला बटन दबाएं।
आखिर में क्या होगा: मशीन आपसे पूछेगी कि कितने पैसे निकालना चाहते हैं।

पांचवां कदम: राशि चुनना और पैसे लेना
पहले क्या करें: जितने पैसे निकालने हैं, वो अंक डालें (जैसे: 500, 1000, 2000)।
फिर क्या करें: मशीन आपको पैसे देगी, उन्हें ले लें। फिर अपना कार्ड भी ले लें।
आखिर में क्या होगा: मशीन एक पर्ची भी देगी जिसमें लिखा होगा कितने पैसे निकाले और आपके खाते में कितने बचे। पर्ची और पैसे दोनों ले लें और बाहर आ जाएं।

याद रखें:
- अपना पिन नंबर कभी किसी को न बताएं
- ATM से पैसे निकालते समय आसपास देखते रहें
- अगर कोई परेशानी हो, तो तुरंत बैंक में बताएं""",
                    "timestamp": datetime.now().isoformat()
                }
            }
            self.save_cache("financial", basic_financial)
    
    def get_emergency_cache_file(self):
        """Get or create emergency assistance cache file"""
        cache_path = self.get_cache_path("emergency")
        if not os.path.exists(cache_path):
            emergency_data = {
                hashlib.md5("emergency numbers".encode()).hexdigest(): {
                    "query": "emergency numbers",
                    "response": """आपातकालीन नंबर (Emergency Numbers):

📞 पुलिस (Police): 100
   - चोरी, लड़ाई, खतरा

📞 एम्बुलेंस (Ambulance): 108
   - बीमारी, चोट, दुर्घटना

📞 फायर ब्रिगेड (Fire): 101
   - आग लगना

📞 महिला हेल्पलाइन: 1091
   - महिलाओं की सुरक्षा, घरेलू हिंसा

📞 बाल हेल्पलाइन: 1098
   - बच्चों की समस्या, गुम बच्चे

📞 साइबर क्राइम: 1930
   - ऑनलाइन धोखाधड़ी, UPI फ्रॉड

📞 आपदा प्रबंधन: 1078
   - बाढ़, भूकंप, तूफान

📞 किसान कॉल सेंटर: 1800-180-1551
   - फसल की समस्या, कृषि सलाह""",
                    "timestamp": datetime.now().isoformat()
                },
                hashlib.md5("सांप ने काट लिया".encode()).hexdigest(): {
                    "query": "सांप ने काट लिया",
                    "response": """🚨 तुरंत एम्बुलेंस बुलाएं: 108
        
पहली सहायता:
1. बिल्कुल शांत रहें, हिलें-डुलें नहीं
2. काटी हुई जगह को दिल से नीचे रखें
3. कसके पट्टी न बांधें
4. जड़ी-बूटी पर समय बर्बाद न करें
5. सीधे अस्पताल जाएं
        
⏰ जल्दी करें! देर मत करें!""",
                    "timestamp": datetime.now().isoformat()
                }
            }
            self.save_cache("emergency", emergency_data)
    
    def get_agriculture_cache_file(self):
        """Get or create agriculture cache file"""
        cache_path = self.get_cache_path("agriculture")
        if not os.path.exists(cache_path):
            # This will be populated from crop_data folder in the future
            self.save_cache("agriculture", {})
    
    def get_schemes_cache_file(self):
        """Get or create schemes cache file"""
        cache_path = self.get_cache_path("schemes")
        if not os.path.exists(cache_path):
            # This will be populated from scheme_data folder in the future
            self.save_cache("schemes", {})
    
    def get_calculator_cache_file(self):
        """Get or create calculator cache file"""
        cache_path = self.get_cache_path("calculator")
        if not os.path.exists(cache_path):
            # Simple calculations that can be done offline
            calc_data = {
                hashlib.md5("100 गुना 5".encode()).hexdigest(): {
                    "query": "100 गुना 5",
                    "response": "100 × 5 = 500",
                    "timestamp": datetime.now().isoformat()
                },
                hashlib.md5("1000 में से 200 घटा".encode()).hexdigest(): {
                    "query": "1000 में से 200 घटा",
                    "response": "1000 - 200 = 800",
                    "timestamp": datetime.now().isoformat()
                }
            }
            self.save_cache("calculator", calc_data)

# Example usage
if __name__ == "__main__":
    offline_mgr = OfflineMode()
    
    # Example of getting a response in offline mode
    response, from_cache = offline_mgr.get_response("financial", "बैंक अकाउंट कैसे खोलें", None)
    print(f"Response from cache: {from_cache}")
    print(response)