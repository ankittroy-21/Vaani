"""
Emergency Assistance Service for Illiterate Users
Quick access to emergency numbers, basic first aid, and crisis helplines
"""

class EmergencyAssistanceService:
    def __init__(self):
        """Initialize emergency service with important numbers"""
        
        # Critical emergency numbers
        self.emergency_numbers = {
            'police': {
                'number': '100',
                'name_hi': 'पुलिस',
                'when': 'चोरी, लड़ाई, खतरा'
            },
            'ambulance': {
                'number': '108',
                'name_hi': 'एम्बुलेंस',
                'when': 'बीमारी, चोट, दुर्घटना'
            },
            'fire': {
                'number': '101',
                'name_hi': 'फायर ब्रिगेड',
                'when': 'आग लगना'
            },
            'women_helpline': {
                'number': '1091',
                'name_hi': 'महिला हेल्पलाइन',
                'when': 'महिलाओं की सुरक्षा, घरेलू हिंसा'
            },
            'child_helpline': {
                'number': '1098',
                'name_hi': 'बाल हेल्पलाइन',
                'when': 'बच्चों की समस्या, गुम बच्चे'
            },
            'cyber_crime': {
                'number': '1930',
                'name_hi': 'साइबर क्राइम',
                'when': 'ऑनलाइन धोखाधड़ी, UPI फ्रॉड'
            },
            'disaster': {
                'number': '1078',
                'name_hi': 'आपदा प्रबंधन',
                'when': 'बाढ़, भूकंप, तूफान'
            },
            'farmer_helpline': {
                'number': '1800-180-1551',
                'name_hi': 'किसान कॉल सेंटर',
                'when': 'फसल की समस्या, कृषि सलाह'
            },
            'covid': {
                'number': '1075',
                'name_hi': 'कोरोना हेल्पलाइन',
                'when': 'कोरोना के लक्षण, टेस्ट, वैक्सीन'
            }
        }
        
        # Detection keywords
        self.emergency_keywords = {
            'help': ['मदद', 'help', 'बचाओ', 'emergency', 'तुरंत', 'urgent'],
            'health': ['बीमार', 'चोट', 'दर्द', 'खून', 'बेहोश', 'दुर्घटना', 'accident'],
            'safety': ['चोर', 'लड़ाई', 'डर', 'खतरा', 'मारपीट', 'हिंसा'],
            'fire': ['आग', 'fire', 'धुआं', 'जल रहा'],
            'women': ['छेड़छाड़', 'परेशान', 'महिला', 'लड़की'],
            'fraud': ['धोखा', 'fraud', 'ठगी', 'पैसे चोरी', 'फ्रॉड']
        }
        
        # Basic first aid in simple Hindi
        self.first_aid = {
            'bleeding': """
            खून बह रहा है तो:
            1. साफ कपड़ा लेकर घाव पर दबाकर रखें
            2. घाव को ऊपर उठाएं (अगर हाथ/पैर है)
            3. कपड़ा भीग जाए तो ऊपर से और कपड़ा रखें
            4. तुरंत 108 पर कॉल करें
            5. घाव को पानी से धोएं (अगर साफ पानी है)
            """,
            'burn': """
            जलने पर:
            1. जल्दी से ठंडे पानी में रखें (10-15 मिनट)
            2. बर्फ मत लगाएं
            3. तेल, मक्खन, टूथपेस्ट मत लगाएं
            4. साफ कपड़े से ढकें
            5. ज़्यादा जलने पर 108 पर कॉल करें
            """,
            'snakebite': """
            सांप काटने पर:
            1. बिल्कुल शांत रहें, हिलें-डुलें नहीं
            2. काटी हुई जगह को दिल से नीचे रखें
            3. तुरंत 108 पर कॉल करें
            4. कसके पट्टी न बांधें
            5. जड़ी-बूटी, झाड़-फूंक पर समय बर्बाद न करें
            6. अस्पताल जल्दी जाएं
            """,
            'electric_shock': """
            बिजली लगने पर:
            1. पहले बिजली का स्विच बंद करें
            2. लकड़ी या प्लास्टिक से व्यक्ति को हटाएं (हाथ से नहीं)
            3. अगर बेहोश है तो 108 पर कॉल करें
            4. चेहरे पर पानी के छींटे मारें
            5. खुली हवा में लिटाएं
            """,
            'unconscious': """
            बेहोश होने पर:
            1. जल्दी से 108 पर कॉल करें
            2. करवट के बल लिटाएं (सीधा नहीं)
            3. कॉलर ढीला करें
            4. मुंह में कुछ न डालें
            5. खुली हवा दें
            6. चेहरे पर पानी के छींटे मारें
            """
        }
    
    def detect_emergency(self, query):
        """Detect if query is an emergency"""
        query_lower = query.lower()
        
        # Check for emergency keywords
        for category, keywords in self.emergency_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return True, category
        
        return False, None
    
    def get_emergency_number(self, situation):
        """Get appropriate emergency number for situation"""
        query_lower = situation.lower()
        
        # Check each emergency type
        if any(word in query_lower for word in ['बीमार', 'चोट', 'दुर्घटना', 'accident', 'एम्बुलेंस']):
            return self.emergency_numbers['ambulance']
        
        elif any(word in query_lower for word in ['पुलिस', 'police', 'चोर', 'लड़ाई']):
            return self.emergency_numbers['police']
        
        elif any(word in query_lower for word in ['आग', 'fire', 'जल रहा']):
            return self.emergency_numbers['fire']
        
        elif any(word in query_lower for word in ['महिला', 'लड़की', 'छेड़छाड़']):
            return self.emergency_numbers['women_helpline']
        
        elif any(word in query_lower for word in ['धोखा', 'fraud', 'ठगी', 'upi']):
            return self.emergency_numbers['cyber_crime']
        
        elif any(word in query_lower for word in ['फसल', 'खेत', 'किसान']):
            return self.emergency_numbers['farmer_helpline']
        
        else:
            return self.emergency_numbers['police']  # Default to police
    
    def get_first_aid_guidance(self, situation):
        """Get simple first aid guidance"""
        query_lower = situation.lower()
        
        if any(word in query_lower for word in ['खून', 'bleeding', 'कटा', 'घाव']):
            return self.first_aid['bleeding']
        
        elif any(word in query_lower for word in ['जल गया', 'burn', 'जलना', 'आग लगी']):
            return self.first_aid['burn']
        
        elif any(word in query_lower for word in ['सांप', 'snake', 'काटा']):
            return self.first_aid['snakebite']
        
        elif any(word in query_lower for word in ['बिजली', 'shock', 'करंट']):
            return self.first_aid['electric_shock']
        
        elif any(word in query_lower for word in ['बेहोश', 'unconscious', 'गिर गया']):
            return self.first_aid['unconscious']
        
        return None
    
    def get_all_emergency_numbers(self):
        """Get formatted list of all emergency numbers"""
        message = "🚨 ज़रूरी नंबर:\n\n"
        
        for key, info in self.emergency_numbers.items():
            message += f"📞 {info['name_hi']}: {info['number']}\n"
            message += f"   कब: {info['when']}\n\n"
        
        return message


# Global instance
_emergency_service = None

def get_emergency_service():
    """Get or create emergency service"""
    global _emergency_service
    if _emergency_service is None:
        _emergency_service = EmergencyAssistanceService()
    return _emergency_service


def handle_emergency_query(query, voice_output_func):
    """Handle emergency queries"""
    service = get_emergency_service()
    
    is_emergency, category = service.detect_emergency(query)
    
    if not is_emergency:
        # Check if asking for emergency numbers list
        if any(word in query.lower() for word in ['emergency number', 'हेल्पलाइन', 'helpline', 'नंबर बताओ']):
            numbers = service.get_all_emergency_numbers()
            print(numbers)
            voice_output_func(numbers, lang='hi')
            return True
        return False
    
    print(f"⚠️ EMERGENCY DETECTED: {category}")
    
    # Get appropriate emergency number
    emergency_info = service.get_emergency_number(query)
    
    response = f"🚨 तुरंत {emergency_info['name_hi']} को फोन करें!\n\n"
    response += f"📞 नंबर: {emergency_info['number']}\n\n"
    
    # Get first aid if applicable
    first_aid = service.get_first_aid_guidance(query)
    if first_aid:
        response += "पहली सहायता:\n" + first_aid + "\n\n"
    
    response += "⏰ जल्दी करें! देर मत करें!"
    
    print(response)
    voice_output_func(response, lang='hi')
    
    return True


# Test function
if __name__ == "__main__":
    service = EmergencyAssistanceService()
    
    print("=" * 70)
    print("🚨 Testing Emergency Assistance Service")
    print("=" * 70)
    
    test_queries = [
        "मेरी मां बीमार हैं, मदद चाहिए",
        "घर में आग लग गई",
        "चोर घर में घुस गया",
        "सांप ने काट लिया",
        "खून बह रहा है",
        "UPI फ्रॉड हो गया",
        "सभी emergency numbers बताओ"
    ]
    
    for query in test_queries:
        print("\n" + "=" * 70)
        print(f"Q: {query}")
        print("-" * 70)
        
        is_emergency, category = service.detect_emergency(query)
        
        if is_emergency:
            print(f"Category: {category}")
            emergency_info = service.get_emergency_number(query)
            print(f"\n📞 {emergency_info['name_hi']}: {emergency_info['number']}")
            
            first_aid = service.get_first_aid_guidance(query)
            if first_aid:
                print(f"\nFirst Aid:\n{first_aid}")
        else:
            if 'नंबर' in query or 'number' in query:
                print(service.get_all_emergency_numbers())
    
    print("\n" + "=" * 70)
    print("✅ Test Complete!")
    print("=" * 70)
