from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class estudiante(BaseModel):
    telefono: str
    price: float
    is_offer: bool | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, estudianteActualizacion: estudiante):
    return {"estudiante_telefono": estudianteActualizacion.telefono, "item_id": item_id}