from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#  uvicorn simple_agent:app --reload

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent

agent = create_agent(
    model="xai:grok-3-mini",
    system_prompt="Please review the German Text and Translate and give feedback of it back in English. Keep the answer in one sentence."
)

class GermanFeedback(BaseModel):
    text : str

@app.post("/feedback")
async def german_ai_feedback(data: GermanFeedback):
    result = await agent.ainvoke({"messages" :
    {"role" : "user", "content" : f"{data.text}" }
    })
    return result["messages"][-1]