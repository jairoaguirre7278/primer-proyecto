from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Annotated, List, Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.security import OAuth2PasswordBearer


app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
    token: Annotated[str, Depends(oauth2_scheme)]
):
    estudiantes= session.exec(select(usuarioModelo)).all()
    return usuarios


@app.post("/usuarios")
def crear_estudiante(
    usuario: usuarioModelo,
    session: SessionDep,
    token: Annotated[str, Depends(oauth2_scheme)]
)-> usuarioModelo:
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@app.put("/usuario/{id}")
def update_usuario(id: int, usuarioActualizacion: usuario):
    return {"usuario_telefono": usuarioActualizacion.telefono, "id": id}
