from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Body, HTTPException, Response, Request
from passlib.context import CryptContext
import jwt

from src.schemas.users import UserRequestAdd, UserAdd
from src.db import async_session_maker
from src.repositories.users import UsersRepository
from src.config import settings
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register")
async def register_user(
        data: UserRequestAdd = Body(
            openapi_examples={
                "1": {"summary": "user1", "value": {"email": "aaa@yandex.ru", "password": "123456"}},
                "2": {"summary": "user2", "value": {"email": "bbb@yandex.ru", "password": "1234"}}
            }
        )
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}


@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = AuthService().create_access_token({"user_id": user.id})
        await session.commit()
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.get("/only_auth")
async def only_auth(request: Request):
    access_token = request.cookies["access_token"] or None
    return {"access_token": access_token}
