from fastapi import Depends, HTTPException, Security, APIRouter
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from typing import Literal


router = APIRouter()

api_header = APIKeyHeader(name="X-API-KEY")
recipes_db = {}

valid_api_keys = {
    "api_key_123" : "junior_dev_01",
    "api_key_456" : "senior_dev_02"
    }

class RecipeBody(BaseModel):
    name : str
    cuisine : Literal["mexican", "italian", "japanese"]
    ingredients : list = Field(min_length=3)
    instructions : str

def validate_api_key(api_key : str = Security(api_header)):
    if api_key not in valid_api_keys:
        raise HTTPException(status_code=401, detail="Not a valid API Key")
    else:
        return api_key

def validate_recipe_id(recipe_id : int):
    if recipe_id not in recipes_db:
        raise  HTTPException(status_code=404, detail=f"No such recipe with id {recipe_id} in database")
    else:
        return recipes_db[recipe_id]

@router.post("/recipes/")
async def create_recipe(recipe : RecipeBody, api_key : str = Depends(validate_api_key)):
    recipe_id = len(recipes_db) +1
    recipes_db[recipe_id] = {"name" : recipe.name, "cuisine" : recipe.cuisine, "ingredients" : recipe.ingredients, "instructions" : recipe.instructions}
    return recipes_db[recipe_id]

@router.get("/recipes/")
async def get_all_recipes(cuisine : str = None,  api_key : str = Depends(validate_api_key)):
    if cuisine == None:
        return recipes_db
    
    else:
        filtered_recipes = []
        for id, recipe in recipes_db.items():
            if recipe["cuisine"] == cuisine:
                filtered_recipes.append(recipe)
        
        return filtered_recipes


@router.get("/recipes/{recipe_id}")
async def get_one_recipe(recipe : dict = Depends(validate_recipe_id),  api_key : str = Depends(validate_api_key)):
    return recipe

@router.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id : int, recipe : dict = Depends(validate_recipe_id),  api_key : str = Depends(validate_api_key)):
    return {"deleted_recipe" : recipes_db.pop(recipe_id)}

