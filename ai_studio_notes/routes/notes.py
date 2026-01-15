from fastapi import  Depends, HTTPException, APIRouter, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Literal
from bg_tasks import save_to_log

from agents import grok_agent

notes_db = {}

router = APIRouter()

def note_or_404(note_id : int):
    if note_id not in notes_db:
        raise HTTPException(status_code=404, detail="No note with htis id exists")
    return notes_db[note_id]


class NoteBody(BaseModel):
    title : str = Field(min_length=1, max_length=1000)
    content : str
    subject : Literal["math", "history", "science"]

@router.post("/notes/")
async def create_note(note : NoteBody):
    id = len(notes_db) +1
    new_note = {"title" : note.title, "content": note.content, "subject" : note.subject}
    notes_db[id] = new_note

    return {"new_note" : new_note}

@router.get("/notes/")
async def read_all_notes(subject : str = None):
    if subject is None:
        return notes_db
    
    filtered = []
    for id , note in notes_db.items():
        if note["subject"] == subject:
            filtered.append(note)
    
    return filtered


@router.get("/notes/{note_id}")
async def get_note_by_id(note : dict = Depends(note_or_404)):
    return note


@router.put("/notes/{note_id}")
async def edit_note(note_id : int, data : NoteBody, note : dict = Depends(note_or_404)):
    notes_db[note_id] = {"title" : data.title, "content": data.content, "subject" : data.subject}
    return notes_db[note_id]


@router.delete("/notes/{note_id}")
async def delete_note(note_id : int, note : dict = Depends(note_or_404)):
    return {"deleted" : notes_db.pop(note_id)}

@router.post("/notes/{note_id}/analize")
async def ai_input(note_id: int, background_tasks: BackgroundTasks, note: dict = Depends(note_or_404)):
    answer = await grok_agent.ainvoke(
        {"messages": {"role": "user", "content": f"Make a 1 sentence analizys of this note {note}"}})
    
    answer_text = answer["messages"][-1].content  # Extract string first
    
    background_tasks.add_task(save_to_log, note_id, "analyze request", answer_text)

    return answer_text