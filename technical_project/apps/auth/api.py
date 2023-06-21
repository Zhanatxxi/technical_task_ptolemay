from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, HTTPException, status, APIRouter

from apps.auth.models import User
from apps.auth.schemas import UserCreateSchema, UserInDB, LoginSchema
from apps.auth.services import get_user_by_email, signup, verify_password, get_user_by_id
from db.deps import get_db_session
from technical_project.config.settings import settings
from technical_project.config.jwt_settings import AuthJWT


ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN

auth_routers = APIRouter()


@auth_routers.post("/sign-up", response_model=UserInDB)
async def sign_up(
        user: UserCreateSchema,
        db: AsyncSession = Depends(get_db_session),
):
    users = await get_user_by_email(db, email=user.email)

    if users:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    user_ins = await signup(
        db,
        email=user.email,
        password=user.password,
    )

    return user_ins


@auth_routers.post("/login")
async def login(
        user_in: LoginSchema,
        Authorize: AuthJWT = Depends(),
        db: AsyncSession = Depends(get_db_session),
):
    user: User | None = await get_user_by_email(db, email=user_in.email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Incorrect Email or Password"
        )

    if not verify_password(user_in.password, user.hash_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect Email or Password"
        )

    access_token = Authorize.create_access_token(
        subject=str(user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    refresh_token = Authorize.create_refresh_token(
        subject=str(user.id), expires_time=timedelta(days=REFRESH_TOKEN_EXPIRES_IN))

    return {
        "email": user.email,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@auth_routers.get('/refresh')
async def refresh_token(Authorize: AuthJWT = Depends(),
                        db: AsyncSession = Depends(get_db_session)):
    try:
        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()

        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')

        user = await get_user_by_id(db, user_id=int(user_id))

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The user belonging to this token no logger exist')

        access_token = Authorize.create_access_token(
            subject=str(user.id), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    except Exception as e:
        error = e.__class__.__name__
        print(error)
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return {
        'access_token': access_token,
        "logged_in": True
    }

