from pydantic import BaseModel
from pydantic.fields import Field


class EmployeeCreateSchema(BaseModel):
    username: str = Field(..., max_length=50)
    surname: str = Field(..., max_length=50)
    age: int
    salary: int
    position: str = Field(..., max_length=100)
    departament_id: int = Field(gt=0)


class EmployeeOutDB(EmployeeCreateSchema):
    id: int

    class Config:
        orm_mode = True

