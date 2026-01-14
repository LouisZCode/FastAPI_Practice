# this one was more an exmaple than a project, moving to the AI_studio_notes   to practice

from fastapi import Depends, HTTPException, APIRouter

router = APIRouter()

task_db = {}

def get_task_or_404(task_id: int):
    if task_id not in task_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_db[task_id]

@router.get("/tasks/{task_id}")
async def get_task(task: dict = Depends(get_task_or_404)):
    return task