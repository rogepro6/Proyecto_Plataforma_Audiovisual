import db
from models.usuarios import Usuario
from main import interfazUsuario

from models.audiovisual import Pelicula, Serie

if __name__ == "__main__":
    db.Base.metadata.drop_all(bind=db.engine, checkfirst=True)
    db.Base.metadata.create_all(db.engine)

    #Creacion del usuario administrador
    admin = Usuario("a", "a")
    db.session.add(admin)
    db.session.commit()

    #Creacion de un usuario normal
    user = Usuario("us", "us")
    db.session.add(user)
    db.session.commit()

    #Introduccion de peliculas de prueba
    db.session.add(Pelicula("El padrino", "mafia", "jpg", 180, 1972, "Francis"))
    db.session.add(Pelicula("El padrino 2", "mafia", "jpg", 190, 1974, "Francis"))
    db.session.add(Pelicula("Matrix", "scifi", "pnj", 120, 1999, "Wachosky"))
    db.session.add(Pelicula("Matrix 2", "scifi", "pnj", 120, 2001, "Wachosky"))
    db.session.add(Pelicula("La comunidad del anillo", "fantasia", "pnj", 150, 2001, "Peter Jackson"))
    db.session.add(Pelicula("Las dos torres", "fantasia", "pnj", 170, 2002, "Peter Jackson"))
    db.session.add(Pelicula("El retorno del rey", "fantasia", "pnj", 180, 2003, "Peter Jackson"))
    db.session.commit()

    #Introduccion de series de prueba
    db.session.add(Serie("The Boys", "heroes", "jpg", 3, 10, 60))
    db.session.add(Serie("Juego de tronos", "fantasia", "jpg", 12, 12, 50))
    db.session.add(Serie("Breaking Bad", "mafia", "pnj", 5, 12, 40))
    db.session.commit()

    #LLamada a la function principal
    interfazUsuario()

