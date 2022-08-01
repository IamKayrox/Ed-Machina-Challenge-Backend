from sqlalchemy import Column, Date, Float, ForeignKey, Integer, Interval, String, Table
from sqlalchemy.orm import relationship

from .database import Base, engine

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    address = Column(String)
    phone = Column(String)

    inscriptions = relationship("Inscription")

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    inscriptions = relationship("Inscription", back_populates="subject")

class Inscription(Base):
    __tablename__ = "inscriptions"

    owner_id = Column(Integer, ForeignKey("leads.id", ondelete="CASCADE"), primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), primary_key=True)

    duration = Column(Float)
    carerr = Column(String)
    date = Column(Date)
    attemps = Column(Integer)

    subject = relationship("Subject")
    lead = relationship("Lead", back_populates="inscriptions")

Base.metadata.create_all(engine)