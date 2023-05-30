from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#Engine
#El engine sqlalchemy permite comunicarse con la base de datos
#https://docs.sqlalchemy.org/en/14/core/engines.html
engine = create_engine('sqlite:///database/plataforma.db', connect_args={'check_same_thread': False})
#Advertencia:Crear el engine no conecta inmediatamente a la base de datos, eso lo hacemos mas adelante
#Sesion
#Nos permite realizar transacciones (operaciones) dentro de nuestra bd
Session = sessionmaker(bind=engine)
session = Session()
#Vinculacion
#Ahora vamos al fichero models y en las clases que queramos que se trasnformen en tablas le añadiremos esta variable y
#esto se encargara de mapear y vincular la clase a la tabla
Base = declarative_base()