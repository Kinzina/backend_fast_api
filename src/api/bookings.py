from fastapi import APIRouter, Body

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post(path="")
async def add_booking(
        db: DBDep,
        user_id: UserIdDep,
        booking_data: BookingAddRequest = Body(openapi_examples={
            "1": {"summary": "first", "value": {
                "room_id": 3, "date_from": "2025-01-12", "date_to": "2025-01-15"
            }}
        })):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    _booking_data = BookingAdd(user_id=user_id, price=room.price,  **booking_data.model_dump())
    booking = await db.bookings.add(_booking_data)
    await db.session.commit()
    return {"status": "OK", "data": booking}


@router.get(path="/bookings")
async def get_bookings(db: DBDep):
    bookings = await db.bookings.get_all()
    return {"data": bookings}


@router.get(path="/me")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    bookings = await db.bookings.get_filtered(user_id=user_id)
    return {"data": bookings}
