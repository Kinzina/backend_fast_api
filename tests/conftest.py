import pytest
from httpx import AsyncClient
import json

from src.config import settings
from src.db import Base, engine_null_pool
from src.main import app
from src.models import *


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", "r", encoding="utf-8") as fh:
        data = json.load(fh)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        for dat in data:
            await ac.post(
                "/hotels",
                json={"title": dat["title"], "location": dat["location"]}
            )

    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("facilities", json={"title": "wifi"})
        await ac.post("facilities", json={"title": "phone"})

    with open("tests/mock_rooms.json", "r", encoding="utf-8") as fh:
        data = json.load(fh)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        for dat in data:
            await ac.post(
                f"/hotels/{dat['hotel_id']}/rooms",
                json={
                    "title": dat["title"],
                    "description": dat["description"],
                    "price": dat["price"],
                    "quantity": dat["quantity"],
                    "facilities_ids": [1, 2]
                }
            )


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={"email": "cot@pes.ru", "password": "1234"}
        )
