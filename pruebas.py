import db
from models import audiovisual
from math import ceil

# Calcular el numero de  graficas a mostrar
    users = db.session.query(Usuario).all()
    filas = ceil(len(users) / 2)
    print(dict_peliculas_audiovisual)
    len(dict_peliculas_audiovisual)

fig, ax = plt.subplots(filas, 2, sharey=True, sharex=True)
    tiempo_empleado = [6, 6]
    tipo_audiovisual = ["Series", "Peliculas"]

if filas >= 2:
    for i in range(filas):
        for j in range(2):
            ax[i, j].barh(tipo_audiovisual, tiempo_empleado)
    config_grafica(fig, ventana_graficas)
else:
    print("Pocos clientes para mostrar las graficas")


