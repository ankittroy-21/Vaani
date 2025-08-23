import json
import os
import random
from Voice_tool import bolo
import time

SCHEME_DATA = {}

def load_scheme_data():
    """Loads social scheme data from JSON file."""
    global SCHEME_DATA
    if SCHEME_DATA:
        return SCHEME_DATA
    
    try:
        file_path = os.path.join('scheme_data', 'social_schemes.json')
        if not os.path.exists(file_path):
            print(f"Error: Social scheme data file not found at {file_path}")
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            SCHEME_DATA = data
            return data
    except Exception as e:
        print(f"Error loading social scheme data: {e}")
        return None

def ask_eligibility_questions():
    """Asks simple questions to determine eligibility."""
    questions = [
        {"question": "क्या आप महिला हैं?", "key": "महिला"},
        {"question": "क्या आप विधवा हैं?", "key": "विधवा"},
        {"question": "क्या आपकी उम्र 60 साल से ज्यादा है?", "key": "60 वर्ष से अधिक आयु"},
        {"question": "क्या आप गाँव में रहते हैं?", "key": "ग्रामीण क्षेत्र के निवासी"},
        {"question": "क्या आपकी आय बहुत कम है?", "key": "गरीबी रेखा से नीचे"},
        {"question": "क्या आप किसान हैं?", "key": "किसान"},
        {"question": "क्या आप विकलांग हैं?", "key": "40% या अधिक विकलांगता"}
    ]
    
    user_profile = []
    
    for q in questions:
        bolo(q["question"])
        # In a real implementation, you would listen for yes/no response
        # For now, we'll simulate with a pause
        time.sleep(2)
        # Assume yes for demonstration
        user_profile.append(q["key"])
    
    return user_profile

def find_eligible_schemes(user_profile):
    """Finds schemes that match the user's profile."""
    scheme_data = load_scheme_data()
    if not scheme_data:
        return []
    
    eligible_schemes = []
    
    for scheme in scheme_data.get("schemes", []):
        eligibility_criteria = scheme.get("eligibility", [])
        matches = sum(1 for criterion in eligibility_criteria if criterion in user_profile)
        
        # If at least one criterion matches, consider eligible
        if matches > 0:
            eligible_schemes.append(scheme)
    
    return eligible_schemes

def explain_scheme(scheme, bolo_func):
    """Explains a scheme in simple terms."""
    bolo_func(f"{scheme['name']} के बारे में जानकारी:")
    time.sleep(0.5)
    
    bolo_func(f"इस योजना के लाभ: {scheme['benefits']}")
    time.sleep(0.5)
    
    bolo_func("आवेदन कैसे करें:")
    time.sleep(0.3)
    bolo_func(scheme['application_process'])
    
    time.sleep(0.5)
    bolo_func("जरूरी दस्तावेज:")
    for doc in scheme.get('documents', []):
        bolo_func(f"• {doc}")
        time.sleep(0.3)

def handle_scheme_selection(command, bolo_func, context):
    """Handles user's selection of a scheme from the list."""
    schemes = context.data.get('schemes', [])
    hindi_numbers = {"एक": 1, "पहला": 1, "1": 1, "दो": 2, "दूसरा": 2, "2": 2, 
                    "तीन": 3, "तीसरा": 3, "3": 3, "चार": 4, "चौथा": 4, "4": 4, 
                    "पांच": 5, "पांचवा": 5, "5": 5}
    
    selected_number = None
    for word, number in hindi_numbers.items():
        if word in command:
            selected_number = number
            break
    
    if selected_number and 1 <= selected_number <= len(schemes):
        explain_scheme(schemes[selected_number - 1], bolo_func)
        context.clear()
    elif any(phrase in command for phrase in ["बंद", "रुको", "नहीं", "बस"]):
        bolo_func("ठीक है, योजना चयन सत्र समाप्त हुआ।")
        context.clear()
    else:
        bolo_func("माफ कीजिए, मैं समझी नहीं। कृपया 1 से 5 के बीच का नंबर बताएं या 'बंद करो' कहें。")

def handle_social_schemes_query(command, bolo_func, context):
    """Handles queries about social schemes and eligibility."""
    social_scheme_keywords = ["योजना", "सहायता", "पेंशन", "मनरेगा", "वृद्धावस्था", "विधवा", "दिव्यांग", "किसान सम्मान"]
    
    if any(keyword in command for keyword in social_scheme_keywords):
        bolo_func("मैं आपके लिए उपलब्ध सरकारी योजनाओं की जानकारी दे सकती हूँ।")
        time.sleep(0.5)
        bolo_func("कृपया कुछ सवालों के जवाब दें ताकि मैं आपके लिए सही योजनाएं ढूंढ सकूँ।")
        
        user_profile = ask_eligibility_questions()
        eligible_schemes = find_eligible_schemes(user_profile)
        
        if eligible_schemes:
            bolo_func(f"मैंने आपके लिए {len(eligible_schemes)} योजनाएं ढूंढी हैं।")
            for i, scheme in enumerate(eligible_schemes):
                bolo_func(f"{i+1}. {scheme['name']}")
                time.sleep(0.5)
            
            bolo_func("क्या आप किसी विशेष योजना के बारे में और जानना चाहेंगे?")
            # Set context for follow-up
            context.set(
                topic='social_schemes',
                state='awaiting_scheme_selection',
                data={'schemes': eligible_schemes}
            )
        else:
            bolo_func("माफ कीजिए, मुझे आपके लिए कोई उपयुक्त योजना नहीं मिली।")
        
        return True
    
    return False