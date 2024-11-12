import uvicorn
from fastapi import FastAPI, Query, Body

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Fafi", "name": "fafi"}
]


@app.get(
    path="/hotels",
    summary="получение списка отелей",
    description="получение списка отелей по введенным данным",
)
def get_hotels(
        id: int | None = Query(None, description="айдишник"),
        title: str | None = Query(None, description="название")
):
    return [hotel for hotel in hotels if not (id and hotel["id"] != id or title and hotel["title"] != title)]


@app.post(
    path="/hotels",
    summary="добавление отеля",
    description="будет добавлен новый отель",
)
def create_hotels(title: str = Body(embed=True)):
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1,
                   "title": title
                   })
    return {"status": "OK"}


@app.put(
    path="/hotels/{hotel_id}",
    summary="полное изменение данных отеля",
    description="будут изменены все поля отеля",
)
def put_hotel(hotel_id: int, title: str = Body(), name: str = Body()):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = title
    hotel["name"] = name
    return {"status": "OK"}


@app.patch(
    path="/hotels/{hotel_id}",
    summary="частичное изменение данных отеля",
    description="можете вводить не все поля для изменения",
)
def patch_hotel(hotel_id: int, title: str | None = Body(None), name: str = Body(None)):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if title:
        hotel["title"] = title
    if name:
        hotel["name"] = name
    return {"status": "OK"}


@app.delete(
    path="/hotels/{hotel_id}",
    summary="удаление отеля",
    description="удаление отеля по его идентификатору",
)
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
