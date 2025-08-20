import Config
from Voice_tool import bolo

from agri_price_service import handle_price_query
from agri_scheme_service import handle_scheme_query
from agri_advisory_service import handle_advice_query

def process_agriculture_command(command, bolo_func):
    """
    Analyzes the user's command and routes it to the correct handler.
    Returns True if an agriculture command was handled, otherwise False.
    """
    command = command.lower()

    if any(word in command for word in Config.agri_advice_trigger):
        handle_advice_query(command, bolo_func)
        return True

    # Route to Market Price handler
    if any(word in command for word in Config.agri_price_trigger):
        handle_price_query(command, bolo_func)
        return True

    # Route to Government Scheme handler
    if any(word in command for word in Config.agri_scheme_trigger):
        handle_scheme_query(command, bolo_func)
        return True

    # If no specific agriculture command was detected
    return False
