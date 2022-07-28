from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..models import Subject, Inscription
from ..schemas import SubjectSchema, SubjectBase, SubjectPatch
from ..database import get_db

router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"]
)

@router.get("/", response_model=list[SubjectSchema])
async def get_all_subjects(db: Session = Depends(get_db)):
    subjects = db.query(Subject).all()
    return subjects

@router.post("/", response_model=SubjectSchema)
async def create_subject(new_subject: SubjectBase, db: Session = Depends(get_db)):
    new_subject = Subject(**new_subject.dict())
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject

@router.get("/{subject_id}", response_model=SubjectSchema)
async def get_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).one()
    return subject

@router.patch("/{subject_id}")
async def update_subject(subject_id: int, subject: SubjectPatch, db: Session = Depends(get_db)):
    current_subject = db.query(Subject).filter(Subject.id == subject_id).one()
    update_data = subject.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(current_subject, key, value)
    db.add(current_subject)
    db.commit()
    db.refresh(current_subject)
    return current_subject

@router.delete("/{subject_id}", response_model=str)
async def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    db.query(Subject).filter(Subject.id == subject_id).delete()
    db.query(Inscription).filter(Inscription.subject_id == subject_id).delete()
    db.commit()
    return "SUCCESS"