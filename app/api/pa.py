from fastapi import APIRouter, HTTPException, Depends
from app.auth.deps import get_current_user   # <-- Add this import
from datetime import datetime, timezone
from typing import Optional
import io
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

from app.storage.memory_store import save_pa, update_pa, get_pa
from app.services.pdf_service import generate_pdf


router = APIRouter(prefix="/api/pa", tags=["Prior Authorization"])

# ------- Models --------
class PAForm(BaseModel):
    diagnosis: str
    procedure: str
    medical_necessity: str

class ApprovalRequest(BaseModel):
    reviewer: str
    decision: str  # APPROVED / REJECTED
    comments: Optional[str] = None


# ================= PROTECTED ROUTES ================= #

@router.post("/save")
def save_pa_form(data: PAForm, user=Depends(get_current_user)):   # <-- Auth added
    pa_data = data.dict()
    pa_data.update({
        "status": "DRAFT",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "created_by": user["sub"]                       # Track who created it
    })
    pa_id = save_pa(pa_data)
    return {"pa_id": pa_id, "status": "DRAFT"}


@router.put("/{pa_id}")
def update_pa_form(pa_id: str, data: PAForm, user=Depends(get_current_user)):   # <-- Auth added
    pa = get_pa(pa_id)
    if not pa:
        raise HTTPException(404, "PA not found")

    if pa.get("status") == "APPROVED":
        raise HTTPException(400, "Approved PA cannot be edited")

    update_pa(pa_id, data.dict())
    return {"status": "updated"}


@router.get("/{pa_id}")
def fetch(pa_id: str, user=Depends(get_current_user)):   # <-- Auth added
    pa = get_pa(pa_id)
    if not pa:
        raise HTTPException(404, "Not found")
    return pa


@router.post("/{pa_id}/approve")
def approve(pa_id: str, approval: ApprovalRequest, user=Depends(get_current_user)):  # <-- Auth added
    pa = get_pa(pa_id)
    if not pa:
        raise HTTPException(404, "Not found")

    update_pa(pa_id, {
        "status": approval.decision,
        "reviewer": approval.reviewer,
        "comments": approval.comments,
        "reviewed_at": datetime.now(timezone.utc).isoformat()
    })
    return {"pa_id": pa_id, "status": approval.decision}


@router.get("/{pa_id}/download")
def download(pa_id: str, user=Depends(get_current_user)):  # <-- Auth added
    pa = get_pa(pa_id)
    if not pa:
        raise HTTPException(404, "Not found")
    if pa.get("status") != "APPROVED":
        raise HTTPException(403, "PA not approved yet")

    pdf = generate_pdf(pa)
    return StreamingResponse(io.BytesIO(pdf),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=PA_Form.pdf"})
