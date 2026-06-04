from dotenv import load_dotenv
from llm.provider import LLM_PROVIDER

env= load_dotenv()

if env.get("LLM_PROVIDER") == "openai":
    from llm.openai_rca_agent import analyze_incident
else:
    from llm.ollama_rca_agent import analyze_incident