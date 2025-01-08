from datetime import date

from sqlalchemy import select, func

from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(
            self,
            title,
            location,
            limit,
            offset
    ) -> list[Hotel]:
        query = select(HotelsOrm)
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
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

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
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
        #return await self.get_filtered(HotelsOrm.id.in_(hotels_ids))
