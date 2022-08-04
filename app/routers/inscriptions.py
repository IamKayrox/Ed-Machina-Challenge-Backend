from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import InscriptionSchema, InscriptionPatch, InscriptionBase

from ..services import inscriptions as service

router = APIRouter(
    prefix="/inscriptions",
    tags=["Inscriptions"]
)

@router.get("/", response_model=list[InscriptionSchema])
async def get_all_inscriptions(db: Session = Depends(get_db)):
    inscriptions = service.get_all(db)
    return inscriptions

@router.get("/by_lead/{lead_id}", response_model=list[InscriptionSchema])
async def get_all_lead_inscriptions(lead_id: int, db: Session = Depends(get_db)):
    inscriptions = service.get_by_lead_id(db, lead_id)
    return inscriptions

@router.get("/by_subject/{subject_id}", response_model=list[InscriptionSchema])
async def get_all_subscribed_leads(subject_id: int, db: Session = Depends(get_db)):
    inscriptions = service.get_by_subject_id(db, subject_id)
    return inscriptions

@router.post("/", response_model=InscriptionSchema)
async def create_inscription(inscription: InscriptionBase, db: Session = Depends(get_db)):
    existing_inscription = service.get_one(db, inscription.owner_id, inscription.subject_id)
    if existing_inscription:
        raise HTTPException(400, "El lead ya se encuentra inscripto a la materia")
    new_inscription = service.create_one(db, inscription)
    return new_inscription

@router.get("/{lead_id}/{subject_id}", response_model=InscriptionSchema)
async def get_single_inscription(lead_id: int, subject_id: int, db: Session = Depends(get_db)):
    inscription = service.get_one(db, lead_id, subject_id)
    return inscription

@router.patch("/{lead_id}/{subject_id}", response_model=InscriptionSchema)
async def update_inscription(lead_id: int, subject_id: int, data: InscriptionPatch, db: Session = Depends(get_db)):
    inscription = service.get_one(db, lead_id, subject_id)
    new_inscription = service.update_one(db, inscription, data)
    return new_inscription

@router.delete("/{lead_id}/{subject_id}", response_model=str)
async def delete_inscription(lead_id: int, subject_id: int, db: Session = Depends(get_db)):
    service.delete_one(db, lead_id, subject_id)
    return "SUCCESS"