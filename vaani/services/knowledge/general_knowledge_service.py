"""
General Knowledge Service using Gemini API
Handles curious questions that children might ask their parents
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

load_dotenv()

class GeneralKnowledgeService:
    def __init__(self):
        """Initialize the Gemini API with the API key"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
        self.request_timeout = float(os.getenv('GEMINI_TIMEOUT_SECONDS', '4.5'))
        self.max_cache_size = int(os.getenv('GEMINI_CACHE_SIZE', '200'))
        self.response_cache = {}
        self.intent_cache = {}
        self.intent_cache_size = 300

        self.quick_replies = {
            'तुम कौन हो': 'मैं वाणी हूँ, आपकी आवाज सहायक। आप मुझसे मौसम, खबर, योजना और सामान्य जानकारी पूछ सकते हैं।',
            'who are you': 'मैं वाणी हूँ, आपकी voice assistant। आप मुझसे जानकारी वाले सवाल पूछ सकते हैं।',
            'क्या कर सकते हो': 'मैं मौसम, खबर, सरकारी योजनाएं, खेती और सामान्य सवालों में मदद कर सकती हूँ।',
            'what can you do': 'मैं weather, news, schemes, farming और general knowledge में मदद कर सकती हूँ।'
        }

        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            self.model = None
            print("Warning: GEMINI_API_KEY not found in .env file")
    
    def is_configured(self):
        """Check if Gemini API is properly configured"""
        return self.model is not None
    
    def ask_question(self, question):
        """
        Ask a general knowledge question to Gemini API
        Returns a child-friendly answer
        """
        if not self.is_configured():
            return None, "Gemini API is not configured. Please add GEMINI_API_KEY to your .env file."

        normalized_question = ' '.join(str(question or '').strip().lower().split())
        if not normalized_question:
            return None, "कृपया अपना सवाल दोबारा पूछें।"

        if normalized_question in self.quick_replies:
            return self.quick_replies[normalized_question], None

        if normalized_question in self.response_cache:
            return self.response_cache[normalized_question], None
        
        try:
            prompt = f"""
            आप एक तेज और स्पष्ट हिंदी सहायक हैं।
            सवाल: {question}
            निर्देश:
            - 3-6 छोटे वाक्य
            - आसान हिंदी
            - तथ्यात्मक और सीधे मुद्दे पर
            - अनावश्यक भूमिका या दोहराव नहीं
            जवाब:
            """

            def _generate():
                return self.model.generate_content(
                    prompt,
                    generation_config={
                        'temperature': 0.35,
                        'top_p': 0.9,
                        'max_output_tokens': 220
                    }
                )

            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(_generate)
                response = future.result(timeout=self.request_timeout)
            
            if response and response.text:
                clean_text = response.text.strip()
                clean_text = ' '.join(clean_text.split())
                clean_text = clean_text.replace('।', '। ')
                clean_text = clean_text.replace('!', '! ')
                clean_text = clean_text.replace('?', '? ')
                clean_text = ' '.join(clean_text.split())

                if len(self.response_cache) >= self.max_cache_size:
                    first_key = next(iter(self.response_cache))
                    del self.response_cache[first_key]
                self.response_cache[normalized_question] = clean_text

                return clean_text, None
            else:
                return None, "मुझे इस सवाल का जवाब नहीं मिल पाया।"

        except FuturesTimeoutError:
            return None, "जवाब आने में समय लग रहा है। कृपया छोटा सवाल पूछें या दोबारा कोशिश करें।"
                
        except Exception as e:
            error_msg = f"Error in Gemini API call: {str(e)}"
            print(error_msg)
            return None, "क्षमा करें, मुझे कुछ तकनीकी समस्या आ रही है। कृपया फिर से कोशिश करें।"

    def classify_intent_label(self, query):
        """
        Return one compact intent label for routing.
        Labels: weather, news, agri_scheme, agri_advice, social_scheme, finance_basic, general
        """
        if not self.is_configured():
            return None

        normalized_query = ' '.join(str(query or '').strip().lower().split())
        if not normalized_query:
            return None

        if normalized_query in self.intent_cache:
            return self.intent_cache[normalized_query]

        prompt = f"""
        Classify user intent and return only one label from this list:
        weather, news, agri_scheme, agri_advice, social_scheme, finance_basic, general

        User query: {query}

        Output format: label only
        """

        def _generate_label():
            return self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.0,
                    'top_p': 0.8,
                    'max_output_tokens': 8
                }
            )

        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(_generate_label)
                response = future.result(timeout=min(self.request_timeout, 2.5))

            if not response or not response.text:
                return None

            label = response.text.strip().lower().split()[0]
            allowed = {'weather', 'news', 'agri_scheme', 'agri_advice', 'social_scheme', 'finance_basic', 'general'}
            if label not in allowed:
                return None

            if len(self.intent_cache) >= self.intent_cache_size:
                first_key = next(iter(self.intent_cache))
                del self.intent_cache[first_key]
            self.intent_cache[normalized_query] = label
            return label

        except Exception:
            return None
    
    def is_general_knowledge_question(self, query):
        """
        Determine if the query is a general knowledge question
        Uses simple heuristics for now
        """
        # Common question words in Hindi
        question_words = [
            'क्या', 'क्यों', 'कैसे', 'कौन', 'कहाँ', 'कब', 'किसने', 'किसका',
            'कितना', 'कितने', 'किस', 'किससे', 'किसको', 'क्यूँ',
            'बताओ', 'बताइए', 'समझाओ', 'समझाइए', 'जानना चाहता', 'जानना चाहती',
            'what', 'why', 'how', 'who', 'where', 'when', 'which',
            'सवाल', 'question', 'answer', 'जवाब'
        ]
        
        query_lower = query.lower()
        
        # Check if query contains question words
        has_question_word = any(word in query_lower for word in question_words)
        
        # Check if it ends with question mark
        has_question_mark = '?' in query
        
        return has_question_word or has_question_mark


# Global instance
_gk_service = None

def get_gk_service():
    """Get or create the global GeneralKnowledgeService instance"""
    global _gk_service
    if _gk_service is None:
        _gk_service = GeneralKnowledgeService()
    return _gk_service


def handle_general_knowledge_query(query, voice_output_func, force=False):
    """
    Main function to handle general knowledge queries
    
    Args:
        query: The user's question
        voice_output_func: Function to speak the answer (e.g., bolo)
    
    Returns:
        bool: True if query was handled, False otherwise
    """
    service = get_gk_service()
    
    # Check if it's a general knowledge question unless forced fallback mode is used
    if not force and not service.is_general_knowledge_question(query):
        return False
    
    # Check if Gemini is configured
    if not service.is_configured():
        print("Gemini API not configured. Skipping general knowledge query.")
        return False
    
    print(f"Processing general knowledge question: {query}")
    
    # Get answer from Gemini
    answer, error = service.ask_question(query)
    
    if error:
        print(f"Error: {error}")
        voice_output_func(error)
        return True
    
    if answer:
        print(f"Answer: {answer}")
        voice_output_func(answer, lang='hi')
        return True
    
    return False


def get_fast_intent_label(query):
    """Get a fast intent label from Gemini for ambiguous queries only."""
    service = get_gk_service()
    return service.classify_intent_label(query)


def test_general_knowledge():
    """Test function to verify Gemini integration"""
    service = get_gk_service()
    
    if not service.is_configured():
        print("❌ Gemini API is not configured!")
        print("Please add GEMINI_API_KEY to your .env file")
        return False
    
    print("✅ Gemini API is configured!")
    
    # Test with some sample questions
    test_questions = [
        "आसमान नीला क्यों होता है?",
        "बारिश कैसे होती है?",
        "चाँद पर क्या होता है?"
    ]
    
    print("\nTesting with sample questions:\n")
    for question in test_questions:
        print(f"Q: {question}")
        answer, error = service.ask_question(question)
        if answer:
            print(f"A: {answer}\n")
        else:
            print(f"Error: {error}\n")
    
    return True


if __name__ == "__main__":
    # Run test when module is executed directly
    test_general_knowledge()
