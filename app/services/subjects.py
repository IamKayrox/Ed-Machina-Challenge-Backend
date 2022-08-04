from sqlalchemy.orm import Session

from ..models import Subject
from ..schemas import SubjectBase, SubjectPatch

from . import inscriptions as inscriptions_service

def get_all(db: Session):
    return db.query(Subject).all()

def get_one_by_id(db: Session, id: int):
    return db.query(Subject).filter(Subject.id == id).one()

def create_one(db: Session, subject: SubjectBase):
    new_subject = Subject(**subject.dict())
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject

def update_one(db: Session, new_subject: SubjectPatch, current_subject: Subject):
    update_data = new_subject.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(current_subject, key, value)
    db.add(current_subject)
    db.commit()
    db.refresh(current_subject)
    return current_subject

def delete_one(db: Session, id: int):
    db.query(Subject).filter(Subject.id == id).delete()
    db.commit()
    inscriptions_service.delete_all_by_subject(db, id)
