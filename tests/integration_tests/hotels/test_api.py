async def test_get_hotels(ac):
    responce = await ac.get(
        url="/hotels",
        params={
            "date_from": "2025-08-01",
            "date_to": "2025-08-14",
        },
    )
    print(f"{responce.json()=}")

    assert responce.status_code == 200
