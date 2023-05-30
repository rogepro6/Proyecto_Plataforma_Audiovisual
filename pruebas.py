import db
from models import audiovisual

peli = audiovisual.Pelicula("El padrino", "mafia", "img.png", 170, 1976, "Francis Fran coppola")
serie = audiovisual.Serie("Juego de Tronos", "Epica", "img2.png", 8, 10, 60)

db.Base.metadata.drop_all(bind=db.engine, checkfirst=True)
db.Base.metadata.create_all(db.engine)

db.session.add(peli)
db.session.add(serie)
db.session.commit()



