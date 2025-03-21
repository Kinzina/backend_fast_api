from datetime import date
from sqlalchemy import select, func

from src.models.rooms import RoomsOrm
from src.models.bookings import BookingsOrm


def rooms_ids_for_booking(date_from: date, date_to: date, hotel_id: int | None = None):
    rooms_count = (
        select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsOrm)
        .filter(BookingsOrm.date_from <= date_to, BookingsOrm.date_to >= date_from)
        .group_by(BookingsOrm.room_id)
        .cte(name="rooms_count")
    )
    rooms_free_table = (
        select(
            RoomsOrm.id.label("room_id"),
            (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_free")
        )
        .select_from(RoomsOrm)
        .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
        .cte(name="rooms_free_table")
    )
    rooms_ids_from_hotel = (
        select(RoomsOrm.id)
        .select_from(RoomsOrm)
    )
    if hotel_id is not None:
        rooms_ids_from_hotel = rooms_ids_from_hotel.filter_by(hotel_id=hotel_id)
    rooms_ids_from_hotel = rooms_ids_from_hotel.subquery(name="rooms_ids_from_hotels")
    rooms_ids = (
        select(rooms_free_table.c.room_id)
        .select_from(rooms_free_table)
        .filter(
            rooms_free_table.c.rooms_free > 0,
            rooms_free_table.c.room_id.in_(rooms_ids_from_hotel)
        )
    )

    return rooms_ids
