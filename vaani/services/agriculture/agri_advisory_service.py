"""
Agricultural Advisory Service Module
Provides farming guidance and crop-specific information.
"""

import json
import os
import time
import logging
from typing import Optional, Dict, Any

from vaani.core import config as Config
from vaani.core.voice_tool import bolo

# Setup logging
logger = logging.getLogger(__name__)

# In-memory cache for crop data
CROP_DATABASE: Dict[str, Dict[str, Any]] = {}


def load_crop_data(crop_name: str) -> Optional[Dict[str, Any]]:
    """
    Load crop data from JSON file with caching.
    
    Args:
        crop_name: Name of the crop in Hindi
        
    Returns:
        Dictionary containing crop information or None if not found
    """
    global CROP_DATABASE
    
    # Return from cache if available
    if crop_name in CROP_DATABASE:
        logger.info(f"Using cached data for {crop_name}")
        return CROP_DATABASE[crop_name]

    try:
        file_path = os.path.join('data', 'crop_data', f'{crop_name}.json')
        
        if not os.path.exists(file_path):
            logger.error(f"Data file not found for crop '{crop_name}' at {file_path}")
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            CROP_DATABASE[crop_name] = data
            logger.info(f"Loaded data for {crop_name}")
            return data
            
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error for {crop_name}: {str(e)}")
        return None
    except FileNotFoundError as e:
        logger.error(f"File not found for {crop_name}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error loading data for {crop_name}: {str(e)}")
        return None



def speak_full_info(crop_name: str, crop_data: Dict[str, Any], bolo_func) -> None:
    """
    Speaks the full crop information section by section in a structured manner.
    
    Args:
        crop_name: Name of the crop
        crop_data: Dictionary containing crop information
        bolo_func: Function to speak the response
    """
    bolo_func(f"ज़रूर, मैं आपको {crop_name} के बारे में पूरी जानकारी देती हूँ।")
    time.sleep(0.4)

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
                    time.sleep(0.3)
        else:
            bolo_func(str(main_value))
            
        time.sleep(0.8)


def get_farming_advisory(
    crop: str, 
    stage: Optional[str], 
    bolo_func, 
    context
) -> None:
    """
    Provides farming advisory based on crop and stage with contextual handling.
    
    Args:
        crop: Name of the crop in Hindi
        stage: Farming stage or topic (e.g., बुवाई, सिंचाई)
        bolo_func: Function to speak the response
        context: Context object for managing conversation state
    """
    crop_data = load_crop_data(crop)
    
    if not crop_data:
        response = f"माफ़ कीजिए, '{crop}' फसल के लिए कोई जानकारी उपलब्ध नहीं है। क्या आप किसी अन्य फसल के बारे में जानना चाहेंगे?"
        bolo_func(response)
        logger.warning(f"No data available for crop: {crop}")
        return

    # Handle full information request
    if stage == "पूरी जानकारी":
        speak_full_info(crop, crop_data, bolo_func)
        return

    # If no stage specified, list available options
    if not stage:
        available_stages = ", ".join(list(crop_data.keys())[:5])  # Limit to 5 to avoid long list
        response = f"आप {crop} के बारे में क्या जानना चाहते हैं? आप पूछ सकते हैं: {available_stages}, या पूरी जानकारी।"
        bolo_func(response)
        
        # Set context for follow-up
        context.set(
            topic='agriculture',
            state='awaiting_agri_response',
            data={'query_type': 'advice_stage', 'crop': crop}
        )
        return

    # Provide specific stage information
    if stage in crop_data:
        stage_info = crop_data[stage]
        response = f"{crop} के लिए {stage} की जानकारी: "
        
        if isinstance(stage_info, dict):
            bolo_func(response)
            time.sleep(0.3)
            
            for key, value in stage_info.items():
                formatted_key = key.replace('_', ' ').capitalize()
                bolo_func(f"{formatted_key}: {value}")
                time.sleep(0.4)
        else:
            response += str(stage_info)
            bolo_func(response)
            
        logger.info(f"Provided {stage} info for {crop}")
    else:
        # Stage not found, provide introduction as fallback
        intro = crop_data.get("परिचय", f"'{crop}' के लिए कोई सामान्य जानकारी नहीं मिली।")
        response = f"माफ़ कीजिए, मुझे '{stage}' के बारे में विशेष जानकारी नहीं मिली। लेकिन यहाँ {crop} का परिचय है: {intro}"
        bolo_func(response)
        logger.warning(f"Stage '{stage}' not found for crop '{crop}'")


def handle_advice_query(command: str, bolo_func, context) -> None:
    """
    Main handler for agricultural advice queries with context management.
    
    Args:
        command: User's command in Hindi
        bolo_func: Function to speak the response
        context: Context object for managing conversation state
    """
    # Check if this is a contextual reply for a crop name
    if (context.state == 'awaiting_agri_response' and 
        context.data.get('query_type') == 'advice_crop'):
        found_crop = next((c for c in Config.agri_commodities if c in command), None)
        if found_crop:
            get_farming_advisory(found_crop, None, bolo_func, context)
            return
    
    # Extract crop from command
    found_crop = next((c for c in Config.agri_commodities if c in command), None)

    if not found_crop:
        response = (
            "आप किस फसल के लिए सलाह चाहते हैं? "
            "कृपया फसल का नाम बताएं। जैसे: गेहूं, धान, आलू, टमाटर।"
        )
        bolo_func(response)
        
        # Set context to handle the user's next response
        context.set(
            topic='agriculture',
            state='awaiting_agri_response',
            data={'query_type': 'advice_crop'}
        )
        return

    # Check if user wants full information
    full_info_keywords = [
        "पूरी जानकारी", "पूरी", "सब कुछ", "बारे में बताओ", 
        "जानकारी दें", "सब बताओ", "विस्तार से"
    ]
    
    if any(keyword in command for keyword in full_info_keywords):
        found_stage = "पूरी जानकारी"
    else:
        # Try to extract stage from command
        found_stage = next((s for s in Config.agri_stages if s in command), None)

    get_farming_advisory(found_crop, found_stage, bolo_func, context)
    logger.info(f"Handled advice query for crop: {found_crop}, stage: {found_stage}")