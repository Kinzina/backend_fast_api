async def test_get_facilities(ac):
    responce = await ac.get(url="/facilities")
    assert responce.status_code == 200
    assert isinstance(responce.json(), list)


async def test_post_facilities(ac):
    facility_title = 'Массаж'
    responce = await ac.post(url="/facilities", json={'title': facility_title})
    # print(f"{responce.json()=}")
    assert responce.status_code == 200
    res = responce.json()
    assert isinstance(res, dict)
    assert 'data' in res
    assert res['data']['title'] == facility_title
