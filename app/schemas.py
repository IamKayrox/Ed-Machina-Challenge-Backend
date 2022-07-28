from pydantic import BaseModel
from datetime import date

class SubjectBase(BaseModel):
    name: str

class SubjectPatch(SubjectBase):
    name: str | None

class SubjectSchema(SubjectBase):
    id: int

    class Config:
        orm_mode = True

class InscriptionBase(BaseModel):
    owner_id: int
    subject_id: int
    duration: float
    carerr: str
    date: date
    attemps: int

class InscriptionPatch(InscriptionBase):
    owner_id: None
    subject_id: None
    duration: float | None
    carerr: str | None
    date: date | None
    attemps: int | None

class InscriptionSchema(InscriptionBase):
    subject: SubjectSchema | None

    class Config:
        orm_mode = True

class LeadBase(BaseModel):
    email: str
    firstname: str
    lastname: str
    address: str
    phone: str

class LeadPatch(LeadBase):
    email: None
    firstname: str | None
    lastname: str | None
    address: str | None
    phone: str | None

class LeadSchema(LeadBase):
    id: int
    inscriptions: list[InscriptionSchema] | None

    class Config:
        orm_mode = True