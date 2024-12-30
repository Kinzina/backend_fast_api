from sqlalchemy import select, insert

from src.schemas.hotels import Hotel


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, title, location):
        stmt = insert(self.model).values(title=title, location=location)
        # printstmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(stmt)
        return Hotel(title=title, location=location)
