"""
Simple Calculator & Number Helper for Illiterate Users
Helps with basic math, counting money, measuring land, etc.
"""

import re
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class SimpleCalculatorService:
    def __init__(self):
        """Initialize calculator service"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None
        
        # Hindi number words
        self.hindi_numbers = {
            'एक': 1, 'दो': 2, 'तीन': 3, 'चार': 4, 'पांच': 5,
            'छह': 6, 'सात': 7, 'आठ': 8, 'नौ': 9, 'दस': 10,
            'ग्यारह': 11, 'बारह': 12, 'तेरह': 13, 'चौदह': 14, 'पंद्रह': 15,
            'सोलह': 16, 'सत्रह': 17, 'अठारह': 18, 'उन्नीस': 19, 'बीस': 20,
            'तीस': 30, 'चालीस': 40, 'पचास': 50, 'साठ': 60,
            'सत्तर': 70, 'अस्सी': 80, 'नब्बे': 90, 'सौ': 100,
            'हजार': 1000, 'लाख': 100000, 'करोड़': 10000000
        }
        
        # Units for agriculture/land
        self.land_units = {
            'एकड़': 'acre', 'bigha': 'bigha', 'बीघा': 'bigha',
            'हेक्टेयर': 'hectare', 'गुंठा': 'guntha'
        }
        
        # Common calculations for farmers/laborers
        self.calc_keywords = [
            'जोड़', 'add', 'plus', 'और', 'मिलाकर',
            'घटा', 'subtract', 'minus', 'कम',
            'गुणा', 'multiply', 'times', 'बार',
            'भाग', 'divide', 'बांटो', 'हिस्सा',
            'कुल', 'total', 'जोड़', 'कितना'
        ]
    
    def is_configured(self):
        """Check if service is configured"""
        return self.model is not None
    
    def detect_calculation_query(self, query):
        """Detect if query needs calculation"""
        query_lower = query.lower()
        
        # Check for calculation keywords
        has_calc_keyword = any(keyword in query_lower for keyword in self.calc_keywords)
        
        # Check for numbers
        has_numbers = bool(re.search(r'\d+', query)) or any(word in query_lower for word in self.hindi_numbers.keys())
        
        return has_calc_keyword and has_numbers
    
    def solve_with_explanation(self, query):
        """
        Solve calculation and explain in simple terms
        """
        if not self.is_configured():
            return None, "Calculator service not available"
        
        try:
            prompt = f"""
            तुम एक बहुत ही सरल तरीके से गणित समझाने वाले शिक्षक हो।
            एक अनपढ़ व्यक्ति ने तुमसे यह सवाल पूछा है:
            
            सवाल: {query}
            
            कृपया:
            1. सबसे पहले सवाल को सरल हिंदी में दोहराओ
            2. चरण-दर-चरण हल करके दिखाओ (बहुत आसान तरीके से)
            3. रोज़मर्रा के उदाहरण से समझाओ
            4. अंत में जवाब बड़े अक्षरों में बताओ: "जवाब: [संख्या]"
            
            उदाहरण:
            सवाल: 5 बोरी चावल हैं, हर बोरी में 50 किलो है, कुल कितना चावल है?
            
            जवाब:
            आपके पास 5 बोरी चावल हैं।
            हर एक बोरी में 50 किलो चावल है।
            
            तो, 5 बोरी x 50 किलो = 250 किलो
            
            जवाब: 250 किलो चावल
            
            अब इसी तरह समझाओ (केवल हिंदी में):
            """
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                clean_text = ' '.join(response.text.strip().split())
                return clean_text, None
            else:
                return None, "हल नहीं मिला"
                
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    def help_with_money_counting(self, query):
        """Help count money - especially useful for daily wages"""
        if not self.is_configured():
            return None, "Service not available"
        
        try:
            prompt = f"""
            एक मजदूर/किसान को पैसे गिनने में मदद करो।
            
            सवाल: {query}
            
            सरल हिंदी में:
            1. कुल पैसे कितने हैं
            2. अगर नोट/सिक्के हैं तो गिनती बताओ
            3. यह कितने दिन की मजदूरी/कमाई है
            
            बहुत आसान भाषा में बताओ।
            
            जवाब (केवल हिंदी में):
            """
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                clean_text = ' '.join(response.text.strip().split())
                return clean_text, None
            else:
                return None, "गणना नहीं हो पाई"
                
        except Exception as e:
            return None, f"Error: {str(e)}"


# Global instance
_calculator_service = None

def get_calculator_service():
    """Get or create calculator service"""
    global _calculator_service
    if _calculator_service is None:
        _calculator_service = SimpleCalculatorService()
    return _calculator_service


def handle_calculation_query(query, voice_output_func):
    """Handle calculation queries"""
    service = get_calculator_service()
    
    if not service.detect_calculation_query(query):
        return False
    
    if not service.is_configured():
        print("Calculator service not available")
        return False
    
    print(f"Processing calculation: {query}")
    
    # Check if it's about money counting
    money_keywords = ['पैसे', 'रुपये', 'कमाई', 'मजदूरी', 'तनख्वाह', 'नोट']
    is_money = any(keyword in query.lower() for keyword in money_keywords)
    
    if is_money:
        result, error = service.help_with_money_counting(query)
    else:
        result, error = service.solve_with_explanation(query)
    
    if error:
        print(f"Error: {error}")
        return True
    
    if result:
        print(f"Result: {result}")
        voice_output_func(result, lang='hi')
        return True
    
    return False


# Test function
if __name__ == "__main__":
    service = SimpleCalculatorService()
    
    print("=" * 70)
    print("🔢 Testing Simple Calculator for Illiterate Users")
    print("=" * 70)
    
    if not service.is_configured():
        print("❌ Service not configured")
        exit(1)
    
    print("✅ Service ready\n")
    
    test_queries = [
        "5 बोरी चावल हैं, हर बोरी में 50 किलो है, कुल कितना?",
        "मेरी 300 रुपये रोज़ की मजदूरी है, 10 दिन में कितना होगा?",
        "1000 रुपये में से 350 खर्च किए, कितने बचे?",
        "2 एकड़ ज़मीन में 50 किलो बीज चाहिए, 5 एकड़ में कितना?",
        "20 मज़दूरों को 500 रुपये बांटने हैं, हर एक को कितना मिलेगा?",
    ]
    
    for query in test_queries:
        print("\n" + "=" * 70)
        print(f"Q: {query}")
        print("-" * 70)
        
        result, error = service.solve_with_explanation(query)
        if not error:
            print(f"A: {result}")
        else:
            print(f"Error: {error}")
    
    print("\n" + "=" * 70)
    print("✅ Test Complete!")
    print("=" * 70)
