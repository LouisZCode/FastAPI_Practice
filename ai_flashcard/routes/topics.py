from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from agents import flash_agent

topics_db = {}
flash_card_db = {}

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
    id = len(topics_db) +1
    new_topic = {"name" : topic.name, "category" : topic.category}
    topics_db[id] = new_topic 
    return new_topic

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

@router.delete("/topics/{topic_id}")
async def delete_topic(topic_id : int , topic : dict = Depends(exist_or_404)):
    return {"deleted" : topics_db.pop(topic_id)}


@router.post("/topics/{topic_id}/generate")
async def generate_flashcard(topic_id : int, topic : dict =  Depends(exist_or_404)):

    context = topics_db[topic_id]
    answer = await flash_agent.ainvoke({"messages" : {"role" : "user" , "content" : f"this is the context for the flashcard : {context}"}})
    flash_card = answer["messages"][-1].content

    if topic_id not in flash_card_db:
        flash_card_db[topic_id] = [flash_card]
    else:
        flash_card_db[topic_id].append(flash_card)

    return {"new_flashcard" : flash_card} 

@router.get("/topics/{topic_id}/flashcards")
async def fetch_flashcards(topic_id : int, topic : dict = Depends(exist_or_404)):
    if topic_id not in flash_card_db:
        return [] 
    return flash_card_db[topic_id]
