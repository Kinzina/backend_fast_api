from datetime import date

from sqlalchemy import select, func

from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mapper.mapper import HotelDataMapper
from src.repositories.utils import rooms_ids_for_booking


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            title: str,
            location: str,
            limit: int,
            offset: int
    ):

        rooms_ids = rooms_ids_for_booking(date_from=date_from, date_to=date_to)

        hotels_ids = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids))

        )
        query = (
            select(self.model)
            .select_from(HotelsOrm)
            .filter(HotelsOrm.id.in_(hotels_ids))
        )
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        query = (
            query
            .limit(limit=limit)
            .offset(offset=offset)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]
