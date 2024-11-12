import uvicorn
from fastapi import FastAPI, Query, Body

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Fafi", "name": "fafi"}
]


@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="айдишник"),
        title: str | None = Query(None, description="название")
):
    return [hotel for hotel in hotels if not (id and hotel["id"] != id or title and hotel["title"] != title)]


@app.post("/hotels")
def create_hotels(title: str = Body(embed=True)):
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1,
                   "title": title
                   })
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def full_change_hotel(hotel_id: int, title: str = Body(), name: str = Body()):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = title
    hotel["name"] = name
    return {"status": "OK"}


@app.patch("/hotels/{hotel_id}")
def change_hotel(hotel_id: int, title: str | None = Body(None), name: str = Body(None)):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if title:
        hotel["title"] = title
    if name:
        hotel["name"] = name
    return {"status": "OK"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@app.get("/")
def func():
    return "Hello12!"


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
