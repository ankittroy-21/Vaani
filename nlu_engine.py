# nlu_engine.py (Enhanced Version)

from sentence_transformers import SentenceTransformer, util
import torch
import Config 
import re

print("Loading NLU model... This may take a moment.")
model = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v1')
print("NLU model loaded successfully.")

# --- Enhanced INTENT_EXAMPLES for better accuracy ---
INTENT_EXAMPLES = {
    "get_agri_price": [
        "आलू का भाव क्या है", 
        "मंडी में गेहूं का दाम बताओ", 
        "प्याज की कीमत पता करो",
        "टमाटर का क्या रेट है",
        "आज का भाव",
        "कितने का आलू बिक रहा है",
        "गेहूं की कीमत क्या है",
        "मूंगफली का दाम बताओ",
        "लखनऊ में आलू का भाव",
        "दिल्ली मंडी में टमाटर की कीमत",
        "उत्तर प्रदेश में गेहूं का दाम",
        "क्या भाव है चावल का",
        "कीमत बताओ धान की",
        "सोयाबीन का भाव पता करो",
        "कपास का दाम क्या है",
        "गेहूं", # Contextual example
        "आलू" # Contextual example
    ],
    "get_agri_scheme": [
        "किसानों के लिए कौन सी योजना है", 
        "सब्सिडी के बारे में बताओ", 
        "मुझे लोन चाहिए",
        "सरकारी मदद कैसे मिलेगी",
        "बीमा योजना की जानकारी दो",
        "गेहूं की खेती के लिए सब्सिडी",
        "धान के लिए सरकारी योजना",
        "किसान कर्ज योजना",
        "फसल बीमा के बारे में बताओ",
        "आर्थिक सहायता कैसे मिलेगी",
        "सरकारी सहायता योजना",
        "कृषि ऋण कहाँ से मिलेगा",
        "अनुदान योजना की जानकारी",
        "किसान सम्मान निधि के बारे में बताओ",
        # --- NEW EXAMPLES FOR DRONE AND MECHANIZATION ---
        "ड्रोन योजना के बारे में जानकारी दो",
        "ड्रोन सब्सिडी योजना",
        "कृषि ड्रोन योजना",
        "ड्रोन खरीदने की सब्सिडी",
        "मुख्यमंत्री कृषि यंत्रीकरण योजना",
        "कृषि यंत्रीकरण सब्सिडी",
        "ट्रैक्टर पर सब्सिडी",
        # --- NEW EXAMPLES TO FIX MISCLASSIFICATION ---
        "ऋण के बारे में जानकारी दो",
        "कृषि लोन कैसे मिलेगा",
        "कर्ज की जानकारी चाहिए"
    ],
    "get_agri_advice": [
        "गेहूं की बुवाई कैसे करें", 
        "फसल में बीमारी लग गयी", 
        "खाद के बारे में सलाह दो",
        "सिंचाई कब करनी है",
        "आलू की खेती कैसे करें",
        "धान की रोग रोकथाम",
        "टमाटर की उन्नत किस्में",
        "मिट्टी और जलवायु की जानकारी",
        "कटाई का सही समय",
        "भंडारण कैसे करें",
        "कीट प्रबंधन के उपाय",
        "खेती की प्रक्रिया बताओ",
        "फसल की पूरी जानकारी दो",
        "बीमारी का इलाज क्या है",
        "रोकथाम के तरीके बताओ",
        "गेहूं की जानकारी" # Contextual example
    ],
    "get_news_detail": [
        "पहली खबर के बारे में विस्तार से बताओ",
        "तीसरी खबर सुनाओ",
        "उसके बारे में और बताओ",
        "नंबर दो वाली खबर",
        "दूसरी खबर की जानकारी दो",
        "चौथी खबर सुनाओ",
        "पांचवीं खबर के बारे में बताओ"
    ],
    "get_weather": [
        "आज मौसम कैसा है", 
        "तापमान बताओ", 
        "क्या कल बारिश होगी", 
        "बाहर निकलना ठीक रहेगा क्या?",
        "लखनऊ का मौसम",
        "दिल्ली में तापमान क्या है",
        "मुंबई में बारिश होगी क्या",
        "हवा की गति बताओ",
        "नमी कितनी है",
        "मौसम की पूरी जानकारी दो"
    ],
    "get_time": [
        "समय बताओ", 
        "अभी टाइम क्या है", 
        "कितने बजे हैं", 
        "वक्त बताओ",
        "टाइम क्या हुआ",
        "घड़ी में क्या बजा है",
        "वर्तमान समय बताओ",
        "समय की जानकारी दो"
    ],
    "get_news": [
        "आज की खबरें सुनाओ", 
        "खबर सुनाओ", 
        "समाचार बताओ", 
        "मुख्य समाचार क्या हैं", 
        "ताज़ा न्यूज़ बताओ",
        "हेडलाइंस क्या हैं",
        "देश में क्या चल रहा है",
        "आज की सुर्खियाँ",
        "ताजा खबरें बताओ",
        "समाचार सुनाओ",
        "दुनिया की खबरें",
        "भारत की खबरें"
    ],
    "get_wikipedia": [
        "विकिपीडिया पर खोजो", 
        "भारत के बारे में बताओ",
        "विकिपीडिया से जानकारी दो",
        "इंटरनेट पर खोजो",
        "जानकारी ढूंढो",
        "विकिपीडिया पर पता करो"
    ],
    "get_historical_date": [
        "इस दिन इतिहास में क्या हुआ था", 
        "आज के दिन क्या खास है",
        "तारीख के बारे में बताओ",
        "इतिहास की जानकारी दो",
        "आज का इतिहास क्या है"
    ],
    "greet": [
        "नमस्ते", 
        "हेलो", 
        "क्या हाल है", 
        "और बताओ", 
        "नमस्कार",
        "प्रणाम",
        "सत श्री अकाल",
        "राम राम",
        "जय श्री राम"
    ],
    "goodbye": [
       "प्रोग्राम बंद करो",
        "अब बंद कर दो",
        "अलविदा",
        "बाहर निकलो",
        "एग्जिट करो",
        "चुप हो जाओ",
        "सिस्टम बंद करो",
        "टाटा बाय बाय"
    ]
}

# Pre-compute embeddings for all example phrases for faster performance
intent_embeddings = {intent: model.encode(examples, convert_to_tensor=True) for intent, examples in INTENT_EXAMPLES.items()}

def recognize_intent(command):
    """Recognizes the user's primary intent using semantic similarity."""
    if not command or len(command.split()) == 0:
        return "unknown", 0.0

    command_embedding = model.encode(command, convert_to_tensor=True)
    best_score = 0
    best_intent = "unknown"

    for intent, examples_embedding in intent_embeddings.items():
        cos_scores = util.cos_sim(command_embedding, examples_embedding)[0]
        top_score = torch.max(cos_scores).item()

        if top_score > best_score:
            best_score = top_score
            best_intent = intent
    
    # Adjust confidence threshold based on the intent
    CONFIDENCE_THRESHOLD = 0.60
    if best_intent.startswith("get_agri_"):
        CONFIDENCE_THRESHOLD = 0.55  # Lower threshold for agriculture queries
    
    if best_score >= CONFIDENCE_THRESHOLD:
        return best_intent, best_score
    else:
        return "unknown", best_score

def extract_entities(command):
    """Extracts key entities from the command using Config.py lists and aliases."""
    entities = {}

    # --- NEW: Check for scheme-specific keywords ---
    scheme_keywords = {
        "ड्रोन": "यंत्रीकरण",
        "यंत्रीकरण": "यंत्रीकरण", 
        "मशीनीकरण": "यंत्रीकरण",
        "ट्रैक्टर": "यंत्रीकरण",
        "मशीन": "यंत्रीकरण"
    }
    
    for keyword, entity_value in scheme_keywords.items():
        if keyword in command:
            entities['scheme_type'] = entity_value
            break
            
    # Check for crop entities
    for crop in Config.agri_commodities:
        if crop in command:
            entities['crop'] = crop
            break
    
    # Check for market entities
    for market in Config.agri_markets:
        if market in command:
            entities['market'] = market
            break
            
    # Check for state entities
    for state in Config.agri_states:
        if state in command:
            entities['state'] = state
            break
    
    # Use aliases for better recognition
    for alias, canonical_name in Config.ENTITY_ALIASES.items():
        if alias in command:
            # Determine entity type based on which list the canonical name belongs to
            if canonical_name in Config.agri_commodities:
                entities['crop'] = canonical_name
            elif canonical_name in Config.agri_markets:
                entities['market'] = canonical_name
            elif canonical_name in Config.agri_states:
                entities['state'] = canonical_name
    
    # Extract stage information for agriculture advice
    if any(trigger in command for trigger in Config.agri_advice_trigger):
        for stage in Config.agri_stages:
            if stage in command:
                entities['stage'] = stage
                break
    
    return entities

def process_nlu(command):
    """A single function to get both intent and entities."""
    intent, score = recognize_intent(command)
    entities = {}
    
    if intent != "unknown":
        entities = extract_entities(command)
    
    # Special handling for agriculture queries with low confidence
    if intent == "unknown" and score > 0.4:
        # Check if it might be an agriculture query that didn't meet the threshold
        agriculture_keywords = Config.agri_price_trigger + Config.agri_scheme_trigger + Config.agri_advice_trigger
        if any(keyword in command for keyword in agriculture_keywords):
            # Try to determine which type of agriculture query it is
            if any(price_word in command for price_word in Config.agri_price_trigger):
                intent = "get_agri_price"
            elif any(scheme_word in command for scheme_word in Config.agri_scheme_trigger):
                intent = "get_agri_scheme"
            elif any(advice_word in command for advice_word in Config.agri_advice_trigger):
                intent = "get_agri_advice"
            
            # Extract entities again with the determined intent
            entities = extract_entities(command)
    
    return intent, score, entities