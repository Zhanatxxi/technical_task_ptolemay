from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    email: str
    password: str


class UserInDB(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


class LoginSchema(UserCreateSchema):
    pass
