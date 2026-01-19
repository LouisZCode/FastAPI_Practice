#   uvicorn main:app --reload

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal


app = FastAPI()

recipes_db = {}

class RecipeBody(BaseModel):
    name : str
    cuisine : Literal("mexican", "italian", "japanese")
    ingredients : list = Field(min_length=3)
    instruction : str

@app.post("/recipes/")
async def create_recipe(recipe : RecipeBody):
    recipe_id = len(recipes_db) +1
    