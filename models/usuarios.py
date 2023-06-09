from sqlalchemy import Column, Integer, String
import db


class Usuario(db.Base):
    db = "database/plataforma.db"
    __tablename__ = "usuario"
    __table_args = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    contra = Column(String(200), nullable=False)
    numusuarios = 0

    def get_nombre(self):
        return self.nombre

    def __init__(self, nombre, contra):
        self.nombre = nombre
        self.contra = contra

        self.conectado = False
        self.intentos = 3

        Usuario.numusuarios += 1

    def __str__(self):
        if self.conectado:
            conexion = "conectado"
        else:
            conexion = "desconectado"
        return f"Mi nombre de usuario es {self.nombre} y estoy {conexion}"
