import Config
from Voice_tool import bolo

# Import the handlers that this processor will route commands to
from agri_price_service import handle_price_query
from agri_scheme_service import handle_scheme_query
from agri_advisory_service import handle_advice_query

def process_agriculture_command(command, bolo_func, entities, context, force_intent=None):

    command = command.lower()
    intent_to_use = force_intent
    
    # 1. Determine the final intent if it's not already forced by the context manager
    if not intent_to_use:
        # High-priority keywords for schemes (rule-based override)
        drone_keywords = ["ड्रोन", "यंत्रीकरण", "मशीनीकरण", "ट्रैक्टर", "मशीन"]
        if any(keyword in command for keyword in drone_keywords) or any(word in command for word in Config.agri_scheme_trigger):
            intent_to_use = "get_agri_scheme"
        # Check for price triggers
        elif any(word in command for word in Config.agri_price_trigger):
            intent_to_use = "get_agri_price"
        # Check for advice triggers
        elif any(word in command for word in Config.agri_advice_trigger):
            intent_to_use = "get_agri_advice"
        else:
            # Fallback for general agriculture keywords that were not classified
            agriculture_keywords = Config.agri_commodities + ["खेती", "फसल", "किसान", "बीज", "खाद", "सिंचाई"]
            if any(keyword in command for keyword in agriculture_keywords):
                # If no other trigger is found, default to providing advice
                intent_to_use = "get_agri_advice"
            else:
                bolo_func("मैं आपका कृषि संबंधी प्रश्न समझ नहीं पायी। कृपया दोबारा पूछें।")
                return True # Command was agricultural but unhandled

    # 2. Route to the correct handler based on the determined intent
    print(f"--- Agri Command Router --- Intent: {intent_to_use}")
    
    if intent_to_use == "get_agri_price":
        handle_price_query(command, bolo_func, entities)
    elif intent_to_use == "get_agri_scheme":
        # Pass the context object so the handler can set it for follow-up questions
        handle_scheme_query(command, bolo_func, context)
    elif intent_to_use == "get_agri_advice":
        # Pass the context object here as well
        handle_advice_query(command, bolo_func, context)
    else:
        # This case handles if a command was passed here but no intent could be determined
        bolo_func("मैं आपकी कृषि संबंधी सहायता नहीं कर सकती। कृपया कुछ और पूछें।")

    return True # Return True as an agriculture command was processed