import db
from models.usuarios import Usuario
from main import interfazUsuario

from models.audiovisual import Pelicula, Serie

if __name__ == "__main__":
    # Limpiar la base de datos y crear las tablas
    db.Base.metadata.drop_all(bind=db.engine, checkfirst=True)
    db.Base.metadata.create_all(db.engine)

    # Creacion del usuario administrador
    admin = Usuario("a", "a")
    db.session.add(admin)
    db.session.commit()

    # Creacion de un usuario normal
    user = Usuario("us", "us")
    db.session.add(user)
    db.session.commit()

    # Introduccion de peliculas de prueba
    db.session.add(Pelicula("El padrino", "mafia", "padrino.png", 180, 1972, "Francis"))
    db.session.add(Pelicula("El padrino 2", "mafia", "padrino2.png", 190, 1974, "Francis"))
    db.session.add(Pelicula("Matrix", "scifi", "matrix.png", 120, 1999, "Wachosky"))
    db.session.add(Pelicula("Matrix 2", "scifi", "matrix2.png", 120, 2001, "Wachosky"))
    db.session.add(Pelicula("La comunidad del anillo", "fantasia", "LaComunidadDelAnillo.png", 150, 2001, "Peter "
                                                                                                          "Jackson"))
    db.session.add(Pelicula("Las dos torres", "fantasia", "LasDosTorres.png", 170, 2002, "Peter Jackson"))
    db.session.add(Pelicula("El retorno del rey", "fantasia", "ElRetornoDelRey.png", 180, 2003, "Peter Jackson"))
    db.session.commit()

    # Introduccion de series de prueba
    db.session.add(Serie("The Boys", "heroes", "TheBoys.png", 3, 10, 60))
    db.session.add(Serie("Juego de tronos", "fantasia", "JuegoDeTronos.png", 12, 12, 50))
    db.session.add(Serie("Breaking Bad", "mafia", "BreakingBad.png", 5, 12, 40))
    db.session.commit()

    # LLamada a la function principal
    interfazUsuario()
