# lets say this is   users.py

from fastapi import APIRouter

router = APIRouter(prefix="/users")

@router.get("/{id}")
def get_user(id:int):
    return {"user" : id}

"""
# in main.py

from fastapi import FastAPI
from routes import users   <- taking users from "router" folder

app = FastAPI()
app.include_router(users.router)    <- adding it to the app
"""