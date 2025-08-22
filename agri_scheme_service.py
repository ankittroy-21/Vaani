import json
import os
import Config
from Voice_tool import bolo
import time

# फसल-विशिष्ट सब्सिडी योजनाओं के लिए मैपिंग
CROP_SUBSIDY_MAP = {
    "गेहूं": "gehu_subsidies.json",
    "धान": "dhan_subsidies.json",
    "गन्ना": "ganna_subsidies.json",
    "सब्जियां": "sabjiyan_subsidies.json",
    "दालें": "dalen_subsidies.json"
}

# सामान्य योजनाओं और लोन के लिए मैपिंग
GENERAL_SCHEME_MAP = {
    "किसान सम्मान निधि": "pm_kisan.json",
    "मुद्रा योजना": "pm_mudra_yojana.json",
    "कुसुम योजना": "pm_kusum.json",
    "आयुष्मान भारत": "ayushman_bharat.json",
    "फसल बीमा": "pm_fasal_bima_yojana.json",
    "कृषि सिंचाई": "pm_krishi_sinchai_yojana.json",
    "टिकाऊ कृषि": "sustainable_agriculture_mission.json",
    "कृषि यंत्रीकरण": "agricultural_mechanization_scheme.json",
    "कृषि बीमा": "national_agriculture_insurance.json"
}

def load_json_data(folder, filename):
    """
    एक निर्दिष्ट फ़ोल्डर से JSON फ़ाइल लोड करने के लिए एक सामान्य फ़ंक्शन।
    """
    try:
        file_path = os.path.join(folder, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def speak_scheme_details(scheme_data, bolo_func):
    """
    योजना की विस्तृत जानकारी को भागों में बोलता है।
    """
    if not scheme_data:
        return

    bolo_func(f"{scheme_data.get('yojana_ka_naam', 'इस योजना का नाम उपलब्ध नहीं है।')}")
    bolo_func(f"इसके बारे में जानकारी यह है: {scheme_data.get('yojana_ke_baare_mein', 'विवरण उपलब्ध नहीं है।')}")
    
    benefits = scheme_data.get('kya_laabh_milega', [])
    if benefits:
        bolo_func("इस योजना के तहत आपको यह लाभ मिलेंगे:")
        for benefit in benefits:
            bolo_func(benefit)
            time.sleep(0.5)

def get_subsidy_info(crop_type, bolo_func):
    """
    फसल के आधार पर सब्सिडी की जानकारी देता है।
    """
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

def get_loan_info(bolo_func):
    """
    कृषि ऋण की जानकारी JSON फ़ाइल से देता है।
    """
    loan_data = load_json_data('loan_data', 'loans.json')
    if loan_data:
        bolo_func("कृषि ऋण के बारे में कुछ जानकारी यहाँ दी गई है:")
        for loan in loan_data:
            bolo_func(f"{loan.get('loan_ka_naam')}: {loan.get('vivaran')}")
            time.sleep(0.5)
    else:
        bolo_func("माफ़ कीजिए, लोन की जानकारी अभी उपलब्ध नहीं है।")


def handle_scheme_query(command, bolo_func):
    """
    योजना या लोन से संबंधित प्रश्नों को प्रोसेस करता है।
    """
    # सामान्य योजनाओं के कीवर्ड
    scheme_keywords = {
        "किसान सम्मान": "किसान सम्मान निधि",
        "मुद्रा": "मुद्रा योजना",
        "सोलर पंप": "कुसुम योजना",
        "कुसुम": "कुसुम योजना",
        "स्वास्थ्य बीमा": "आयुष्मान भारत",
        "आयुष्मान": "आयुष्मान भारत",
        "फसल बीमा": "फसल बीमा",
        "सिंचाई": "कृषि सिंचाई",
        "ड्रोन": "कृषि यंत्रीकरण",
        "मशीन": "कृषि यंत्रीकरण",
        "ट्रैक्टर": "कृषि यंत्रीकरण"
    }

    found_scheme_key = next((key for key in scheme_keywords if key in command), None)
    
    if found_scheme_key:
        scheme_name = scheme_keywords[found_scheme_key]
        filename = GENERAL_SCHEME_MAP.get(scheme_name)
        scheme_data = load_json_data('scheme_data', filename)
        if scheme_data:
            speak_scheme_details(scheme_data, bolo_func)
        else:
            bolo_func(f"माफ़ कीजिए, {scheme_name} के बारे में जानकारी नहीं मिली।")
        return

    found_crop = next((c for c in Config.agri_commodities if c in command), None)
    if found_crop:
        get_subsidy_info(found_crop, bolo_func)
        return

    if "लोन" in command or "ऋण" in command:
        get_loan_info(bolo_func)
        return

    bolo_func("मैं आपका सवाल समझ नहीं पाई। क्या आप किसी विशेष योजना, फसल सब्सिडी या लोन के बारे में जानना चाहते हैं?")