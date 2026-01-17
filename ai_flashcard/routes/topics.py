from fastapi import APIRouter, HTTPException, Depends
from langchain_core.tools import retriever
from pydantic import BaseModel, Field
from typing import Literal

topics_db = {}

router = APIRouter()

def exist_or_404(topic_id : int):
    try:
        return topics_db[topic_id]
    except:
        raise HTTPException(status_code=404, detail="not such topic in the database")

class TopicBody(BaseModel):
    name : str = Field(min_length=2, max_length=20)
    category : str

@router.post("/topics/")
async def create_topic(topic : TopicBody):
    topic_id = len(topics_db) + 1
    topic_content = {"name" : topic.name, "category" : topic.category}
    topics_db[topic_id] = topic_content
    return topics_db[topic_id]

@router.get("/topics/")
async def list_topics(category : str = None):
    if category is None:
        return topics_db

    filtered_topics = []
    for id, topic in topics_db.items():
        if category == topic["category"]:
            filtered_topics.append(topic)

    return filtered_topics
    
@router.get("/topics/{topic_id}")
async def get_topic(topic : dict = Depends(exist_or_404)):
    return topic

@router.delete("/topic/{topic_id}")
async def delete_topic(topic_id : int , topic : dict = Depends(exist_or_404)):
    return {"deleted" : topics_db.pop(topic_id)}
