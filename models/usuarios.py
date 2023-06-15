from sqlalchemy import Column, Integer, String
from database import db


class Usuario(db.Base):
    db = "database/plataforma.db"
    __tablename__ = "usuario"
    __table_args = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    contra = Column(String(200), nullable=False)

    def get_nombre(self):
        return self.nombre

    def __init__(self, nombre, contra):
        self.nombre = nombre
        self.contra = contra

