from fastapi import APIRouter
from fastapi import FastAPI, Body, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Any, Coroutine, Optional, List
##Importamos lo necesario para que corra la base de datos sql lite
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
##Importamos el middleware que creamos para el manejo de errores




movie_router = APIRouter()

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


##Ahora vemos mas a fondo el metodo GET
@movie_router.get("/movies", tags=["Movies"])
def get_movies():
    ##Abrimos una sesión de la base de datos
    db = Session()
    ###Hacemos un query a la Table MovieModel para traer todos los registros.
    result = db.query(MovieModel).all()
    return result

##Ahora aprendemos a hacer filtros, en este caso filtraremos por el id
##Filtramos por id de pelicula
###Estos son parametros de ruta de la url
@movie_router.get("/movies/{id_movie}", tags=["movies"])
def get_movie(id_movie: int):
    db = Session()
    ###Hacemos un query a la tabla movie con filtro
    result = db.query(MovieModel).filter(MovieModel.id == id_movie).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No se encontro ninguna pelicula con ese id"})
    
    return JSONResponse(status_code = 200, content=jsonable_encoder(result))

###Ahora usaremos Parametros query, estos se pasan por la función y no por la url
@movie_router.get("/movies/Category/", tags=["movies"])
def get_movies_by_category(category: str, year: int):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    return JSONResponse(content=jsonable_encoder(result))

###Ahora veremos el metodo POST, para publicar peliculas
##Lo que ponemos al lado de los parametros (= Body()) es para que los parametros los envien y se reciban en el body de la API
# @app.post("/movies/create", tags=["movies"], dependencies=[Depends(JWTBearer())])
@movie_router.post("/movies/create", tags=["movies"], status_code=201)
def add_movie(movie: Movie):
    ##Creamos una sesión para acceder a la base de datos
    db = Session()
    ##Agregamos la pelicula al MovieModel como parametro 
    new_movie = MovieModel(**dict(movie))
    ##Añadimos la pelicula a la base de datos
    db.add(new_movie)
    ##Hacemos commit para que se guarde la pelicula
    db.commit()
    db.refresh(new_movie)
    return JSONResponse(content={"Se agrego exitosamente la pelicula:": jsonable_encoder(new_movie)})


###Usamos el Metodo PUT
@movie_router.put("/movies/{id_movie}", tags=["movies"])
def modify_movie(id_movie:int, movie: Movie):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id_movie).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No se encontro ninguna pelicula con ese id"})

    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    ##Recargamos la pelicula desde la base de datos para obtener los valores actualizados de la pelicula ya filtrada anteriormente
    db.refresh(result)
    return f"Se modifico exitosamente la pelicula: {jsonable_encoder(result)}"

###Usamos el Metodo DELETE
@movie_router.delete("/movie/{id_movie}", tags=["movies"])
def delete_movie(id_movie:int):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id_movie).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No se encontro ninguna pelicula con ese id"})

    ###Eliminamos la pelicula que se econtro con el filtro que hicimos
    db.delete(result)
    db.commit()
    ###Esta vez no usamos refresh para que no de error por refrescar una pelicula que no existe ya
    return f"Haz eliminado exitosamente la pelicula: {jsonable_encoder(result)}"