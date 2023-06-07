from functools import partial
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

from models.audiovisual import Pelicula, Serie
from clientes_busquedas import dict_peliculas_audiovisual, dict_series_audiovisual

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import db
from styles import styles


def mostrar_catalogos(resultados, audiovisual, nombre, tipo=None):
    ventana_mostrar = Toplevel()
    ventana_mostrar.config(width=400, height=320, background=styles.BG_VENTANA)
    ventana_mostrar.title("Resultados busqueda")  # Titulo de la ventana
    ventana_mostrar.resizable(True, True)

    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                    font=styles.TABLAS)  # Se modifica la fuente de la tabla
    style.configure("mystyle.Treeview.Heading",
                    font=styles.TABLAS_CABECERAS)  # Se modifica la fuente de las cabeceras
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    # Estructura de la tabla de Peliculas
    tabla = ttk.Treeview(ventana_mostrar, height=10, columns=["#0", "#1", "#2", "#3", "#4", "#5", "#6"],
                         style="mystyle.Treeview")
    tabla.grid(row=0, column=0, ipadx=5, ipady=5, padx=10, pady=10)
    tabla.heading(column="#0", text="ID", anchor=CENTER)
    tabla.heading(column="#1", text="Titulo", anchor=CENTER)
    tabla.heading(column="#2", text="Categoria", anchor=CENTER)
    tabla.heading(column="#3", text="Imagen", anchor=CENTER)

    def eliminar(diccionario, tipo, nombre):
        try:
            diccionario[str(nombre) + tipo].remove(
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
        if tipo == "_vistas":

            boton_borrar = Button(ventana_mostrar, text="Eliminar del catalogo", foreground=styles.FG_BOTON,
                                  activeforeground=styles.AFG_BOTON,
                                  activebackground=styles.ABG_BOTON,
                                  command=lambda: eliminar(dict_peliculas_audiovisual, "_vistas", nombre))

            boton_borrar.grid(row=2, column=0, columnspan=3, sticky=W + E)

        elif tipo == "_favoritos":

            boton_borrar = Button(ventana_mostrar, text="Eliminar del catalogo", foreground=styles.FG_BOTON,
                                  activeforeground=styles.AFG_BOTON,
                                  activebackground=styles.ABG_BOTON,
                                  command=lambda: eliminar(dict_peliculas_audiovisual, "_favoritos", nombre))
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
        if tipo == "_vistas":

            boton_borrar = Button(ventana_mostrar, text="Eliminar del catalogo", foreground=styles.FG_BOTON,
                                  activeforeground=styles.AFG_BOTON,
                                  activebackground=styles.ABG_BOTON,
                                  command=lambda: eliminar(dict_series_audiovisual, "_vistas", nombre))

            boton_borrar.grid(row=2, column=0, columnspan=3, sticky=W + E)

        elif tipo == "_favoritos":

            boton_borrar = Button(ventana_mostrar, text="Eliminar del catalogo", foreground=styles.FG_BOTON,
                                  activeforeground=styles.AFG_BOTON,
                                  activebackground=styles.ABG_BOTON,
                                  command=lambda: eliminar(dict_series_audiovisual, "_favoritos", nombre))
            boton_borrar.grid(row=2, column=0, columnspan=3, sticky=W + E)

    mensaje = Label(ventana_mostrar, text="", fg="red", background=styles.BG_VENTANA)
    mensaje.grid(row=1, column=0, columnspan=2, sticky=W + E)

    boton_salir = Button(ventana_mostrar, text="Salir", foreground=styles.FG_BOTON,
                         activeforeground=styles.AFG_BOTON,
                         activebackground=styles.ABG_BOTON_SALIR,
                         command=lambda: ventana_mostrar.destroy())
    boton_salir.grid(row=3, column=0, columnspan=3, sticky=W + E)


def catalogo_completo(audiovisual, nombre):
    if audiovisual == "Pelicula":
        peliculas = db.session.query(Pelicula).all()
        mostrar_catalogos(peliculas, "Pelicula", nombre)
    elif audiovisual == "Serie":
        series = db.session.query(Serie).all()
        mostrar_catalogos(series, "Serie", nombre)


def listas_usuarios(audiovisual, tipo, nombre):
    if audiovisual == "Pelicula":
        peliculas = []
        try:
            titulos = dict_peliculas_audiovisual[str(nombre) + tipo]
            for i in titulos:
                peliculas.append(db.session.query(Pelicula).filter(Pelicula.titulo == i).first())
            mostrar_catalogos(peliculas, "Pelicula", nombre, tipo=tipo)
        except KeyError:
            mb.showwarning("Error", "No tiene ninunga pelicula en esta seccion")
    elif audiovisual == "Serie":
        series = []
        try:
            titulos = dict_series_audiovisual[str(nombre) + tipo]
            for i in titulos:
                series.append(db.session.query(Serie).filter(Serie.titulo == i).first())
            mostrar_catalogos(series, "Serie", nombre, tipo=tipo)
        except KeyError:
            mb.showwarning("Error", "No tiene ninunga serie en esta seccion")


def config_grafica(grafica, ventana):
    canvas = FigureCanvasTkAgg(grafica, ventana)  # CREAR AREA DE DIBUJO DE TKINTER.
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, ventana)  # barra de iconos
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    boton_salir = ttk.Button(ventana, text="Cerrar", command=lambda: ventana.destroy())
    boton_salir.pack(side=BOTTOM)


def grafica_vision(nombre):
    try:
        print(nombre)
        pelis_vistas = dict_peliculas_audiovisual[str(nombre) + "_vistas"]  # linea propensa de error
        series_vistas = dict_series_audiovisual[str(nombre) + "_vistas"]  # linea propensa de error
    except KeyError:
        mb.showwarning("Error", "No existen estadísticas para mostrar. Debe haber visto al menos una de cada para "
                                "mostrar sus graficas")
    else:
        numero_pelis = len(pelis_vistas)
        numero_series = len(series_vistas)

        ventana_grafica = Toplevel()  # Crear una ventana por delante de la principal
        ventana_grafica.title(f"Grafica de visiones de {nombre}")  # Titulo de la ventana
        ventana_grafica.resizable(True, True)

        if numero_series >= numero_pelis:
            rango = numero_series
        else:
            rango = numero_pelis

        # configuracion de la gráfica
        fig, ax = plt.subplots()
        ax.bar(["Series", "Peliculas"], [numero_series, numero_pelis], color="indianred")
        ax.set_title('Cantidades vistas', loc="left",
                     fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
        ax.set_ylabel("Numero de vistas", fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
        ax.set_yticks(range(0, rango + 1))

        config_grafica(fig, ventana_grafica)


def grafica_tiempo(nombre):
    try:
        pelis_vistas = dict_peliculas_audiovisual[str(nombre) + "_vistas"]  # linea propensa de error
        series_vistas = dict_series_audiovisual[str(nombre) + "_vistas"]  # linea propensa de error
    except KeyError:
        mb.showwarning("Error", "No existen estadísticas para mostrar. Debe haber visto al menos una de cada para "
                                "mostrar sus graficas")
    else:
        duracion_peliculas_vistas = 0
        duracion_series_vistas = 0

        ventana_grafica = Toplevel()  # Crear una ventana por delante de la principal
        ventana_grafica.title(f"Grafica de tiempo de {nombre}")  # Titulo de la ventana
        ventana_grafica.resizable(True, True)

        # calcular las metricas
        for i in pelis_vistas:
            pelicula = db.session.query(Pelicula).filter(Pelicula.titulo == i).first()
            duracion_peliculas_vistas += pelicula.duracion

        for i in series_vistas:
            serie = db.session.query(Serie).filter(Serie.titulo == i).first()
            duracion_series_vistas += (serie.duracion_capitulo * serie.capitulos * serie.temporadas)

        duracion_peliculas_vistas /= 60  # Conversion a horas para la gráfica
        duracion_series_vistas /= 60  # Conversion a horas para la gráfica

        # configuracion de la gráfica
        fig, ax = plt.subplots()
        ax.barh(["Series", "Peliculas"], [duracion_series_vistas, duracion_peliculas_vistas], color="indianred")
        ax.set_title('Tiempo de visionado', loc="left",
                     fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
        ax.set_xlabel("Horas", fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})

        config_grafica(fig, ventana_grafica)


def catalogos(audiovisual, nombre):
    if audiovisual == "pelicula":

        ventana_catalogo_peliculas = Toplevel()  # Crear una ventana por delante de la principal
        ventana_catalogo_peliculas.config(width=400, height=320, background=styles.BG_VENTANA)
        ventana_catalogo_peliculas.title(f"Catalogo de peliculas de {nombre}")  # Titulo de la ventana
        ventana_catalogo_peliculas.resizable(True, True)

        titulo = Label(ventana_catalogo_peliculas, text=f"Usuario {nombre}", font=styles.ENCABEZADOS,
                       background=styles.BG_ETIQUETA)
        titulo.grid(column=0, row=0, padx=10, pady=10, columnspan=4, sticky=W + E)

        boton_catalogo_completo = Button(ventana_catalogo_peliculas, text="Catalogo completo",
                                         foreground=styles.FG_BOTON,
                                         activeforeground=styles.AFG_BOTON,
                                         activebackground=styles.ABG_BOTON,
                                         command=partial(catalogo_completo, "Pelicula", nombre))
        boton_catalogo_completo.grid(column=0, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

        boton_catalogo_favoritos = Button(ventana_catalogo_peliculas, text="Catalogo Favoritas",
                                          foreground=styles.FG_BOTON,
                                          activeforeground=styles.AFG_BOTON,
                                          activebackground=styles.ABG_BOTON,
                                          command=partial(listas_usuarios, "Pelicula", "_favoritos", nombre))
        boton_catalogo_favoritos.grid(column=1, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

        boton_catalogo_vistas = Button(ventana_catalogo_peliculas, text="Catalogo Vistas", foreground=styles.FG_BOTON,
                                       activeforeground=styles.AFG_BOTON,
                                       activebackground=styles.ABG_BOTON,
                                       command=partial(listas_usuarios, "Pelicula", "_vistas", nombre))
        boton_catalogo_vistas.grid(column=2, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

        boton_salir = Button(ventana_catalogo_peliculas, text="Salir", foreground=styles.FG_BOTON,
                             activeforeground=styles.AFG_BOTON,
                             activebackground=styles.ABG_BOTON_SALIR,
                             command=lambda: ventana_catalogo_peliculas.destroy())
        boton_salir.grid(row=2, column=0, columnspan=4, sticky=W + E)

    elif audiovisual == "serie":

        ventana_catalogo_series = Toplevel()  # Crear una ventana por delante de la principal
        ventana_catalogo_series.title(f"Catalogo de series de {nombre}")  # Titulo de la ventana
        ventana_catalogo_series.config(width=400, height=320, background=styles.BG_VENTANA)
        ventana_catalogo_series.resizable(True, True)

        titulo = Label(ventana_catalogo_series, text=f"Usuario {nombre}", font=styles.ENCABEZADOS,
                       background=styles.BG_ETIQUETA)
        titulo.grid(column=0, row=0, padx=10, pady=10, columnspan=4, sticky=W + E)

        boton_catalogo_completo = Button(ventana_catalogo_series, text="Catalogo completo", foreground=styles.FG_BOTON,
                                         activeforeground=styles.AFG_BOTON,
                                         activebackground=styles.ABG_BOTON,
                                         command=partial(catalogo_completo, "Serie", nombre))
        boton_catalogo_completo.grid(column=0, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

        boton_catalogo_favoritos = Button(ventana_catalogo_series, text="Catalogo Favoritas",
                                          foreground=styles.FG_BOTON,
                                          activeforeground=styles.AFG_BOTON,
                                          activebackground=styles.ABG_BOTON,
                                          command=partial(listas_usuarios, "Serie", "_favoritos", nombre))
        boton_catalogo_favoritos.grid(column=1, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

        boton_catalogo_vistas = Button(ventana_catalogo_series, text="Catalogo Vistas", foreground=styles.FG_BOTON,
                                       activeforeground=styles.AFG_BOTON,
                                       activebackground=styles.ABG_BOTON,
                                       command=partial(listas_usuarios, "Serie", "_vistas", nombre))
        boton_catalogo_vistas.grid(column=2, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

        boton_salir = Button(ventana_catalogo_series, text="Salir", foreground=styles.FG_BOTON,
                             activeforeground=styles.AFG_BOTON,
                             activebackground=styles.ABG_BOTON_SALIR,
                             command=lambda: ventana_catalogo_series.destroy())
        boton_salir.grid(row=2, column=0, columnspan=4, sticky=W + E)
