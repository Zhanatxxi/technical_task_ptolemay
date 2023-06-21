from fastapi import Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from passlib.context import CryptContext

from apps.auth.models import User
from config.jwt_settings import AuthJWT
from db.deps import get_db_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def signup(
        db: AsyncSession,
        *,
        email: str,
        password: str,
        is_active=True,
):
    user = await create_user(
        db,
        email=email,
        password=password,
        is_active=is_active,
    )
    return user


async def create_user(
        db: AsyncSession,
        *,
        email: str,
        password: str,
        is_active: bool,
) -> User:
    hash_password = get_password_hash(password)
    user = User(
        email=email,
        hash_password=hash_password,
        is_active=is_active
    )
    db.add(user)
    await db.flush()
    await db.commit()
    await db.refresh(user)

    return user


async def get_user_by_id(db: AsyncSession, *, user_id: int):
    stmt = select(User) \
        .where(User.id == user_id)
    result = await db.scalar(stmt)
    return result


async def get_user_by_email(db: AsyncSession, *, email: str) -> User | None:
    stmt = select(User).where(User.email.like("%{}%".format(email)))
    result = await db.scalar(stmt)
    return result


async def require_user(db: AsyncSession = Depends(get_db_session), Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()

        user = await get_user_by_id(db, user_id=int(user_id))

        if not user:
            raise Exception('User no longer exist')


    except Exception as e:

        error = e.__class__.__name__

        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not logged in')
        if error == 'UserNotFound':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='User no longer exist')
        if error == 'NotVerified':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Please verify your account')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid or has expired')
    return user_id
