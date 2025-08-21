import json
import os
import time
import Config
from Voice_tool import bolo

CROP_DATABASE = {}

def load_crop_data(crop_name):
    """
    Loads advisory data for a specific crop from its JSON file.
    Caches the data to avoid reading the file multiple times.
    """
    global CROP_DATABASE
    if crop_name in CROP_DATABASE:
        return CROP_DATABASE[crop_name]

    try:
        file_path = os.path.join('crop_data', f'{crop_name}.json')
        if not os.path.exists(file_path):
            print(f"Error: Data file not found for crop '{crop_name}' at {file_path}")
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            CROP_DATABASE[crop_name] = data
            return data
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading data for {crop_name}: {e}")
        return None

def speak_full_info(crop_name, crop_data, bolo_func):
    """
    Speaks the full crop information section by section to avoid long silences.
    """
    bolo_func(f"ठीक है, मैं आपको {crop_name} के बारे में पूरी जानकारी दे रही हूँ।")
    time.sleep(0.5) # A small pause for natural flow

    # 2. Stream the information section by section.
    for main_key, main_value in crop_data.items():
        bolo_func(f"{main_key}:")
        if isinstance(main_value, dict):
            for sub_key, sub_value in main_value.items():
                if isinstance(sub_value, dict):
                    bolo_func(f"{sub_key} के तहत:")
                    for item_key, item_value in sub_value.items():
                        bolo_func(f"{item_key}: {item_value}")
                        time.sleep(0.3)
                else:
                    bolo_func(f"{sub_key}: {sub_value}")
        else:
            bolo_func(main_value)
        time.sleep(1) 

def get_farming_advisory(crop, stage, bolo_func):
    """
    Provides advisory based on crop and stage. Handles full info requests separately.
    """
    crop_data = load_crop_data(crop)
    if not crop_data:
        bolo_func(f"माफ़ कीजिए, '{crop}' फसल के लिए कोई जानकारी उपलब्ध नहीं है।")
        return

    if not stage or stage == "पूरी जानकारी":
        speak_full_info(crop, crop_data, bolo_func)
        return

    if stage in crop_data:
        stage_info = crop_data[stage]
        response = f"{crop} की {stage} की सलाह: "
        if isinstance(stage_info, dict):
            for key, value in stage_info.items():
                response += f"{key} - {value}. "
        else:
            response += stage_info
        bolo_func(response)
    else:
        # Fallback if a specific stage is asked but not found
        intro = crop_data.get("परिचय", f"'{crop}' के लिए कोई सामान्य जानकारी नहीं मिली।")
        bolo_func(intro)

def handle_advice_query(command, bolo_func):
    """
    Primary function to process a farming advice query.
    """
    all_commodities = Config.agri_commodities + ["मशरूम", "मूंगफली", "उड़द", "मूंग", "चना", "गेहूं", "धान", "आलू", "टमाटर","मिर्च","धान"]
    found_crop = next((c for c in all_commodities if c in command), None)
    
    if not found_crop:
        bolo_func("आप किस फसल के लिए सलाह चाहते हैं?")
        return

    all_stages = Config.agri_stages + ["पूरी जानकारी", "परिचय", "मिट्टी और जलवायु", "उन्नत किस्में", "खेती की प्रक्रिया", "रोग और कीट प्रबंधन", "कटाई और भंडारण", "बाजार और बिक्री"]
    found_stage = next((s for s in all_stages if s in command), None) # Default to None to get all info
    
    get_farming_advisory(found_crop, found_stage, bolo_func)
    
    # Ask a follow-up question
    time.sleep(1) # Pause before asking the next question
    bolo_func("क्या आप किसी और फसल के बारे में जानना चाहेंगे?")
