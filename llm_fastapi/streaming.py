# uvicorn streaming:app --reload
from simple_agent import agent
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

app = FastAPI()

class UserMessage(BaseModel):
    message : str = Field(min_length=1)

@app.post("/chat/")
async def call_agent(user_message: UserMessage):

    async def generate():
        async for chunk in agent.astream({"messages": {"role": "user", "content": user_message.message}}, stream_mode="messages"):
            msg, metadata = chunk  # Unpack tuple
            if msg.content:  # Only yield if there's content
                yield msg.content
    
    return StreamingResponse(generate(), media_type="text/plain")