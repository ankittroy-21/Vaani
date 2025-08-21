import Config
from Voice_tool import bolo

def get_subsidy_info(crop_type):
    """Returns information about subsidies available for a specific crop type."""
    subsidy_db = {
        "गेहूं": ["प्रधानमंत्री किसान सम्मान निधि (PM-KISAN)", "राष्ट्रीय खाद्य सुरक्षा मिशन (NFSM) पर सब्सिडी"],
        "धान": ["प्रधानमंत्री किसान सम्मान निधि (PM-KISAN)", "बीज पर सब्सिडी", "जैविक खेती पर प्रोत्साहन"],
        "गन्ना": ["किसान क्रेडिट कार्ड (KCC)", "चीनी मिलों से अग्रिम भुगतान"],
        "सब्जियां": ["परंपरागत कृषि विकास योजना (PKVY) - जैविक खेती", "सूक्ष्म सिंचाई योजना"],
        "दालें": ["राष्ट्रीय खाद्य सुरक्षा मिशन (NFSM) - दलहन", "बीज विस्तार कार्यक्रम"]
    }
    return subsidy_db.get(crop_type, ["इस फसल के लिए विशिष्ट योजनाएं खोज रहा हूं।"])

def get_loan_info():
    """Returns information about agricultural loans."""
    loan_info = [
        "किसान क्रेडिट कार्ड (KCC): 3 लाख रुपये तक का लोन, 4% ब्याज दर तक सब्सिडी।",
        "प्रधानमंत्री मुद्रा योजना: छोटे किसानों के लिए 10 लाख रुपये तक का ऋण।",
        "राष्ट्रीय कृषि बीमा योजना (NAIS): फसल बीमा के साथ ऋण सुविधा।"
    ]
    return loan_info

def handle_scheme_query(command, bolo_func):
    """
    Primary function to process a scheme or loan query.
    """
    found_crop = next((c for c in Config.agri_commodities if c in command), None)

    if found_crop:
        schemes = get_subsidy_info(found_crop)
        response = f"{found_crop} की खेती के लिए ये योजनाएं उपलब्ध हैं: {', '.join(schemes[:2])}।"
    else:
        loans = get_loan_info()
        response = "कृषि ऋण के बारे में कुछ जानकारी: " + " ".join(loans[:2])
    
    bolo_func(response + " पूरी जानकारी के लिए कृपया अपने स्थानीय कृषि विभाग से संपर्क करें।")
