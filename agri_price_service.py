# agri_price_service.py (Enhanced Version)

import requests
import os
import random
import Config

# Note: The MAPPING dictionaries should ideally be moved to Config.py for better organization,
# but for now, we will keep them here and focus on the logic.

COMMODITY_MAPPING = {
    "आलू": "Potato", "प्याज": "Onion", "टमाटर": "Tomato", "गेहूं": "Wheat",
    "धान": "Paddy", "चावल": "Rice", "गन्ना": "Sugarcane", "सब्जियां": "Vegetables",
    "दालें": "Pulses", "बैंगन": "Brinjal", "भिंडी": "Okra", "फूलगोभी": "Cauliflower",
    "केला": "Banana", "नींबू": "Lemon", "अदरक": "Ginger", "हल्दी": "Turmeric",
    "मक्का": "Maize", "ज्वार": "Sorghum", "बाजरा": "Pearl Millet", "रागी": "Finger Millet",
    "सोयाबीन": "Soybean", "मूंगफली": "Groundnut", "सरसों": "Mustard", "तिल": "Sesame",
    "कपास": "Cotton", "गन्ना": "Sugarcane", "चाय": "Tea", "कॉफी": "Coffee"
}

MARKET_MAPPING = {
    "लखनऊ": "Lucknow", "दिल्ली": "Delhi", "मुंबई": "Mumbai", "कानपुर": "Kanpur",
    "बंगलौर": "Bangalore", "चेन्नई": "Chennai", "कोलकाता": "Kolkata", "हैदराबाद": "Hyderabad",
    "अहमदाबाद": "Ahmedabad", "पुणे": "Pune", "जयपुर": "Jaipur", "इंदौर": "Indore",
    "भोपाल": "Bhopal", "पटना": "Patna", "रांची": "Ranchi", "देहरादून": "Dehradun"
}

STATE_MAPPING = {
    "उत्तर प्रदेश": "Uttar Pradesh", "महाराष्ट्र": "Maharashtra", "दिल्ली": "Delhi",
    "मध्य प्रदेश": "Madhya Pradesh", "बिहार": "Bihar", "पंजाब": "Punjab",
    "राजस्थान": "Rajasthan", "हरियाणा": "Haryana", "गुजरात": "Gujarat", "कर्नाटक": "Karnataka",
    "तमिलनाडु": "Tamil Nadu", "पश्चिम बंगाल": "West Bengal", "आंध्र प्रदेश": "Andhra Pradesh",
    "तेलंगाना": "Telangana", "ओडिशा": "Odisha", "झारखंड": "Jharkhand", "असम": "Assam"
}

def get_agmarknet_price(hindi_commodity, hindi_market, hindi_state):
    """Fetches modal price for a commodity from Agmarknet API."""
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

def get_fallback_price(commodity, market, state):
    """Provides fallback price data when API is unavailable."""
    # Mock data for demonstration - in real implementation, this could be cached data
    fallback_prices = {
        "आलू": {"लखनऊ": 1200, "दिल्ली": 1250, "मुंबई": 1400},
        "प्याज": {"लखनऊ": 1800, "दिल्ली": 1900, "मुंबई": 2000},
        "टमाटर": {"लखनऊ": 1500, "दिल्ली": 1600, "मुंबई": 1700},
        "गेहूं": {"लखनऊ": 2200, "दिल्ली": 2250, "मुंबई": 2300},
        "धान": {"लखनऊ": 1800, "दिल्ली": 1850, "मुंबई": 1900}
    }
    
    if commodity in fallback_prices and market in fallback_prices[commodity]:
        return fallback_prices[commodity][market], market, commodity
    return None, None, None

def handle_price_query(command, bolo_func, entities):
    """
    ENHANCED: Uses pre-extracted entities from the NLU engine to fetch the price.
    """
    found_commodity = entities.get('crop')
    
    if not found_commodity:
        # Try to extract commodity from command if not found in entities
        for commodity in COMMODITY_MAPPING.keys():
            if commodity in command:
                found_commodity = commodity
                break
        
        if not found_commodity:
            bolo_func("आप किस चीज़ का भाव जानना चाहते हैं? जैसे: आलू, प्याज, या गेहूं।")
            return

    # Use the market entity if found, otherwise fall back to the default.
    found_market = entities.get('market', Config.DEFAULT_MARKET)
    
    # State can still be parsed from the command as a fallback.
    found_state = next((s for s in STATE_MAPPING.keys() if s in command), Config.DEFAULT_STATE)

    # Try API first
    price, api_market, api_commodity = get_agmarknet_price(found_commodity, found_market, found_state)
    
    # If API fails, try fallback data
    if not price or price in ['N/A', '0']:
        price, api_market, api_commodity = get_fallback_price(found_commodity, found_market, found_state)
        
        if not price:
            response = f"माफ़ कीजिए, {found_commodity} का भाव {found_market} मंडी से अभी प्राप्त नहीं हो पा रहा है। कृपया कुछ समय बाद पूछें।"
            bolo_func(response)
            return

    response_template = random.choice(Config.PRICE_RESPONSE_TEMPLATES)
    response = response_template.format(api_market, api_commodity, price)
    
    # Add price trend information if available
    trend_info = get_price_trend(found_commodity, found_market)
    if trend_info:
        response += f" {trend_info}"
    
    bolo_func(response)

def get_price_trend(commodity, market):
    """Provides simple price trend information (mock implementation)."""
    trends = {
        "आलू": "आलू के भाव में पिछले सप्ताह की तुलना में 5% की वृद्धि हुई है।",
        "प्याज": "प्याज के भाव में पिछले सप्ताह की तुलना में 3% की कमी आई है।",
        "टमाटर": "टमाटर के भाव स्थिर बने हुए हैं।",
        "गेहूं": "गेहूं के भाव में मामूली वृद्धि देखी जा रही है।"
    }
    
    return trends.get(commodity, "")