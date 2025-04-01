import json

from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.init import redis_manager
from src.schemas.facilities import FacilityAdd
from src.api.dependencies import DBDep

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get(
    path="",
    summary="получение списка удобств",
    description="получение списка удобств",
)
@cache(expire=100)
async def get_facilities(
        db: DBDep,
):
    print("ИДУ В БАЗУ ДАННЫХ")
    return await db.facilities.get_all()
    # facilities_from_cache = await redis_manager.get("facilities")
    # if not facilities_from_cache:
    #     print("ИДУ В БАЗУ ДАННЫХ")
    #     facilities = await db.facilities.get_all()
    #     facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
    #     facilities_json = json.dumps(facilities_schemas)
    #     await redis_manager.set("facilities", facilities_json, 10)
    #
    #     return facilities
    # else:
    #     print("ИДУ В КЭШ")
    #     facilities_dicts = json.loads(facilities_from_cache)
    #     return facilities_dicts


@router.post(
    path="",
    summary="создание удобства",
    description="создание удобства",
)
async def create_facilities(
        db: DBDep,
        facility_data: FacilityAdd = Body(openapi_examples={
            "1": {"summary": "first", "value": {"title": "wi-fi"}},
            "2": {"summary": "second", "value": {"title": "condition"}},
        })):
    facility = await db.facilities.add(facility_data)
    await db.session.commit()

    return {"status": "OK", "data": facility}
