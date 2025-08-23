# agri_scheme_service.py

import json
import os
import Config
from Voice_tool import bolo
import time

# --- File Mappings (No Change) ---
CROP_SUBSIDY_MAP = {
    "गेहूं": "gehu_subsidies.json",
    "धान": "dhan_subsidies.json",
    "गन्ना": "ganna_subsidies.json",
    "सब्जियां": "sabjiyan_subsidies.json",
    "दालें": "dalen_subsidies.json"
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
}

# --- Helper Functions (No Change) ---
def load_json_data(folder, filename):
    try:
        file_path = os.path.join(folder, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def speak_scheme_details(scheme_data, bolo_func):
    if not scheme_data:
        return
    bolo_func(f"{scheme_data.get('yojana_ka_naam', 'इस योजना का नाम उपलब्ध नहीं है।')}")
    bolo_func(f"इसके बारे में जानकारी यह है: {scheme_data.get('yojana_ke_baare_mein', 'विवरण उपलब्ध नहीं है।')}")
    benefits = scheme_data.get('kya_laabh_milega', [])
    if isinstance(benefits, list):
        bolo_func("इस योजना के तहत आपको यह लाभ मिलेंगे:")
        for benefit in benefits:
            bolo_func(benefit)
            time.sleep(0.5)

def get_subsidy_info(crop_type, bolo_func):
    filename = CROP_SUBSIDY_MAP.get(crop_type)
    if not filename:
        bolo_func(f"{crop_type} के लिए कोई विशेष सब्सिडी योजना नहीं मिली।")
        return
    subsidy_data = load_json_data('subsidy_data', filename)
    if subsidy_data:
        scheme_names = [s.get('yojana_naam', '') for s in subsidy_data]
        response = f"{crop_type} की खेती के लिए ये योजनाएं उपलब्ध हैं: {', '.join(scheme_names)}।"
        bolo_func(response)
    else:
        bolo_func(f"{crop_type} के लिए सब्सिडी डेटा लोड करने में समस्या हुई।")

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




def handle_scheme_query(command, bolo_func):
    """
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
    }
    
    if "कुसुम" in command or "सोलर" in command or "मुद्रा" in command:
        handle_loan_query(command, bolo_func)
        return "HANDLED"

    found_scheme_key = next((key for key in scheme_keywords if key in command), None)
    if found_scheme_key:
        # ... (logic to speak details) ...
        return "HANDLED"

    found_crop = next((c for c in Config.agri_commodities if c in command), None)
    if found_crop:
        get_subsidy_info(found_crop, bolo_func)
        return "HANDLED"

    # If an agri scheme trigger was in the command but no specific scheme was found
    return "SCHEME_NOT_FOUND"