import os
from dotenv import load_dotenv

load_dotenv()

# --- Model Settings ---
EMBEDDING_MODEL = "gemini-embedding-001"
CHAT_MODEL = "gemini-2.5-flash-lite" # High speed for Agents
DIMENSIONS = 768

# --- API Keys ---
GEMINI_API_KEY1 = "AIzaSyD_WSFHm6HdELjgKZ9ebyVlM2K7Sayk2E0"
GEMINI_API_KEY2 = "AIzaSyD8RmN3EIokfKpUP57Or9o9YHeE6-QInks"
GEMINI_API_KEY3 = "AIzaSyAcQygZrcHFOou_hk8FDRq8wcZ2Byc2VEY"
GEMINI_API_KEY4 = "AIzaSyAYBZtfj5YzBDD2S-7-rY862OCHUas3LDo"

# Create the rotation list (Filters out any None values if a key is missing)
GEMINI_API_KEYS = [
    key for key in [GEMINI_API_KEY1, GEMINI_API_KEY2, GEMINI_API_KEY3, GEMINI_API_KEY4] 
    if key
]


GEMINI_API_KEY = GEMINI_API_KEYS[0] if GEMINI_API_KEYS else None
PINECONE_API_KEY = "pcsk_6j1U1u_T4CFtoT3c6mBDHMtsEuUTmoEwJt5ox4LDYRxWK6P42LUoM32LHjRNUjG88teNhw"
PINECONE_INDEX = "data"

# Weather Tool
WEATHER_API_KEY = "0ca3a2820ab59bf6f9632e7a0b154f44"