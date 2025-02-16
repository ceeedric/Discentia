import flask_sqlalchemy as alchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    assignments = relationship('Assignment', back_populates='students', cascade='all, delete-orphan')

    # Many-to-one with teacher
    teacher = relationship('Teacher', back_populates='students')
    teacher_id = Column(Integer, ForeignKey('teachers.id'))

