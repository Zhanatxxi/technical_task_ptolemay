from pydantic import BaseSettings, validator


class Setting(BaseSettings):

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    SQLALCHEMY_DATABASE_URI: str | None = None

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v, values, **kwargs):
        if isinstance(v, str):
            return v
        return f'postgresql+asyncpg://{values.get("DATABASE_USER")}' \
               f':{values.get("DATABASE_PASSWORD")}@localhost:{values.get("DATABASE_PORT")}/{values.get("DATABASE_NAME")}'

    class Config:
        env_file = '.env'


settings = Setting()
