from fastapi import APIRouter, Body
from passlib.context import CryptContext

from src.schemas.users import UserRequestAdd, UserAdd
from src.db import async_session_maker
from src.repositories.users import UsersRepository

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register")
async def register_user(
        data: UserRequestAdd = Body(
            openapi_examples={
                "1": {"summary": "user1", "value": {"email": "aaa@yandex.ru", "password": "123456"}},
                "2": {"summary": "user2", "value": {"email": "bbb@yandex.ru", "password": "1234"}}
            }
        )
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}
