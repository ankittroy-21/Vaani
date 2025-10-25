"""
Agricultural Scheme Service Module
Provides information about government schemes, subsidies, and loans for farmers.
"""

import json
import os
import time
import logging
from typing import Optional, Dict, Any, List

from vaani.core import config as Config
from vaani.core.voice_tool import bolo

# Setup logging
logger = logging.getLogger(__name__)

# --- Data Mappings ---


# --- Data Mappings ---

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
    "कृषि बीमा": "national_agriculture_insurance.json",
    "प्रधानमंत्री किसान मान धन योजना": "pm_kisan_man_dhan.json",
    "राष्ट्रीय कृषि बाजार": "e_nam.json",
    "किसान क्रेडिट कार्ड": "kisan_credit_card.json"
}

# Fallback data for critical schemes
SCHEME_FALLBACK_DATA = {
    "कृषि यंत्रीकरण": {
        'yojana_ka_naam': "कृषि यंत्रीकरण योजना",
        'yojana_ke_baare_mein': "यह योजना किसानों को कृषि मशीनरी खरीदने में आर्थिक सहायता प्रदान करती है।",
        'kya_laabh_milega': "इस योजना में विभिन्न कृषि उपकरणों की खरीद पर सब्सिडी मिलती है।",
        'पात्रता': [
            "किसान होना अनिवार्य है।",
            "कम से कम 1 एकड़ कृषि भूमि होनी चाहिए।",
            "आधार कार्ड और बैंक खाता आवश्यक है।"
        ],
        'aavedan_prakriya': "अपने नजदीकी कृषि कार्यालय या ऑनलाइन पोर्टल पर आवेदन करें।",
        'sampark_jankari': "अधिक जानकारी के लिए कृषि विभाग से संपर्क करें।"
    }
}


# --- Utility Functions ---

def clean_text(text: Any) -> str:
    """Utility to clean and normalize text."""
    if isinstance(text, str):
        return ' '.join(text.split())
    return str(text)


def load_json_data(folder: str, filename: str) -> Optional[Dict[str, Any]]:
    """
    Load JSON file from specified folder with error handling.
    
    Args:
        folder: Folder name within the data directory
        filename: JSON filename to load
        
    Returns:
        Dictionary containing the data or None if error
    """
    try:
        file_path = os.path.join('data', folder, filename)
        
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.info(f"Successfully loaded {filename} from {folder}")
            return data
            
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error for {folder}/{filename}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error loading {folder}/{filename}: {str(e)}")
        return None



# --- Core Logic Functions ---

def speak_scheme_details(scheme_data: Dict[str, Any], bolo_func) -> None:
    """
    Speaks scheme details in a structured, user-friendly manner.
    
    Args:
        scheme_data: Dictionary containing scheme information
        bolo_func: Function to speak the response
    """
    if not scheme_data:
        bolo_func("माफ़ कीजिए, योजना की जानकारी प्राप्त करने में समस्या हुई।")
        return

    # Clean all text fields
    for key, value in scheme_data.items():
        if isinstance(value, str):
            scheme_data[key] = clean_text(value)
        elif isinstance(value, list):
            scheme_data[key] = [clean_text(str(item)) for item in value]
        elif isinstance(value, dict):
            for sub_key in value:
                if isinstance(value[sub_key], str):
                    value[sub_key] = clean_text(value[sub_key])

    # Speak scheme name and description
    name = scheme_data.get('yojana_ka_naam', 'योजना')
    description = scheme_data.get('yojana_ke_baare_mein', 'विवरण उपलब्ध नहीं है।')

    bolo_func(name)
    time.sleep(0.3)
    bolo_func(f"इस योजना के बारे में: {description}")
    time.sleep(0.4)

    # Speak eligibility criteria
    eligibility = scheme_data.get('पात्रता', []) or scheme_data.get('kaun_laabh_le_sakta_hai', [])
    if eligibility:
        bolo_func("पात्रता मानदंड:")
        time.sleep(0.2)
        for criterion in eligibility:
            bolo_func(f"• {criterion}")
            time.sleep(0.3)

    # Speak benefits
    benefits = scheme_data.get('kya_laabh_milega', [])
    if benefits:
        bolo_func("इस योजना के लाभ:")
        time.sleep(0.2)
        benefits_list = [benefits] if isinstance(benefits, str) else benefits
        for benefit in benefits_list:
            bolo_func(f"• {benefit}")
            time.sleep(0.3)

    # Speak application process
    application_process = scheme_data.get('aavedan_prakriya', "") or scheme_data.get('apply_kaise_karein', "")
    if isinstance(application_process, dict):
        if 'jagah' in application_process:
            bolo_func(f"आवेदन कहाँ करें: {application_process['jagah']}")
            time.sleep(0.3)
        if 'prakriya' in application_process and isinstance(application_process['prakriya'], list):
            bolo_func("आवेदन प्रक्रिया:")
            time.sleep(0.2)
            for i, step in enumerate(application_process['prakriya'], 1):
                bolo_func(f"{i}. {step}")
                time.sleep(0.3)
    elif application_process:
        bolo_func(f"आवेदन प्रक्रिया: {application_process}")
        time.sleep(0.3)

    # Speak contact information
    contact_info = scheme_data.get('sampark_jankari', "")
    if contact_info:
        bolo_func(f"संपर्क जानकारी: {contact_info}")

    logger.info(f"Successfully spoke details for scheme: {name}")


def get_subsidy_info(crop_type: str, bolo_func, context) -> None:
    """
    Provides subsidy information for a specific crop.
    
    Args:
        crop_type: Name of the crop in Hindi
        bolo_func: Function to speak the response
        context: Context object for managing conversation state
    """
    filename = CROP_SUBSIDY_MAP.get(crop_type)
    
    if not filename:
        response = f"{crop_type} के लिए कोई विशेष सब्सिडी योजना की जानकारी उपलब्ध नहीं है। क्या आप किसी अन्य फसल के बारे में जानना चाहेंगे?"
        bolo_func(response)
        logger.warning(f"No subsidy scheme found for crop: {crop_type}")
        return

    subsidy_data = load_json_data('subsidy_data', filename)
    
    if subsidy_data and isinstance(subsidy_data, list):
        scheme_names = [s.get('yojana_naam', 'अज्ञात योजना') for s in subsidy_data]
        response = f"{crop_type} की खेती के लिए ये सब्सिडी योजनाएं उपलब्ध हैं: {', '.join(scheme_names)}।"
        bolo_func(response)
        time.sleep(0.3)
        
        bolo_func("क्या आप इनमें से किसी विशेष योजना के बारे में विस्तार से जानना चाहते हैं?")
        
        # Set context for follow-up
        context.set(
            topic='agriculture',
            state='awaiting_agri_response',
            data={'query_type': 'scheme_selection', 'schemes': subsidy_data}
        )
        logger.info(f"Provided subsidy scheme list for {crop_type}")
        
    elif subsidy_data:
        # Single scheme data
        speak_scheme_details(subsidy_data, bolo_func)
    else:
        response = f"माफ़ कीजिए, {crop_type} के लिए सब्सिडी डेटा लोड करने में समस्या हुई।"
        bolo_func(response)
        logger.error(f"Failed to load subsidy data for {crop_type}")


def get_loan_info(bolo_func) -> None:
    """
    Provides information about agricultural loans.
    
    Args:
        bolo_func: Function to speak the response
    """
    loan_data = load_json_data('loan_data', 'loans.json')
    
    if loan_data:
        bolo_func("कृषि ऋण के बारे में जानकारी:")
        time.sleep(0.3)
        speak_scheme_details(loan_data, bolo_func)
        time.sleep(0.3)
        bolo_func("अधिक जानकारी और आवेदन के लिए, अपने नजदीकी बैंक शाखा से संपर्क करें।")
        logger.info("Provided loan information")
    else:
        response = "माफ़ कीजिए, कृषि ऋण की जानकारी अभी उपलब्ध नहीं है। कृपया बाद में पुनः प्रयास करें।"
        bolo_func(response)
        logger.error("Failed to load loan data")


def get_all_schemes_info(bolo_func, context) -> None:
    """
    Provides a list of all major government schemes.
    
    Args:
        bolo_func: Function to speak the response
        context: Context object for managing conversation state
    """
    bolo_func("केंद्र सरकार की प्रमुख कृषि योजनाएं:")
    time.sleep(0.3)
    
    scheme_list = list(GENERAL_SCHEME_MAP.keys())
    
    for i, scheme in enumerate(scheme_list[:10], 1):  # Limit to top 10 to avoid long list
        bolo_func(f"{i}. {scheme}")
        time.sleep(0.4)
    
    if len(scheme_list) > 10:
        bolo_func(f"और भी कई योजनाएं उपलब्ध हैं।")
        time.sleep(0.3)
    
    bolo_func("आप किस योजना के बारे में जानना चाहते हैं? कृपया उसका नाम बताएं।")
    
    context.set(
        topic='agriculture',
        state='awaiting_agri_response',
        data={'query_type': 'scheme_selection'}
    )
    logger.info("Provided all schemes list")


# --- Main Handler ---

def handle_scheme_query(command: str, bolo_func, context) -> None:
    """
    Main handler for scheme-related queries with keyword matching and context handling.
    
    Args:
        command: User's command in Hindi
        bolo_func: Function to speak the response
        context: Context object for managing conversation state
    """
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
        "यंत्रीकरण": "कृषि यंत्रीकरण",
        "मशीनीकरण": "कृषि यंत्रीकरण",
        "मशीन": "कृषि यंत्रीकरण",
        "ट्रैक्टर": "कृषि यंत्रीकरण",
        "क्रेडिट कार्ड": "किसान क्रेडिट कार्ड",
        "ई नाम": "राष्ट्रीय कृषि बाजार",
        "मान धन": "प्रधानमंत्री किसान मान धन योजना"
    }

    # Handle contextual response for scheme selection
    if (context.state == 'awaiting_agri_response' and 
        context.data.get('query_type') == 'scheme_selection'):
        available_schemes = context.data.get('schemes', [])
        
        if available_schemes:
            selected_scheme_data = next(
                (s for s in available_schemes if s.get('yojana_naam', '') in command),
                None
            )
            if selected_scheme_data:
                speak_scheme_details(selected_scheme_data, bolo_func)
                context.clear()
                return

    # Handle "all schemes" query
    if any(keyword in command for keyword in ["सभी योजनाएं", "सारी योजनाएं", "योजनाओं की सूची"]):
        get_all_schemes_info(bolo_func, context)
        return

    # Try to match specific scheme keywords
    found_scheme_key = next((key for key in scheme_keywords if key in command), None)
    
    if found_scheme_key:
        scheme_name = scheme_keywords[found_scheme_key]
        filename = GENERAL_SCHEME_MAP.get(scheme_name)
        
        if filename:
            scheme_data = load_json_data('scheme_data', filename) or SCHEME_FALLBACK_DATA.get(scheme_name)
            
            if scheme_data:
                speak_scheme_details(scheme_data, bolo_func)
                logger.info(f"Provided info for scheme: {scheme_name}")
            else:
                response = f"माफ़ कीजिए, {scheme_name} के लिए डेटा लोड करने में समस्या हुई।"
                bolo_func(response)
                logger.error(f"Failed to load data for scheme: {scheme_name}")
        else:
            response = f"माफ़ कीजिए, {scheme_name} के लिए कोई योजना फ़ाइल उपलब्ध नहीं है।"
            bolo_func(response)
        return

    # Handle crop-specific subsidy queries
    found_crop = next((c for c in Config.agri_commodities if c in command), None)
    if "सब्सिडी" in command and found_crop:
        get_subsidy_info(found_crop, bolo_func, context)
        return

    # Handle loan queries
    if any(keyword in command for keyword in ["लोन", "ऋण", "कर्ज", "कर्जा"]):
        get_loan_info(bolo_func)
        return
        
    # Handle general subsidy query without crop
    if any(keyword in command for keyword in ["सब्सिडी", "अनुदान"]):
        response = (
            "आप किस फसल के लिए सब्सिडी जानना चाहते हैं? "
            "कृपया फसल का नाम बताएं। जैसे: गेहूं, धान, गन्ना, या सब्जियां।"
        )
        bolo_func(response)
        
        context.set(
            topic='agriculture',
            state='awaiting_agri_response',
            data={'query_type': 'subsidy'}
        )
        return

    # Fallback response
    response = (
        "मैं आपको कृषि योजनाओं, सब्सिडी, या ऋण के बारे में जानकारी दे सकती हूँ। "
        "कृपया बताएं कि आप किस बारे में जानना चाहते हैं।"
    )
    bolo_func(response)
    logger.info("Provided fallback response for scheme query")