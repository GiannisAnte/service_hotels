from fastapi import FastAPI, Query, Body
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn


app = FastAPI(docs_url=None)

hotels = [
    {"id": 1, "title": "Sochi", 'name': 'sochi',},
    {"id": 2, "title": "Дубай", 'name': 'dubai',},
]


@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}
@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def full_update_hotel(
    hotel_id: int,
    title: str = Body(...),
    name: str = Body(...),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": "OK"}
    return {"status": "Error", "message": "Hotel not found"}


@app.patch("/hotels/{hotel_id}")
def partial_update_hotel(
    hotel_id: int,
    title: str | None = Body(None),
    name: str | None = Body(None),
):
    if title is None and name is None:
        return {"status": "Error", "message": "Empty query"}

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title is not None:
                hotel["title"] = title
            if name is not None:
                hotel["name"] = name
            return {"status": "OK"}
    return {"status": "Error", "message": "Hotel not found"}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)