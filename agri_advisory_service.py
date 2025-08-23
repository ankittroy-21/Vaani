
import json
import os
import time
import Config
from Voice_tool import bolo

CROP_DATABASE = {}

def load_crop_data(crop_name):
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
    bolo_func(f"ज़रूर, मैं आपको {crop_name} के बारे में पूरी जानकारी देता हूँ।")
    time.sleep(0.5)

    for main_key, main_value in crop_data.items():
        spoken_key = main_key.replace('_', ' ').capitalize()
        bolo_func(f"{spoken_key}:")
        if isinstance(main_value, dict):
            for sub_key, sub_value in main_value.items():
                spoken_sub_key = sub_key.replace('_', ' ').capitalize()
                if isinstance(sub_value, dict):
                    bolo_func(f"{spoken_sub_key} के तहत:")
                    for item_key, item_value in sub_value.items():
                        spoken_item_key = item_key.replace('_', ' ').capitalize()
                        bolo_func(f"{spoken_item_key}: {item_value}")
                        time.sleep(0.3)
                else:
                    bolo_func(f"{spoken_sub_key}: {sub_value}")
        else:
            bolo_func(main_value)
        time.sleep(1)

def get_farming_advisory(crop, stage, bolo_func, context):
    """
    Provides advisory based on crop and stage. Handles full info requests separately.
    """
    crop_data = load_crop_data(crop)
    if not crop_data:
        bolo_func(f"माफ़ कीजिए, '{crop}' फसल के लिए कोई जानकारी उपलब्ध नहीं है।")
        return

    if stage == "पूरी जानकारी":
        speak_full_info(crop, crop_data, bolo_func)
        return

    if not stage:
        available_stages = ", ".join(list(crop_data.keys()))
        bolo_func(f"आप {crop} के बारे में क्या जानना चाहते हैं? आप पूछ सकते हैं: {available_stages}, या पूरी जानकारी।")
        context.set(
            topic='agriculture',
            state='awaiting_agri_response',
            data={'query_type': 'advice_stage', 'crop': crop}
        )
        return

    if stage in crop_data:
        stage_info = crop_data[stage]
        response = f"{crop} के लिए {stage} की जानकारी यहाँ है: "
        if isinstance(stage_info, dict):
            for key, value in stage_info.items():
                response += f"{key.replace('_', ' ').capitalize()} - {value}. "
        else:
            response += stage_info
        bolo_func(response)
    else:
        intro = crop_data.get("परिचय", f"'{crop}' के लिए कोई सामान्य जानकारी नहीं मिली।")
        bolo_func(f"माफ़ कीजिए, मुझे '{stage}' के बारे में जानकारी नहीं मिली, लेकिन यहाँ {crop} का परिचय है: {intro}")

def handle_advice_query(command, bolo_func, context): 
    # Check if this is a contextual reply for a crop name
    if context.state == 'awaiting_agri_response' and context.data.get('query_type') == 'advice_crop':
        found_crop = next((c for c in Config.agri_commodities if c in command), None)
        if found_crop:
            get_farming_advisory(found_crop, None, bolo_func, context)
            return
    
    found_crop = next((c for c in Config.agri_commodities if c in command), None)

    if not found_crop:
        bolo_func("आप किस फसल के लिए सलाह चाहते हैं? कृपया फसल का नाम बताएं।")
        context.set(
            topic='agriculture',
            state='awaiting_agri_response',
            data={'query_type': 'advice_crop'}
        )
        return

    full_info_keywords = ["पूरी जानकारी", "पूरी", "सब कुछ", "बारे में बताओ", "जानकारी दें"]
    if any(keyword in command for keyword in full_info_keywords):
        found_stage = "पूरी जानकारी"
    else:
        found_stage = next((s for s in Config.agri_stages if s in command), None)

    get_farming_advisory(found_crop, found_stage, bolo_func, context)