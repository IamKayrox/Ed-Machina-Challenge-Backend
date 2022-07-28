from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Inscription
from ..schemas import InscriptionSchema, InscriptionPatch, InscriptionBase

router = APIRouter(
    prefix="/inscriptions",
    tags=["Inscriptions"]
)

@router.get("/", response_model=list[InscriptionSchema])
async def get_all_inscriptions(db: Session = Depends(get_db)):
    inscriptions = db.query(Inscription).all()
    return inscriptions

@router.get("/by_lead/{lead_id}", response_model=list[InscriptionSchema])
async def get_all_lead_inscriptions(lead_id: int, db: Session = Depends(get_db)):
    inscriptions = db.query(Inscription).filter(Inscription.owner_id == lead_id).all()
    return inscriptions

@router.get("/by_subject/{subject_id}", response_model=list[InscriptionSchema])
async def get_all_subscribed_leads(subject_id: int, db: Session = Depends(get_db)):
    inscriptions = db.query(Inscription).filter(Inscription.subject_id == subject_id).all()
    return inscriptions

@router.post("/", response_model=InscriptionSchema)
async def create_inscription(inscription: InscriptionBase, db: Session = Depends(get_db)):
    existing_inscription = db.query(Inscription).filter(Inscription.owner_id == inscription.owner_id, Inscription.subject_id == inscription.subject_id).one_or_none()
    if existing_inscription:
        raise HTTPException(400, "El lead ya se encuentra inscripto a la materia")
    new_inscription = Inscription(**inscription.dict())
    db.add(new_inscription)
    db.commit()
    db.refresh(new_inscription)
    return new_inscription

@router.get("/{lead_id}/{subject_id}", response_model=InscriptionSchema)
async def get_single_inscription(lead_id: int, subject_id: int, db: Session = Depends(get_db)):
    inscription = db.query(Inscription).filter(Inscription.owner_id == lead_id, Inscription.subject_id == subject_id).one()
    return inscription

@router.patch("/{lead_id}/{subject_id}", response_model=InscriptionSchema)
async def update_inscription(lead_id: int, subject_id: int, inscription: InscriptionPatch, db: Session = Depends(get_db)):
    inscription = db.query(Inscription).filter(Inscription.owner_id == lead_id, Inscription.subject_id == subject_id).one()
    update_data = inscription.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(inscription, key, value)
    db.add(inscription)
    db.commit()
    db.refresh(inscription)
    return inscription

@router.delete("/{lead_id}/{subject_id}", response_model=str)
async def delete_inscription(lead_id: int, subject_id: int, db: Session = Depends(get_db)):
    db.query(Inscription).filter(Inscription.owner_id == lead_id, Inscription.subject_id == subject_id).delete()
    db.commit()
    return "SUCCESS"