from langchain_core.messages import HumanMessage, AIMessage, trim_messages
from .config import CHAT_MODEL

# 1. THE CONTEXT TRIMMER (Your "Past 3" Rule)
# This logic ensures that no matter how long the chat goes, 
# the AI only "sees" the most recent relevant context.
trimmer = trim_messages(
    max_tokens=6,             # 3 User + 3 AI turns = 6 messages
    strategy="last",          # Always keep the most recent
    token_counter=len,        # Simple message count for your STAYSIDDH prototype
    start_on="human",         # Always start the context with a User question
    include_system=True       # Always keep the "You are Boost AI" instructions
)

class ChatMemory:
    def __init__(self):
        # In a real Django app, you would store this in Redis or a Database.
        # For our build, we will start with an in-memory list.
        self.history = []

    def add_user_message(self, text):
        self.history.append(HumanMessage(content=text))

    def add_ai_message(self, text):
        self.history.append(AIMessage(content=text))

    def get_active_context(self):
        """Returns the trimmed history based on your 3-turn rule."""
        return trimmer.invoke(self.history)

    def clear(self):
        self.history = []