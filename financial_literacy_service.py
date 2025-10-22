"""
Financial Literacy & Assistance Service for Illiterate Users
SDG Goal 1: No Poverty
Helps users understand banking, savings, loans, and financial schemes
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class FinancialLiteracyService:
    def __init__(self):
        """Initialize financial literacy service"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None
            print("Warning: GEMINI_API_KEY not found")
        
        # Common financial topics for illiterate users
        self.topics = {
            'banking': {
                'keywords': ['बैंक', 'खाता', 'account', 'atm', 'passbook', 'पासबुक', 'balance', 'बैलेंस'],
                'help': 'बैंक खाता, पैसे जमा करना, निकालना, ATM इस्तेमाल करना'
            },
            'savings': {
                'keywords': ['बचत', 'saving', 'जमा', 'deposit', 'पैसे बचाना', 'fixed deposit', 'एफडी'],
                'help': 'पैसे बचाना, बचत खाता, सुरक्षित तरीके से पैसे रखना'
            },
            'loans': {
                'keywords': ['लोन', 'loan', 'कर्ज', 'ब्याज', 'interest', 'emi', 'किस्त', 'उधार'],
                'help': 'लोन कैसे लें, ब्याज क्या है, EMI कैसे चुकाएं'
            },
            'insurance': {
                'keywords': ['बीमा', 'insurance', 'फसल बीमा', 'जीवन बीमा', 'स्वास्थ्य बीमा'],
                'help': 'बीमा क्या है, फसल बीमा, जीवन बीमा, परिवार को सुरक्षा'
            },
            'pension': {
                'keywords': ['पेंशन', 'pension', 'बुढ़ापा', 'retirement', 'वृद्धावस्था'],
                'help': 'पेंशन योजना, बुढ़ापे की सुरक्षा, सरकारी पेंशन'
            },
            'digital_payment': {
                'keywords': ['upi', 'यूपीआई', 'phonepe', 'paytm', 'google pay', 'डिजिटल पेमेंट', 'qr code'],
                'help': 'UPI कैसे चलाएं, फोन से पेमेंट, QR कोड स्कैन करना'
            },
            'scam_protection': {
                'keywords': ['धोखा', 'fraud', 'scam', 'फ्रॉड', 'ठगी', 'otp', 'pin'],
                'help': 'धोखाधड़ी से बचाव, OTP किसी को न दें, सुरक्षित रहें'
            },
            'money_management': {
                'keywords': ['खर्च', 'budget', 'बजट', 'हिसाब', 'पैसे का प्रबंधन', 'expense'],
                'help': 'पैसे का हिसाब रखना, खर्च कम करना, बचत बढ़ाना'
            }
        }
    
    def is_configured(self):
        """Check if Gemini API is configured"""
        return self.model is not None
    
    def detect_financial_query(self, query):
        """Detect if query is about financial literacy"""
        query_lower = query.lower()
        
        for topic, info in self.topics.items():
            if any(keyword in query_lower for keyword in info['keywords']):
                return True, topic
        
        return False, None
    
    def get_simple_explanation(self, query, topic=None):
        """
        Get simple, visual explanation suitable for illiterate users
        Uses storytelling and examples from daily life
        """
        if not self.is_configured():
            return None, "Financial literacy service not available"
        
        try:
            # Create a prompt optimized for illiterate users
            prompt = f"""
            तुम एक बहुत ही सरल और प्यार से समझाने वाले शिक्षक हो।
            तुम्हें एक अनपढ़ किसान या मजदूर को समझाना है जिसने कभी स्कूल नहीं गया।
            
            सवाल: {query}
            
            कृपया इस तरह समझाओ:
            
            1. बहुत ही आसान हिंदी में (जैसे 5 साल के बच्चे को समझाते हैं)
            2. रोज़मर्रा की कहानी या उदाहरण से समझाओ
            3. तकनीकी शब्दों का इस्तेमाल मत करो
            4. 3-4 छोटे वाक्यों में समझाओ
            5. चरण-दर-चरण (step by step) बताओ
            6. सकारात्मक और उत्साहवर्धक लहजे में
            7. अगर किसी धोखे से बचना है तो ज़रूर बताओ
            
            उदाहरण:
            - बैंक = "बैंक आपके पैसों का तिजोरी है, जहाँ आपके पैसे सुरक्षित रहते हैं"
            - ATM = "ATM एक मशीन है जहाँ से आप अपने कार्ड से पैसे निकाल सकते हैं, जैसे दुकान से सामान निकालते हैं"
            
            अब समझाओ (केवल हिंदी में):
            """
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                clean_text = ' '.join(response.text.strip().split())
                return clean_text, None
            else:
                return None, "व्याख्या नहीं मिली"
                
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(error_msg)
            return None, "कुछ तकनीकी समस्या आई"
    
    def get_step_by_step_guide(self, task):
        """
        Get step-by-step audio guide for tasks like opening bank account, using ATM
        """
        if not self.is_configured():
            return None, "Service not available"
        
        try:
            prompt = f"""
            एक अनपढ़ व्यक्ति को चरण-दर-चरण बहुत सरल हिंदी में समझाओ:
            
            काम: {task}
            
            हर चरण को इस तरह बताओ:
            - पहले क्या करें
            - फिर क्या करें
            - आखिर में क्या होगा
            
            बहुत ही आसान भाषा में, जैसे छोटे बच्चे को सिखाते हैं।
            कोई अंग्रेजी शब्द नहीं।
            5-6 छोटे चरणों में बताओ।
            
            जवाब (केवल हिंदी में):
            """
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                clean_text = ' '.join(response.text.strip().split())
                return clean_text, None
            else:
                return None, "गाइड नहीं मिली"
                
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    def warn_about_scam(self, query):
        """Detect potential scam scenarios and warn user"""
        scam_keywords = [
            'otp दो', 'pin बताओ', 'पासवर्ड दो', 'account number बताओ',
            'कार्ड नंबर', 'cvv', 'लॉटरी जीती', 'इनाम मिला', 
            'मुफ्त पैसे', 'free money', 'link पर click'
        ]
        
        query_lower = query.lower()
        
        for keyword in scam_keywords:
            if keyword in query_lower:
                return True, """
                ⚠️ धोखाधड़ी की चेतावनी! ⚠️
                
                याद रखें:
                1. अपना OTP, PIN, CVV किसी को न बताएं - बैंक वाले भी नहीं पूछते!
                2. किसी अनजान लिंक पर क्लिक न करें
                3. "लॉटरी जीती" या "मुफ्त पैसे" के झांसे में न आएं
                4. संदेह हो तो बैंक जाकर खुद पूछें
                5. अगर कोई जबरदस्ती करे तो 1930 (साइबर क्राइम) पर कॉल करें
                
                आपकी सुरक्षा सबसे ज़रूरी है! 🛡️
                """
        
        return False, None


# Global instance
_financial_service = None

def get_financial_service():
    """Get or create financial literacy service"""
    global _financial_service
    if _financial_service is None:
        _financial_service = FinancialLiteracyService()
    return _financial_service


def handle_financial_query(query, voice_output_func):
    """
    Handle financial literacy queries
    """
    service = get_financial_service()
    
    # Check for scam warning
    is_scam, warning = service.warn_about_scam(query)
    if is_scam:
        print(warning)
        voice_output_func(warning)
        return True
    
    # Detect if it's a financial query
    is_financial, topic = service.detect_financial_query(query)
    
    if not is_financial:
        return False
    
    if not service.is_configured():
        print("Financial literacy service not available")
        return False
    
    print(f"Processing financial query (topic: {topic}): {query}")
    
    # Check if it's a "how to" query
    how_to_keywords = ['कैसे', 'how', 'तरीका', 'सिखाओ', 'बताओ कैसे']
    is_how_to = any(keyword in query.lower() for keyword in how_to_keywords)
    
    if is_how_to:
        # Provide step-by-step guide
        guide, error = service.get_step_by_step_guide(query)
        if error:
            print(f"Error: {error}")
            return True
        if guide:
            print(f"Guide: {guide}")
            voice_output_func(guide, lang='hi')
            return True
    else:
        # Provide simple explanation
        explanation, error = service.get_simple_explanation(query, topic)
        if error:
            print(f"Error: {error}")
            return True
        if explanation:
            print(f"Explanation: {explanation}")
            voice_output_func(explanation, lang='hi')
            return True
    
    return False


# Test function
if __name__ == "__main__":
    service = FinancialLiteracyService()
    
    print("=" * 70)
    print("💰 Testing Financial Literacy Service (SDG Goal 1)")
    print("=" * 70)
    
    if not service.is_configured():
        print("❌ Gemini API not configured")
        exit(1)
    
    print("✅ Service configured\n")
    
    # Test queries from illiterate users
    test_queries = [
        "बैंक में खाता कैसे खोलें?",
        "ATM से पैसे कैसे निकालें?",
        "लोन क्या होता है?",
        "UPI कैसे चलाते हैं?",
        "फसल बीमा क्या है?",
        "पैसे बचाने का क्या तरीका है?",
        "OTP किसी को देना चाहिए?",  # Scam test
    ]
    
    for query in test_queries:
        print("\n" + "=" * 70)
        print(f"Q: {query}")
        print("-" * 70)
        
        # Check for scam
        is_scam, warning = service.warn_about_scam(query)
        if is_scam:
            print(warning)
            continue
        
        # Get explanation
        is_financial, topic = service.detect_financial_query(query)
        if is_financial:
            print(f"Topic: {topic}")
            explanation, error = service.get_simple_explanation(query, topic)
            if not error:
                print(f"A: {explanation}")
            else:
                print(f"Error: {error}")
    
    print("\n" + "=" * 70)
    print("✅ Test Complete!")
    print("=" * 70)
