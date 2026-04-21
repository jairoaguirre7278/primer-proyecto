from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Annotated, List, Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.security import OAuth2PasswordBearer


app = FastAPI()



class usuarioModelo(SQLModel, table=True):
    id: int = Field(primary_key=True)
    nombre: str = Field(max_length=30)
    telefono: int Field(max_length=10)


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


class usuario(BaseModel, table=True):
    id: int = Field(primary_key=True)
    nombre: str
    telefono: int
    
                
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/usuarios")
def read_root(
    session: SessionDep,
):
    usuario = session.exec(select(usuarioModelo)).all()
    return usuarios


@app.get("/usuarios/{id}")
def read_root(
    session: SessionDep,
):
    usuario =  session.get(nombre, id)
    return usuario


@app.post("/usuarios")
def crear_estudiante(
    usuario: usuarioModelo,
    session: SessionDep,
)-> usuarioModelo:
    session.add(usuario)
    session.commit()
    session.refresh(db_usuario)
    return db_usuario


@app.put("/usuario/{id}")
def update_usuario(id: int, usuarioActualizacion: usuario):
  item_id: int,
    item: ItemCreate,
    session: Session = Depends(get_session)
):
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="No encontrado")
    data = usuario.model_dump(exclude_unset=True)
    db_item.sqlmodel_update(data)
    session.commit()
    session.refresh(db_usuario)
    return db_usuario


app.delete("/usuario/{id}", status_code=204)
def eliminar_item(id: int, session: Session = Depends(get_session)):
    db_id = session.get(usuario, id)
    if not db_id:
        raise HTTPException(status_code=404, detail="No encontrado")
    session.delete(db_usuario)
    session.commit()
