from sqlalchemy import delete, insert, select

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.repositories.mapper.mapper import FacilityDataMapper, RoomFacilityDataMapper


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    mapper = RoomFacilityDataMapper

    async def set_rooms_facilities(self, room_id, facilities_ids: list[int]) -> None:
        query = select(self.model.facility_id).filter_by(room_id=room_id)
        res = await self.session.execute(query)
        current_facilities_ids: list[int] = res.scalars().all()

        facilities_exist = set(current_facilities_ids)
        facilities_need = set(facilities_ids)

        facilities_ids_to_delete: list[int] = list(facilities_exist.difference(facilities_need))
        facilities_ids_to_insert: list[int] = list(facilities_need.difference(facilities_exist))

        if facilities_ids_to_delete:
            delete_rooms_facilities_stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(facilities_ids_to_delete)
                )
            )

            await self.session.execute(delete_rooms_facilities_stmt)

        if facilities_ids_to_insert:
            insert_rooms_facilities_stmt = (
                insert(self.model)
                .values([{"room_id": room_id, "facility_id": f_id} for f_id in facilities_ids_to_insert]
                )
            )

            await self.session.execute(insert_rooms_facilities_stmt)
