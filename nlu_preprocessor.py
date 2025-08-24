import re

# Dictionary to map common colloquialisms, slang, and synonyms to a standard term
REGIONAL_SYNONYMS = {
    # Price/Rate related
    r'\bभाव\b': 'कीमत',
    r'\bरेट\b': 'कीमत',
    r'\bदाम\b': 'कीमत',
    r'\bbhav\b': 'कीमत',
    r'\bdaam\b': 'कीमत',
    
    # Time related
    r'\bटाइम\b': 'समय',
    r'\btime\b': 'समय',
    r'\bटेम\b': 'समय',
    r'\bवक्त\b': 'समय',
    
    # Weather related
    r'\bबरखा\b': 'बारिश',
    r'\bबरसात\b': 'बारिश',
    r'\bbarish\b': 'बारिश',
    
    # News related
    r'\bसमाचार\b': 'खबर',
    r'\bन्यूज़\b': 'खबर',
    r'\bnews\b': 'खबर',
    
    # Agriculture related
    r'\bधान\b': 'चावल',
    r'\bगेहूँ\b': 'गेहूं', # <<< Spelling corrected here
    r'\bgehu\b': 'गेहूं',
    r'\baloo\b': 'आलू',
    r'\bpyaz\b': 'प्याज'
}

# Common fillers to remove from the start or end of a command
FILLERS_TO_REMOVE = [
    "जरा", "तो", "ना", "ज़रा", "एक बार", "प्लीज", "please", 
    "मुझे", "मेरा", "मेरी", "मेरे", "मैं", "तुम", "आप",
    "बताओ", "बता", "बताइए", "बताएं", "बोलो", "कहो",
    "दो", "देना", "दीजिए", "जानकारी", "चाहिए",
    "अरे", "सुनो", "हे", "ओके", "ok", "अच्छा"
]

def normalize_query(command: str) -> str:
    """
    Cleans and standardizes a user's spoken command.
    """
    if not command:
        return ""
        
    cmd = command.strip().lower()

    # 1. Replace synonyms and colloquialisms
    for pattern, canonical in REGIONAL_SYNONYMS.items():
        cmd = re.sub(pattern, canonical, cmd, flags=re.IGNORECASE)

    # 2. Remove filler words from the start and end for cleaner processing
    for filler in FILLERS_TO_REMOVE:
        # Match filler words at the beginning or end of the string
        cmd = re.sub(r'^\s*' + re.escape(filler) + r'\b\s*', '', cmd, flags=re.IGNORECASE)
        cmd = re.sub(r'\s*\b' + re.escape(filler) + r'\s*$', '', cmd, flags=re.IGNORECASE)
    
    # 3. Collapse repeated words (e.g., "समय बताओ समय बताओ" -> "समय बताओ")
    cmd = re.sub(r'\b(\w+)\s+\1\b', r'\1', cmd)
    
    # 4. Strip any leftover whitespace
    return cmd.strip()