import requests
import os
import random
import Config

# --- Data Mappings (Specific to this module) ---
COMMODITY_MAPPING = {
    "आलू": "Potato", "प्याज": "Onion", "टमाटर": "Tomato", "गेहूं": "Wheat",
    "धान": "Paddy", "चावल": "Rice", "गन्ना": "Sugarcane", "सब्जियां": "Vegetables",
    "दालें": "Pulses", "बैंगन": "Brinjal", "भिंडी": "Okra", "फूलगोभी": "Cauliflower",
    "केला": "Banana", "नींबू": "Lemon", "अदरक": "Ginger", "हल्दी": "Turmeric"
}

MARKET_MAPPING = {
    "लखनऊ": "Lucknow", "दिल्ली": "Delhi", "मुंबई": "Mumbai", "कानपुर": "Kanpur",
    "बंगलौर": "Bangalore", "चेन्नई": "Chennai", "कोलकाता": "Kolkata", "हैदराबाद": "Hyderabad"
}

STATE_MAPPING = {
    "उत्तर प्रदेश": "Uttar Pradesh", "महाराष्ट्र": "Maharashtra", "दिल्ली": "Delhi",
    "मध्य प्रदेश": "Madhya Pradesh", "बिहार": "Bihar", "पंजाब": "Punjab",
    "राजस्थान": "Rajasthan", "हरियाणा": "Haryana"
}

def get_agmarknet_price(hindi_commodity, hindi_market, hindi_state):
    """
    Fetches modal price for a commodity from a specific market using the Agmarknet API.
    """
    try:
        api_key = os.getenv('AGMARKNET_API_KEY')
        if not api_key:
            print("ERROR: AGMARKNET_API_KEY not found.")
            return None, None, None

        params = {
            'api-key': api_key, 'format': 'json', 'limit': '5',
            'filters[commodity]': COMMODITY_MAPPING.get(hindi_commodity, hindi_commodity),
            'filters[market]': MARKET_MAPPING.get(hindi_market, hindi_market),
            'filters[state]': STATE_MAPPING.get(hindi_state, hindi_state),
            'sort[arrival_date]': 'desc'
        }
        
        response = requests.get(Config.AGMARKNET_BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get('records'):
            record = data['records'][0]
            return record.get('modal_price'), record.get('market'), record.get('commodity')
        return None, None, None
    except requests.exceptions.RequestException as e:
        print(f"Agmarknet API Error: {e}")
        return None, None, None

def get_mock_price(commodity, market):
    """Fallback mock data for testing."""
    mock_prices = {
        "आलू": {"लखनऊ": 1800, "दिल्ली": 2200}, "प्याज": {"लखनऊ": 1500, "दिल्ली": 1800},
        "टमाटर": {"लखनऊ": 1200, "दिल्ली": 1500}, "गेहूं": {"लखनऊ": 2100, "दिल्ली": 2300}
    }
    return mock_prices.get(commodity, {}).get(market)

def handle_price_query(command, bolo_func):
    """
    Parses the command for commodity and market, fetches the price, and speaks the result.
    This is the primary entry point for this module.
    """
    found_commodity = next((c for c in Config.agri_commodities if c in command), None)
    
    if not found_commodity:
        bolo_func("आप किस चीज़ का भाव जानना चाहते हैं? जैसे: आलू, प्याज, या गेहूं।")
        return

    found_market = next((m for m in Config.agri_markets if m in command), Config.DEFAULT_MARKET)
    found_state = next((s for s in STATE_MAPPING.keys() if s in command), Config.DEFAULT_STATE)

    price, api_market, api_commodity = get_agmarknet_price(found_commodity, found_market, found_state)
    
    if not price or price in ['N/A', '0']:
        print("INFO: API failed or returned no data. Falling back to mock data.")
        price = get_mock_price(found_commodity, found_market)
        api_market, api_commodity = found_market, found_commodity

    if price:
        response_template = random.choice(Config.PRICE_RESPONSE_TEMPLATES)
        response = response_template.format(api_market, api_commodity, price)
    else:
        response = f"माफ़ कीजिए, {found_commodity} का भाव {found_market} मंडी में अभी उपलब्ध नहीं है।"
    
    bolo_func(response)

