from tkinter import *
from tkinter import ttk
import db
from models.audiovisual import Pelicula, Serie


def add_pelicula():
    def registrar_peli():
        if len(tituloEntry.get()) and len(categoriaEntry.get()) and len(imagenEntry.get()) and \
                len(duracionEntry.get()) and len(anioEntry.get()) and len(directorEntry.get()):

            pelicula = Pelicula(
                tituloEntry.get(),
                categoriaEntry.get(),
                imagenEntry.get(),
                duracionEntry.get(),
                anioEntry.get(),
                directorEntry.get()
            )
            db.session.add(pelicula)
            db.session.commit()
            mensaje["fg"] = "blue"
            mensaje["text"] = f"Pelicula {tituloEntry.get()} añadida con exito"
        else:
            mensaje["fg"] = "red"
            mensaje["text"] = "Debe introducir todos los datos"

    ventana_admin = Toplevel()  # Crear una ventana por delante de la principal
    ventana_admin.title("Registro de peliculas")  # Titulo de la ventana
    ventana_admin.resizable(False, False)

    tituloPeli = Label(ventana_admin, text="Titulo ")
    tituloPeli.grid(column=0, row=1)
    categoriaPeli = Label(ventana_admin, text="Categoria ")
    categoriaPeli.grid(column=0, row=2)
    imagenPeli = Label(ventana_admin, text="Imagen")
    imagenPeli.grid(column=0, row=3)
    duracionPeli = Label(ventana_admin, text="Duracion")
    duracionPeli.grid(column=0, row=4)
    anioPeli = Label(ventana_admin, text="Año")
    anioPeli.grid(column=0, row=5)
    directorPeli = Label(ventana_admin, text="Director")
    directorPeli.grid(column=0, row=6)

    tituloEntry = Entry(ventana_admin, textvariable=StringVar())
    tituloEntry.grid(column=1, row=1)
    categoriaEntry = Entry(ventana_admin, textvariable=StringVar())
    categoriaEntry.grid(column=1, row=2)
    imagenEntry = Entry(ventana_admin, textvariable=StringVar())
    imagenEntry.grid(column=1, row=3)
    duracionEntry = Entry(ventana_admin, textvariable=StringVar())
    duracionEntry.grid(column=1, row=4)
    anioEntry = Entry(ventana_admin, textvariable=StringVar())
    anioEntry.grid(column=1, row=5)
    directorEntry = Entry(ventana_admin, textvariable=StringVar())
    directorEntry.grid(column=1, row=6)

    boton_registrar = ttk.Button(ventana_admin, text="Registrar", command=registrar_peli)
    boton_registrar.grid(column=0, row=8, sticky=W + E, columnspan=1)

    boton_salir = ttk.Button(ventana_admin, text="Salir", command=lambda: ventana_admin.destroy())
    boton_salir.grid(column=1, row=8, sticky=W + E, columnspan=1)

    mensaje = Label(ventana_admin, text="", fg="red")
    mensaje.grid(column=0, row=7, columnspan=2, sticky=W + E)


def editar_Peli():
    def eliminar():

        mensaje["text"] = ""
        try:
            tabla.item(tabla.selection())["values"][0]
        except IndexError as e:
            mensaje["fg"] = "red"
            mensaje["text"] = "Seleccione una pelicula"
            return
        db.session.query(Pelicula).filter(Pelicula.id == tabla.item(tabla.selection())["text"]).delete()
        db.session.commit()
        nombre = tabla.item(tabla.selection())["values"][0]
        mensaje["fg"] = "blue"
        mensaje['text'] = 'Pelicula {} eliminado con éxito'.format(nombre)

        get_peliculas()

    def get_peliculas():

        registros = tabla.get_children()

        for fila in registros:
            tabla.delete(fila)

        peliculas = db.session.query(Pelicula).all()

        for pelicula in peliculas:
            tabla.insert("", 0, text=pelicula.id, values=(pelicula.titulo,
                                                          pelicula.categoria,
                                                          pelicula.imagen,
                                                          pelicula.duracion,
                                                          pelicula.anio,
                                                          pelicula.director))

    def editar():

        mensaje["text"] = ""

        try:
            tabla.item(tabla.selection())["values"][0]
        except IndexError as e:
            mensaje["fg"] = "red"
            mensaje["text"] = "Selecciona una pelicula"
            return

        old_titulo = tabla.item(tabla.selection())["values"][0]
        old_categoria = tabla.item(tabla.selection())["values"][1]
        old_imagen = tabla.item(tabla.selection())["values"][2]
        old_duracion = tabla.item(tabla.selection())["values"][3]
        old_anio = tabla.item(tabla.selection())["values"][4]
        old_director = tabla.item(tabla.selection())["values"][5]

        ventana_editar = Toplevel()
        ventana_editar.title = "Edicion de peliculas"
        ventana_editar.resizable(False, False)

        # Configuracion ventana editar

        cabecera = Label(ventana_editar, text="Editar Pelicula", font=("calibri", 40, "bold"))
        cabecera.grid(column=0, row=0)

        frame_ep = LabelFrame(ventana_editar, text="Editar pelicula")
        frame_ep.grid(row=1, column=0, columnspan=2, pady=30, padx=30)

        etiqueta_titulo_antiguo = Label(frame_ep, text="Titulo antiguo")
        etiqueta_titulo_antiguo.grid(row=2, column=0)
        input_titulo_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_titulo),
                                     state="readonly")
        input_titulo_antiguo.grid(row=2, column=1)
        etiqueta_titulo_nuevo = Label(frame_ep, text="Titulo nuevo:")
        etiqueta_titulo_nuevo.grid(row=3, column=0)
        input_titulo_nuevo = Entry(frame_ep)
        input_titulo_nuevo.grid(row=3, column=1)

        etiqueta_categoria_antiguo = Label(frame_ep, text="Categoria Antigua")
        etiqueta_categoria_antiguo.grid(row=4, column=0)
        input_categoria_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_categoria),
                                        state="readonly")
        input_categoria_antiguo.grid(row=4, column=1)
        etiqueta_categoria_nuevo = Label(frame_ep, text="Categoria Nueva:")
        etiqueta_categoria_nuevo.grid(row=5, column=0)
        input_categoria_nuevo = Entry(frame_ep)
        input_categoria_nuevo.grid(row=5, column=1)

        etiqueta_imagen_antiguo = Label(frame_ep, text="Imagen Antigua")
        etiqueta_imagen_antiguo.grid(row=6, column=0)
        input_imagen_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_imagen),
                                     state="readonly")
        input_imagen_antiguo.grid(row=6, column=1)
        etiqueta_imagen_nuevo = Label(frame_ep, text="Imagen Nueva:")
        etiqueta_imagen_nuevo.grid(row=7, column=0)
        input_imagen_nuevo = Entry(frame_ep)
        input_imagen_nuevo.grid(row=7, column=1)

        etiqueta_duracion_antiguo = Label(frame_ep, text="Duracion Antigua")
        etiqueta_duracion_antiguo.grid(row=8, column=0)
        input_duracion_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_duracion),
                                       state="readonly")
        input_duracion_antiguo.grid(row=8, column=1)
        etiqueta_duracion_nuevo = Label(frame_ep, text="Duracion Nueva:")
        etiqueta_duracion_nuevo.grid(row=9, column=0)
        input_duracion_nuevo = Entry(frame_ep)
        input_duracion_nuevo.grid(row=9, column=1)

        etiqueta_anio_antiguo = Label(frame_ep, text="Año antiguo")
        etiqueta_anio_antiguo.grid(row=10, column=0)
        input_anio_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_anio), state="readonly")
        input_anio_antiguo.grid(row=10, column=1)
        etiqueta_anio_nuevo = Label(frame_ep, text="Año Nuevo:")
        etiqueta_anio_nuevo.grid(row=11, column=0)
        input_anio_nuevo = Entry(frame_ep)
        input_anio_nuevo.grid(row=11, column=1)

        etiqueta_director_antiguo = Label(frame_ep, text="Director Antiguo")
        etiqueta_director_antiguo.grid(row=12, column=0)
        input_director_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_director),
                                       state="readonly")
        input_director_antiguo.grid(row=12, column=1)
        etiqueta_director_nuevo = Label(frame_ep, text="Director Nuevo:")
        etiqueta_director_nuevo.grid(row=13, column=0)
        input_director_nuevo = Entry(frame_ep)
        input_director_nuevo.grid(row=13, column=1)

        boton_salir = ttk.Button(frame_ep, text="Salir", command=lambda: ventana_editar.destroy())
        boton_salir.grid(row=15, sticky=W + E, columnspan=2)

        # Boton de actuazlizar
        def actualiza():
            titulo = input_titulo_nuevo.get() if input_titulo_nuevo.get() != "" else old_titulo
            categoria = input_categoria_nuevo.get() if input_categoria_nuevo.get() != "" else old_categoria
            imagen = input_imagen_nuevo.get() if input_imagen_nuevo.get() != "" else old_imagen
            duracion = input_duracion_nuevo.get() if input_duracion_nuevo.get() != "" else old_duracion
            anio = input_anio_nuevo.get() if input_anio_nuevo.get() != "" else old_anio
            director = input_director_nuevo.get() if input_director_nuevo.get() != "" else old_director

            db.session.query(Pelicula).filter(Pelicula.id == tabla.item(tabla.selection())["text"]).update(
                {
                    Pelicula.titulo: titulo,
                    Pelicula.categoria: categoria,
                    Pelicula.imagen: imagen,
                    Pelicula.duracion: duracion,
                    Pelicula.anio: anio,
                    Pelicula.director: director
                }
            )
            db.session.commit()
            ventana_editar.destroy()
            get_peliculas()
            mensaje["fg"] = "blue"
            mensaje["text"] = f"Pelicula {old_titulo} actualizada"

        s = ttk.Style()
        s.configure("my.TButton")
        boton_actualizar = ttk.Button(frame_ep, text="Actualizar Pelicula", command=actualiza)
        boton_actualizar.grid(row=14, columnspan=2, sticky=W + E)

    # ---------------------------#
    ventana_admin = Toplevel()  # Crear una ventana por delante de la principal
    ventana_admin.title("Edicion de Peliculas")  # Titulo de la ventana

    mensaje = Label(ventana_admin, text="", fg="red")
    mensaje.grid(column=0, row=1, columnspan=2, sticky=W + E)

    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                    font=('Calibri', 10))  # Se modifica la fuente de la tabla
    style.configure("mystyle.Treeview.Heading",
                    font=('Calibri', 10, 'bold'))  # Se modifica la fuente de las cabeceras
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    # Estructura de la tabla de Peliculas
    tabla = ttk.Treeview(ventana_admin, height=10, columns=["#0", "#1", "#2", "#3", "#4", "#5", "#6"],
                         style="mystyle.Treeview")
    tabla.grid(row=0, column=0)
    tabla.heading(column="#0", text="ID", anchor=CENTER)
    tabla.heading(column="#1", text="Titulo", anchor=CENTER)
    tabla.heading(column="#2", text="Categoria", anchor=CENTER)
    tabla.heading(column="#3", text="Imagen", anchor=CENTER)
    tabla.heading(column="#4", text="Duracion", anchor=CENTER)
    tabla.heading(column="#5", text="Año", anchor=CENTER)
    tabla.heading(column="#6", text="Director", anchor=CENTER)

    get_peliculas()

    boton_eliminar = ttk.Button(ventana_admin, text="Eliminar", command=eliminar)
    boton_eliminar.grid(column=0, row=2, sticky=W + E)

    boton_editar = ttk.Button(ventana_admin, text="Editar", command=editar)
    boton_editar.grid(column=0, row=3, sticky=W + E)

    boton_salir = ttk.Button(ventana_admin, text="Salir", command=lambda: ventana_admin.destroy())
    boton_salir.grid(column=0, row=4, sticky=W + E)


# -----------------------------------Series------------------------------------------------(Lo mismo que con las pelis)

def add_serie():
    def registrar_serie():
        serie = Serie(
            tituloEntry.get(),
            categoriaEntry.get(),
            imagenEntry.get(),
            temporadasEntry.get(),
            capitulosEntry.get(),
            duracion_capitulos_serieEntry.get()
        )
        db.session.add(serie)
        db.session.commit()
        mensaje["fg"] = "blue"
        mensaje["text"] = f"Serie {tituloEntry.get()} añadida con exito"

    ventana_admin = Toplevel()  # Crear una ventana por delante de la principal
    ventana_admin.title("Registro de series")  # Titulo de la ventana
    ventana_admin.resizable(False, False)

    tituloSerie = Label(ventana_admin, text="Titulo ")
    tituloSerie.grid(column=0, row=1)
    categoriaSerie = Label(ventana_admin, text="Categoria ")
    categoriaSerie.grid(column=0, row=2)
    imagenSerie = Label(ventana_admin, text="Imagen")
    imagenSerie.grid(column=0, row=3)
    temporadasSerie = Label(ventana_admin, text="Temporadas")
    temporadasSerie.grid(column=0, row=4)
    capitulosSerie = Label(ventana_admin, text="Capitulos")
    capitulosSerie.grid(column=0, row=5)
    duracion_capitulos_serie = Label(ventana_admin, text="Duracion Capitulos")
    duracion_capitulos_serie.grid(column=0, row=6)

    tituloEntry = Entry(ventana_admin, textvariable=StringVar())
    tituloEntry.grid(column=1, row=1)
    categoriaEntry = Entry(ventana_admin, textvariable=StringVar())
    categoriaEntry.grid(column=1, row=2)
    imagenEntry = Entry(ventana_admin, textvariable=StringVar())
    imagenEntry.grid(column=1, row=3)
    temporadasEntry = Entry(ventana_admin, textvariable=StringVar())
    temporadasEntry.grid(column=1, row=4)
    capitulosEntry = Entry(ventana_admin, textvariable=StringVar())
    capitulosEntry.grid(column=1, row=5)
    duracion_capitulos_serieEntry = Entry(ventana_admin, textvariable=StringVar())
    duracion_capitulos_serieEntry.grid(column=1, row=6)

    boton_registrar = ttk.Button(ventana_admin, text="Registrar", command=registrar_serie)
    boton_registrar.grid(column=0, row=8, sticky=W + E)

    boton_salir = ttk.Button(ventana_admin, text="Salir", command=lambda: ventana_admin.destroy())
    boton_salir.grid(column=1, row=8, sticky=W + E)

    mensaje = Label(ventana_admin, text="", fg="red")
    mensaje.grid(column=0, row=7, columnspan=2, sticky=W + E)


def editar_Serie():
    def eliminar():

        mensaje["text"] = ""
        try:
            tabla.item(tabla.selection())["values"][0]
        except IndexError as e:
            mensaje["fg"] = "red"
            mensaje["text"] = "Seleccione una serie"
            return
        db.session.query(Serie).filter(Serie.id == tabla.item(tabla.selection())["text"]).delete()
        db.session.commit()
        nombre = tabla.item(tabla.selection())["values"][0]
        mensaje["fg"] = "blue"
        mensaje['text'] = 'Serie {} eliminada con éxito'.format(nombre)

        get_series()

    def get_series():

        registros = tabla.get_children()

        for fila in registros:
            tabla.delete(fila)

        series = db.session.query(Serie).all()

        for serie in series:
            tabla.insert("", 0, text=serie.id, values=(serie.titulo,
                                                       serie.categoria,
                                                       serie.imagen,
                                                       serie.temporadas,
                                                       serie.capitulos,
                                                       serie.duracion_capitulo))

    def editar():

        mensaje["text"] = ""

        try:
            tabla.item(tabla.selection())["values"][0]
        except IndexError as e:
            mensaje["fg"] = "red"
            mensaje["text"] = "Selecciona una serie"
            return

        old_titulo = tabla.item(tabla.selection())["values"][0]
        old_categoria = tabla.item(tabla.selection())["values"][1]
        old_imagen = tabla.item(tabla.selection())["values"][2]
        old_temporadas = tabla.item(tabla.selection())["values"][3]
        old_capitulos = tabla.item(tabla.selection())["values"][4]
        old_duracion_capitulo = tabla.item(tabla.selection())["values"][5]

        ventana_editar = Toplevel()
        ventana_editar.title = "Edicion de series"
        ventana_editar.resizable(False, False)

        # Configuracion ventana editar

        cabecera = Label(ventana_editar, text="Editar Serie", font=("calibri", 40, "bold"))
        cabecera.grid(column=0, row=0)

        frame_ep = LabelFrame(ventana_editar, text="Editar serie")
        frame_ep.grid(row=1, column=0, columnspan=2, pady=30, padx=30)

        etiqueta_titulo_antiguo = Label(frame_ep, text="Titulo antiguo")
        etiqueta_titulo_antiguo.grid(row=2, column=0)
        input_titulo_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_titulo),
                                     state="readonly")
        input_titulo_antiguo.grid(row=2, column=1)
        etiqueta_titulo_nuevo = Label(frame_ep, text="Titulo nuevo:")
        etiqueta_titulo_nuevo.grid(row=3, column=0)
        input_titulo_nuevo = Entry(frame_ep)
        input_titulo_nuevo.grid(row=3, column=1)

        etiqueta_categoria_antiguo = Label(frame_ep, text="Categoria Antigua")
        etiqueta_categoria_antiguo.grid(row=4, column=0)
        input_categoria_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_categoria),
                                        state="readonly")
        input_categoria_antiguo.grid(row=4, column=1)
        etiqueta_categoria_nuevo = Label(frame_ep, text="Categoria Nueva:")
        etiqueta_categoria_nuevo.grid(row=5, column=0)
        input_categoria_nuevo = Entry(frame_ep)
        input_categoria_nuevo.grid(row=5, column=1)

        etiqueta_imagen_antiguo = Label(frame_ep, text="Imagen Antigua")
        etiqueta_imagen_antiguo.grid(row=6, column=0)
        input_imagen_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_imagen),
                                     state="readonly")
        input_imagen_antiguo.grid(row=6, column=1)
        etiqueta_imagen_nuevo = Label(frame_ep, text="Imagen Nueva:")
        etiqueta_imagen_nuevo.grid(row=7, column=0)
        input_imagen_nuevo = Entry(frame_ep)
        input_imagen_nuevo.grid(row=7, column=1)

        etiqueta_temporadas_antiguo = Label(frame_ep, text="Temporadas antiguo")
        etiqueta_temporadas_antiguo.grid(row=8, column=0)
        input_temporadas_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_temporadas),
                                       state="readonly")
        input_temporadas_antiguo.grid(row=8, column=1)
        etiqueta_temporadas_nuevo = Label(frame_ep, text="Temporadas nuevo:")
        etiqueta_temporadas_nuevo.grid(row=9, column=0)
        input_temporadas_nuevo = Entry(frame_ep)
        input_temporadas_nuevo.grid(row=9, column=1)

        etiqueta_capitulos_antiguo = Label(frame_ep, text="Capitulos antiguo")
        etiqueta_capitulos_antiguo.grid(row=10, column=0)
        input_capitulos_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_capitulos), state="readonly")
        input_capitulos_antiguo.grid(row=10, column=1)
        etiqueta_capitulos_nuevo = Label(frame_ep, text="Capitulos nuevo:")
        etiqueta_capitulos_nuevo.grid(row=11, column=0)
        input_capitulos_nuevo = Entry(frame_ep)
        input_capitulos_nuevo.grid(row=11, column=1)

        etiqueta_duracioncapitulos_antiguo = Label(frame_ep, text="Duracion de capitulos antiguo")
        etiqueta_duracioncapitulos_antiguo.grid(row=12, column=0)
        input_duracioncapitulos_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_duracion_capitulo),
                                       state="readonly")
        input_duracioncapitulos_antiguo.grid(row=12, column=1)
        etiqueta_duracioncapitulos_nuevo = Label(frame_ep, text="Duracion de capitulos nuevo:")
        etiqueta_duracioncapitulos_nuevo.grid(row=13, column=0)
        input_duracioncapitulos_nuevo = Entry(frame_ep)
        input_duracioncapitulos_nuevo.grid(row=13, column=1)

        boton_salir = ttk.Button(frame_ep, text="Salir", command=lambda: ventana_editar.destroy())
        boton_salir.grid(row=15, sticky=W + E, columnspan=2)

        def actualiza():
            titulo = input_titulo_nuevo.get() if input_titulo_nuevo.get() != "" else old_titulo
            categoria = input_categoria_nuevo.get() if input_categoria_nuevo.get() != "" else old_categoria
            imagen = input_imagen_nuevo.get() if input_imagen_nuevo.get() != "" else old_imagen
            temporadas = input_temporadas_nuevo.get() if input_temporadas_nuevo.get() != "" else old_temporadas
            capitulos = input_temporadas_nuevo.get() if input_temporadas_nuevo.get() != "" else old_temporadas
            duracion_capitulos = input_duracioncapitulos_nuevo.get() if input_duracioncapitulos_nuevo.get() != "" else old_duracion_capitulo

            db.session.query(Serie).filter(Serie.id == tabla.item(tabla.selection())["text"]).update(
                {
                    Serie.titulo: titulo,
                    Serie.categoria: categoria,
                    Serie.imagen: imagen,
                    Serie.temporadas: temporadas,
                    Serie.capitulos: capitulos,
                    Serie.duracion_capitulo: duracion_capitulos
                }
            )
            db.session.commit()
            ventana_editar.destroy()
            get_series()
            mensaje["fg"] = "blue"
            mensaje["text"] = f"Pelicula {old_titulo} actualizada"

        s = ttk.Style()
        s.configure("my.TButton")
        boton_actualizar = ttk.Button(frame_ep, text="Actualizar Serie", command=actualiza)
        boton_actualizar.grid(row=14, columnspan=2, sticky=W + E)

    # ---------------------------#
    ventana_admin = Toplevel()  # Crear una ventana por delante de la principal
    ventana_admin.title("Edicion de Series")  # Titulo de la ventana

    mensaje = Label(ventana_admin, text="", fg="red")
    mensaje.grid(column=0, row=1, columnspan=2, sticky=W + E)

    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 10))  # Se modifica la fuente de la tabla
    style.configure("mystyle.Treeview.Heading",
                        font=('Calibri', 10, 'bold'))  # Se modifica la fuente de las cabeceras
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    # Estructura de la tabla de Peliculas
    tabla = ttk.Treeview(ventana_admin, height=10, columns=["#0", "#1", "#2", "#3", "#4", "#5", "#6"],
                             style="mystyle.Treeview")
    tabla.grid(row=0, column=0)
    tabla.heading(column="#0", text="ID", anchor=CENTER)
    tabla.heading(column="#1", text="Titulo", anchor=CENTER)
    tabla.heading(column="#2", text="Categoria", anchor=CENTER)
    tabla.heading(column="#3", text="Imagen", anchor=CENTER)
    tabla.heading(column="#4", text="Temporadas", anchor=CENTER)
    tabla.heading(column="#5", text="Capitulos", anchor=CENTER)
    tabla.heading(column="#6", text="Duracion de Capitulos", anchor=CENTER)

    get_series()

    boton_eliminar = ttk.Button(ventana_admin, text="Eliminar", command=eliminar)
    boton_eliminar.grid(column=0, row=2, sticky=W + E)

    boton_editar = ttk.Button(ventana_admin, text="Editar", command=editar)
    boton_editar.grid(column=0, row=3, sticky=W + E)

    boton_salir = ttk.Button(ventana_admin, text="Salir", command=lambda: ventana_admin.destroy())
    boton_salir.grid(column=0, row=4, sticky=W + E)
