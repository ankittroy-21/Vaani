# context_manager.py

class Context:
    """A simple class to manage conversational context."""
    def __init__(self):
        self.current_topic = None
        self.data = {}  # To store things like news articles or scheme details
        self.state = None  
        
    def set(self, topic, state, data=None):
        """Sets the current context."""
        print(f"CONTEXT SET: Topic='{topic}', State='{state}'")
        self.current_topic = topic
        self.state = state
        self.data = data if data is not None else {}

    def clear(self):
        """Clears the context to end the current conversational flow."""
        print("CONTEXT CLEARED")
        self.current_topic = None
        self.data = {}
        self.state = None