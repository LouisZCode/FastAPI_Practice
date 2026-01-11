from fastapi import FastAPI
from pydantic import BaseModel

#try with      uvicorn main:app --reload
# then open   http://127.0.0.1:8000/    and the app will be there

# Create the FastAPI app (your "building")
app = FastAPI()

# Create your first endpoint (your first "door")
@app.get("/")
def greet_user(name:str):
	return {"message" : f"hello from Fastapi!"}


class GermanText(BaseModel):
    text : str
    user_level : str

@app.post("/feedback")
def get_ai_feedback(data : GermanText):

    feedback = f"Analizing: '{data.text}' for {data.user_level} level"

    return {
        "original_text": data.text,
        "level": data.user_level,
        "feedback": feedback
    }

# fast api also creates automatic documents:   http://127.0.0.1:8000/docs