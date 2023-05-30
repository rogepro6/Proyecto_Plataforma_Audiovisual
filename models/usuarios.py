from sqlalchemy import Column, Integer, String
import db


class Usuario (db.Base):

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

    def conectar(self,contrasenia=None):

        if contrasenia == None:
            myContra = input("Ingrese contraseña: ")
        else:
            myContra = contrasenia
        if myContra == self.contra:
            print("Se ha conectado exitosamente")
            self.conectado = True
            return True
        else:
            self.intentos -= 1
            if self.intentos > 0:
                print("Contraseña incorrecta. Intentelo de nuevo...")
                if contrasenia != None:
                    return False
                print("Intentos restantes", self.intentos)
                self.conectar()
            else:
                print("Error, no se pudo iniciar sesion, intentos agotados")

    def desconectar(self):
        if self.conectado:
            print("Se cerró sesion con exito")
            self.conectado = False
        else:
            print("No ha iniciado sesion aun")

    def __str__(self):
        if self.conectado:
            conexion = "conectado"
        else:
            conexion = "desconectado"
        return f"Mi nombre de usuario es {self.nombre} y estoy {conexion}"


