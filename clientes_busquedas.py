from functools import partial
from tkinter import *
from tkinter import ttk
from models.audiovisual import Pelicula, Serie
import db

import main

dict_peliculas_audiovisual = {}
dict_series_audiovisual = {}


def mostrar_resultados(resultados, audiovisual):
    def favoritos(tipo):
        mensaje["text"] = ""
        try:
            titulo = tabla.item(tabla.selection())["values"][0]
        except IndexError:
            mensaje["fg"] = "red"
            mensaje["text"] = "Seleccione un registro"
            return

        if tipo == "peliculas":
            try:
                if titulo in dict_peliculas_audiovisual[str(main.nombreUsuario.get()) + "_favoritos"]:
                    mensaje["fg"] = "red"
                    mensaje["text"] = "La pelicula ya esta en favoritos"
                    return
                else:
                    dict_peliculas_audiovisual[str(main.nombreUsuario.get()) + "_favoritos"].append(titulo)
                    mensaje["fg"] = "blue"
                    mensaje["text"] = f"Pelicula {titulo} añadida a favoritos"
            except:
                dict_peliculas_audiovisual[str(main.nombreUsuario.get()) + "_favoritos"] = []
                dict_peliculas_audiovisual[str(main.nombreUsuario.get()) + "_favoritos"].append(titulo)
                mensaje["fg"] = "blue"
                mensaje["text"] = f"Pelicula {titulo} añadida a favoritos"

        elif tipo == "series":
            try:
                if titulo in dict_series_audiovisual[str(main.nombreUsuario.get()) + "_favoritos"]:
                    mensaje["fg"] = "red"
                    mensaje["text"] = "La serie ya esta en favoritos"
                    return
                else:
                    dict_series_audiovisual[str(main.nombreUsuario.get()) + "_favoritos"].append(titulo)
                    mensaje["fg"] = "blue"
                    mensaje["text"] = f"Serie {titulo} añadida a favoritos"
            except:
                dict_series_audiovisual[str(main.nombreUsuario.get()) + "_favoritos"] = []
                dict_series_audiovisual[str(main.nombreUsuario.get()) + "_favoritos"].append(titulo)
                mensaje["fg"] = "blue"
                mensaje["text"] = f"Serie {titulo} añadida a favoritos"

    def vistas(tipo):
        mensaje["text"] = ""
        try:
            titulo = tabla.item(tabla.selection())["values"][0]
        except IndexError:
            mensaje["fg"] = "red"
            mensaje["text"] = "Selecciona un registro"
            return
        if tipo == "peliculas":
            try:
                if titulo in dict_peliculas_audiovisual[str(main.nombreUsuario.get()) + "_vistas"]:
                    mensaje["fg"] = "red"
                    mensaje["text"] = "La pelicula ya esta en vistas"
                    return
                else:
                    dict_peliculas_audiovisual[str(main.nombreUsuario.get()) + "_vistas"].append(titulo)
                    mensaje["fg"] = "blue"
                    mensaje["text"] = f"Pelicula {titulo} añadida a vistas"
            except:
                dict_peliculas_audiovisual[str(main.nombreUsuario.get()) + "_vistas"] = []
                dict_peliculas_audiovisual[str(main.nombreUsuario.get()) + "_vistas"].append(titulo)
                mensaje["fg"] = "blue"
                mensaje["text"] = f"Pelicula {titulo} añadida a vistas"
        if tipo == "series":
            try:
                if titulo in dict_series_audiovisual[str(main.nombreUsuario.get()) + "_vistas"]:
                    mensaje["fg"] = "red"
                    mensaje["text"] = "La serie ya esta en vistas"
                    return
                else:
                    dict_series_audiovisual[str(main.nombreUsuario.get()) + "_vistas"].append(titulo)
                    mensaje["fg"] = "blue"
                    mensaje["text"] = f"Serie {titulo} añadida a vistas"
            except:
                dict_series_audiovisual[str(main.nombreUsuario.get()) + "_vistas"] = []
                dict_series_audiovisual[str(main.nombreUsuario.get()) + "_vistas"].append(titulo)
                mensaje["fg"] = "blue"
                mensaje["text"] = f"Serie {titulo} añadida a vistas"

    ventana_resultados_busqueda = Toplevel()
    ventana_resultados_busqueda.title("Resultados busqueda")  # Titulo de la ventana
    ventana_resultados_busqueda.resizable(True, True)

    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                    font=('Calibri', 10))  # Se modifica la fuente de la tabla
    style.configure("mystyle.Treeview.Heading",
                    font=('Calibri', 10, 'bold'))  # Se modifica la fuente de las cabeceras
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    # Estructura de la tabla de Peliculas
    tabla = ttk.Treeview(ventana_resultados_busqueda, height=10, columns=["#0", "#1", "#2", "#3", "#4", "#5", "#6"],
                         style="mystyle.Treeview")

    if audiovisual == "peliculas":

        tabla.grid(row=0, column=0)
        tabla.heading(column="#0", text="ID", anchor=CENTER)
        tabla.heading(column="#1", text="Titulo", anchor=CENTER)
        tabla.heading(column="#2", text="Categoria", anchor=CENTER)
        tabla.heading(column="#3", text="Imagen", anchor=CENTER)
        tabla.heading(column="#4", text="Duracion", anchor=CENTER)
        tabla.heading(column="#5", text="Año", anchor=CENTER)
        tabla.heading(column="#6", text="Director", anchor=CENTER)

        registros = tabla.get_children()
        for fila in registros:
            tabla.delete(fila)

        for pelicula in resultados:
            tabla.insert("", 0, text=pelicula.id, values=(pelicula.titulo,
                                                          pelicula.categoria,
                                                          pelicula.imagen,
                                                          pelicula.duracion,
                                                          pelicula.anio,
                                                          pelicula.director))

        boton_favoritas = ttk.Button(ventana_resultados_busqueda, text="Añadir a favoritas",
                                     command=partial(favoritos, "peliculas"))
        boton_favoritas.grid(row=2, column=0, columnspan=2, sticky=W + E)

        boton_vistas = ttk.Button(ventana_resultados_busqueda, text="Pelicula vista",
                                  command=partial(vistas, "peliculas"))
        boton_vistas.grid(row=3, column=0, columnspan=2, sticky=W + E)

        boton_salir = ttk.Button(ventana_resultados_busqueda, text="Salir",
                                 command=lambda: ventana_resultados_busqueda.destroy())
        boton_salir.grid(row=4, column=0, columnspan=2, sticky=W + E)

        mensaje = Label(ventana_resultados_busqueda, text="", fg="red")
        mensaje.grid(row=1, column=0, columnspan=2, sticky=W + E)

    if audiovisual == "series":

        tabla.grid(row=0, column=0)
        tabla.heading(column="#0", text="ID", anchor=CENTER)
        tabla.heading(column="#1", text="Titulo", anchor=CENTER)
        tabla.heading(column="#2", text="Categoria", anchor=CENTER)
        tabla.heading(column="#3", text="Imagen", anchor=CENTER)
        tabla.heading(column="#4", text="Temporadas", anchor=CENTER)
        tabla.heading(column="#5", text="Capitulos", anchor=CENTER)
        tabla.heading(column="#6", text="Duracion de capitulos", anchor=CENTER)

        registros = tabla.get_children()
        for fila in registros:
            tabla.delete(fila)

        for serie in resultados:
            tabla.insert("", 0, text=serie.id, values=(serie.titulo,
                                                       serie.categoria,
                                                       serie.imagen,
                                                       serie.temporadas,
                                                       serie.capitulos,
                                                       serie.duracion_capitulo))

        boton_favoritas = ttk.Button(ventana_resultados_busqueda, text="Añadir a favoritas",
                                     command=partial(favoritos, "series"))
        boton_favoritas.grid(row=2, column=0, columnspan=2, sticky=W + E)

        boton_vistas = ttk.Button(ventana_resultados_busqueda, text="Serie vista",
                                  command=partial(vistas, "series"))
        boton_vistas.grid(row=3, column=0, columnspan=2, sticky=W + E)

        boton_salir = ttk.Button(ventana_resultados_busqueda, text="Salir",
                                 command=lambda: ventana_resultados_busqueda.destroy())
        boton_salir.grid(row=4, column=0, columnspan=2, sticky=W + E)

        mensaje = Label(ventana_resultados_busqueda, text="", fg="red")
        mensaje.grid(row=1, column=0, columnspan=2, sticky=W + E)


def buscar_audiovisual(audiovisual):
    def busqueda(tipo):
        if busqueda_entry.get() == "":
            mensaje["fg"] = "red"
            mensaje["text"] = "Seleccione una busqueda"
        else:
            if tipo == "peliculas":
                if modo_busqueda.get() == "titulo":
                    resultados = db.session.query(Pelicula).filter_by(titulo=busqueda_entry.get())
                    mostrar_resultados(resultados, tipo)
                elif modo_busqueda.get() == "categoria":
                    resultados = db.session.query(Pelicula).filter_by(categoria=busqueda_entry.get())
                    mostrar_resultados(resultados, tipo)
            elif tipo == "series":
                if modo_busqueda.get() == "titulo":
                    resultados = db.session.query(Serie).filter_by(titulo=busqueda_entry.get())
                    mostrar_resultados(resultados, tipo)
                elif modo_busqueda.get() == "categoria":
                    resultados = db.session.query(Serie).filter_by(categoria=busqueda_entry.get())
                    mostrar_resultados(resultados, tipo)

    ventana_buscar = Toplevel()  # Crear una ventana por delante de la principal
    ventana_buscar.title(f"Buscador de {audiovisual}")  # Titulo de la ventana
    ventana_buscar.resizable(True, True)

    modo_busqueda = StringVar()
    radiobutton1 = Radiobutton(ventana_buscar, text="Titulo", variable=modo_busqueda, value="titulo")
    radiobutton1.grid(row=0, column=0, padx=10, pady=10)
    radiobutton2 = Radiobutton(ventana_buscar, text="Categoria", variable=modo_busqueda, value="categoria")
    radiobutton2.grid(row=0, column=1, padx=10, pady=10)

    busqueda_entry = Entry(ventana_buscar)
    busqueda_entry.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky=W + E)

    boton_buscar = ttk.Button(ventana_buscar, text="Buscar", command=partial(busqueda, audiovisual))
    boton_buscar.grid(row=3, column=0, columnspan=2, sticky=W + E)

    boton_salir = ttk.Button(ventana_buscar, text="Salir", command=lambda: ventana_buscar.destroy())
    boton_salir.grid(row=4, column=0, columnspan=2, sticky=W + E)

    mensaje = Label(ventana_buscar, text="", fg="red")
    mensaje.grid(column=0, row=2, columnspan=2, sticky=W + E)
