#   uvicorn main:app --reload

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Literal


app = FastAPI()

recipes_db = {}

class RecipeBody(BaseModel):
    name : str
    cuisine : Literal["mexican", "italian", "japanese"]
    ingredients : list = Field(min_length=3)
    instructions : str

def validate_recipe_id(recipe_id : int):
    if recipe_id not in recipes_db:
        raise  HTTPException(status_code=404, detail=f"No such recipe with id {recipe_id} in database")
    else:
        return recipes_db[recipe_id]

@app.post("/recipes/")
async def create_recipe(recipe : RecipeBody):
    recipe_id = len(recipes_db) +1
    recipes_db[recipe_id] = {"name" : recipe.name, "cuisine" : recipe.cuisine, "ingredients" : recipe.ingredients, "instructions" : recipe.instructions}
    return recipes_db[recipe_id]

@app.get("/recipes/")
async def get_all_recipes(cuisine : str = None):
    if cuisine == None:
        return recipes_db
    
    else:
        filtered_recipes = []
        for id, recipe in recipes_db.items():
            if recipe["cuisine"] == cuisine:
                filtered_recipes.append(recipe)
        
        return filtered_recipes


@app.get("/recipes/{recipe_id}")
async def get_one_recipe(recipe : dict = Depends(validate_recipe_id)):
    return recipe
