##Importamos el modelo Base para que la clase Movie sea un modelo de la base de datos
from config.database import Base
##Importamos los tipos de datos y columnas de sql alchemy
from sqlalchemy import Column, Integer, String, Float

class Movie(Base):

    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)