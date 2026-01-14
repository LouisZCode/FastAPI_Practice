from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

task_db = {}

class TaskBody(BaseModel):
    title: str
    description: str
    completed: bool

@router.post("/tasks/")
async def create_task(task: TaskBody):
    new_id = len(task_db) + 1
    task_db[new_id] = {"title": task.title, "description": task.description, "completed": False}
    
    return {"id": new_id, "task": task_db[new_id]}

@router.get("/tasks/{task_id}")
async def get_task(task_id: int):
    if task_id not in task_db:
        raise HTTPException(status_code=404, detail="Task not found")

    return task_db[task_id]

@router.get("/tasks/")
async def list_tasks(completed: bool = None):
    if completed is None:
        return task_db
    
    tasks = []
    for task_id, task in task_db.items():
        if task["completed"] == completed:
            tasks.append(task)
    return tasks

@router.put("/tasks/{task_id}")
async def update_task(task_id : int, data : TaskBody):
    if task_id not in task_db:
        raise HTTPException(status_code=404, detail="No task identified")

    task_db[task_id] = {"title" : data.title, "description" : data.description, "completed" : data.completed}
    return task_db[task_id]


@router.delete("/tasks/{task_id}")
async def delete_task(task_id : int):
    if task_id not in task_db:
        raise HTTPException(status_code=404, detail="No such task in directory")

    deleted_task = task_db.pop(task_id)
    return f"deleted {deleted_task}"