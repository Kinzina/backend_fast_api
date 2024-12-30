from sqlalchemy import select, func

from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            title,
            location,
            limit,
            offset
    ):
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
        # print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        return result.scalars().all()
