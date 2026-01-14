#  uvicorn main:app --reload

from fastapi import FastAPI
# If there are more You import each one. It's explicit:
from routes.tasks import router as task_router

app = FastAPI()
# Same here, if there are more, you add each one. 
app.include_router(task_router)