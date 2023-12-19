from fastapi import FastAPI, Body, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Any, Coroutine, Optional, List
##Importamos la función que genera el token para autenticación del usuario
from utils.jwt_manager import create_token
from starlette.requests import Request
##Importamos lo necesario para que corra la base de datos sql lite
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

##Importamos el middleware que creamos para el manejo de errores
from middlewares.error_handler import ErrorHandler

##Importamos la clase jwt_bearer para el manejo de autenticaciones
from middlewares.jwt_bearer import JWTBearer
##Importamos el router de movie
from routers.movie import movie_router


# ###Clase para pedir autenticación en determinadas rutas
# class JWTBearer(HTTPBearer):
#     async def __call__(self, request: Request): #-> Coroutine[Any, Any, HTTPAuthorizationCredentials | None]:
#         auth =  await super().__call__(request)
#         data = validate_token(auth.credentials)
#         if data["email"] != "admin@gmail.com":
#             raise HTTPException(status_code=403, detail="Invalid Credentials")



app = FastAPI()

##Para acceder a la documentación autogenerada de FastAPI Tenemos que entrar a la url de la API y poner /docs

##Sirve para cambiar el titulo de la documentación de la aplicación
app.title = "Mi aplicación del Curso de FastAPI"

##Sirve para cambiar la version de la aplicación
app.version = "0.0.1"

##Agregar directamente el middleware para manejo de errores directamente en la app de fastAPI
app.add_middleware(ErrorHandler)

##Incluimos el Router de movies a la app
app.include_router(movie_router)


##Creamos la tabla en sql lite
Base.metadata.create_all(bind=engine)


###Creamos una clase para permitir el log in del usuario
class User(BaseModel):
    email:str
    password:str


###Creamos una clase Movie para no tener que escribir varias veces los parametros que se necesitan para crearo modificar una pelicula
class Movie(BaseModel):
    id:Optional[int] = None
    title:str
    overview:str
    year:int
    rating:float = Field(ge=1, le=10)
    category:str
    ##Hacer un valor opcional
    ##id: Optional[int] = None


###Creamos una ruta para permitir el log in del Usuario
@app.post("/login", tags=["authentication"])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(dict(user))
    return JSONResponse(status_code=200, content=token)

##Los tags son como los titulos que se les da a esa llamada en especifico de la API
@app.get('/', tags=["Home-Messages"])
def message():
    return HTMLResponse("<h1>Hello World</h1>")