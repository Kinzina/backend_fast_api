from fastapi import APIRouter
from fastapi import Query, Body

from schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get(
    path="",
    summary="получение списка отелей",
    description="получение списка отелей по введенным данным",
    response_model=list[Hotel]
)
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="айдишник"),
        title: str | None = Query(None, description="название"),
):
    return [hotel for hotel in hotels
            if not (id and hotel["id"] != id or title and hotel["title"] != title)][(pagination.per_page * (pagination.page - 1)):(pagination.per_page * pagination.page)]


@router.post(
    path="",
    summary="добавление отеля",
    description="будет добавлен новый отель",
)
def create_hotels(hotel_data: Hotel = Body(
    openapi_examples={"1": {"summary": "schochi", "value": {"title": "Сочи", "name": "Сочи1"}},
                      "2": {"summary": "dubai", "value": {"title": "Дубай", "name": "Дубай1"}}})):
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1,
                   "title": hotel_data.title,
                   "name": hotel_data.name,
                   })
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
