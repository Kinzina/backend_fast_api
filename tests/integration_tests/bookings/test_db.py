from datetime import date

from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2023, month=12, day=12),
        date_to=date(year=2024, month=1, day=2),
        price=10
    )
    new_booking = await db.bookings.add(booking_data)

    # получить эту бронь и убедиться что бронирование в базе
    booking = await db.bookings.get_one_or_none(id=new_booking.id)

    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id

    # обновить эту бронь
    new_price = 20
    updated_booking_data = BookingAdd(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2023, month=12, day=12),
        date_to=date(year=2024, month=1, day=2),
        price=new_price
    )
    await db.bookings.edit(updated_booking_data, id=booking.id)
    up_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert up_booking
    assert up_booking.price == new_price

    # удалить эту бронь
    await db.bookings.delete(id=booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking
