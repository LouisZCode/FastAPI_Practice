from turtle import title
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

#   Launch with    cd exercise_GET_POST   uvicorn random_id:app --reload

app = FastAPI()
task_db = {}

#This is what the User will send us!!
class TaskBody(BaseModel):
    title : str
    description : str
    completed : bool


#this would create a new task whit the elements that the user chooses (limited by BaseModef)
@app.post("/tasks/")
async def create_task(task : TaskBody):

    new_id = len(task_db) + 1
    new_task = {"title" : task.title, "description" : task.description, "completed" : False}
    task_db[new_id] = new_task

    return task

#but what if i want to rédit the or a task?
@app.put("/tasks/{task_id}")
async def update_task(task_id : int, data : TaskBody):
    if task_id not in task_db:
        raise HTTPException(status_code=404, detail="No task identified")
    
    task_db[task_id] = {"title" : data.title, "description" : data.description, "completed" : data.completed}

    return task_db[task_id]


@app.get("/tasks/{task_id}")
async def get_task(task_id : int):
    if task_id not in task_db:
        raise HTTPException(status_code=404, detail="Task not found")

    task = task_db[task_id]
    return task


@app.get("/tasks/")
async def see_all_tasks(completed : bool = None):
    if completed == None:
        return task_db

    tasks = []
    for task_id, task in task_db.items():
        if task["completed"] == completed:
            tasks.append(task)

    return tasks


@app.delete("/tasks/{task_id}")
async def delete_task(task_id : int):
    if task_id not in task_db:
        raise HTTPException(status_code=404, detail="No such task in directory")
    
    deleted_task = task_db.pop(task_id)
    return f"deleted {deleted_task}"
