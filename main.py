from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo de datos
class Item(BaseModel):
    id: int
    nombre: str
    descripcion: str = None
    precio: float
    disponible: bool = True

# Base de datos en memoria con dos elementos
items_db: List[Item] = [
    Item(id=1, nombre="Muñeca", descripcion="muñeca bonita", precio=12000.0, disponible=True),
    Item(id=2, nombre="Carrito", descripcion="A control remoto", precio=7500.0, disponible=False),
    Item(id=3, nombre="Carrito2", descripcion="carro verde", precio=7500.0, disponible=True),
]

@app.get("/")
def leer_raiz():
    return {"mensaje": "¡Bienvenido a la API de Juguete!"}

@app.get("/items", response_model=List[Item])
def obtener_items():
    return items_db

@app.get("/items/{item_id}", response_model=Item)
def obtener_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item no encontrado")

@app.post("/items", response_model=Item)
def crear_item(item: Item):
    if any(i.id == item.id for i in items_db):
        raise HTTPException(status_code=400, detail="ID ya existe")
    items_db.append(item)
    return item
