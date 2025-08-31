
from Voice_tool import bolo
from agri_price_service import handle_price_query
from agri_scheme_service import handle_scheme_query
from agri_advisory_service import handle_advice_query

def process_agriculture_command(command, bolo_func, entities, context, force_intent=None):
    """
    Processes agricultural commands by trusting the intent passed from the NLU engine
    and handling contextual follow-ups.
    """
    
    # --- Step 1: Handle Contextual Responses First ---
    # If the assistant is waiting for an answer, it should be handled by the relevant service.
    if context.state == 'awaiting_agri_response':
        query_type = context.data.get('query_type', '')
        if 'advice' in query_type:
            handle_advice_query(command, bolo_func, context)
            return True
        elif 'scheme' in query_type or 'subsidy' in query_type:
            handle_scheme_query(command, bolo_func, context)
            return True

    # --- Step 2: Route New Queries Based on the Forced Intent ---
    # For new commands, we rely on the intent determined by the NLU in main.py.
    # We no longer try to re-guess the intent here.
    
    intent_to_use = force_intent
    
    print(f"--- Agri Command Router --- Intent: {intent_to_use}")
    
    if intent_to_use == "get_agri_price":
        handle_price_query(command, bolo_func, entities)
    elif intent_to_use == "get_agri_scheme":
        handle_scheme_query(command, bolo_func, context)
    elif intent_to_use == "get_agri_advice":
        handle_advice_query(command, bolo_func, context)
    else:
        # This is a fallback if a non-agri intent was mistakenly sent here.
        bolo_func("मैं आपकी कृषि संबंधी सहायता नहीं कर सकती। कृपया कुछ और पूछें।")

    return True