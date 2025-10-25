
"""
Agricultural Command Processor Module
Main entry point for routing agricultural queries to appropriate services.
"""

import logging
from typing import Optional

from vaani.core.voice_tool import bolo
from vaani.services.agriculture.agri_price_service import handle_price_query
from vaani.services.agriculture.agri_scheme_service import handle_scheme_query
from vaani.services.agriculture.agri_advisory_service import handle_advice_query
from vaani.core import config as Config

# Setup logging
logger = logging.getLogger(__name__)


def process_agriculture_command(
    command: str,
    bolo_func,
    entities: dict,
    context,
    force_intent: Optional[str] = None
) -> bool:
    """
    Main router for agricultural commands using keyword-based intent detection.
    
    This function analyzes the user's command and routes it to the appropriate
    agricultural service (price, scheme, or advisory).
    
    Args:
        command: User's command in Hindi
        bolo_func: Function to speak the response
        entities: Dictionary of extracted entities (crop, market, etc.)
        context: Context object for managing conversation state
        force_intent: Optional forced intent to override detection
        
    Returns:
        bool: True if command was processed successfully
    """
    # --- Step 1: Handle Contextual Responses First ---
    if hasattr(context, 'state') and context.state == 'awaiting_agri_response':
        query_type = context.data.get('query_type', '')
        
        logger.info(f"Processing contextual response for query_type: {query_type}")
        
        if 'advice' in query_type:
            handle_advice_query(command, bolo_func, context)
            return True
        elif 'scheme' in query_type or 'subsidy' in query_type:
            handle_scheme_query(command, bolo_func, context)
            return True

    # --- Step 2: Keyword-Based Intent Detection ---
    command_lower = command.lower()
    intent_to_use = force_intent
    
    # If no forced intent, detect based on keywords
    if not intent_to_use:
        # Priority order: price > scheme > advice (most specific to most general)
        if any(keyword in command_lower for keyword in Config.price_keywords):
            intent_to_use = "get_agri_price"
        elif any(keyword in command_lower for keyword in Config.scheme_keywords):
            intent_to_use = "get_agri_scheme"
        elif any(keyword in command_lower for keyword in Config.advice_keywords):
            intent_to_use = "get_agri_advice"
        else:
            # Check if any crop is mentioned - default to advice
            found_crop = next((c for c in Config.agri_commodities if c in command), None)
            if found_crop:
                intent_to_use = "get_agri_advice"
            else:
                intent_to_use = "get_agri_advice"  # Default fallback
    
    logger.info(f"Agriculture Command Router - Intent: {intent_to_use}, Command: {command[:50]}...")
    
    # --- Step 3: Route to Appropriate Service ---
    try:
        if intent_to_use == "get_agri_price":
            handle_price_query(command, bolo_func, entities)
        elif intent_to_use == "get_agri_scheme":
            handle_scheme_query(command, bolo_func, context)
        elif intent_to_use == "get_agri_advice":
            handle_advice_query(command, bolo_func, context)
        else:
            # Fallback for unknown intent
            bolo_func(
                "कृषि संबंधी कुछ और पूछें। मैं भाव, योजना, या खेती की सलाह दे सकती हूँ।"
            )
            logger.warning(f"Unknown intent: {intent_to_use}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error processing agriculture command: {str(e)}")
        bolo_func("माफ़ कीजिए, आपके प्रश्न को प्रोसेस करने में कुछ समस्या आई। कृपया पुनः प्रयास करें।")
        return False