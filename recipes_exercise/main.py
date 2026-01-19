#   uvicorn main:app --reload

from fastapi import FastAPI, Request
from routes import router as recipes_router
import time

app = FastAPI()
app.include_router(recipes_router)

@app.get("/health/")
async def check_health():
    return {"status" : "ok"}

@app.middleware("/http/")
async def log_info(request : Request, call_next):
    start = time.time()

    response = await call_next(request)

    duration = time.time() - start
    print(f"{request.method}, {request.url.path} - {duration:.2f}s")
    return response