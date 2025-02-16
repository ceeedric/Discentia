from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Assignment(Base):
    __tablename__ = 'assignments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    grade = Column(Float, nullable=False)
    date_created = Column(DateTime)
    date_due = Column(DateTime)

    # Many-to-one with students
    student_id = Column(Integer, ForeignKey('students.id'))
    student = relationship('Student', back_populates='assignments', cascade='all')


