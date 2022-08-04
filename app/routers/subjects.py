from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas import SubjectSchema, SubjectBase, SubjectPatch
from ..database import get_db

from ..services import subjects as service

router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"]
)

@router.get("/", response_model=list[SubjectSchema])
async def get_all_subjects(db: Session = Depends(get_db)):
    subjects = service.get_all(db)
    return subjects

@router.post("/", response_model=SubjectSchema)
async def create_subject(new_subject: SubjectBase, db: Session = Depends(get_db)):
    new_subject = service.create_one(db, new_subject)
    return new_subject

@router.get("/{subject_id}", response_model=SubjectSchema)
async def get_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = service.get_one_by_id(db, subject_id)
    return subject

@router.patch("/{subject_id}")
async def update_subject(subject_id: int, subject: SubjectPatch, db: Session = Depends(get_db)):
    current_subject = service.get_one_by_id(db, subject_id)
    updated_subject = service.update_one(db, subject, current_subject)
    return updated_subject

@router.delete("/{subject_id}", response_model=str)
async def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    service.delete_one(db, subject_id)
    return "SUCCESS"