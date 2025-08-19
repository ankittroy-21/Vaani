import requests
import json
from datetime import datetime
import Config
import os
from Voice_tool import bolo
import random

# --- Commodity Mapping (Hindi to English) ---
COMMODITY_MAPPING = {
    "आलू": "Potato",
    "प्याज": "Onion", 
    "टमाटर": "Tomato",
    "गेहूं": "Wheat",
    "धान": "Paddy",
    "चावल": "Rice",
    "गन्ना": "Sugarcane",
    "सब्जियां": "Vegetables",
    "दालें": "Pulses",
    "बैंगन": "Brinjal",
    "भिंडी": "Okra",
    "फूलगोभी": "Cauliflower",
    "केला": "Banana",
    "नींबू": "Lemon",
    "अदरक": "Ginger",
    "हल्दी": "Turmeric"
}

# --- Market Mapping (Hindi to English) --- 
MARKET_MAPPING = {
    "लखनऊ": "Lucknow",
    "दिल्ली": "Delhi",
    "मुंबई": "Mumbai",
    "कानपुर": "Kanpur",
    "बंगलौर": "Bangalore",
    "चेन्नई": "Chennai",
    "कोलकाता": "Kolkata",
    "हैदराबाद": "Hyderabad"
}

# --- State Mapping (Hindi to English) ---
STATE_MAPPING = {
    "उत्तर प्रदेश": "Uttar Pradesh",
    "महाराष्ट्र": "Maharashtra",
    "दिल्ली": "Delhi",
    "मध्य प्रदेश": "Madhya Pradesh",
    "बिहार": "Bihar",
    "पंजाब": "Punjab",
    "राजस्थान": "Rajasthan",
    "हरियाणा": "Haryana"
}

# --- Agmarknet API Functions (Market Prices) ---
def get_agmarknet_price(hindi_commodity, hindi_market="Lucknow", hindi_state="Uttar Pradesh"):
    """
    Fetches modal price for a commodity from a specific market using the Agmarknet API.
    """
    try:
        # Convert Hindi names to English for API
        english_commodity = COMMODITY_MAPPING.get(hindi_commodity, hindi_commodity)
        english_market = MARKET_MAPPING.get(hindi_market, hindi_market)
        english_state = STATE_MAPPING.get(hindi_state, hindi_state)
        
        # Use configuration from Config.py
        api_key = os.getenv('AGMARKNET_API_KEY')
        base_url = Config.AGMARKNET_BASE_URL
        
        # Build the API URL with parameters - using correct field names from API response
        params = {
            'api-key': api_key,
            'format': 'json',
            'filters[commodity]': english_commodity,
            'filters[market]': english_market,
            'filters[state]': english_state,
            'limit': '10',
            'sort[arrival_date]': 'desc'
        }
        
        print(f"DEBUG: Calling API with - Commodity: {english_commodity}, Market: {english_market}, State: {english_state}")
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        print(f"DEBUG: API found {data.get('total', 0)} records")
        
        if data.get('records'):
            # Get the latest record (first one due to sorting)
            latest_record = data['records'][0]
            
            # Use the correct field names from the API response
            modal_price = latest_record.get('modal_price', 'डाटा उपलब्ध नहीं')
            market_name = latest_record.get('market', english_market)
            commodity_name = latest_record.get('commodity', english_commodity)
            state_name = latest_record.get('state', english_state)
            arrival_date = latest_record.get('arrival_date', 'तारीख उपलब्ध नहीं')
            
            print(f"DEBUG: Found price - {modal_price} on {arrival_date}")
            return modal_price, market_name, commodity_name, state_name, arrival_date
        else:
            print("DEBUG: No records found in API response")
            return None, None, None, None, None

    except requests.exceptions.RequestException as e:
        print(f"Agmarknet API Error: {e}")
        return None, None, None, None, None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, None, None, None, None

# --- Mock Data Fallback Function ---
def get_mock_price(commodity, market):
    """Fallback mock data for testing"""
    mock_prices = {
        "आलू": {"लखनऊ": 1800, "दिल्ली": 2200, "मुंबई": 2500, "कानपुर": 1900},
        "प्याज": {"लखनऊ": 1500, "दिल्ली": 1800, "मुंबई": 2000, "कानपुर": 1600},
        "टमाटर": {"लखनऊ": 1200, "दिल्ली": 1500, "मुंबई": 1700, "कानपुर": 1300},
        "गेहूं": {"लखनऊ": 2100, "दिल्ली": 2300, "मुंबई": 2400, "कानपुर": 2200},
        "धान": {"लखनऊ": 1600, "दिल्ली": 1800, "मुंबई": 1900, "कानपुर": 1700},
        "चावल": {"लखनऊ": 2800, "दिल्ली": 3200, "मुंबई": 3500, "कानपुर": 2900},
    }
    
    return mock_prices.get(commodity, {}).get(market, None)

# --- Government Scheme Functions ---
def get_subsidy_info(crop_type):
    """Returns information about subsidies available for a specific crop type."""
    # Local database of schemes. Can be expanded massively.
    subsidy_db = {
        "गेहूं": ["प्रधानमंत्री किसान सम्मान निधि (PM-KISAN)", "राष्ट्रीय खाद्य सुरक्षा मिशन (NFSM) पर सब्सिडी"],
        "धान": ["प्रधानमंत्री किसान सम्मान निधि (PM-KISAN)", "बीज पर सब्सिडी", "जैविक खेती पर प्रोत्साहन"],
        "गन्ना": ["किसान क्रेडिट कार्ड (KCC)", "चीनी मिलों से अग्रिम भुगतान"],
        "सब्जियां": ["परंपरागत कृषि विकास योजना (PKVY) - जैविक खेती", "सूक्ष्म सिंचाई योजना"],
        "दालें": ["राष्ट्रीय खाद्य सुरक्षा मिशन (NFSM) - दलहन", "बीज विस्तार कार्यक्रम"]
    }
    return subsidy_db.get(crop_type, ["इस फसल के लिए विशिष्ट योजनाएं खोज रहा हूं। कृपया स्थानीय कृषि अधिकारी से संपर्क करें।"])

def get_loan_info():
    """Returns information about agricultural loans."""
    loan_info = [
        "किसान क्रेडिट कार्ड (KCC): 3 लाख रुपये तक का लोन, 4% ब्याज दर तक सब्सिडी।",
        "प्रधानमंत्री मुद्रा योजना: छोटे किसानों के लिए 10 लाख रुपये तक का ऋण।",
        "राष्ट्रीय कृषि बीमा योजना (NAIS): फसल बीमा के साथ ऋण सुविधा।"
    ]
    return loan_info

# --- Advisory Functions ---
def get_farming_advisory(crop, stage="बुवाई"):
    """Provides advisory based on crop and its growth stage."""
    advisory_db = {
        "गेहूं": {
            "बुवाई": "बुवाई का सही समय अक्टूबर-नवंबर है। 100 kg बीज प्रति हेक्टेयर प्रयोग करें।",
            "सिंचाई": "पहली सिंचाई बुवाई के 20-25 दिन बाद करें। कुल 4-6 सिंचाईयाँ पर्याप्त हैं।",
            "कटाई": "जब फसल पककर सुनहरी हो जाए, तब कटाई करें।"
        },
        "धान": {
            "बुवाई": "नर्सरी में बीज मई-जून में बोएं। 25-30 दिन की पौध रोपाई के लिए तैयार होगी।",
            "रोपाई": "रोपाई जुलाई में करें। पौध से पौध की दूरी 20 cm रखें।",
            "सिंचाई": "खेत में 2-3 इंच पानी बनाए रखें।"
        }
    }
    return advisory_db.get(crop, {}).get(stage, "इस फसल के लिए सलाह उपलब्ध नहीं है।")


# --- Updated Main Function ---
def process_agriculture_command(command, bolo_func):
    """
    The main function that listens for agriculture-related keywords in the command
    and calls the appropriate function.
    """

    # 1. Market Price Query
    if any(word in command for word in Config.agri_price_trigger):
        found_commodity = next((c for c in Config.agri_commodities if c in command), None)
        found_market = next((m for m in Config.agri_markets if m in command), "लखनऊ")
        found_state = next((s for s in STATE_MAPPING.keys() if s in command), "उत्तर प्रदेश")

        if found_commodity:
            # Try to get price from API first
            price, market_name, commodity_name, state_name, date = get_agmarknet_price(found_commodity, found_market, found_state)
            
            # If API fails, use mock data
            if price is None:
                price = get_mock_price(found_commodity, found_market)
                market_name = found_market
                commodity_name = found_commodity
            
            if price:
                response = f"{market_name} मंडी में {commodity_name} का भाव प्रति क्विंटल {price} रुपये है।"
            else:
                response = f"माफ़ कीजिए, {found_commodity} का भाव {found_market} मंडी में अभी उपलब्ध नहीं है।"
            
            bolo_func(response)
            return True
        else:
            bolo_func("किस चीज़ का भाव जानना चाहते हैं? जैसे: आलू, प्याज, टमाटर, गेहूं, धान, चावल, केला, बैंगन।")
            return True

    # 2. Government Scheme Query (unchanged)
    if any(word in command for word in Config.agri_scheme_trigger):
        found_crop = next((c for c in Config.agri_commodities if c in command), None)

        if found_crop:
            schemes = get_subsidy_info(found_crop)
            response = f"{found_crop} की खेती के लिए ये योजनाएं उपलब्ध हैं: {', '.join(schemes[:2])}। पूरी जानकारी के लिए कृषि विभाग से संपर्क करें।"
        else:
            loans = get_loan_info()
            response = "कृषि ऋण के बारे में जानकारी: " + " ".join(loans[:2])
        bolo_func(response)
        return True

    # 3. Farming Advice Query (unchanged)
    if any(word in command for word in Config.agri_advice_trigger):
        found_crop = next((c for c in Config.agri_commodities if c in command), None)
        found_stage = next((s for s in ["बुवाई", "सिंचाई", "कटाई"] if s in command), "बुवाई")

        if found_crop:
            advice = get_farming_advisory(found_crop, found_stage)
            response = f"{found_crop} की {found_stage} की सलाह: {advice}"
            bolo_func(response)
            return True
        else:
            bolo_func("किस फसल की सलाह चाहिए? जैसे: गेहूं, धान, आलू, टमाटर।")
            return True

    # If no agriculture command was detected
    return False