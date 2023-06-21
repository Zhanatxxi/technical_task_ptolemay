from datetime import date

from pydantic import BaseModel


class DepartmentSchema(BaseModel):
    id: int
    date: date | None
    title: str
    employee_count: int | None
    total_salary: int | None
    # employees: list | None

    class Config:
        orm_mode = True
