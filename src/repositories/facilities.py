from sqlalchemy import delete, insert

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    # async def edit_bulk(self, data: list[RoomFacility]):
    #     query = select(self.model).filter_by(**filter_by)
    #     result = await self.session.execute(query)
    #     model = result.scalars().one_or_none()
    #     if model is None:
    #         return None
    #     return self.schema.model_validate(model, from_attributes=True)
    #     smtp = select(self.model).from ()
    #     for item in data:
    #         delete(self.model).filter_by(room_id=item.room_id, facility_id=item.facility_id)
    #     add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
    #     await self.session.execute(add_data_stmt)

    # async def edit_bulk(self, data: list[RoomFacility]):
    #     if not data:
    #         return
    #
    #     # Собираем уникальные room_id и facility_id для удаления
    #     unique_ids = {(item.room_id, item.facility_id) for item in data}
    #
    #     # Удаляем существующие записи
    #     await self.session.execute(
    #         delete(self.model).where(
    #             (self.model.room_id.in_([room_id for room_id, _ in unique_ids])) &
    #             (self.model.facility_id.in_([facility_id for _, facility_id in unique_ids]))
    #         )
    #     )
    #
    #     # Подготовляем данные для вставки
    #     add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
    #     await self.session.execute(add_data_stmt)
    #
    #     await self.session.commit()  # Важно комитить изменения
