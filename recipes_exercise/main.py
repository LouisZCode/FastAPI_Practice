#   uvicorn main:app --reload

from fastapi import FastAPI
from routes import router as recipes_router

app = FastAPI()
app.include_router(recipes_router)

@app.get("/health/")
async def check_health():
    return {"status" : "ok"}

