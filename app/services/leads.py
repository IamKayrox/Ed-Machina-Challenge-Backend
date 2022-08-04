from sqlalchemy.orm import Session

from ..models import Lead, Inscription
from ..schemas import LeadBase, LeadPatch
from . import inscriptions as inscription_service

def get_all(db: Session):
    return db.query(Lead).all()

def get_one_by_id(db: Session, id: int):
    return db.query(Lead).filter(Lead.id == id).one()

def get_one_by_email(db: Session, email: str):
    return db.query(Lead).filter(Lead.email == email).one()

def create_one(db: Session, lead: LeadBase):
    new_lead = Lead(**lead.dict())
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return new_lead

def update_one(db: Session, lead: LeadPatch, current_lead: Lead):
    update_data = lead.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(current_lead, key, value)
    db.add(current_lead)
    db.commit()
    db.refresh(current_lead)
    return current_lead

def delete_one(db: Session, id: int):
    db.query(Lead).filter(Lead.id == id).delete()
    db.commit()
    inscription_service.delete_all_by_lead(db, id)