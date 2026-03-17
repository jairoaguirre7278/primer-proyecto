from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select



app = FastAPI()
class estudianteModelo(SQLModel, table=True):
    id: int = Field(primary_key=True)
    nombre: str = Field(max_length=30)


# Code above omitted 👆

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# Code below omitted 👇
class estudiante(BaseModel):
    telefono: str
    price: float
    is_offer: bool | None = None

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/estudiantes")
def crear_estudiante(estudiante: estudianteModelo, session: SessionDep)-> estudianteModelo:
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante

@app.get("/estudiantes")
def read_root(session: SessionDep):
    estudiantes= session.exec(select(estudianteModelo)).all()
    return estudiantes


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, estudianteActualizacion: estudiante):
    return {"estudiante_telefono": estudianteActualizacion.telefono, "item_id": item_id}