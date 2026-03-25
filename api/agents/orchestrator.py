import logging
from google import genai
from google.genai import types

# Import configurations and memory
from .config import GEMINI_API_KEYS, CHAT_MODEL
from .memory import ChatMemory

# Import the specialized tools
from .tools.api_agents import get_weather_and_aqi
from .tools.sql_agent import check_room_availability
from .tools.vector_agents import search_eco_rules

logger = logging.getLogger(__name__)

# Your routing instructions
SYSTEM_INSTRUCTION = """
You are an intelligent routing layer for a multi-agent RAG system. 
Analyze the user's query and invoke ONLY the specific agent(s) required to answer it. 

---
## AGENTS AVAILABLE
1. **AQI_AGENT / WEATHER_AGENT** -> Trigger `get_weather_and_aqi`
   - Handles: Air quality, pollution, temperature, rain, wind, forecasts.
   - You MUST estimate the latitude and longitude of the location.

2. **CROWD_AGENT** -> Trigger `check_room_availability`
   - Handles: Crowd density, hotel booking load, tourist footfall, occupancy.

3. **CHUNK_AGENT / ALERT_AGENT** -> Trigger `search_eco_rules`
   - Handles: General knowledge, trail guidelines, safety warnings, advisories.
   - Use as fallback for eco/trail questions ONLY.

---
## ROUTING RULES
1. **GREETINGS / SMALL TALK:** If the user says a simple greeting (e.g., "hello", "hi", "hlo"), respond politely and ask how you can help them with their EcoTrail trip. DO NOT invoke any agents.
2. **Specific Query:** Single Agent.
3. **Vague/General Query:** Relevant Multi-Agent (e.g., "How is Shimla?" -> Run AQI + CROWD + WEATHER).
4. **Planning / Trip Intent:** All Agents + Decision Layer. Synthesize all outputs into a GO / AVOID / CAUTION recommendation.

## STRICT CONSTRAINTS
- NEVER invoke an agent whose domain is unrelated.
- If a query is ambiguous, ask ONE clarifying question before routing.
- Return structured, readable output using sections per agent when multiple are invoked.
"""

class MasterOrchestrator:
    def __init__(self):
        # Initialize the GenAI Client
        self.client = genai.Client(api_key=GEMINI_API_KEYS[0])
        self.memory = ChatMemory()
        
        # Map your conceptual agents to the actual Python functions
        self.tools = [
            get_weather_and_aqi,     
            check_room_availability, 
            search_eco_rules         
        ]

    def _get_formatted_history(self):
        """Bridges LangChain memory trimmer with Google GenAI Content types."""
        formatted_history = []
        past_context = self.memory.get_active_context()
        
        for msg in past_context:
            role = "user" if msg.type == "human" else "model"
            formatted_history.append(
                types.Content(role=role, parts=[types.Part.from_text(text=msg.content)])
            )
        return formatted_history

    def process_query(self, user_message: str) -> str:
        """The main entry point for the Django view."""
        logger.info(f"🧠 [ORCHESTRATOR] Processing query: {user_message}")
        
        try:
            # 1. Initialize the Chat Session with trimmed history and tools
            chat_session = self.client.chats.create(
                model=CHAT_MODEL,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    tools=self.tools,
                    temperature=0.1, # Low temperature forces stricter routing adherence
                ),
                history=self._get_formatted_history()
            )
            
            # 2. Send the message. 
            # The SDK will automatically execute the Python tools if the model decides to route to them!
            response = chat_session.send_message(user_message)
            final_text = response.text
            
            # 3. Update the LangChain memory tracker for the next turn
            self.memory.add_user_message(user_message)
            self.memory.add_ai_message(final_text)
            
            return final_text
            
        except Exception as e:
            logger.error(f"🔥 [ORCHESTRATOR ERROR] {str(e)}")
            return "System Error: The EcoTrail orchestrator encountered an issue processing your request."

# Instantiate a singleton to be imported by your Django views
agent_brain = MasterOrchestrator()