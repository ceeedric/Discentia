from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database import Base

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)

    students = relationship('Student', back_populates='teacher')
