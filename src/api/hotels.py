from fastapi import APIRouter
from fastapi import Query, Body
from sqlalchemy import insert, select

from src.db import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    path="",
    summary="получение списка отелей",
    description="получение списка отелей по введенным данным",
    # response_model=list[Hotel]
)
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="название"),
        location: str | None = Query(None, description="местонахождение"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if title:
            query = query.where(HotelsOrm.title.like(f'%{title}%'))
        if location:
            query = query.where(HotelsOrm.location.like(f'%{location}%'))
        query = (
            query
            .limit(limit=per_page)
            .offset(offset=per_page * (pagination.page - 1))
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
        print(hotels)
        return hotels

@router.post(
    path="",
    summary="добавление отеля",
    description="будет добавлен новый отель",
)
async def create_hotels(hotel_data: Hotel = Body(
    openapi_examples={"1": {"summary": "sochi", "value": {"title": "Отель_01", "location": "г. Сочи, ул. Герцена, д. 1"}},
                      "2": {"summary": "yalta", "value": {"title": "Отель_01", "location": "г. Ялта, ул. Герцена, д. 1"}}})):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router.put(
    path="/{hotel_id}",
    summary="полное изменение данных отеля",
    description="будут изменены все поля отеля",
)
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
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
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
