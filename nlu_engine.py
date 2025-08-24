# nlu_engine.py (Enhanced Version)

from sentence_transformers import SentenceTransformer, util
import torch
import Config
import re
from rapidfuzz import process as fuzzprocess # <<< NEW: Import for fuzzy matching

print("Loading NLU model... This may take a moment.")
# --- ENHANCEMENT: You can optionally switch to a model fine-tuned on Indian languages ---
# To use, uncomment the line below and comment out the original 'distiluse' model.
# model = SentenceTransformer('ai4bharat/indic-sentence-transformer')
model = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v1')
print("NLU model loaded successfully.")

# --- ENHANCEMENT: INTENT_EXAMPLES now include ultra-short, colloquial queries ---
INTENT_EXAMPLES = {
    "get_agri_price": [
        "आलू का भाव क्या है", "मंडी में गेहूं का दाम बताओ", "प्याज की कीमत पता करो", "टमाटर का क्या रेट है",
        "आज का भाव", "कितने का आलू बिक रहा है", "गेहूं की कीमत क्या है", "मूंगफली का दाम", "लखनऊ में आलू का भाव",
        "दिल्ली मंडी में टमाटर की कीमत", "उत्तर प्रदेश में गेहूं का दाम", "क्या भाव है चावल का", "कीमत बताओ धान की",
        # Ultra-short and direct queries
        "भाव", "कीमत", "दाम", "रेट", "प्याज भाव", "आलू कीमत", "टमाटर"
    ],
    "get_agri_scheme": [
        "किसानों के लिए कौन सी योजना है", "सब्सिडी के बारे में बताओ", "मुझे लोन चाहिए", "सरकारी मदद कैसे मिलेगी",
        "बीमा योजना की जानकारी दो", "गेहूं की खेती के लिए सब्सिडी", "धान के लिए सरकारी योजना", "किसान कर्ज योजना",
        "फसल बीमा के बारे में बताओ", "आर्थिक सहायता कैसे मिलेगी", "सरकारी सहायता योजना", "कृषि ऋण कहाँ से मिलेगा",
        "ड्रोन योजना के बारे में जानकारी दो", "ट्रैक्टर पर सब्सिडी", "मशीनरी खरीदने की योजना",
        # Ultra-short and direct queries
        "योजना", "सब्सिडी", "लोन", "कर्ज", "ऋण", "बीमा", "ड्रोन", "ट्रैक्टर"
    ],
    "get_agri_advice": [
        "गेहूं की बुवाई कैसे करें", "फसल में बीमारी लग गयी", "खाद के बारे में सलाह दो", "सिंचाई कब करनी है",
        "आलू की खेती कैसे करें", "धान की रोग रोकथाम", "टमाटर की उन्नत किस्में", "मिट्टी और जलवायु की जानकारी",
        "कटाई का सही समय", "भंडारण कैसे करें", "कीट प्रबंधन के उपाय", "खेती की प्रक्रिया बताओ", "फसल की पूरी जानकारी दो",
        # Ultra-short and direct queries
        "खेती", "बुवाई", "सिंचाई", "कटाई", "खाद", "बीमारी", "कीट", "रोकथाम", "गेहूं की जानकारी"
    ],
    "get_news_detail": [
        "पहली खबर के बारे में विस्तार से बताओ", "तीसरी खबर सुनाओ", "उसके बारे में और बताओ", "नंबर दो वाली खबर",
        "दूसरी खबर की जानकारी दो"
    ],
    "get_weather": [
        "आज मौसम कैसा है", "तापमान बताओ", "क्या कल बारिश होगी", "बाहर निकलना ठीक रहेगा क्या?", "लखनऊ का मौसम",
        "दिल्ली में तापमान क्या है", "मुंबई में बारिश होगी क्या", "हवा की गति", "नमी कितनी है", "मौसम की पूरी जानकारी दो",
        # Ultra-short and direct queries
        "मौसम", "तापमान", "हवा", "नमी", "गर्मी", "सर्दी", "बारिश", "धूप"
    ],
    "get_time": [
        "समय बताओ", "अभी टाइम क्या है", "कितने बजे हैं", "वक्त बताओ", "टाइम क्या हुआ", "घड़ी में क्या बजा है",
        # Ultra-short and direct queries
        "समय", "टाइम", "कितना बजा"
    ],
    "get_news": [
        "आज की खबरें सुनाओ", "खबर सुनाओ", "समाचार बताओ", "मुख्य समाचार क्या हैं", "ताज़ा न्यूज़ बताओ",
        "हेडलाइंस क्या हैं", "देश में क्या चल रहा है", "आज की सुर्खियाँ",
        # Ultra-short and direct queries
        "खबर", "समाचार", "न्यूज़", "हेडलाइंस"
    ],
    "get_wikipedia": [
        "विकिपीडिया पर खोजो", "भारत के बारे में बताओ", "विकिपीडिया से जानकारी दो", "इंटरनेट पर खोजो",
        "जानकारी ढूंढो", "विकिपीडिया पर पता करो"
    ],
    "get_historical_date": [
        "इस दिन इतिहास में क्या हुआ था", "आज के दिन क्या खास है", "तारीख के बारे में बताओ",
        "आज का इतिहास क्या है"
    ],
    "greet": [
        "नमस्ते", "हेलो", "क्या हाल है", "और बताओ", "नमस्कार", "प्रणाम", "राम राम"
    ],
    "goodbye": [
       "प्रोग्राम बंद करो", "अब बंद कर दो", "अलविदा", "बाहर निकलो", "एग्जिट करो", "चुप हो जाओ", "सिस्टम बंद करो", "टाटा"
    ],
    "get_social_schemes": [
        "मेरे लिए कौन सी सरकारी योजना है", "मैं किस योजना के लिए पात्र हूँ", "सरकारी सहायता के बारे में बताओ",
        "पेंशन योजना के बारे में जानकारी दो", "मनरेगा के बारे में बताओ", "वृद्धावस्था पेंशन कैसे मिलेगी"
    ]
}

# Pre-compute embeddings for faster performance
intent_embeddings = {intent: model.encode(examples, convert_to_tensor=True) for intent, examples in INTENT_EXAMPLES.items()}

def recognize_intent_semantic(command):
    """Recognizes intent using semantic similarity (Sentence Transformer)."""
    if not command:
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
    
    return best_intent, best_score

def fuzzy_intent_fallback(command, intents_dict, threshold=75):
    """
    NEW: A fallback mechanism using fuzzy string matching for low-confidence queries.
    This acts as a safety net for misheard words or very short commands.
    """
    all_examples = []
    example_to_intent_map = {}
    for intent, examples in intents_dict.items():
        all_examples.extend(examples)
        for example in examples:
            example_to_intent_map[example] = intent

    best_match, score, _ = fuzzprocess.extractOne(command, all_examples)
    
    if score >= threshold:
        matched_intent = example_to_intent_map[best_match]
        return matched_intent, score / 100.0  # Normalize score to 0-1 range
    
    return "unknown", 0.0

def extract_entities(command):
    """Extracts key entities from the command using Config.py lists and aliases."""
    # This function remains largely the same as your original, as it's effective.
    entities = {}
    scheme_keywords = {
        "ड्रोन": "यंत्रीकरण", "यंत्रीकरण": "यंत्रीकरण", "मशीनीकरण": "यंत्रीकरण",
        "ट्रैक्टर": "यंत्रीकरण", "मशीन": "यंत्रीकरण"
    }
    for keyword, entity_value in scheme_keywords.items():
        if keyword in command:
            entities['scheme_type'] = entity_value
            break
    for crop in Config.agri_commodities:
        if crop in command:
            entities['crop'] = crop; break
    for market in Config.agri_markets:
        if market in command:
            entities['market'] = market; break
    for state in Config.agri_states:
        if state in command:
            entities['state'] = state; break
    for alias, canonical_name in Config.ENTITY_ALIASES.items():
        if alias in command:
            if canonical_name in Config.agri_commodities:
                entities['crop'] = canonical_name
            elif canonical_name in Config.agri_markets:
                entities['market'] = canonical_name
            elif canonical_name in Config.agri_states:
                entities['state'] = canonical_name
    if any(trigger in command for trigger in Config.agri_advice_trigger):
        for stage in Config.agri_stages:
            if stage in command:
                entities['stage'] = stage; break
    return entities

# In nlu_engine.py

def process_nlu(command):
    """
    A single function to get both intent and entities, now with a rule-based override.
    """
    # 1. Get the initial intent and entities
    intent, score = recognize_intent_semantic(command)
    entities = extract_entities(command)
    
    # <<< START: NEW RULE-BASED OVERRIDE LOGIC >>>
    # If the model confidently thinks it's weather BUT we found a crop, it's wrong.
    # Override the intent to 'get_agri_price'.
    if intent == "get_weather" and 'crop' in entities:
        print(f"--- RULE OVERRIDE: Corrected intent from 'get_weather' to 'get_agri_price' based on found crop: '{entities['crop']}' ---")
        intent = "get_agri_price"
    # <<< END: NEW RULE-BASED OVERRIDE LOGIC >>>

    CONFIDENCE_THRESHOLD = 0.60
    if intent.startswith("get_agri_"):
        CONFIDENCE_THRESHOLD = 0.55

    # 2. If semantic score is too low, try the fuzzy fallback as a safety net
    if score < CONFIDENCE_THRESHOLD:
        print(f"--- Semantic score low ({score:.2f}). Trying fuzzy fallback... ---")
        fuzzy_intent, fuzzy_score = fuzzy_intent_fallback(command, INTENT_EXAMPLES)
        if fuzzy_intent != "unknown":
            print(f"--- Fuzzy fallback succeeded! Intent: {fuzzy_intent} (Score: {fuzzy_score:.2f}) ---")
            intent = fuzzy_intent
            score = fuzzy_score # Use the fuzzy score
    
    # 3. Re-extract entities if intent was changed by fuzzy fallback
    if not entities:
        entities = extract_entities(command)

    return intent, score, entities