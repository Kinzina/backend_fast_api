from fastapi import APIRouter, Body

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post(path="")
async def get_smth(
        db: DBDep,
        user_id: UserIdDep,
        booking_data: BookingAddRequest = Body(openapi_examples={
            "1": {"summary": "first", "value": {
                "room_id": 3, "date_from": "2025-01-12", "date_to": "2025-01-15"
            }}
        })):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    boooking_price = room.price * (booking_data.date_to - booking_data.date_from).days
    _booking_data = BookingAdd(user_id=user_id, price=boooking_price,  **booking_data.model_dump())
    await db.bookings.add(_booking_data)
    await db.session.commit()
    return {"status": "OK", "user_id": user_id}
