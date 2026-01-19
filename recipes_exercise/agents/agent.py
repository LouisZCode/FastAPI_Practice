from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

recipe_agent = create_agent(
    model="xai:grok-3-mini",
    system_prompt="You will receive a recipe from the user, your only task is to improve the recipe you received. The improvement will be just one sentence, and you will give it back with no preambles"
)