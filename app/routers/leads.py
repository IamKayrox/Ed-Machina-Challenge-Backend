from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import Lead, Inscription
from ..schemas import LeadSchema, LeadBase, LeadPatch
from ..database import get_db

router = APIRouter(
    prefix="/leads",
    tags=["Leads"]
)

@router.get("/", response_model=list[LeadSchema])
async def get_all_leads(db: Session = Depends(get_db)):
    db_lead = db.query(Lead).all()
    return db_lead

@router.post("/", response_model=LeadSchema)
async def create_lead(lead: LeadBase, db: Session = Depends(get_db)):
    existing_lead = db.query(Lead).filter(Lead.email == lead.email).one_or_none()
    if existing_lead:
        raise HTTPException(status_code=400, detail="El email ya se encuentra en uso")
    new_lead = Lead(**lead.dict())
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return new_lead

@router.get("/{lead_id}", response_model=LeadSchema)
async def get_lead(lead_id: str, db: Session = Depends(get_db)):
    db_lead = db.query(Lead).filter(Lead.id == lead_id).one()
    return db_lead

@router.patch("/{lead_id}", response_model=LeadSchema)
async def update_lead(lead: LeadPatch, db: Session = Depends(get_db)):
    current_lead = db.query(Lead).filter(Lead.id == lead.id).one()
    update_data = lead.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(current_lead, key, value)
    db.add(current_lead)
    db.commit()
    db.refresh(current_lead)
    return current_lead

@router.delete("/{lead_id}", response_model=str)
async def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    db.query(Lead).filter(Lead.id == lead_id).delete()
    db.query(Inscription).filter(Inscription.owner_id == lead_id).delete()
    db.commit()
    return 'SUCCESS'