from fastapi import FastAPI
from pydantic import BaseModel, Field
from simple_agent import agent

app = FastAPI()

class UserMessage(BaseModel):
    message : str = Field(min_length=1)

@app.post("/chat/")
async def call_agent(user_message : UserMessage):
    answer = await agent.ainvoke({"messages" :{"role" : "user", "content" : user_message.message }})

    ai_message = answer["messages"][-1].content

    return {"response" : ai_message}


# uvicorn async_await:app --reload