from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from models.audiovisual import Pelicula, Serie
from clientes_busquedas import dict_peliculas_audiovisual
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import main
import db


def mostrar_catalogos(resultados, audiovisual):
    ventana_mostrar = Toplevel()
    ventana_mostrar.title("Resultados busqueda")  # Titulo de la ventana
    ventana_mostrar.resizable(True, True)

    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                    font=('Calibri', 10))  # Se modifica la fuente de la tabla
    style.configure("mystyle.Treeview.Heading",
                    font=('Calibri', 10, 'bold'))  # Se modifica la fuente de las cabeceras
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    # Estructura de la tabla de Peliculas
    tabla = ttk.Treeview(ventana_mostrar, height=10, columns=["#0", "#1", "#2", "#3", "#4", "#5", "#6"],
                         style="mystyle.Treeview")
    tabla.grid(row=0, column=0)
    tabla.heading(column="#0", text="ID", anchor=CENTER)
    tabla.heading(column="#1", text="Titulo", anchor=CENTER)
    tabla.heading(column="#2", text="Categoria", anchor=CENTER)
    tabla.heading(column="#3", text="Imagen", anchor=CENTER)

    if audiovisual == "Pelicula":

        tabla.heading(column="#4", text="Duracion", anchor=CENTER)
        tabla.heading(column="#5", text="Año", anchor=CENTER)
        tabla.heading(column="#6", text="Director", anchor=CENTER)

        registros = tabla.get_children()
        for fila in registros:
            tabla.delete(fila)

        for item in resultados:
            tabla.insert("", 0, text=item.id, values=(item.titulo,
                                                      item.categoria,
                                                      item.imagen,
                                                      item.duracion,
                                                      item.anio,
                                                      item.director))

    elif audiovisual == "Serie":

        tabla.heading(column="#4", text="Temporadas", anchor=CENTER)
        tabla.heading(column="#5", text="Capitulos", anchor=CENTER)
        tabla.heading(column="#6", text="Duracion de capitulos", anchor=CENTER)

        registros = tabla.get_children()
        for fila in registros:
            tabla.delete(fila)

        for item in resultados:
            tabla.insert("", 0, text=item.id, values=(item.titulo,
                                                      item.categoria,
                                                      item.imagen,
                                                      item.temporadas,
                                                      item.capitulos,
                                                      item.duracion_capitulos))

    boton_salir = ttk.Button(ventana_mostrar, text="Salir",
                             command=lambda: ventana_mostrar.destroy())
    boton_salir.grid(row=1, column=0, columnspan=3, sticky=W + E)


def pelis_completo():
    peliculas = db.session.query(Pelicula).all()
    mostrar_catalogos(peliculas, "Pelicula")


def pelis_vistas():
    peliculas = []
    try:
        titulos_vistos = dict_peliculas_audiovisual[str(main.nombreUsuario.get()) + "_vistas"]
        for i in titulos_vistos:
            peliculas.append(db.session.query(Pelicula).filter(Pelicula.titulo == i).first())
        mostrar_catalogos(peliculas, "Pelicula")
    except KeyError:
        mb.showwarning("Error", "No tiene ninunga pelicula en esta seccion")


def pelis_favoritas():
    peliculas = []
    try:
        titulos_favoritos = dict_peliculas_audiovisual[str(main.nombreUsuario.get()) + "_favoritos"]
        for i in titulos_favoritos:
            peliculas.append(db.session.query(Pelicula).filter(Pelicula.titulo == i).first())
        mostrar_catalogos(peliculas, "Pelicula")
    except KeyError:
        mb.showwarning("Error", "No tiene ninunga pelicula en esta seccion")


def graficas():
    try:
        pelis_vistas = dict_peliculas_audiovisual[str(main.nombreUsuario.get()) + "_vistas"]  # linea propensa de error
        duracion_peliculas_vistas = 0

        ventana_grafica = Toplevel()  # Crear una ventana por delante de la principal
        ventana_grafica.title(f"Grafica de {main.nombreUsuario.get()}")  # Titulo de la ventana
        ventana_grafica.resizable(True, True)

        # calcular las metricas
        for peli in pelis_vistas:
            pelicula = db.session.query(Pelicula).filter(Pelicula.titulo == peli).first()
            duracion_peliculas_vistas += pelicula.duracion
            print(duracion_peliculas_vistas)

        duracion_peliculas_vistas /= 60  # Conversion a horas para la gráfica

        # configuracion de la gráfica
        fig, ax = plt.subplots()
        ax.barh(["Series", "Peliculas"], [1, duracion_peliculas_vistas], color="indianred")
        ax.set_title('Tiempo de visionado', loc="left",
                     fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
        ax.set_xlabel("Horas", fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})

        canvas = FigureCanvasTkAgg(fig, ventana_grafica)  # CREAR AREA DE DIBUJO DE TKINTER.
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, ventana_grafica)  # barra de iconos
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        boton_salir = ttk.Button(ventana_grafica, text="Cerrar", command=lambda: ventana_grafica.destroy())
        boton_salir.pack(side=BOTTOM)
    except KeyError:
        mb.showwarning("Error", "No existen estadísticas para mostrar")


def catalogo_peliculas():
    ventana_catalogo_peliculas = Toplevel()  # Crear una ventana por delante de la principal
    ventana_catalogo_peliculas.title(f"Catalogos de {main.nombreUsuario.get()}")  # Titulo de la ventana
    ventana_catalogo_peliculas.resizable(True, True)

    titulo = Label(ventana_catalogo_peliculas, text=f"Usuario {main.nombreUsuario.get()}", font=("Arial", 36))
    titulo.grid(column=0, row=0, padx=10, pady=10, columnspan=4, sticky=W + E)

    catalogo_completo = ttk.Button(ventana_catalogo_peliculas, text="Catalogo completo", command=pelis_completo)
    catalogo_completo.grid(column=0, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

    catalogo_favoritas = ttk.Button(ventana_catalogo_peliculas, text="Catalogo Favoritas", command=pelis_favoritas)
    catalogo_favoritas.grid(column=1, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

    catalogo_vistas = ttk.Button(ventana_catalogo_peliculas, text="Catalogo Vistas", command=pelis_vistas)
    catalogo_vistas.grid(column=2, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

    boton_salir = ttk.Button(ventana_catalogo_peliculas, text="Salir",
                             command=lambda: ventana_catalogo_peliculas.destroy())
    boton_salir.grid(row=2, column=0, columnspan=4, sticky=W + E)


def catalogo_series():
    pass
