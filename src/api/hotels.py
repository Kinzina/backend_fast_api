from fastapi import APIRouter
from fastapi import Query, Body

from src.db import async_session_maker
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.repositories.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    path="",
    summary="получение списка отелей",
    description="получение списка отелей по введенным данным",
)
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="название"),
        location: str | None = Query(None, description="местонахождение"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )


@router.post(
    path="",
    summary="добавление отеля",
    description="будет добавлен новый отель",
)
async def create_hotels(hotel_data: Hotel = Body(
    openapi_examples={
        "1": {"summary": "sochi", "value": {"title": "Отель_01", "location": "г. Сочи, ул. Герцена, д. 1"}},
        "2": {"summary": "yalta", "value": {"title": "Отель_01", "location": "г. Ялта, ул. Герцена, д. 1"}}})):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put(
    path="/{hotel_id}",
    summary="полное изменение данных отеля",
    description="будут изменены все поля отеля",
)
async def put_hotel(
        hotel_id: int,
        hotel_data: Hotel = Body(
            openapi_examples={
                "1": {"summary": "sochi", "value": {"title": "Отель_01", "location": "г. Сочи, ул. Герцена, д. 1"}},
                "2": {"summary": "yalta", "value": {"title": "Отель_01", "location": "г. Ялта, ул. Герцена, д. 1"}}
            }
        )
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()

    return {"status": "OK"}


@router.patch(
    path="/{hotel_id}",
    summary="частичное изменение данных отеля",
    description="можете вводить не все поля для изменения",
)
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.delete(
    path="/{hotel_id}",
    summary="удаление отеля",
    description="удаление отеля по его идентификатору",
)
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()

    return {"status": "OK"}
