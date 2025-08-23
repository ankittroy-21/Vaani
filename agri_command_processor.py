import Config
from Voice_tool import bolo

from agri_price_service import handle_price_query
from agri_scheme_service import handle_scheme_query
from agri_advisory_service import handle_advice_query

def process_agriculture_command(command, bolo_func):
    """
    Analyzes the command and returns a specific status:
    "HANDLED", "SCHEME_NOT_FOUND", or "NOT_HANDLED".
    """
    command = command.lower()

    if any(word in command for word in Config.agri_advice_trigger):
        handle_advice_query(command, bolo_func)
        return "HANDLED"

    if any(word in command for word in Config.agri_price_trigger):
        handle_price_query(command, bolo_func)
        return "HANDLED"

    if any(word in command for word in Config.agri_scheme_trigger):
        return handle_scheme_query(command, bolo_func)

    return "NOT_HANDLED"