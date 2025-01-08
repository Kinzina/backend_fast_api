from fastapi import APIRouter, Body

from src.schemas.facilities import FacilitiesAdd
from src.api.dependencies import DBDep

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get(
    path="",
    summary="получение списка удобств",
    description="получение списка удобств",
)
async def get_rooms(
        db: DBDep,
):
    return await db.facilities.get_all()


@router.post(
    path="",
    summary="создание удобства",
    description="создание удобства",
)
async def create_room(
        db: DBDep,
        facility_data: FacilitiesAdd = Body(openapi_examples={
            "1": {"summary": "first", "value": {"title": "wi-fi"}},
            "2": {"summary": "second", "value": {"title": "condition"}},
        })):
    facility = await db.facilities.add(facility_data)
    await db.session.commit()

    return {"status": "OK", "data": facility}
