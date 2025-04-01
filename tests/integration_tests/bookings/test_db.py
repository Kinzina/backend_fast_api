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
    await db.bookings.add(booking_data)

    # получить эту бронь и убедиться что бронирование в базе
    booking_data = (await db.bookings.get_all())[0]
    assert booking_data.room_id == room_id
    assert booking_data.user_id == user_id
    assert booking_data.date_from == date(year=2023, month=12, day=12)
    assert booking_data.date_to == date(year=2024, month=1, day=2)
    assert booking_data.price == 10

    # обновить эту бронь
    booking_data.price = 20
    await db.bookings.edit(booking_data)
    up_booking_data = (await db.bookings.get_all())[0]
    assert up_booking_data.price == 20

    # удалить эту бронь
    await db.bookings.delete()
    del_booking_data = await db.bookings.get_all()
    assert del_booking_data == []

    await db.commit()
