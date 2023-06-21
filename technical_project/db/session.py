from asyncio import current_task

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from technical_project.config.settings import settings
from sqlalchemy.orm import sessionmaker


engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=True,
)


Session = async_scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession
    ),
    scopefunc=current_task
)
