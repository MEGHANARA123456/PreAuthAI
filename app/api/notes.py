from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.pa_generator import generate_pa_form

router = APIRouter()

class NoteRequest(BaseModel):
    note: str

@router.post("/analyze")
def analyze_notes(req: NoteRequest):
    if not req.note.strip():
        raise HTTPException(status_code=400, detail="Note is empty")
    return generate_pa_form(req.note)