from fastapi import APIRouter, Body, Query
from datetime import date

from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.schemas.facilities import RoomFacility, RoomFacilityAdd
from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get(
    path="/{hotel_id}/rooms",
    summary="получение списка номеров",
    description="получение списка номеров по введенным данным",
)
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example="2024-01-02"),
        date_to: date = Query(example="2024-01-12"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get(
    path="/{hotel_id}/rooms/{room_id}",
    summary="получение конкретного номера",
    description="получение конкретного номера",
)
async def get_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
):
    return await db.rooms.get_one_or_none_reals(id=room_id, hotel_id=hotel_id)


@router.post(
    path="/{hotel_id}/rooms",
    summary="создание номера",
    description="создание номера",
)
async def create_room(
        db: DBDep,
        hotel_id: int,
        room_data: RoomAddRequest = Body(openapi_examples={
            "1": {"summary": "first", "value": {
                "title": "s", "description": "ss", "price": 10, "quantity": 1, "facilities_ids": [1, 2]
            }}
        })):

    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)

    await db.session.commit()

    return {"status": "OK", "data": room}


@router.put(
    path="/{hotel_id}/rooms/{room_id}",
    summary="полное изменение номера",
    description="полное изменение номера",
)
async def edit_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest = Body(openapi_examples={
            "1": {"summary": "first", "value": {
                "hotel_id": 28, "title": "s4", "description": "ss", "price": 10, "quantity": 1, "facilities_ids": [1, 2]
            }}
        })):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)

    await db.rooms_facilities.set_rooms_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)

    await db.session.commit()

    return {"status": "OK"}


@router.patch(
    path="/{hotel_id}/rooms/{room_id}",
    summary="частичное изменение номера",
    description="частичное изменение номера",
)
async def partially_edit_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_rooms_facilities(
            room_id=room_id,
            facilities_ids=_room_data_dict["facilities_ids"]
        )

    await db.session.commit()

    return {"status": "OK"}


@router.delete(
    path="/{hotel_id}/rooms/{room_id}",
    summary="удаление номера",
    description="удаление номера"
)
async def delete_room(
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    await db.hotels.delete(id=room_id, hotel_id=hotel_id)
    await db.session.commit()

    return {"status": "OK"}
