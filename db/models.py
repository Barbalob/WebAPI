from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    surname = Column(String, index=True, unique=True)
    school = relationship('School', back_populates='students', cascade='all, delete-orphan')

class School(Base):
    __tablename__ = 'school'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    students = relationship('User', back_populates='school')