from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()


flash_agent = create_agent(
    model="xai:grok-3-mini",
    system_prompt="you are an expert flashcard creator. You are going to get context from the user, and the only thing you need to give back is a flashcard in this structure:'[{question: a question, answer: the answer}]'. That is it. No preambles"
)