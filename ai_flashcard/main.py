#   uvicorn main:app --reload

from routes import router as topics_router
from fastapi import FastAPI, Request
import time
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
    )

app.include_router(topics_router)

@app.middleware("http")
async def log(request : Request, call_next):
    start = time.time()

    response = await call_next(request)

    duration = time.time() - start
    print(f"{request.method} {request.url.path}  - {duration:.2f}s")

    return response


@app.get("/health/")
def health_check():
    return {"status" : "ok"}