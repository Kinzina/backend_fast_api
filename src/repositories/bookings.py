from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mapper.mapper import BookingDataMapper
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper
