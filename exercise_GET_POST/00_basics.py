from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Learning POST first:
class BookReview(BaseModel):
    rating : int
    title: str
    review_text : str

@app.post("/reviews/")
async def receive_book_review(review : BookReview):
    #something saved in the reviews
    return {"confirmation" : "Book review submited", "review": review}


#Learning POST second:
task_db = {}

class TasksBody(BaseModel):
    title : str
    description : str
    completed : bool

@app.post("/tasks/")
async def create_task(task : TasksBody):
    #Some save in the DB 
    return {"confirmation":f"Added this task to your task list: {task}"}

@app.get("/tasks/{task_id}")
async def get_task(data : TasksBody, task_id : int):

    id = task_db(id)

    return {"title" : f"{data.title}", "description" : f"{data.description}", "completed" : f"{data.completed}"}

@app.get("/tasks/")
async def list_tasks():
    return {"tasks" : f"{task_db}"}



