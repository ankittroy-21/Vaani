from sentence_transformers import SentenceTransformer, util
import torch
import Config
import re
from rapidfuzz import process as fuzzprocess
import nltk 
from pos_tagger import get_pos_tags 

print("Loading NLU model... This may take a moment.")
model = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v1')
print("NLU model loaded successfully.")

INTENT_EXAMPLES = {
    "get_agri_price": [
        "आलू का भाव क्या है", "मंडी में गेहूं का दाम बताओ", "प्याज की कीमत पता करो", "टमाटर का क्या रेट है",
        "आज का भाव", "कितने का आलू बिक रहा है", "गेहूं की कीमत क्या है", "मूंगफली का दाम", "लखनऊ में आलू का भाव",
        "दिल्ली मंडी में टमाटर की कीमत", "उत्तर प्रदेश में गेहूं का दाम", "क्या भाव है चावल का", "कीमत बताओ धान की",
        "भाव", "कीमत", "दाम", "रेट", "प्याज भाव", "आलू कीमत", "टमाटर"
    ],
    "get_agri_scheme": [
        "किसानों के लिए कौन सी योजना है", "सब्सिडी के बारे में बताओ", "मुझे लोन चाहिए", "सरकारी मदद कैसे मिलेगी",
        "बीमा योजना की जानकारी दो", "गेहूं की खेती के लिए सब्सिडी", "धान के लिए सरकारी योजना", "किसान कर्ज योजना",
        "फसल बीमा के बारे में बताओ", "आर्थिक सहायता कैसे मिलेगी", "सरकारी सहायता योजना", "कृषि ऋण कहाँ से मिलेगा",
        "ड्रोन योजना के बारे में जानकारी दो", "ट्रैक्टर पर सब्सिडी", "मशीनरी खरीदने की योजना",
        "योजना", "सब्सिडी", "लोन", "कर्ज", "ऋण", "बीमा", "ड्रोन", "ट्रैक्टर"
    ],
    "get_agri_advice": [
        "गेहूं की बुवाई कैसे करें", "फसल में बीमारी लग गयी", "खाद के बारे में सलाह दो", "सिंचाई कब करनी है",
        "आलू की खेती कैसे करें", "धान की रोग रोकथाम", "टमाटर की उन्नत किस्में", "मिट्टी और जलवायु की जानकारी",
        "कटाई का सही समय", "भंडारण कैसे करें", "कीट प्रबंधन के उपाय", "खेती की प्रक्रिया बताओ", "फसल की पूरी जानकारी दो",
        "खेती", "बुवाई", "सिंचाई", "कटाई", "खाद", "बीमारी", "कीट", "रोकथाम", "गेहूं की जानकारी"
    ],
    "get_news_detail": [
        "पहली खबर के बारे में विस्तार से बताओ", "तीसरी खबर सुनाओ", "उसके बारे में और बताओ", "नंबर दो वाली खबर",
        "दूसरी खबर की जानकारी दो"
    ],
    "get_weather": [
        "आज मौसम कैसा है", "तापमान बताओ", "क्या कल बारिश होगी", "बाहर निकलना ठीक रहेगा क्या?", "लखनऊ का मौसम",
        "दिल्ली में तापमान क्या है", "मुंबई में बारिश होगी क्या", "हवा की गति", "नमी कितनी है", "मौसम की पूरी जानकारी दो",
        "मौसम", "तापमान", "हवा", "नमी", "गर्मी", "सर्दी", "बारिश", "धूप"
    ],
    "get_time": [
        "समय बताओ", "अभी टाइम क्या है", "कितने बजे हैं", "वक्त बताओ", "टाइम क्या हुआ", "घड़ी में क्या बजा है",
        "समय", "टाइम", "कितना बजा"
    ],
    "get_news": [
        "आज की खबरें सुनाओ", "खबर सुनाओ", "समाचार बताओ", "मुख्य समाचार क्या हैं", "ताज़ा न्यूज़ बताओ",
        "हेडलाइंस क्या हैं", "देश में क्या चल रहा है", "आज की सुर्खियाँ",
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
    A fallback mechanism using fuzzy string matching for low-confidence queries.
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

# --- Start of Updated Block ---

def extract_noun_phrases(command):
    """
    First, tokenizes the command, then uses our POS tagger and a chunk grammar
    to extract meaningful noun phrases (potential entities).
    """
    tokens = nltk.word_tokenize(command)
    pos_tags = get_pos_tags(tokens)

    # Define a chunk grammar: NP (Noun Phrase)
    # This rule says an NP can be an optional Determiner ('the', 'a'), followed by
    # any number of Adjectives, and then one or more Nouns.
    grammar = "NP: {<DT>?<JJ.*>*<NN.*>+}"
    
    cp = nltk.RegexpParser(grammar)
    tree = cp.parse(pos_tags)
    
    noun_phrases = []
    for subtree in tree.subtrees():
        if subtree.label() == 'NP':
            # Join the words of the chunk back into a single string
            np_text = " ".join(word for word, tag in subtree.leaves())
            noun_phrases.append(np_text)
            
    return noun_phrases


def map_entities(noun_phrases):
    """
    Takes the extracted noun phrases and maps them to the known entities
    from the Config file. Now also recognizes general agri terms.
    """
    entities = {}
    
    # First, check for specific commodities, markets, and states
    for phrase in noun_phrases:
        for crop in Config.agri_commodities:
            if crop in phrase:
                entities['crop'] = crop; break
        for market in Config.agri_markets:
            if market in phrase:
                entities['market'] = market; break
        for state in Config.agri_states:
            if state in phrase:
                entities['state'] = state; break
    
    # If no specific crop was found, check for a general agriculture topic
    if 'crop' not in entities:
        for phrase in noun_phrases:
            for term in Config.agri_general_terms:
                if term in phrase:
                    # Mark that a general agriculture topic was found
                    entities['topic'] = 'agriculture'
                    # Store the specific term found, e.g., 'फसल'
                    entities['term'] = term
                    break
            if 'topic' in entities:
                break
                
    return entities

def process_nlu(command):
    """
    A single function to get both intent and entities, now with the most robust override rules.
    """
    intent, score = recognize_intent_semantic(command)
    noun_phrases = extract_noun_phrases(command)
    entities = map_entities(noun_phrases)
    
    # --- Start of Final Rule-Based Override Logic ---
    
    # Rule 1: Corrects if a crop-related query is wrongly identified as weather.
    if intent == "get_weather" and 'crop' in entities:
        print(f"--- RULE OVERRIDE: Corrected intent from 'get_weather' to 'get_agri_price' ---")
        intent = "get_agri_price"
        
    # Rule 2: Corrects if a price query is wrongly identified as a social scheme.
    price_keywords = ['भाव', 'कीमत', 'दाम', 'रेट']
    if intent == "get_social_schemes" and 'crop' in entities and any(keyword in command for keyword in price_keywords):
        print(f"--- RULE OVERRIDE: Corrected intent from '{intent}' to 'get_agri_price' ---")
        intent = "get_agri_price"

    # Rule 3: Corrects intent if a general agri term is found but the intent is wrong.
    if entities.get('topic') == 'agriculture' and not intent.startswith('get_agri_'):
        print(f"--- RULE OVERRIDE: Corrected intent from '{intent}' to 'get_agri_advice' based on general term '{entities.get('term')}' ---")
        intent = "get_agri_advice"

    # Rule 4 (NEW & MOST IMPORTANT): If a command asks for information about a crop,
    # it must be an advice query, not a price query.
    advice_keywords = ['जानकारी', 'बारे में', 'कैसे करें', 'क्या करें', 'सलाह']
    if 'crop' in entities and any(keyword in command for keyword in advice_keywords):
        if intent != 'get_agri_advice':
            print(f"--- RULE OVERRIDE: Corrected intent from '{intent}' to 'get_agri_advice' based on advice keywords. ---")
            intent = "get_agri_advice"

    # --- End of Final Rule-Based Override Logic ---

    CONFIDENCE_THRESHOLD = 0.60
    if intent.startswith("get_agri_"):
        CONFIDENCE_THRESHOLD = 0.55

    # Fuzzy fallback for low-confidence scores
    if score < CONFIDENCE_THRESHOLD:
        fuzzy_intent, fuzzy_score = fuzzy_intent_fallback(command, INTENT_EXAMPLES)
        if fuzzy_intent != "unknown":
            intent = fuzzy_intent
            score = fuzzy_score

    # Re-extract entities if none were found
    if not entities:
        noun_phrases = extract_noun_phrases(command)
        entities = map_entities(noun_phrases)

    return intent, score, entities