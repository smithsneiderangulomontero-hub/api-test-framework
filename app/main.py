from fastapi import FastAPI, HTTPException, status

from app.models import Item, ItemCreate

app = FastAPI(
    title="Items API",
    description="API de ejemplo (SUT) para el framework de pruebas",
    version="1.0.0",
)

# "Base de datos" en memoria: suficiente para un SUT de pruebas,
# se reinicia en cada arranque del proceso.
_db: dict[int, Item] = {}
_next_id = 1


@app.get("/health", tags=["meta"])
def health() -> dict:
    return {"status": "ok"}


@app.post(
    "/items", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["items"]
)
def create_item(payload: ItemCreate) -> Item:
    global _next_id
    item = Item(id=_next_id, **payload.model_dump())
    _db[_next_id] = item
    _next_id += 1
    return item


@app.get("/items", response_model=list[Item], tags=["items"])
def list_items() -> list[Item]:
    return list(_db.values())


@app.get("/items/{item_id}", response_model=Item, tags=["items"])
def get_item(item_id: int) -> Item:
    item = _db.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} no encontrado")
    return item


@app.put("/items/{item_id}", response_model=Item, tags=["items"])
def update_item(item_id: int, payload: ItemCreate) -> Item:
    if item_id not in _db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} no encontrado")
    item = Item(id=item_id, **payload.model_dump())
    _db[item_id] = item
    return item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["items"])
def delete_item(item_id: int) -> None:
    if item_id not in _db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} no encontrado")
    del _db[item_id]
