import requests
import os
from datetime import datetime
import Config

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

def get_mock_price(commodity, market):
    """Fallback mock data for testing"""
    mock_prices = {
        "आलू": {"लखनऊ": 1800, "दिल्ली": 2200, "मुंबई": 2500, "कानपुर": 1900},
        "प्याज": {"लखनऊ": 1500, "दिल्ली": 1800, "मुंबई": 2000, "कानपुर": 1600},
        "टमाटर": {"लखनऊ": 1200, "दिल्ली": 1500, "मुंबई": 1700, "कानपур": 1300},
        "गेहूं": {"लखनऊ": 2100, "दिल्ली": 2300, "मुंबई": 2400, "कानपुर": 2200},
        "धान": {"लखनऊ": 1600, "दिल्ली": 1800, "मुंबई": 1900, "कानपुर": 1700},
        "चावल": {"लखनऊ": 2800, "दिल्ली": 3200, "मुंबई": 3500, "कानपुर": 2900},
    }
    
    return mock_prices.get(commodity, {}).get(market, None)