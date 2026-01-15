#   uvicorn main:app --reload

import time
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from routes.notes import router as notes_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change later to the 
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.middleware("http")
async def log_request(request : Request, call_next):
    start = time.time()

    response = await call_next(request)

    duration = time.time() - start
    print(f"{request.method} {request.url.path} - {duration:.2f}s")
    print(f"  IP: {request.client.host}")
    print(f"  Device: {request.headers.get('user-agent', 'Unknown')}")

    return response