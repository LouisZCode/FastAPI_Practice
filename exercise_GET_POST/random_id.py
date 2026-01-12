from ast import Return
from fastapi import FastAPI
from pydantic import BaseModel

#   Launch with    cd exercise_GET_POST   uvicorn random_id:app --reload

app = FastAPI()
task_db = {}

#This is what the User will send us!!
class TaskBody(BaseModel):
    title : str
    description : str
    completed : bool

@app.post("/tasks/")
async def create_task(task : TaskBody):

    new_id = len(task_db) + 1
    new_task = {"title" : task.title, "description" : task.description, "completed" : False}
    task_db[new_id] = new_task

    return task


@app.get("/tasks/{task_id}")
async def get_task(task_id : int):
    if task_id in task_db:
        task = task_db[task_id]
        return task
    else:
        return f"No id: {task_id} in the database"


@app.get("/tasks/")
async def see_all_tasks(completed : bool = None):
    match completed:
        case True:

            completed_tasks = []
            for task_id, task in task_db.items():
                if task["completed"] == True:
                    completed_tasks.append(task)
            return completed_tasks

        case False:

            incompleted_tasks = []
            for task_id, task in task_db.items():
                if task["completed"] == False:
                    incompleted_tasks.append(task)
            return incompleted_tasks

        case None:
            return task_db
    