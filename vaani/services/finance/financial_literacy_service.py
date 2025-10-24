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
    
    def get_quick_answer(self, query):
        """Get quick pre-defined answers for common questions to save API calls"""
        query_lower = query.lower()
        
        # Quick answers dictionary - SHORT and CRISP
        quick_answers = {
            'खाता': 'बैंक खाता आपके पैसों का सुरक्षित घर है। पैसे बैंक में रखो, सुरक्षित रहेंगे। आधार कार्ड लेकर बैंक जाओ।',
            'atm': 'एटीएम एक मशीन है जहाँ से आप कार्ड डालकर पैसे निकाल सकते हो। पिन नंबर किसी को मत बताना।',
            'बचत': 'हर महीने थोड़े पैसे अलग रखो। छोटी-छोटी बचत बड़ी होती है। बैंक में जमा करो, ब्याज मिलेगा।',
            'लोन': 'लोन मतलब उधार पैसे। वापस करने में ब्याज भी देना पड़ता है। सिर्फ ज़रूरत पर लो।',
            'emi': 'ईएमआई मतलब हर महीने की किस्त। लोन को छोटे हिस्सों में चुकाना। समय पर दो।',
            'बीमा': 'बीमा एक सुरक्षा है। छोटी रकम देकर बड़ी परेशानी से बचाव। फसल बीमा, जीवन बीमा लो।',
            'upi': 'यूपीआई से फोन से पेमेंट करो। बहुत आसान और सुरक्षित। पिन किसी को मत बताना।',
            'otp': 'ओटीपी को किसी को भी मत बताओ। यह आपका गुप्त कोड है। बैंक कभी फोन पर नहीं माँगता।',
            'धोखा': 'किसी को भी ओटीपी, पिन, या कार्ड नंबर मत बताओ। बैंक कभी फोन पर नहीं माँगता।',
            'fraud': 'किसी को भी ओटीपी, पिन, या कार्ड नंबर मत बताओ। बैंक कभी फोन पर नहीं माँगता।',
            'पेंशन': 'पेंशन बुढ़ापे का सहारा है। सरकारी योजनाओं में जुड़ो। हर महीने पैसे मिलेंगे।',
            'ब्याज': 'ब्याज पैसों पर मिलने वाला फायदा है। बैंक में पैसे रखो तो ब्याज मिलता है। लोन पर ब्याज देना पड़ता है।'
        }
        
        for key, answer in quick_answers.items():
            if key in query_lower:
                return answer
        
        return None
    
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
        # First check if we have a quick answer
        quick_answer = self.get_quick_answer(query)
        if quick_answer:
            return quick_answer, None
        
        if not self.is_configured():
            return None, "Financial literacy service not available"
        
        try:
            # Create a prompt optimized for illiterate users - VERY SHORT
            prompt = f"""
            एक अनपढ़ व्यक्ति से बात कर रहे हो। बहुत छोटा जवाब दो।
            
            सवाल: {query}
            
            नियम:
            1. केवल 2-3 छोटे वाक्य (maximum 30-40 words)
            2. बहुत आसान हिंदी, कोई अंग्रेजी नहीं
            3. रोज़मर्रा का उदाहरण दो
            4. तकनीकी शब्द बिल्कुल नहीं
            
            बहुत छोटा जवाब दो (2-3 वाक्य):
            """
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                # Better formatting: Fix extra whitespace but preserve paragraphs
                lines = response.text.strip().split('\n')
                clean_lines = [' '.join(line.split()) for line in lines]
                clean_text = '\n'.join(clean_lines)
                # Remove markdown formatting that causes issues in TTS
                clean_text = clean_text.replace('**', '')
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
            एक अनपढ़ व्यक्ति को बताओ: {task}
            
            नियम:
            1. केवल 3-4 मुख्य चरण (बहुत छोटे)
            2. हर चरण में 1-2 वाक्य
            3. कुल 40-50 शब्द maximum
            4. बहुत आसान हिंदी, कोई अंग्रेजी नहीं
            
            बहुत छोटा जवाब दो:
            """
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                # Better formatting: Fix extra whitespace but preserve paragraphs
                lines = response.text.strip().split('\n')
                clean_lines = [' '.join(line.split()) for line in lines]
                clean_text = '\n'.join(clean_lines)
                # Remove markdown formatting that causes issues in TTS
                clean_text = clean_text.replace('**', '')
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
