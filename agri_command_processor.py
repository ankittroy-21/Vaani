import random
from Voice_tool import bolo
import Config
from agri_price_service import get_agmarknet_price, get_mock_price, STATE_MAPPING
from agri_scheme_service import get_subsidy_info, get_loan_info
from agri_advisory_service import get_farming_advisory

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

    # 2. Government Scheme Query
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

    # 3. Farming Advice Query
    if any(word in command for word in Config.agri_advice_trigger):
        found_crop = next((c for c in Config.agri_commodities if c in command), None)
        found_stage = next((s for s in ["बुवाई", "सिंचाई", "कटाई"] if s in command), "बुवाई")

        if found_crop:
            advice = get_farming_advisory(found_crop, found_stage)
            response = f"{found_crop} की {found_stage} की सलाह: {advice}"
            bolo_func(response)
            return True
        else:
            bolo_func("किस फसल की सलाह चाहिए? जैसे: गेहूं, धान, आलू, टमाटर。")
            return True

    # If no agriculture command was detected
    return False