from datetime import date

from fastapi import APIRouter
from fastapi import Query, Body

from src.schemas.hotels import HotelAdd, HotelPATCH
from src.api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    path="",
    summary="получение списка отелей со свободными номерами",
    description="получение списка отелей со свободными номерами",
)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        date_from: date = Query(example="2024-01-02"),
        date_to: date = Query(example="2024-01-12"),
        title: str | None = Query(None, description="название"),
        location: str | None = Query(None, description="местонахождение"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        date_from=date_from, date_to=date_to,
        title=title,
        location=location,
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )


@router.get(
    path="/{hotel_id}",
    summary="получение отеля по id",
    description="получение отеля по id",
)
async def get_hotel_by_id(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post(
    path="",
    summary="добавление отеля",
    description="будет добавлен новый отель",
)
async def create_hotels(db: DBDep, hotel_data: HotelAdd = Body(
    openapi_examples={
        "1": {"summary": "sochi", "value": {"title": "Отель_01", "location": "г. Сочи, ул. Герцена, д. 1"}},
        "2": {"summary": "yalta", "value": {"title": "Отель_01", "location": "г. Ялта, ул. Герцена, д. 1"}}})):
    hotel = await db.hotels.add(hotel_data)
    await db.session.commit()

    return {"status": "OK", "data": hotel}


@router.put(
    path="/{hotel_id}",
    summary="полное изменение данных отеля",
    description="будут изменены все поля отеля",
)
async def put_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelAdd = Body(
            openapi_examples={
                "1": {"summary": "sochi", "value": {"title": "Отель_01", "location": "г. Сочи, ул. Герцена, д. 1"}},
                "2": {"summary": "yalta", "value": {"title": "Отель_01", "location": "г. Ялта, ул. Герцена, д. 1"}}
            }
        )
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.session.commit()

    return {"status": "OK"}


@router.patch(
    path="/{hotel_id}",
    summary="частичное изменение данных отеля",
    description="можете вводить не все поля для изменения",
)
async def partially_edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPATCH):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.session.commit()

    return {"status": "OK"}


@router.delete(
    path="/{hotel_id}",
    summary="удаление отеля",
    description="удаление отеля по его идентификатору",
)
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.session.commit()

    return {"status": "OK"}
