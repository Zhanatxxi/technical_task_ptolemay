from sqlalchemy import Column, String, Integer, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from technical_project.db.base_model import Base, TableSettings


class Employee(Base, TableSettings):
    username = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False, index=True)
    position = Column(String(100), nullable=True)
    salary = Column(Integer)
    age = Column(SmallInteger)

    departament_id = Column(Integer, ForeignKey("departament.id"))
    departament = relationship("Departament", back_populates="employees")

    @property
    def full_name(self):
        return f"Name: {self.username} {self.surname}"

    def __repr__(self):
        return f"id: {self.id}, full_name: {self.full_name}"

