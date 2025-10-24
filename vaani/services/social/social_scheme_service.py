import json
import os
import random
import time
from vaani.core.voice_tool import bolo, listen_command

class SocialSchemeService:
    """
    An enhanced, stateful service to handle social scheme queries intelligently.
    """
    def __init__(self):
        self.schemes = self._load_scheme_data()
        self.user_profile = {}
        self.potential_schemes = []

    def _load_scheme_data(self):
        """Loads social scheme data from the new JSON file using a robust, absolute path."""
        try:
            # --- START OF FIX ---
            # Get the absolute path of the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Build the full path to the JSON file
            file_path = os.path.join(script_dir, 'scheme_data', 'social_schemes_data.json')
            # --- END OF FIX ---

            if not os.path.exists(file_path):
                print(f"CRITICAL ERROR: Social scheme data file not found at the expected path: {file_path}")
                print("Please ensure you have a 'scheme_data' folder in the same directory as this script, and it contains 'social_schemes_data.json'.")
                return []
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f).get("schemes", [])
        except Exception as e:
            print(f"Error loading social scheme data: {e}")
            return []

    def _find_scheme_by_name(self, command):
        """Finds a specific scheme mentioned in the command using its name or aliases."""
        for scheme in self.schemes:
            if scheme['name'] in command:
                return scheme
            for alias in scheme.get('aliases', []):
                if alias in command:
                    return scheme
        return None

    def explain_scheme(self, scheme, bolo_func):
        """Explains a single scheme's details in a clear, structured manner."""
        bolo_func(f"{scheme['name']} के बारे में जानकारी इस प्रकार है:")
        time.sleep(0.5)
        
        bolo_func(f"यह योजना {scheme.get('summary', 'का विवरण उपलब्ध नहीं है।')}")
        time.sleep(0.5)

        bolo_func(f"इसके लाभ हैं: {scheme.get('benefits', 'लाभों की जानकारी उपलब्ध नहीं है।')}")
        time.sleep(0.5)
        
        bolo_func("आवेदन करने की प्रक्रिया: " + scheme.get('application_process', 'आवेदन प्रक्रिया की जानकारी उपलब्ध नहीं है।'))
        time.sleep(0.5)

        docs = scheme.get('documents', [])
        if docs:
            bolo_func("इसके लिए इन दस्तावेज़ों की ज़रूरत पड़ती है:")
            for doc in docs:
                bolo_func(f"• {doc}")
                time.sleep(0.3)
        
        bolo_func("अधिक जानकारी के लिए आप संबंधित विभाग से संपर्क कर सकते हैं।")

    def handle_query(self, command, bolo_func, context):
        """Main handler for all social scheme related queries."""
        direct_scheme = self._find_scheme_by_name(command)
        if direct_scheme:
            bolo_func(f"ज़रूर, मैं आपको {direct_scheme['name']} के बारे में बताती हूँ।")
            self.explain_scheme(direct_scheme, bolo_func)
            context.clear()
            return

        # For now, we'll list all available social schemes if not a direct query
        bolo_func("मेरे पास इन सरकारी योजनाओं की जानकारी है:")
        if not self.schemes:
            bolo_func("माफ़ कीजिए, अभी कोई भी सामाजिक योजना की जानकारी उपलब्ध नहीं है।")
            return

        for i, scheme in enumerate(self.schemes, 1):
            bolo_func(f"{i}. {scheme['name']}")
            time.sleep(0.5)
        
        bolo_func("आप किस योजना के बारे में विस्तार से जानना चाहेंगे? कृपया उसका नाम या नंबर बताएं।")
        context.set(
            topic='social_schemes',
            state='awaiting_scheme_selection',
            data={'schemes': self.schemes}
        )

# --- Standalone Functions to be called from main.py ---

def handle_social_schemes_query(command, bolo_func, context):
    """Entry point for handling social scheme queries."""
    service = SocialSchemeService()
    service.handle_query(command, bolo_func, context)

def handle_scheme_selection(command, bolo_func, context):
    """Handles user's selection of a scheme from the list."""
    schemes_data = context.data.get('schemes', [])
    selected_scheme = None

    # Try matching by name first
    for scheme in schemes_data:
        if scheme['name'] in command or any(alias in command for alias in scheme.get('aliases', [])):
            selected_scheme = scheme
            break
    
    # If not found by name, try by number
    if not selected_scheme:
        hindi_numbers = {"एक": 1, "पहला": 1, "1": 1, "दो": 2, "दूसरा": 2, "2": 2, 
                         "तीन": 3, "तीसरा": 3, "3": 3}
        selected_number = None
        for word, number in hindi_numbers.items():
            if word in command:
                selected_number = number
                break
        
        if selected_number and 1 <= selected_number <= len(schemes_data):
            selected_scheme = schemes_data[selected_number - 1]

    if selected_scheme:
        service = SocialSchemeService()
        service.explain_scheme(selected_scheme, bolo_func)
        context.clear()
    elif any(phrase in command for phrase in ["बंद", "रुको", "नहीं", "बस"]):
        bolo_func("ठीक है, योजना सत्र समाप्त हुआ।")
        context.clear()
    else:
        bolo_func("माफ कीजिए, मैं समझी नहीं। कृपया सूची से एक योजना का नाम या नंबर बताएं, या 'बंद करो' कहें।")
