from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from technical_project.db.base_model import Base, TableSettings


class Departament(Base, TableSettings):
    title = Column(String(255), nullable=True)

    employees = relationship(
        "Employee",
        back_populates="departament"
    )

    def __repr__(self):
        return f"id: {self.id}, title: {self.title}"
