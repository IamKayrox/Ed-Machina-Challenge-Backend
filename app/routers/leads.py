from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas import LeadSchema, LeadBase, LeadPatch
from ..database import get_db
from ..services import leads as service

router = APIRouter(
    prefix="/leads",
    tags=["Leads"]
)

@router.get("/", response_model=list[LeadSchema])
async def get_all_leads(db: Session = Depends(get_db)):
    db_lead = service.get_all(db)
    return db_lead

@router.get("/{lead_id}", response_model=LeadSchema)
async def get_lead(lead_id: int, db: Session = Depends(get_db)):
    db_lead = service.get_one_by_id(db, lead_id)
    return db_lead

@router.post("/", response_model=LeadSchema)
async def create_lead(lead: LeadBase, db: Session = Depends(get_db)):
    existing_lead = service.get_one_by_email(lead.email)
    if existing_lead:
        raise HTTPException(status_code=400, detail="El email ya se encuentra en uso")
    new_lead = service.create_one
    return new_lead

@router.patch("/{lead_id}", response_model=LeadSchema)
async def update_lead(lead_id: int, lead: LeadPatch, db: Session = Depends(get_db)):
    current_lead = service.get_one_by_id(lead_id)
    updated = service.update_one(db, lead, current_lead)
    return updated

@router.delete("/{lead_id}", response_model=str)
async def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    service.delete_one(db, lead_id)
    return 'SUCCESS'