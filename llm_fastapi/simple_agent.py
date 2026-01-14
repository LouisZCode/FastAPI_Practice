from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

agent = create_agent(
    model="xai:grok-3-mini",
)

