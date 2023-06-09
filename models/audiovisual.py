from sqlalchemy import Column, Integer, String, Float
from database import db


class Audiovisual:
    def __init__(self, titulo, categoria, imagen):
        self.titulo = titulo
        self.categoria = categoria
        self.imagen = imagen


class Pelicula(Audiovisual, db.Base):
    db = "database/plataforma.db"
    __tablename__ = "pelicula"
    __table_args = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)
    categoria = Column(String(100))
    imagen = Column(String(200))
    duracion = Column(Float)
    anio = Column(Integer)
    director = Column(String(100))

    def __init__(self, titulo, categoria, imagen, duracion, anio, director):
        super().__init__(titulo, categoria, imagen)
        self.duracion = duracion
        self.anio = anio
        self.director = director


class Serie(Audiovisual, db.Base):
    db = "database/plataforma.db"
    __tablename__ = "serie"
    __table_args = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)
    categoria = Column(String(100))
    imagen = Column(String(200))
    temporadas = Column(Integer)
    capitulos = Column(Integer)
    duracion_capitulo = Column(Float)

    def __init__(self, titulo, categoria, imagen, temporadas, capitulos, duracion_capitulo):
        super().__init__(titulo, categoria, imagen)
        self.temporadas = temporadas
        self.capitulos = capitulos
        self.duracion_capitulo = duracion_capitulo
