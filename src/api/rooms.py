from fastapi import APIRouter, Query, Body

from src.db import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPATCH

router = APIRouter(prefix="/rooms", tags=["Номера"])


@router.get(path="")
async def get_rooms():
    return {"status": "OK"}


@router.get(
    path="/{hotel_id}",
    summary="получение списка номеров",
    description="получение списка номеров по введенным данным",
)
async def get_rooms(
        hotel_id: int
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id=hotel_id
        )


@router.post(
    path="",
    summary="создание номера",
    description="создание номера",
)
async def create_room(room_data: RoomAdd = Body(openapi_examples={
    "1": {"summary": "first", "value": {
        "hotel_id": 28, "title": "s", "description": "ss", "price": 10, "quantity": 1
    }}
})):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()

    return {"status": "OK", "data": room}


@router.post(
    path="/{room_id}",
    summary="полное изменение номера",
    description="полное изменение номера",
)
async def put_room(room_id: int,
                   room_data: RoomAdd = Body(openapi_examples={
                       "1": {"summary": "first", "value": {
                           "hotel_id": 28, "title": "s4", "description": "ss", "price": 10, "quantity": 1
                       }}
                   })):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id)
        await session.commit()

    return {"status": "OK"}


@router.patch(
    path="/{room_id}",
    summary="частичное изменение номера",
    description="частичное изменение номера",
)
async def partially_edit_hotel(
        room_id: int,
        room_data: RoomPATCH
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=room_id)
        await session.commit()

    return {"status": "OK"}

@router.delete(
    path="{room_id}",
    summary="удаление номера",
    description="удаление номера"
)
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()

    return {"status": "OK"}
