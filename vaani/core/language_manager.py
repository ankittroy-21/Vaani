"""
Multi-Language Support Manager for Vaani
Supports Hindi, English, Bhojpuri, Marathi, Tamil, Telugu, Gujarati, Bengali
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()

class LanguageManager:
    def __init__(self):
        """Initialize language manager with supported languages"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None
            print("Warning: GEMINI_API_KEY not found")
        
        # Supported languages with their codes and names
        self.languages = {
            'hi': {'name': 'हिंदी', 'name_en': 'Hindi', 'tts_code': 'hi', 'stt_code': 'hi-IN'},
            'en': {'name': 'English', 'name_en': 'English', 'tts_code': 'en', 'stt_code': 'en-IN'},
            'bho': {'name': 'भोजपुरी', 'name_en': 'Bhojpuri', 'tts_code': 'hi', 'stt_code': 'hi-IN'},  # Use Hindi
            'mr': {'name': 'मराठी', 'name_en': 'Marathi', 'tts_code': 'mr', 'stt_code': 'mr-IN'},
            'ta': {'name': 'தமிழ்', 'name_en': 'Tamil', 'tts_code': 'ta', 'stt_code': 'ta-IN'},
            'te': {'name': 'తెలుగు', 'name_en': 'Telugu', 'tts_code': 'te', 'stt_code': 'te-IN'},
            'gu': {'name': 'ગુજરાતી', 'name_en': 'Gujarati', 'tts_code': 'gu', 'stt_code': 'gu-IN'},
            'bn': {'name': 'বাংলা', 'name_en': 'Bengali', 'tts_code': 'bn', 'stt_code': 'bn-IN'},
            'pa': {'name': 'ਪੰਜਾਬੀ', 'name_en': 'Punjabi', 'tts_code': 'pa', 'stt_code': 'pa-IN'},
            'kn': {'name': 'ಕನ್ನಡ', 'name_en': 'Kannada', 'tts_code': 'kn', 'stt_code': 'kn-IN'},
        }
        
        # Default language
        self.current_language = 'hi'
        
        # Common phrases in all languages
        self.phrases = self._load_common_phrases()
    
    def _load_common_phrases(self):
        """Load common phrases for all languages"""
        return {
            'greeting': {
                'hi': ['नमस्ते', 'सुप्रभात', 'शुभ दिन'],
                'en': ['Hello', 'Good morning', 'Good day'],
                'bho': ['प्रणाम', 'राम राम', 'सुप्रभात'],
                'mr': ['नमस्कार', 'सुप्रभात', 'शुभ दिवस'],
                'ta': ['வணக்கம்', 'காலை வணக்கம்', 'நல்ல நாள்'],
                'te': ['నమస్కారం', 'శుభోదయం', 'శుభ దినం'],
                'gu': ['નમસ્તે', 'સુપ્રભાત', 'શુભ દિવસ'],
                'bn': ['নমস্কার', 'সুপ্রভাত', 'শুভ দিন'],
                'pa': ['ਸਤ ਸ੍ਰੀ ਅਕਾਲ', 'ਸ਼ੁਭ ਸਵੇਰ', 'ਸ਼ੁਭ ਦਿਨ'],
                'kn': ['ನಮಸ್ಕಾರ', 'ಶುಭೋದಯ', 'ಶುಭ ದಿನ'],
            },
            'goodbye': {
                'hi': ['धन्यवाद', 'अलविदा', 'फिर मिलेंगे'],
                'en': ['Thank you', 'Goodbye', 'See you'],
                'bho': ['धन्यवाद', 'अलविदा', 'फेर मिलब'],
                'mr': ['धन्यवाद', 'निरोप', 'पुन्हा भेटू'],
                'ta': ['நன்றி', 'விடைபெறுகிறேன்', 'மீண்டும் சந்திப்போம்'],
                'te': ['ధన్యవాదాలు', 'వీడ్కోలు', 'మళ్లీ కలుద్దాం'],
                'gu': ['આભાર', 'વિદાય', 'ફરી મળીશું'],
                'bn': ['ধন্যবাদ', 'বিদায়', 'আবার দেখা হবে'],
                'pa': ['ਧੰਨਵਾਦ', 'ਅਲਵਿਦਾ', 'ਫਿਰ ਮਿਲਾਂਗੇ'],
                'kn': ['ಧನ್ಯವಾದ', 'ವಿದಾಯ', 'ಮತ್ತೆ ಭೇಟಿಯಾಗೋಣ'],
            },
            'error': {
                'hi': 'मैं यह समझ नहीं पाई, कृपया फिर से कहें।',
                'en': 'I could not understand, please say again.',
                'bho': 'हम ना समझ पाईं, फेर से कहीं।',
                'mr': 'मला समजले नाही, कृपया पुन्हा सांगा।',
                'ta': 'எனக்கு புரியவில்லை, மீண்டும் சொல்லுங்கள்.',
                'te': 'నాకు అర్థం కాలేదు, దయచేసి మళ్లీ చెప్పండి.',
                'gu': 'મને સમજાયું નહીં, કૃપા કરીને ફરીથી કહો.',
                'bn': 'আমি বুঝতে পারিনি, অনুগ্রহ করে আবার বলুন।',
                'pa': 'ਮੈਨੂੰ ਸਮਝ ਨਹੀਂ ਆਇਆ, ਕਿਰਪਾ ਕਰਕੇ ਦੁਬਾਰਾ ਕਹੋ।',
                'kn': 'ನನಗೆ ಅರ್ಥವಾಗಲಿಲ್ಲ, ದಯವಿಟ್ಟು ಮತ್ತೆ ಹೇಳಿ.',
            },
            'listening': {
                'hi': 'कृपया बोलिए :',
                'en': 'Please speak:',
                'bho': 'कृपया बोलीं:',
                'mr': 'कृपया बोला:',
                'ta': 'தயவுசெய்து பேசுங்கள்:',
                'te': 'దయచేసి మాట్లాడండి:',
                'gu': 'કૃપા કરીને બોલો:',
                'bn': 'অনুগ্রহ করে বলুন:',
                'pa': 'ਕਿਰਪਾ ਕਰਕੇ ਬੋਲੋ:',
                'kn': 'ದಯವಿಟ್ಟು ಮಾತನಾಡಿ:',
            },
            'you_said': {
                'hi': 'आपने कहा:',
                'en': 'You said:',
                'bho': 'रउआ कहलीं:',
                'mr': 'तुम्ही म्हणालात:',
                'ta': 'நீங்கள் சொன்னீர்கள்:',
                'te': 'మీరు చెప్పారు:',
                'gu': 'તમે કહ્યું:',
                'bn': 'আপনি বলেছেন:',
                'pa': 'ਤੁਸੀਂ ਕਿਹਾ:',
                'kn': 'ನೀವು ಹೇಳಿದ್ದು:',
            }
        }
    
    def get_language_name(self, lang_code=None):
        """Get language name in native script"""
        code = lang_code or self.current_language
        return self.languages.get(code, {}).get('name', 'Unknown')
    
    def get_tts_code(self, lang_code=None):
        """Get TTS language code"""
        code = lang_code or self.current_language
        return self.languages.get(code, {}).get('tts_code', 'hi')
    
    def get_stt_code(self, lang_code=None):
        """Get Speech-to-Text language code for Google Speech Recognition"""
        code = lang_code or self.current_language
        return self.languages.get(code, {}).get('stt_code', 'hi-IN')
    
    def set_language(self, lang_code):
        """Set current language"""
        if lang_code in self.languages:
            self.current_language = lang_code
            return True
        return False
    
    def get_phrase(self, phrase_key, lang_code=None):
        """Get a common phrase in specified language"""
        code = lang_code or self.current_language
        return self.phrases.get(phrase_key, {}).get(code, self.phrases[phrase_key]['hi'])
    
    def detect_language(self, text):
        """
        Detect language from text using simple heuristics
        Returns language code
        """
        text_lower = text.lower()
        
        # Check for language switching commands
        language_keywords = {
            'hi': ['हिंदी', 'hindi', 'हिन्दी में'],
            'en': ['english', 'अंग्रेजी', 'in english'],
            'bho': ['bhojpuri', 'भोजपुरी', 'bhojpuri me'],
            'mr': ['marathi', 'मराठी', 'marathi madhe'],
            'ta': ['tamil', 'தமிழ்', 'tamil la'],
            'te': ['telugu', 'తెలుగు', 'telugu lo'],
            'gu': ['gujarati', 'ગુજરાતી', 'gujarati ma'],
            'bn': ['bangla', 'bengali', 'বাংলা', 'bangla te'],
            'pa': ['punjabi', 'ਪੰਜਾਬੀ', 'punjabi vich'],
            'kn': ['kannada', 'ಕನ್ನಡ', 'kannada dalli'],
        }
        
        for lang_code, keywords in language_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return lang_code
        
        # Default to current language
        return self.current_language
    
    def translate_text(self, text, target_lang=None, source_lang=None):
        """
        Translate text to target language using Gemini
        """
        if not self.model:
            return text, "Translation not available - Gemini API not configured"
        
        target = target_lang or self.current_language
        source = source_lang or 'hi'
        
        # If same language, no translation needed
        if source == target:
            return text, None
        
        target_name = self.languages[target]['name']
        
        try:
            prompt = f"""
            Translate the following text to {target_name} ({target}).
            Keep the meaning exact and natural.
            Only provide the translation, nothing else.
            
            Text: {text}
            
            Translation:
            """
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                translated = response.text.strip()
                # Remove any quotation marks
                translated = translated.strip('"\'')
                return translated, None
            else:
                return text, "Translation failed"
                
        except Exception as e:
            error_msg = f"Translation error: {str(e)}"
            print(error_msg)
            return text, error_msg
    
    def get_multilingual_response(self, query, response_text, user_lang=None):
        """
        Convert response to user's preferred language if different from default
        """
        user_language = user_lang or self.current_language
        
        # If response is already in user's language, return as is
        if user_language == 'hi':  # Assuming most responses are in Hindi
            return response_text
        
        # Translate to user's language
        translated, error = self.translate_text(response_text, target_lang=user_language)
        
        if error:
            print(f"Translation warning: {error}")
            return response_text  # Return original if translation fails
        
        return translated
    
    def list_supported_languages(self):
        """Return list of supported languages"""
        lang_list = []
        for code, info in self.languages.items():
            lang_list.append(f"{info['name']} ({info['name_en']})")
        return lang_list
    
    def get_language_info(self):
        """Get formatted string of supported languages"""
        langs = self.list_supported_languages()
        return "Supported languages: " + ", ".join(langs)


# Global instance
_language_manager = None

def get_language_manager():
    """Get or create the global LanguageManager instance"""
    global _language_manager
    if _language_manager is None:
        _language_manager = LanguageManager()
    return _language_manager


def handle_language_command(command):
    """
    Check if command is a language switching request
    Returns (is_language_command, new_language_code)
    """
    manager = get_language_manager()
    detected_lang = manager.detect_language(command)
    
    # Check if it's explicitly a language change command
    language_switch_phrases = [
        'भाषा बदलो', 'change language', 'language change',
        'में बोलो', 'me bolo', 'में बात करो', 'la pesungal',
        'lo matladandi', 'ma bolav', 'te bolo', 'dalli matladi'
    ]
    
    is_switch_command = any(phrase in command.lower() for phrase in language_switch_phrases)
    
    if is_switch_command and detected_lang != manager.current_language:
        return True, detected_lang
    
    return False, manager.current_language


# Test function
if __name__ == "__main__":
    manager = LanguageManager()
    
    print("=" * 60)
    print("Testing Language Manager")
    print("=" * 60)
    
    print(f"\n✅ Current language: {manager.get_language_name()}")
    print(f"✅ Supported languages: {len(manager.languages)}")
    print("\n" + manager.get_language_info())
    
    # Test phrases
    print("\n" + "=" * 60)
    print("Testing Common Phrases:")
    print("=" * 60)
    
    for lang_code in ['hi', 'en', 'mr', 'ta', 'gu']:
        print(f"\n{manager.get_language_name(lang_code)}:")
        print(f"  Greeting: {manager.get_phrase('greeting', lang_code)[0]}")
        print(f"  Error: {manager.get_phrase('error', lang_code)}")
    
    # Test translation
    if manager.model:
        print("\n" + "=" * 60)
        print("Testing Translation:")
        print("=" * 60)
        
        test_text = "आज मौसम बहुत अच्छा है"
        print(f"\nOriginal (Hindi): {test_text}")
        
        for lang in ['en', 'mr', 'ta']:
            translated, error = manager.translate_text(test_text, target_lang=lang)
            if not error:
                print(f"{manager.get_language_name(lang)}: {translated}")
    else:
        print("\n⚠️ Translation test skipped - Gemini API not configured")
    
    print("\n" + "=" * 60)
    print("✅ Language Manager Test Complete!")
    print("=" * 60)
