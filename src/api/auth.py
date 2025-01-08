from fastapi import APIRouter, Body, HTTPException, Response

from src.api.dependencies import UserIdDep
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService
from src.api.dependencies import DBDep

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register")
async def register_user(
        db: DBDep,
        data: UserRequestAdd = Body(
            openapi_examples={
                "1": {"summary": "user1", "value": {"email": "aaa@yandex.ru", "password": "123456"}},
                "2": {"summary": "user2", "value": {"email": "bbb@yandex.ru", "password": "1234"}}
            }
        )
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    await db.users.add(new_user_data)
    await db.session.commit()

    return {"status": "OK"}


@router.post("/login")
async def login_user(
        db: DBDep,
        data: UserRequestAdd,
        response: Response
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль неверный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    await db.session.commit()
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(
        db: DBDep,
        user_id: UserIdDep,
):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
