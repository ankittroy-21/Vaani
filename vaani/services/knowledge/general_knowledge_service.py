"""
General Knowledge Service using Gemini API
Handles curious questions that children might ask their parents
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeneralKnowledgeService:
    def __init__(self):
        """Initialize the Gemini API with the API key"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # Use the latest stable Gemini model (verified working)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
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
        
        try:
            # Create a neutral, friendly prompt (suitable for adults and children)
            prompt = f"""
            आप एक दोस्ताना, समझाने योग्य और तथ्यात्मक सहायक की भूमिका निभाएँ। उपयोगकर्ता ने यह प्रश्न पूछा है:

            सवाल: {question}

            कृपया:
            1. सरल और स्पष्ट हिंदी में उत्तर दें (2-5 वाक्य)
            2. यदि उपयुक्त हो तो रोज़मर्रा के उदाहरण दें जिससे समझना आसान हो
            3. सकारात्मक और उत्साहवर्धक लहजे में, पर वयस्क-उपयुक्त भाषा में उत्तर दें
            4. संभव हो तो एक छोटा रोचक तथ्य जोड़ें

            जवाब (केवल हिंदी में):
            """
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                # Clean the response text
                clean_text = response.text.strip()
                # Remove excessive whitespace and newlines
                clean_text = ' '.join(clean_text.split())
                # Ensure proper spacing after punctuation
                clean_text = clean_text.replace('।', '। ')
                clean_text = clean_text.replace('!', '! ')
                clean_text = clean_text.replace('?', '? ')
                # Remove multiple spaces
                clean_text = ' '.join(clean_text.split())
                return clean_text, None
            else:
                return None, "मुझे इस सवाल का जवाब नहीं मिल पाया।"
                
        except Exception as e:
            error_msg = f"Error in Gemini API call: {str(e)}"
            print(error_msg)
            return None, "क्षमा करें, मुझे कुछ तकनीकी समस्या आ रही है। कृपया फिर से कोशिश करें।"
    
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
        has_question_mark = '?' in query or '।' in query
        
        return has_question_word or has_question_mark


# Global instance
_gk_service = None

def get_gk_service():
    """Get or create the global GeneralKnowledgeService instance"""
    global _gk_service
    if _gk_service is None:
        _gk_service = GeneralKnowledgeService()
    return _gk_service


def handle_general_knowledge_query(query, voice_output_func):
    """
    Main function to handle general knowledge queries
    
    Args:
        query: The user's question
        voice_output_func: Function to speak the answer (e.g., bolo)
    
    Returns:
        bool: True if query was handled, False otherwise
    """
    service = get_gk_service()
    
    # Check if it's a general knowledge question
    if not service.is_general_knowledge_question(query):
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
