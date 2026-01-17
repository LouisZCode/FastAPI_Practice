from fastapi import APIRouter
from pydantic import BaseModel

topics_db = {}

router = APIRouter()

class TopicBody(BaseModel):
    name : str
    category : str

@router.post("/topics/")
def create_topic(topic : TopicBody):
    topic_id = len(topics_db) + 1
    topic_content = {"name" : topic.name, "category" : topic.category}
    topics_db[topic_id] = topic_content
    return topics_db[topic_id]