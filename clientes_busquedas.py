from tkinter import *
from tkinter import ttk
from models.audiovisual import Pelicula
import db

import main

dict_peliculas_audiovisual = {}
dict_series_audiovisual = {}


def mostrar_resultados(resultados):
    def favoritos():
        mensaje["text"] = ""
        try:
            titulo = tabla.item(tabla.selection())["values"][0]
        except IndexError as e:
            mensaje["fg"] = "red"
            mensaje["text"] = "Selecciona una pelicula"
            return
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

        print(dict_peliculas_audiovisual)

    def vistas():
        mensaje["text"] = ""
        try:
            titulo = tabla.item(tabla.selection())["values"][0]
        except IndexError as e:
            mensaje["fg"] = "red"
            mensaje["text"] = "Selecciona una pelicula"
            return
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

        print(dict_peliculas_audiovisual)

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

    boton_favoritas = ttk.Button(ventana_resultados_busqueda, text="Añadir a favoritas", command=favoritos)
    boton_favoritas.grid(row=2, column=0, columnspan=2, sticky=W + E)

    boton_vistas = ttk.Button(ventana_resultados_busqueda, text="Pelicula vista", command=vistas)
    boton_vistas.grid(row=3, column=0, columnspan=2, sticky=W + E)

    boton_salir = ttk.Button(ventana_resultados_busqueda, text="Salir",
                             command=lambda: ventana_resultados_busqueda.destroy())
    boton_salir.grid(row=4, column=0, columnspan=2, sticky=W + E)

    mensaje = Label(ventana_resultados_busqueda, text="", fg="red")
    mensaje.grid(row=1, column=0, columnspan=2, sticky=W + E)

    print(main.nombreUsuario.get())


def buscar_peli():
    def busqueda():
        if busqueda_entry.get() == "":
            mensaje["fg"] = "red"
            mensaje["text"] = "Seleccione una busqueda"
        else:
            if modo_busqueda.get() == "titulo":
                resultados = db.session.query(Pelicula).filter_by(titulo=busqueda_entry.get())
                mostrar_resultados(resultados)
            elif modo_busqueda.get() == "categoria":
                resultados = db.session.query(Pelicula).filter_by(categoria=busqueda_entry.get())
                mostrar_resultados(resultados)

    ventana_buscar_peli = Toplevel()  # Crear una ventana por delante de la principal
    ventana_buscar_peli.title("Buscador De peliculas")  # Titulo de la ventana
    ventana_buscar_peli.resizable(True, True)

    modo_busqueda = StringVar()
    radiobutton1 = Radiobutton(ventana_buscar_peli, text="Titulo", variable=modo_busqueda, value="titulo")
    radiobutton1.grid(row=0, column=0, padx=10, pady=10)
    radiobutton2 = Radiobutton(ventana_buscar_peli, text="Categoria", variable=modo_busqueda, value="categoria")
    radiobutton2.grid(row=0, column=1, padx=10, pady=10)

    busqueda_entry = Entry(ventana_buscar_peli)
    busqueda_entry.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky=W + E)

    boton_buscar = ttk.Button(ventana_buscar_peli, text="Buscar", command=busqueda)
    boton_buscar.grid(row=3, column=0, columnspan=2, sticky=W + E)

    boton_salir = ttk.Button(ventana_buscar_peli, text="Salir", command=lambda: ventana_buscar_peli.destroy())
    boton_salir.grid(row=4, column=0, columnspan=2, sticky=W + E)

    mensaje = Label(ventana_buscar_peli, text="", fg="red")
    mensaje.grid(column=0, row=2, columnspan=2, sticky=W + E)


def buscar_serie():
    pass
