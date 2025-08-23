<<<<<<< HEAD
# agri_scheme_service.py (Enhanced Version 4)
=======
# agri_scheme_service.py
>>>>>>> 99af8066a8e7c79aaa8fa10d146813ab0e88bc02

import json
import os
import re
import Config
from Voice_tool import bolo
import time
import random

# --- Data Mappings and Fallbacks ---

<<<<<<< HEAD
=======
# --- File Mappings (No Change) ---
>>>>>>> 99af8066a8e7c79aaa8fa10d146813ab0e88bc02
CROP_SUBSIDY_MAP = {
    "गेहूं": "gehu_subsidies.json",
    "धान": "dhan_subsidies.json",
    "गन्ना": "ganna_subsidies.json",
    "सब्जियां": "sabjiyan_subsidies.json",
    "दालें": "dalen_subsidies.json",
    "मक्का": "makka_subsidies.json",
    "सोयाबीन": "soyabean_subsidies.json",
    "कपास": "cotton_subsidies.json",
    "तिलहन": "tilhan_subsidies.json"
}

GENERAL_SCHEME_MAP = {
    "किसान सम्मान निधि": "pm_kisan.json",
    "मुद्रा योजना": "pm_mudra_yojana.json",
    "कुसुम योजना": "pm_kusum.json",
    "आयुष्मान भारत": "ayushman_bharat.json",
    "फसल बीमा": "pm_fasal_bima_yojana.json",
    "कृषि सिंचाई": "pm_krishi_sinchai_yojana.json",
    "टिकाऊ कृषि": "sustainable_agriculture_mission.json",
    "कृषि यंत्रीकरण": "agricultural_mechanization_scheme.json",
<<<<<<< HEAD
    "कृषि बीमा": "national_agriculture_insurance.json",
    "प्रधानमंत्री किसान मान धन योजना": "pm_kisan_man_dhan.json",
    "राष्ट्रीय कृषि बाजार": "e_nam.json",
    "किसान क्रेडिट कार्ड": "kisan_credit_card.json"
}

SCHEME_FALLBACK_DATA = {
    "कृषि यंत्रीकरण": {
        'yojana_ka_naam': "मुख्यमंत्री कृषि यंत्रीकरण योजना",
        'yojana_ke_baare_mein': "यह योजना गुजरात के किसानों के लिए है। इसका मकसद खेती के लिए नए औजार और मशीनें खरीदने में किसानों की पैसे से मदद करना है।",
        'kya_laabh_milega': "इस योजना में, सरकार खेती के अलग-अलग औजार और मशीनें खरीदने के लिए ₹1,200 से लेकर ₹11,00,000 तक की आर्थिक सहायता देती है।",
        'पात्रता': [
            "जो गुजरात राज्य में रहता हो।", "जो एक किसान हो।",
            "किसान के पास कम से कम 1 एकड़ खेती की ज़मीन होनी चाहिए।",
            "किसान का अपना बैंक खाता और आधार कार्ड होना ज़रूरी है।"
        ],
        'aavedan_prakriya': "आप गुजरात सरकार के 'i-Khedut' पोर्टल पर जाकर ऑनलाइन अर्ज़ी दे सकते हैं।",
        'sampark_jankari': "अधिक जानकारी के लिए अपने नजदीकी कृषि कार्यालय में संपर्क करें।"
    }
}

# --- Utility Functions ---

def clean_text(text):
    """Utility to clean text by normalizing whitespace."""
    if isinstance(text, str):
        return ' '.join(text.split())
    return text

def load_json_data(folder, filename):
    """Generic function to load a JSON file from a specified folder."""
=======
}

# --- Helper Functions (No Change) ---
def load_json_data(folder, filename):
>>>>>>> 99af8066a8e7c79aaa8fa10d146813ab0e88bc02
    try:
        file_path = os.path.join(folder, filename)
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return None
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON from {folder}/{filename}: {e}")
        return None

# --- Core Logic Functions ---

def speak_scheme_details(scheme_data, bolo_func):
<<<<<<< HEAD
    """Validates, cleans, and speaks the details of a scheme in a structured way."""
=======
>>>>>>> 99af8066a8e7c79aaa8fa10d146813ab0e88bc02
    if not scheme_data:
        bolo_func("माफ़ कीजिए, योजना की जानकारी प्राप्त करने में समस्या हुई।")
        return
<<<<<<< HEAD

    # Clean all text fields before speaking
    for key, value in scheme_data.items():
        if isinstance(value, str):
            scheme_data[key] = clean_text(value)
        elif isinstance(value, list):
            scheme_data[key] = [clean_text(str(item)) for item in value]
        elif isinstance(value, dict):
            for sub_key, sub_value in value.items():
                value[sub_key] = clean_text(sub_value) if isinstance(sub_value, str) else sub_value

    name = scheme_data.get('yojana_ka_naam', 'इस योजना का नाम उपलब्ध नहीं है।')
    description = scheme_data.get('yojana_ke_baare_mein', 'विवरण उपलब्ध नहीं है।')

    bolo_func(name)
    time.sleep(0.3)
    bolo_func(f"इसके बारे में जानकारी यह है: {description}")

    eligibility = scheme_data.get('पात्रता', []) or scheme_data.get('kaun_laabh_le_sakta_hai', [])
    if eligibility:
        bolo_func("इस योजना के लिए पात्रता मानदंड:")
        for criterion in eligibility:
            bolo_func(f"• {criterion}")
            time.sleep(0.3)

=======
    bolo_func(f"{scheme_data.get('yojana_ka_naam', 'इस योजना का नाम उपलब्ध नहीं है।')}")
    bolo_func(f"इसके बारे में जानकारी यह है: {scheme_data.get('yojana_ke_baare_mein', 'विवरण उपलब्ध नहीं है।')}")
>>>>>>> 99af8066a8e7c79aaa8fa10d146813ab0e88bc02
    benefits = scheme_data.get('kya_laabh_milega', [])
    if isinstance(benefits, list):
        bolo_func("इस योजना के तहत आपको यह लाभ मिलेंगे:")
        benefits_list = [benefits] if isinstance(benefits, str) else benefits
        for benefit in benefits_list:
            bolo_func(f"• {benefit}")
            time.sleep(0.3)

<<<<<<< HEAD
    application_process = scheme_data.get('aavedan_prakriya', "") or scheme_data.get('apply_kaise_karein', "")
    if isinstance(application_process, dict):
        if 'jagah' in application_process:
            bolo_func(f"आवेदन कहाँ करें: {application_process['jagah']}")
        if 'prakriya' in application_process and isinstance(application_process['prakriya'], list):
            bolo_func("आवेदन प्रक्रिया:")
            for i, step in enumerate(application_process['prakriya'], 1):
                bolo_func(f"{i}. {step}")
                time.sleep(0.3)
    elif application_process:
        bolo_func(f"आवेदन प्रक्रिया: {application_process}")

    contact_info = scheme_data.get('sampark_jankari', "")
    if contact_info:
        bolo_func(f"संपर्क जानकारी: {contact_info}")


def get_subsidy_info(crop_type, bolo_func, context):
    """Provides subsidy information for a specific crop and sets context for follow-ups."""
=======
def get_subsidy_info(crop_type, bolo_func):
>>>>>>> 99af8066a8e7c79aaa8fa10d146813ab0e88bc02
    filename = CROP_SUBSIDY_MAP.get(crop_type)
    if not filename:
        bolo_func(f"{crop_type} के लिए कोई विशेष सब्सिडी योजना नहीं मिली।")
        return
    subsidy_data = load_json_data('subsidy_data', filename)
    if subsidy_data and isinstance(subsidy_data, list):
        scheme_names = [s.get('yojana_naam', 'अज्ञात योजना') for s in subsidy_data]
        response = f"{crop_type} की खेती के लिए ये योजनाएं उपलब्ध हैं: {', '.join(scheme_names)}।"
        bolo_func(response)
        
        # Set context to handle user's next response as a scheme selection
        bolo_func("क्या आप इनमें से किसी विशेष योजना के बारे में जानना चाहते हैं?")
        context.set(
            topic='agriculture',
            state='awaiting_agri_response',
            data={'query_type': 'scheme_selection', 'schemes': subsidy_data}
        )
    elif subsidy_data:
        # If data is not a list of schemes, speak the details directly
        speak_scheme_details(subsidy_data, bolo_func)
    else:
        bolo_func(f"{crop_type} के लिए सब्सिडी डेटा लोड करने में समस्या हुई।")

<<<<<<< HEAD

def get_loan_info(bolo_func):
    """Provides general information about agricultural loans."""
    loan_data = load_json_data('loan_data', 'loans.json')
    if loan_data:
        bolo_func("कृषि ऋण के बारे में कुछ जानकारी यहाँ दी गई है:")
        speak_scheme_details(loan_data, bolo_func)
        bolo_func("अधिक जानकारी और आवेदन के लिए, आप अपने नजदीकी बैंक शाखा में संपर्क कर सकते हैं।")
    else:
        bolo_func("माफ़ कीजिए, लोन की जानकारी अभी उपलब्ध नहीं है।")
=======
# --- NEW: Loan & Subsidy Guide Functions ---

def speak_loan_application_guidance(scheme_data, bolo_func):
    """
    Provides step-by-step guidance on how to apply and what documents are needed.
    This directly implements the "Step-by-Step Application Help" feature of your concept.
    """
    apply_info = scheme_data.get('apply_kaise_karein', {})
    if not apply_info:
        bolo_func("आवेदन प्रक्रिया के बारे में जानकारी इस योजना के लिए उपलब्ध नहीं है।")
        return

    bolo_func("अब मैं आपको आवेदन करने की प्रक्रिया बताती हूँ।")
    
    # Where to apply
    jagah = apply_info.get('jagah')
    if jagah:
        bolo_func(f"आवेदन करने के लिए, आपको यहाँ जाना होगा: {jagah}")
        time.sleep(0.5)

    # Application process steps
    prakriya = apply_info.get('prakriya')
    if prakriya:
        bolo_func("आवेदन करने के यह कदम हैं:")
        for i, step in enumerate(prakriya):
            bolo_func(f"कदम {i+1}: {step}")
            time.sleep(0.5)

    # Required documents
    documents = scheme_data.get('zaroori_kaagjaat') or apply_info.get('zaroori_kaagjaat')
    if documents:
        # Handling nested document lists in pm_mudra_yojana.json
        if isinstance(documents, dict):
            for loan_type, doc_list in documents.items():
                type_name = loan_type.replace('_', ' ').replace('ke liye', ' के लिए')
                bolo_func(f"{type_name} यह जरूरी कागजात लगेंगे:")
                for doc in doc_list:
                    bolo_func(doc)
                    time.sleep(0.5)
        else: # Handling flat document lists
            bolo_func("इसके लिए यह जरूरी कागजात लगेंगे:")
            for doc in documents:
                bolo_func(doc)
                time.sleep(0.5)

def handle_loan_query(command, bolo_func):
    """
    Acts as the "Loan & Subsidy Guide". It identifies relevant loan schemes
    and interactively provides details on benefits, subsidies, and application process.
    """
    bolo_func(" ज़रूर, मैं कर्ज़ और सरकारी सहायता योजनाओं के बारे में जानकारी देने में आपकी मदद कर सकती हूँ।")
    
    # Check for specific loan schemes mentioned in the command
    if "मुद्रा" in command:
        scheme_name = "मुद्रा योजना"
        filename = GENERAL_SCHEME_MAP.get(scheme_name)
        scheme_data = load_json_data('scheme_data', filename)
        if scheme_data:
            bolo_func(f"ठीक है, मैं आपको {scheme_name} के बारे में बताती हूँ।")
            speak_scheme_details(scheme_data, bolo_func)
            loan_types = scheme_data.get('loan_ke_prakaar', [])
            if loan_types:
                bolo_func("इस योजना में तीन तरह के लोन मिलते हैं:")
                for loan_type in loan_types:
                    bolo_func(f"{loan_type['naam']}: {loan_type['rashi']}") #
                    time.sleep(0.5)
            speak_loan_application_guidance(scheme_data, bolo_func)
        else:
            bolo_func(f"माफ़ कीजिए, {scheme_name} के बारे में जानकारी नहीं मिली।")
        return

    if "कुसुम" in command or "सोलर" in command:
        scheme_name = "कुसुम योजना"
        filename = GENERAL_SCHEME_MAP.get(scheme_name)
        scheme_data = load_json_data('scheme_data', filename)
        if scheme_data:
            bolo_func(f"ठीक है, मैं आपको {scheme_name} के बारे में बताती हूँ।")
            speak_scheme_details(scheme_data, bolo_func)
            # This directly implements the "Subsidy Information" part of your concept
            bolo_func("इस योजना में सब्सिडी और लोन दोनों की सुविधा है।")
            bolo_func("सरकार सोलर पंप लगाने के लिए कुल खर्चे का 60% पैसा सब्सिडी के रूप में देगी।") #
            bolo_func("आपको बैंक से 30% तक का लोन भी मिल सकता है।") #
            bolo_func("आपको अपनी जेब से सिर्फ 10% पैसा ही लगाना होगा।") #
            speak_loan_application_guidance(scheme_data, bolo_func)
        else:
            bolo_func(f"माफ़ कीजिए, {scheme_name} के बारे में जानकारी नहीं मिली।")
        return

    # If no specific scheme is mentioned, present the available options
    bolo_func("मेरे पास छोटे कारोबार के लिए 'प्रधानमंत्री मुद्रा योजना' और सोलर पंप लगवाने के लिए 'प्रधानमंत्री कुसुम योजना' की जानकारी है। आप किसके बारे में जानना चाहेंगे?")


>>>>>>> 99af8066a8e7c79aaa8fa10d146813ab0e88bc02


def get_all_schemes_info(bolo_func, context):
    """Provides a list of all major government schemes and sets context."""
    bolo_func("केंद्र सरकार की कुछ प्रमुख कृषि योजनाएं हैं:")
    scheme_list = list(GENERAL_SCHEME_MAP.keys())
    
    for i, scheme in enumerate(scheme_list, 1):
        bolo_func(f"{i}. {scheme}")
        time.sleep(0.5)
    
    bolo_func("आप किस योजना के बारे में जानना चाहते हैं? कृपया उसका नाम बताएं।")
    context.set(topic='agriculture', state='awaiting_agri_response', data={'query_type': 'scheme_selection'})


# --- Main Handler ---

def handle_scheme_query(command, bolo_func, context):
    """
<<<<<<< HEAD
    Processes queries related to schemes, subsidies, or loans, and manages conversation context.
    """
    scheme_keywords = {
        "किसान सम्मान": "किसान सम्मान निधि", "मुद्रा": "मुद्रा योजना",
        "सोलर पंप": "कुसुम योजना", "कुसुम": "कुसुम योजना", "स्वास्थ्य बीमा": "आयुष्मान भारत",
        "आयुष्मान": "आयुष्मान भारत", "फसल बीमा": "फसल बीमा", "सिंचाई": "कृषि सिंचाई",
        "ड्रोन": "कृषि यंत्रीकरण", "यंत्रीकरण": "कृषि यंत्रीकरण", "मशीनीकरण": "कृषि यंत्रीकरण",
        "मशीन": "कृषि यंत्रीकरण", "ट्रैक्टर": "कृषि यंत्रीकरण", "क्रेडिट कार्ड": "किसान क्रेडिट कार्ड",
        "ई नाम": "राष्ट्रीय कृषि बाजार", "मान धन": "प्रधानमंत्री किसान मान धन योजना"
=======
    Returns "HANDLED" on success and "SCHEME_NOT_FOUND" on failure.
    """
    loan_keywords = ["लोन", "ऋण", "कर्ज़", "कर्ज", "वित्तीय सहायता"]

    if any(key in command for key in loan_keywords):
        handle_loan_query(command, bolo_func)
        return "HANDLED"

    scheme_keywords = {
        "किसान सम्मान": "किसान सम्मान निधि",
        "स्वास्थ्य बीमा": "आयुष्मान भारत",
        "आयुष्मान": "आयुष्मान भारत",
        "फसल बीमा": "फसल बीमा",
        "सिंचाई": "कृषि सिंचाई",
        "ड्रोन": "कृषि यंत्रीकरण",
        "मशीन": "कृषि यंत्रीकरण",
        "ट्रैक्टर": "कृषि यंत्रीकरण"
>>>>>>> 99af8066a8e7c79aaa8fa10d146813ab0e88bc02
    }
    
    if "कुसुम" in command or "सोलर" in command or "मुद्रा" in command:
        handle_loan_query(command, bolo_func)
        return "HANDLED"

    # Handle contextual response for scheme selection
    if context.state == 'awaiting_agri_response' and context.data.get('query_type') == 'scheme_selection':
        available_schemes = context.data.get('schemes', [])
        selected_scheme_data = next((s for s in available_schemes if s.get('yojana_naam') in command), None)
        if selected_scheme_data:
            speak_scheme_details(selected_scheme_data, bolo_func)
            context.clear()
            return

    if "सभी योजनाएं" in command or "सारी योजनाएं" in command or "योजनाओं की सूची" in command:
        get_all_schemes_info(bolo_func, context)
        return

    found_scheme_key = next((key for key in scheme_keywords if key in command), None)
    if found_scheme_key:
<<<<<<< HEAD
        scheme_name = scheme_keywords[found_scheme_key]
        filename = GENERAL_SCHEME_MAP.get(scheme_name)
        if filename:
            scheme_data = load_json_data('scheme_data', filename) or SCHEME_FALLBACK_DATA.get(scheme_name)
            if scheme_data:
                speak_scheme_details(scheme_data, bolo_func)
            else:
                bolo_func(f"माफ़ कीजिए, {scheme_name} के लिए डेटा लोड करने में समस्या हुई।")
        else:
            bolo_func(f"माफ़ कीजिए, {scheme_name} के लिए कोई योजना मैप नहीं की गई है।")
        return

    found_crop = next((c for c in Config.agri_commodities if c in command), None)
    if "सब्सिडी" in command and found_crop:
        get_subsidy_info(found_crop, bolo_func, context)
        return

    if "लोन" in command or "ऋण" in command or "कर्ज" in command:
        get_loan_info(bolo_func)
        return
        
    if "सब्सिडी" in command or "अनुदान" in command:
        bolo_func("आप किस फसल के लिए सब्सिडी जानना चाहते हैं? कृपया फसल का नाम बताएं।")
        # Set context to handle the user's next response as a crop name for subsidy info
        context.set(
            topic='agriculture',
            state='awaiting_agri_response',
            data={'query_type': 'subsidy'}
        )
        return

    # Fallback response if no specific intent is matched
    bolo_func("मैं आपको कृषि योजनाओं, सब्सिडी, या ऋण के बारे में जानकारी दे सकती हूँ। कृपया बताएं कि आप किस बारे में जानना चाहते हैं।")
=======
        # ... (logic to speak details) ...
        return "HANDLED"

    found_crop = next((c for c in Config.agri_commodities if c in command), None)
    if found_crop:
        get_subsidy_info(found_crop, bolo_func)
        return "HANDLED"

    # If an agri scheme trigger was in the command but no specific scheme was found
    return "SCHEME_NOT_FOUND"
>>>>>>> 99af8066a8e7c79aaa8fa10d146813ab0e88bc02
