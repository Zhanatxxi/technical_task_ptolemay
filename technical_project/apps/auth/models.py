from sqlalchemy import (
    Column, String, Boolean
)


from technical_project.db.base_model import Base, TableSettings


class User(Base, TableSettings):

    email = Column(String(length=255), unique=True, info={
        "verbose_name": "Email пользователя"
    })
    hash_password = Column(String(128), info={
        "verbose_name": "Password пользователя"
    })
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    def __repr__(self):
        return f"id:{self.id} email: {self.email}"