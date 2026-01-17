from fastapi import APIRouter
from langchain_core.tools import retriever
from pydantic import BaseModel, Field
from typing import Literal

topics_db = {}

router = APIRouter()

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
    
