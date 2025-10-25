"""
Agricultural Price Service Module
Provides real-time commodity price information from Agmarknet API with fallback mechanisms.
"""

import requests
import os
import random
import logging
from typing import Optional, Tuple, Dict
from datetime import datetime, timedelta
import json

from vaani.core import config as Config

# Setup logging
logger = logging.getLogger(__name__)

# Mappings for Hindi to English translation
COMMODITY_MAPPING = {
    "आलू": "Potato", "प्याज": "Onion", "टमाटर": "Tomato", "गेहूं": "Wheat",
    "धान": "Paddy", "चावल": "Rice", "गन्ना": "Sugarcane", "सब्जियां": "Vegetables",
    "दालें": "Pulses", "बैंगन": "Brinjal", "भिंडी": "Okra", "फूलगोभी": "Cauliflower",
    "केला": "Banana", "नींबू": "Lemon", "अदरक": "Ginger", "हल्दी": "Turmeric",
    "मक्का": "Maize", "ज्वार": "Sorghum", "बाजरा": "Pearl Millet", "रागी": "Finger Millet",
    "सोयाबीन": "Soybean", "मूंगफली": "Groundnut", "सरसों": "Mustard", "तिल": "Sesame",
    "कपास": "Cotton", "चाय": "Tea", "कॉफी": "Coffee", "मिर्च": "Chilli",
    "गाजर": "Carrot", "मूली": "Radish", "पालक": "Spinach", "चना": "Gram"
}

MARKET_MAPPING = {
    "लखनऊ": "Lucknow", "दिल्ली": "Delhi", "मुंबई": "Mumbai", "कानपुर": "Kanpur",
    "बंगलौर": "Bangalore", "चेन्नई": "Chennai", "कोलकाता": "Kolkata", "हैदराबाद": "Hyderabad",
    "अहमदाबाद": "Ahmedabad", "पुणे": "Pune", "जयपुर": "Jaipur", "इंदौर": "Indore",
    "भोपाल": "Bhopal", "पटना": "Patna", "रांची": "Ranchi", "देहरादून": "Dehradun",
    "आगरा": "Agra", "वाराणसी": "Varanasi", "मेरठ": "Meerut", "नागपुर": "Nagpur"
}

STATE_MAPPING = {
    "उत्तर प्रदेश": "Uttar Pradesh", "महाराष्ट्र": "Maharashtra", "दिल्ली": "Delhi",
    "मध्य प्रदेश": "Madhya Pradesh", "बिहार": "Bihar", "पंजाब": "Punjab",
    "राजस्थान": "Rajasthan", "हरियाणा": "Haryana", "गुजरात": "Gujarat", "कर्नाटक": "Karnataka",
    "तमिलनाडु": "Tamil Nadu", "पश्चिम बंगाल": "West Bengal", "आंध्र प्रदेश": "Andhra Pradesh",
    "तेलंगाना": "Telangana", "ओडिशा": "Odisha", "झारखंड": "Jharkhand", "असम": "Assam"
}

# In-memory cache for API responses
_price_cache: Dict[str, Tuple[any, datetime]] = {}
CACHE_DURATION = timedelta(hours=6)  # Cache prices for 6 hours



def _get_cache_key(commodity: str, market: str, state: str) -> str:
    """Generate cache key for price data."""
    return f"{commodity}_{market}_{state}"


def _get_cached_price(cache_key: str) -> Optional[Tuple[str, str, str]]:
    """Retrieve price from cache if not expired."""
    if cache_key in _price_cache:
        data, timestamp = _price_cache[cache_key]
        if datetime.now() - timestamp < CACHE_DURATION:
            logger.info(f"Cache hit for {cache_key}")
            return data
        else:
            del _price_cache[cache_key]
            logger.info(f"Cache expired for {cache_key}")
    return None


def _set_cached_price(cache_key: str, data: Tuple[str, str, str]) -> None:
    """Store price in cache with timestamp."""
    _price_cache[cache_key] = (data, datetime.now())


def get_agmarknet_price(
    hindi_commodity: str, 
    hindi_market: str, 
    hindi_state: str
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Fetches modal price for a commodity from Agmarknet API with caching.
    
    Args:
        hindi_commodity: Commodity name in Hindi
        hindi_market: Market name in Hindi
        hindi_state: State name in Hindi
        
    Returns:
        Tuple of (price, market, commodity) or (None, None, None) if failed
    """
    try:
        # Check cache first
        cache_key = _get_cache_key(hindi_commodity, hindi_market, hindi_state)
        cached_data = _get_cached_price(cache_key)
        if cached_data:
            return cached_data

        # Get API key from environment
        api_key = os.getenv('AGMARKNET_API_KEY')
        if not api_key:
            logger.warning("AGMARKNET_API_KEY not configured. Using fallback data.")
            return None, None, None

        # Translate to English
        english_commodity = COMMODITY_MAPPING.get(hindi_commodity, hindi_commodity)
        english_market = MARKET_MAPPING.get(hindi_market, hindi_market)
        english_state = STATE_MAPPING.get(hindi_state, hindi_state)

        # Prepare API request
        params = {
            'api-key': api_key,
            'format': 'json',
            'limit': '5',
            'filters[commodity]': english_commodity,
            'filters[market]': english_market,
            'filters[state]': english_state,
            'sort[arrival_date]': 'desc'
        }
        
        logger.info(f"Fetching price for {english_commodity} from {english_market}, {english_state}")
        
        response = requests.get(
            Config.AGMARKNET_BASE_URL,
            params=params,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if data.get('records') and len(data['records']) > 0:
            record = data['records'][0]
            price = record.get('modal_price')
            market = record.get('market')
            commodity = record.get('commodity')
            
            if price and price not in ['N/A', '0', '', 'NA']:
                result = (price, market, commodity)
                _set_cached_price(cache_key, result)
                logger.info(f"Price fetched successfully: {price}")
                return result
        
        logger.warning(f"No valid price data found in API response")
        return None, None, None
        
    except requests.exceptions.Timeout:
        logger.error(f"API request timeout for {hindi_commodity}")
        return None, None, None
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        return None, None, None
    except Exception as e:
        logger.error(f"Unexpected error in get_agmarknet_price: {str(e)}")
        return None, None, None


def get_fallback_price(
    commodity: str, 
    market: str, 
    state: str
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Provides realistic fallback price data when API is unavailable.
    Uses cached offline data or estimated prices.
    """
    try:
        # Try to load from offline cache
        cache_file = os.path.join('data', 'offline_cache', 'price_cache.json')
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                offline_data = json.load(f)
                key = f"{commodity}_{market}"
                if key in offline_data:
                    data = offline_data[key]
                    logger.info(f"Using offline cached price for {commodity}")
                    return data.get('price'), market, commodity
    except Exception as e:
        logger.error(f"Error loading offline cache: {str(e)}")

    # Hardcoded fallback with realistic Indian market prices (₹ per quintal)
    fallback_prices = {
        "आलू": {"लखनऊ": 1200, "दिल्ली": 1250, "मुंबई": 1400, "कानपुर": 1180},
        "प्याज": {"लखनऊ": 1800, "दिल्ली": 1900, "मुंबई": 2000, "कानपुर": 1750},
        "टमाटर": {"लखनऊ": 1500, "दिल्ली": 1600, "मुंबई": 1700, "कानपुर": 1450},
        "गेहूं": {"लखनऊ": 2200, "दिल्ली": 2250, "मुंबई": 2300, "कानपुर": 2180},
        "धान": {"लखनऊ": 1800, "दिल्ली": 1850, "मुंबई": 1900, "कानपुर": 1780},
        "बैंगन": {"लखनऊ": 1100, "दिल्ली": 1200, "मुंबई": 1300, "कानपुर": 1080},
        "भिंडी": {"लखनऊ": 1400, "दिल्ली": 1500, "मुंबई": 1600, "कानपुर": 1350},
        "गाजर": {"लखनऊ": 900, "दिल्ली": 950, "मुंबई": 1000, "कानपुर": 880},
        "मिर्च": {"लखनऊ": 5000, "दिल्ली": 5200, "मुंबई": 5500, "कानपुर": 4900},
    }
    
    if commodity in fallback_prices and market in fallback_prices[commodity]:
        price = str(fallback_prices[commodity][market])
        logger.info(f"Using hardcoded fallback price for {commodity} in {market}")
        return price, market, commodity
    
    return None, None, None



def handle_price_query(command: str, bolo_func, entities: dict) -> None:
    """
    Enhanced price query handler with entity extraction and better error handling.
    
    Args:
        command: User's command in Hindi
        bolo_func: Function to speak the response
        entities: Dictionary containing extracted entities (crop, market, etc.)
    """
    # Extract commodity from entities or command
    found_commodity = entities.get('crop')
    
    if not found_commodity:
        # Fallback: Try to extract from command
        for commodity in COMMODITY_MAPPING.keys():
            if commodity in command:
                found_commodity = commodity
                break
        
        if not found_commodity:
            response = "आप किस चीज़ का भाव जानना चाहते हैं? जैसे: आलू, प्याज, टमाटर, गेहूं, या धान।"
            bolo_func(response)
            return

    # Extract market and state
    found_market = entities.get('market', Config.DEFAULT_MARKET)
    found_state = next(
        (s for s in STATE_MAPPING.keys() if s in command),
        Config.DEFAULT_STATE
    )

    logger.info(f"Price query - Commodity: {found_commodity}, Market: {found_market}, State: {found_state}")

    # Try API first
    price, api_market, api_commodity = get_agmarknet_price(
        found_commodity, 
        found_market, 
        found_state
    )
    
    source = "live API"
    
    # If API fails, try fallback data
    if not price or price in ['N/A', '0', '', 'NA']:
        logger.info(f"API failed, trying fallback for {found_commodity}")
        price, api_market, api_commodity = get_fallback_price(
            found_commodity, 
            found_market, 
            found_state
        )
        source = "cached data"
        
        if not price:
            response = (
                f"माफ़ कीजिए, {found_commodity} का भाव {found_market} मंडी में "
                f"अभी उपलब्ध नहीं है। कृपया कुछ समय बाद पुनः प्रयास करें। "
                f"आप किसी अन्य मंडी या फसल के बारे में पूछ सकते हैं।"
            )
            bolo_func(response)
            return

    # Format response
    try:
        response_template = random.choice(Config.PRICE_RESPONSE_TEMPLATES)
        response = response_template.format(api_market or found_market, api_commodity or found_commodity, price)
        
        # Add data source disclaimer if using fallback
        if source == "cached data":
            response += f" यह पुराना डेटा है, कृपया नवीनतम भाव के लिए मंडी से संपर्क करें।"
        
        bolo_func(response)
        logger.info(f"Response sent: {response}")
        
    except Exception as e:
        logger.error(f"Error formatting response: {str(e)}")
        # Fallback simple response
        response = f"{found_market} मंडी में {found_commodity} का भाव {price} रुपये प्रति क्विंटल है।"
        bolo_func(response)


def clear_price_cache() -> None:
    """Clear the price cache. Useful for testing or manual refresh."""
    global _price_cache
    _price_cache.clear()
    logger.info("Price cache cleared")


def get_price_trend(commodity: str, market: str) -> str:
    """
    Provides simple price trend information.
    
    TODO: Implement actual trend analysis by comparing historical prices
    """
    trends = {
        "आलू": "आलू के भाव में पिछले सप्ताह की तुलना में मामूली उतार-चढ़ाव है।",
        "प्याज": "प्याज के भाव में स्थिरता देखी जा रही है।",
        "टमाटर": "टमाटर के भाव में मौसम के कारण कुछ वृद्धि हो सकती है।",
        "गेहूं": "गेहूं के भाव सरकारी समर्थन मूल्य के अनुसार स्थिर हैं।",
        "धान": "धान के भाव में मंडी आगमन के अनुसार बदलाव आ रहा है।"
    }
    
    return trends.get(commodity, "")