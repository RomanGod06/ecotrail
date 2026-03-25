import logging
from pinecone import Pinecone
from google import genai
from google.genai import types
from ..config import GEMINI_API_KEY, PINECONE_API_KEY, PINECONE_INDEX, EMBEDDING_MODEL, DIMENSIONS

# Set up logging for the terminal demo
logger = logging.getLogger(__name__)

def search_eco_rules(query: str) -> str:
    """
    Searches Pinecone for trail safety guidelines, emergency contacts, 
    and environmental rules (EcoTrail PWA).
    """
    try:
        logger.info(f"🌲 [VECTOR AGENT] Searching knowledge base for: '{query}'")
        
        # 1. Initialize INSIDE the function to prevent Django startup crashes!
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index(PINECONE_INDEX)
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)

        # 2. Embed the user's question
        embed_response = gemini_client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=query,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_QUERY",
                output_dimensionality=DIMENSIONS
            )
        )
        query_vector = embed_response.embeddings[0].values

        # 3. Query Pinecone (Top 2 matches for speed and token limit)
        results = index.query(
            vector=query_vector,
            top_k=2, 
            include_metadata=True
        )

        # 4. Format the result for the Agent
        if not results.matches:
            logger.warning("⚠️ [VECTOR AGENT] No matches found in Pinecone.")
            return "No specific trail guidelines or emergency contacts found for this query."

        # Filter out low-confidence matches (score > 0.60)
        valid_matches = [m.metadata.get('text', '') for m in results.matches if m.score > 0.60]
        
        if not valid_matches:
            logger.warning("⚠️ [VECTOR AGENT] Matches found, but confidence score was too low (< 0.60).")
            return "No high-confidence matches found in the EcoTrail database."

        # 5. The "Anchor" prefix for the LLM
        context = "\n".join(valid_matches)
        logger.info("✅ [VECTOR AGENT] Successfully retrieved knowledge base context.")
        return f"KNOWLEDGE_BASE_REPORT:\n{context}"

    except Exception as e:
        logger.error(f"🔥 [VECTOR AGENT ERROR] {str(e)}")
        return "The trail knowledge base is temporarily offline."