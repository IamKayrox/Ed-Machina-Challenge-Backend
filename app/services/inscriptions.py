from sqlalchemy.orm import Session

from ..models import Inscription
from ..schemas import InscriptionSchema, InscriptionPatch, InscriptionBase

def get_all(db: Session):
    return db.query(Inscription).all()

def get_by_lead_id(db: Session, lead_id: int):
    return db.query(Inscription).filter(Inscription.owner_id == lead_id).all()

def get_by_subject_id(db: Session, subject_id):
    return  db.query(Inscription).filter(Inscription.subject_id == subject_id).all()

def get_one(db: Session, lead_id: int, subject_id: int):
    return  db.query(Inscription).filter(Inscription.owner_id == lead_id, Inscription.subject_id == subject_id).one()

def create_one(db: Session, inscription: InscriptionBase):
    new_inscription = Inscription(**inscription.dict())
    db.add(new_inscription)
    db.commit()
    db.refresh(new_inscription)
    return new_inscription

def update_one(db: Session, old_inscription: Inscription, new_inscription: InscriptionPatch):
    update_data = new_inscription.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(old_inscription, key, value)
    db.add(old_inscription)
    db.commit()
    db.refresh(old_inscription)
    return old_inscription

def delete_all_by_lead(db: Session, lead_id: int):
    db.query(Inscription).filter(Inscription.owner_id == lead_id).delete()
    db.commit()

def delete_all_by_subject(db: Session, subject_id: int):
    db.query(Inscription).filter(Inscription.subject_id == subject_id).delete()
    db.commit()

def delete_one(db: Session, lead_id: int, subject_id: int):
    db.query(Inscription).filter(Inscription.owner_id == lead_id, Inscription.subject_id == subject_id).delete()
    db.commit()