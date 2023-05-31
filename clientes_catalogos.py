from functools import partial
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from models.audiovisual import Pelicula, Serie
from clientes_busquedas import dict_peliculas_audiovisual, dict_series_audiovisual
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import main
import db


def mostrar_catalogos(resultados, audiovisual, tipo=None):
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

    def eliminar(diccionario, tipo):
        try:
            diccionario[str(main.nombreUsuario.get()) + tipo].remove(
                tabla.item(tabla.selection())["values"][0])
        except IndexError:
            mensaje["fg"] = "red"
            mensaje["text"] = "Seleccione un registro"
        except KeyError:
            mensaje["fg"] = "red"
            mensaje["text"] = "No se encuentra el registro"
        except ValueError:
            mensaje["fg"] = "red"
            mensaje["text"] = "Ese registro ya ha sido eliminado. Salga y vuelva a entrar"
        else:
            mensaje["fg"] = "blue"
            mensaje["text"] = "Registro eliminado"

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
        if tipo == "Vistas":

            boton_borrar = ttk.Button(ventana_mostrar, text="Eliminar del catalogo",
                                      command=lambda: eliminar(dict_peliculas_audiovisual, "_vistas"))

            boton_borrar.grid(row=2, column=0, columnspan=3, sticky=W + E)

        elif tipo == "Favoritas":

            boton_borrar = ttk.Button(ventana_mostrar, text="Eliminar del catalogo",
                                      command=lambda: eliminar(dict_peliculas_audiovisual, "_favoritos"))
            boton_borrar.grid(row=2, column=0, columnspan=3, sticky=W + E)

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
                                                      item.duracion_capitulo))
        if tipo == "Vistas":

            boton_borrar = ttk.Button(ventana_mostrar, text="Eliminar del catalogo",
                                      command=lambda: eliminar(dict_series_audiovisual, "_vistas"))

            boton_borrar.grid(row=2, column=0, columnspan=3, sticky=W + E)

        elif tipo == "Favoritas":

            boton_borrar = ttk.Button(ventana_mostrar, text="Eliminar del catalogo",
                                      command=lambda: eliminar(dict_series_audiovisual, "_favoritos"))
            boton_borrar.grid(row=2, column=0, columnspan=3, sticky=W + E)

    mensaje = Label(ventana_mostrar, text="", fg="red")
    mensaje.grid(row=1, column=0, columnspan=2, sticky=W + E)

    boton_salir = ttk.Button(ventana_mostrar, text="Salir",
                             command=lambda: ventana_mostrar.destroy())
    boton_salir.grid(row=3, column=0, columnspan=3, sticky=W + E)


def catalogo_completo(audiovisual):
    if audiovisual == "Pelicula":
        peliculas = db.session.query(Pelicula).all()
        mostrar_catalogos(peliculas, "Pelicula")
    elif audiovisual == "Serie":
        series = db.session.query(Serie).all()
        mostrar_catalogos(series, "Serie")


def catalogo_vistas(audiovisual):
    if audiovisual == "Pelicula":
        peliculas = []
        try:
            titulos_vistos = dict_peliculas_audiovisual[str(main.nombreUsuario.get()) + "_vistas"]
            for i in titulos_vistos:
                peliculas.append(db.session.query(Pelicula).filter(Pelicula.titulo == i).first())
            mostrar_catalogos(peliculas, "Pelicula", "Vistas")
        except KeyError:
            mb.showwarning("Error", "No tiene ninunga pelicula en esta seccion")
    elif audiovisual == "Serie":
        series = []
        try:
            titulos_vistos = dict_series_audiovisual[str(main.nombreUsuario.get()) + "_vistas"]
            for i in titulos_vistos:
                series.append(db.session.query(Serie).filter(Serie.titulo == i).first())
            mostrar_catalogos(series, "Serie", "Vistas")
        except KeyError:
            mb.showwarning("Error", "No tiene ninunga serie en esta seccion")


def catalogo_favoritas(audiovisual):
    if audiovisual == "Pelicula":
        peliculas = []
        try:
            titulos_favoritos = dict_peliculas_audiovisual[str(main.nombreUsuario.get()) + "_favoritos"]
            for i in titulos_favoritos:
                peliculas.append(db.session.query(Pelicula).filter(Pelicula.titulo == i).first())
            mostrar_catalogos(peliculas, "Pelicula", "Favoritas")
        except KeyError:
            mb.showwarning("Error", "No tiene ninunga pelicula en esta seccion")
    elif audiovisual == "Serie":
        series = []
        try:
            titulos_favoritos = dict_series_audiovisual[str(main.nombreUsuario.get()) + "_favoritos"]
            for i in titulos_favoritos:
                series.append(db.session.query(Serie).filter(Serie.titulo == i).first())
            mostrar_catalogos(series, "Serie", "Favoritas")
        except KeyError:
            mb.showwarning("Error", "No tiene ninunga serie en esta seccion")


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


def catalogos(audiovisual):
    if audiovisual == "pelicula":

        ventana_catalogo_peliculas = Toplevel()  # Crear una ventana por delante de la principal
        ventana_catalogo_peliculas.title(f"Catalogo de peliculas de {main.nombreUsuario.get()}")  # Titulo de la ventana
        ventana_catalogo_peliculas.resizable(True, True)

        titulo = Label(ventana_catalogo_peliculas, text=f"Usuario {main.nombreUsuario.get()}", font=("Arial", 36))
        titulo.grid(column=0, row=0, padx=10, pady=10, columnspan=4, sticky=W + E)

        boton_catalogo_completo = ttk.Button(ventana_catalogo_peliculas, text="Catalogo completo",
                                         command=partial(catalogo_completo, "Pelicula"))
        boton_catalogo_completo.grid(column=0, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

        boton_catalogo_favoritos = ttk.Button(ventana_catalogo_peliculas, text="Catalogo Favoritas",
                                          command=partial(catalogo_favoritas, "Pelicula"))
        boton_catalogo_favoritos.grid(column=1, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

        boton_catalogo_vistas = ttk.Button(ventana_catalogo_peliculas, text="Catalogo Vistas",
                                       command=partial(catalogo_vistas, "Pelicula"))
        boton_catalogo_vistas.grid(column=2, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

        boton_salir = ttk.Button(ventana_catalogo_peliculas, text="Salir",
                             command=lambda: ventana_catalogo_peliculas.destroy())
        boton_salir.grid(row=2, column=0, columnspan=4, sticky=W + E)

    elif audiovisual == "serie":

        ventana_catalogo_series = Toplevel()  # Crear una ventana por delante de la principal
        ventana_catalogo_series.title(f"Catalogo de series de {main.nombreUsuario.get()}")  # Titulo de la ventana
        ventana_catalogo_series.resizable(True, True)

        titulo = Label(ventana_catalogo_series, text=f"Usuario {main.nombreUsuario.get()}", font=("Arial", 36))
        titulo.grid(column=0, row=0, padx=10, pady=10, columnspan=4, sticky=W + E)

        boton_catalogo_completo = ttk.Button(ventana_catalogo_series, text="Catalogo completo",
                                             command=partial(catalogo_completo, "Serie"))
        boton_catalogo_completo.grid(column=0, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

        boton_catalogo_favoritos = ttk.Button(ventana_catalogo_series, text="Catalogo Favoritas",
                                              command=partial(catalogo_favoritas, "Serie"))
        boton_catalogo_favoritos.grid(column=1, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

        boton_catalogo_vistas = ttk.Button(ventana_catalogo_series, text="Catalogo Vistas",
                                           command=partial(catalogo_vistas, "Serie"))
        boton_catalogo_vistas.grid(column=2, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

        boton_salir = ttk.Button(ventana_catalogo_series, text="Salir",
                                 command=lambda: ventana_catalogo_series.destroy())
        boton_salir.grid(row=2, column=0, columnspan=4, sticky=W + E)