from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

#uvicorn put_delete:app --reload

app = FastAPI()

notes_db = {}

class  NoteBody(BaseModel):
    title: str = Field(min_length=1, max_length=1000)
    content : str
    category : Literal["work", "fitness", "love"]

@app.post("/notes/")
async def create_note( data : NoteBody):
    note_id = len(notes_db) +1
    notes_db[note_id] = {"title" : data.title, "content" : data.content, "category" : data.category}
    return notes_db[note_id]


@app.get("/notes/")
async def get_all_notes(category : str = None):
    if category == None:
        return notes_db

    selected_notes = []
    for note_id , note in notes_db.items():
        if note["category"] == category:
            selected_notes.append(note)
    
    return selected_notes


@app.get("/notes/{note_id}")
async def get_note(note_id : int):
    if note_id not in notes_db:
        raise HTTPException(status_code=404, detail=f"No note with id: {note_id}")
    
    return notes_db[note_id]

@app.put("/notes/{note_id}")
async def edit_note(note_id : int, data : NoteBody):
    if note_id not in notes_db:
        raise HTTPException(status_code=404, detail=f"No note with id: {note_id}")
    
    notes_db[note_id] = {"title" : data.title, "content" : data.content, "category" : data.category}
    return notes_db[note_id]


@app.delete("/notes/{note_id}")
async def delete_note(note_id : int):
    if note_id not in notes_db:
        raise HTTPException(status_code=404, detail=f"No note with id: {note_id}")
    
    deleted_note = notes_db.pop(note_id)
    return deleted_note

