from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

grok_agent = create_agent(
    model="xai:grok-3-mini",
)
