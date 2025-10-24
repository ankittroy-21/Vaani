
from vaani.core.voice_tool import bolo
from vaani.services.agriculture.agri_price_service import handle_price_query
from vaani.services.agriculture.agri_scheme_service import handle_scheme_query
from vaani.services.agriculture.agri_advisory_service import handle_advice_query
from vaani.core import config as Config

def process_agriculture_command(command, bolo_func, entities, context, force_intent=None):
    """
    Processes agricultural commands using simple keyword-based intent detection
    and handling contextual follow-ups.
    """
    
    # --- Step 1: Handle Contextual Responses First ---
    if hasattr(context, 'state') and context.state == 'awaiting_agri_response':
        query_type = context.data.get('query_type', '')
        if 'advice' in query_type:
            handle_advice_query(command, bolo_func, context)
            return True
        elif 'scheme' in query_type or 'subsidy' in query_type:
            handle_scheme_query(command, bolo_func, context)
            return True

    # --- Step 2: Simple Keyword-Based Intent Detection ---
    command_lower = command.lower()
    intent_to_use = force_intent
    
    # If no forced intent, detect based on keywords
    if not intent_to_use:
        if any(keyword in command_lower for keyword in Config.price_keywords):
            intent_to_use = "get_agri_price"
        elif any(keyword in command_lower for keyword in Config.scheme_keywords):
            intent_to_use = "get_agri_scheme"
        elif any(keyword in command_lower for keyword in Config.advice_keywords):
            intent_to_use = "get_agri_advice"
        else:
            # Default to advice for general agriculture queries
            intent_to_use = "get_agri_advice"
    
    print(f"--- Agri Command Router --- Intent: {intent_to_use}")
    
    if intent_to_use == "get_agri_price":
        handle_price_query(command, bolo_func, entities)
    elif intent_to_use == "get_agri_scheme":
        handle_scheme_query(command, bolo_func, context)
    elif intent_to_use == "get_agri_advice":
        handle_advice_query(command, bolo_func, context)
    else:
        # Fallback 
        bolo_func("कृषि संबंधी कुछ और पूछें। मैं भाव, योजना, या सलाह दे सकती हूँ।")

    return True