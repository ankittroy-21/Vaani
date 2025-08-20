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
    return subsidy_db.get(crop_type, ["इस फसल के लिए विशिष्ट योजनाएं खोज रहा हूं। कृपया स्थानीय कृषि अधिकारी से संपर्क करें。"])

def get_loan_info():
    """Returns information about agricultural loans."""
    loan_info = [
        "किसान क्रेडिट कार्ड (KCC): 3 लाख रुपये तक का लोन, 4% ब्याज दर तक सब्सिडी।",
        "प्रधानमंत्री मुद्रा योजना: छोटे किसानों के लिए 10 लाख रुपये तक का ऋण।",
        "राष्ट्रीय कृषि बीमा योजना (NAIS): फसल बीमा के साथ ऋण सुविधा।"
    ]
    return loan_info