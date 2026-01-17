#   uvicorn main:app --reload

from routes import router as topics_router

from fastapi import FastAPI
app = FastAPI()
app.include_router(topics_router)

@app.get("/health/")
def health_check():
    return {"status" : "ok"}