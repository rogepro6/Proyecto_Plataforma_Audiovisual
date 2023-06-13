from tkinter import *
from tkinter import ttk

from database import db
from styles import styles
from models.audiovisual import Pelicula, Serie


def add_pelicula():
    titulo_pelicula = StringVar()
    categoria_pelicula = StringVar()
    imagen_pelicula = StringVar()
    duracion_pelicula = StringVar()
    anio_pelicula = StringVar()
    director_pelicula = StringVar()

    def registrar_peli():
        #Comprobación de que se rellenen todos los campos
        if len(tituloEntry.get()) and len(categoriaEntry.get()) and len(imagenEntry.get()) and \
                len(duracionEntry.get()) and len(anioEntry.get()) and len(directorEntry.get()):

            try:
                # Comprobación de que los datos introducidos son correctos y se pueden transformar en el tipo de
                # datos que pide nuestra BBDD
                pelicula = Pelicula(
                    str(tituloEntry.get()),
                    str(categoriaEntry.get()),
                    str(imagenEntry.get()),
                    float(duracionEntry.get()),
                    int(anioEntry.get()),
                    str(directorEntry.get())
                )
            except:
                mensaje["fg"] = "red"
                mensaje["text"] = "Los datos introducidos no son válidos"
            else:
                db.session.add(pelicula)
                db.session.commit()
                mensaje["fg"] = "blue"
                mensaje["text"] = f"Película {tituloEntry.get()} añadida con exito"
                titulo_pelicula.set("")
                categoria_pelicula.set("")
                imagen_pelicula.set("")
                duracion_pelicula.set("")
                anio_pelicula.set("")
                director_pelicula.set("")
        else:
            mensaje["fg"] = "red"
            mensaje["text"] = "Debe rellenar todos los campos"

    #Creacion de la ventana
    ventana_admin = Toplevel()  # Crear una ventana por delante de la principal
    ventana_admin.config(width=400, height=320, background=styles.BG_VENTANA)
    ventana_admin.title("Registro de peliculas")  # Título de la ventana
    ventana_admin.resizable(False, False)

    #Etiquetas de los campos
    tituloPeli = ttk.Label(ventana_admin, text="Titulo", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
    tituloPeli.grid(column=0, row=1, ipadx=5, ipady=5, padx=10, pady=10)
    categoriaPeli = ttk.Label(ventana_admin, text="Categoria", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
    categoriaPeli.grid(column=0, row=2, ipadx=5, ipady=5, padx=10, pady=10)
    imagenPeli = ttk.Label(ventana_admin, text="Imagen", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
    imagenPeli.grid(column=0, row=3, ipadx=5, ipady=5, padx=10, pady=10)
    duracionPeli = ttk.Label(ventana_admin, text="Duracion", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
    duracionPeli.grid(column=0, row=4, ipadx=5, ipady=5, padx=10, pady=10)
    anioPeli = ttk.Label(ventana_admin, text="Año", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
    anioPeli.grid(column=0, row=5, ipadx=5, ipady=5, padx=10, pady=10)
    directorPeli = ttk.Label(ventana_admin, text="Director", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
    directorPeli.grid(column=0, row=6, ipadx=5, ipady=5, padx=10, pady=10)

    #Entradas de texto de los campos
    tituloEntry = Entry(ventana_admin, textvariable=titulo_pelicula, font=styles.ENTRADAS_DE_TEXTO)
    tituloEntry.grid(column=1, row=1)
    categoriaEntry = Entry(ventana_admin, textvariable=categoria_pelicula, font=styles.ENTRADAS_DE_TEXTO)
    categoriaEntry.grid(column=1, row=2)
    imagenEntry = Entry(ventana_admin, textvariable=imagen_pelicula, font=styles.ENTRADAS_DE_TEXTO)
    imagenEntry.grid(column=1, row=3)
    duracionEntry = Entry(ventana_admin, textvariable=duracion_pelicula, font=styles.ENTRADAS_DE_TEXTO)
    duracionEntry.grid(column=1, row=4)
    anioEntry = Entry(ventana_admin, textvariable=anio_pelicula, font=styles.ENTRADAS_DE_TEXTO)
    anioEntry.grid(column=1, row=5)
    directorEntry = Entry(ventana_admin, textvariable=director_pelicula, font=styles.ENTRADAS_DE_TEXTO)
    directorEntry.grid(column=1, row=6)

    #Botones de acción
    boton_registrar = Button(ventana_admin, text="Registrar", foreground=styles.FG_BOTON,
                             activeforeground=styles.AFG_BOTON,
                             activebackground=styles.ABG_BOTON, command=registrar_peli)
    boton_registrar.grid(column=0, row=8, sticky=W + E, ipadx=5, ipady=5, padx=5, pady=5, columnspan=1)

    boton_salir = Button(ventana_admin, text="Salir", foreground=styles.FG_BOTON,
                         activeforeground=styles.AFG_BOTON,
                         activebackground=styles.ABG_BOTON_SALIR, command=lambda: ventana_admin.destroy())
    boton_salir.grid(column=1, row=8, sticky=W + E, ipadx=5, ipady=5, padx=5, pady=5, columnspan=1)

    #Mensaje de confirmación o error
    mensaje = Label(ventana_admin, text="", fg="red", background=styles.BG_VENTANA)
    mensaje.grid(column=0, row=7, columnspan=2, sticky=W + E)


def editar_Peli():

    def eliminar():

        mensaje["text"] = ""
        try:
            #Comprobacion de que se selecciona un registro
            tabla.item(tabla.selection())["values"][0]
        except IndexError:
            mensaje["fg"] = "red"
            mensaje["text"] = "Seleccione una pelicula"
            return
        else:
            #Eliminamos el registro y llamamos a la función de obtener todas las películas
            db.session.query(Pelicula).filter(Pelicula.id == tabla.item(tabla.selection())["text"]).delete()
            db.session.commit()
            nombre = tabla.item(tabla.selection())["values"][0]
            mensaje["fg"] = "blue"
            mensaje['text'] = 'Pelicula {} eliminado con éxito'.format(nombre)

            get_peliculas()

    def get_peliculas():
        # Función dedicada a eliminar los registros antiguos e introducir en la tabla todos los registros obtenidos
        # de la BBDD
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
        #Funcion dedicada a editar los contenidos audiovisuales
        mensaje["text"] = ""
        try:
            # Comprobación de que se selecciona un registro
            tabla.item(tabla.selection())["values"][0]
        except IndexError:
            mensaje["fg"] = "red"
            mensaje["text"] = "Seleccione una pelicula"
            return

        #Obtención de los datos antiguos del registro
        old_titulo = tabla.item(tabla.selection())["values"][0]
        old_categoria = tabla.item(tabla.selection())["values"][1]
        old_imagen = tabla.item(tabla.selection())["values"][2]
        old_duracion = tabla.item(tabla.selection())["values"][3]
        old_anio = tabla.item(tabla.selection())["values"][4]
        old_director = tabla.item(tabla.selection())["values"][5]

        #Creacion de la ventana
        ventana_editar = Toplevel()
        ventana_editar.title("Edicion de peliculas")
        ventana_editar.config(width=400, height=320, background=styles.BG_VENTANA)
        ventana_editar.resizable(False, False)

        # Configuración ventana editar
        cabecera = Label(ventana_editar, text="Editar Pelicula", font=styles.ENCABEZADOS,
                         background=styles.BG_ETIQUETA, anchor=CENTER)
        cabecera.grid(column=0, row=0, padx=10, pady=10)

        frame_ep = LabelFrame(ventana_editar, text="Editar pelicula", font=styles.TEXTOS, background=styles.BG_ETIQUETA)
        frame_ep.grid(row=1, column=0, columnspan=2, pady=30, padx=30, ipadx=5, ipady=5)

        etiqueta_titulo_antiguo = Label(frame_ep, text="Titulo antiguo", background=styles.BG_ETIQUETA,
                                        font=styles.TEXTOS)
        etiqueta_titulo_antiguo.grid(row=2, column=0, ipadx=5, ipady=5)
        input_titulo_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_titulo),
                                     state="readonly", font=styles.ENTRADAS_DE_TEXTO)
        input_titulo_antiguo.grid(row=2, column=1, ipadx=5, ipady=5)
        etiqueta_titulo_nuevo = Label(frame_ep, text="Titulo nuevo", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
        etiqueta_titulo_nuevo.grid(row=3, column=0, ipadx=5, ipady=5)
        input_titulo_nuevo = Entry(frame_ep, font=styles.ENTRADAS_DE_TEXTO)
        input_titulo_nuevo.grid(row=3, column=1, ipadx=5, ipady=5)

        etiqueta_categoria_antiguo = Label(frame_ep, text="Categoria Antigua", background=styles.BG_ETIQUETA,
                                           font=styles.TEXTOS)
        etiqueta_categoria_antiguo.grid(row=4, column=0, ipadx=5, ipady=5)
        input_categoria_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_categoria),
                                        state="readonly", font=styles.ENTRADAS_DE_TEXTO)
        input_categoria_antiguo.grid(row=4, column=1, ipadx=5, ipady=5)
        etiqueta_categoria_nuevo = Label(frame_ep, text="Categoria Nueva", background=styles.BG_ETIQUETA,
                                         font=styles.TEXTOS)
        etiqueta_categoria_nuevo.grid(row=5, column=0, ipadx=5, ipady=5)
        input_categoria_nuevo = Entry(frame_ep, font=styles.ENTRADAS_DE_TEXTO)
        input_categoria_nuevo.grid(row=5, column=1, ipadx=5, ipady=5)

        etiqueta_imagen_antiguo = Label(frame_ep, text="Imagen Antigua", background=styles.BG_ETIQUETA,
                                        font=styles.TEXTOS)
        etiqueta_imagen_antiguo.grid(row=6, column=0, ipadx=5, ipady=5)
        input_imagen_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_imagen),
                                     state="readonly", font=styles.ENTRADAS_DE_TEXTO)
        input_imagen_antiguo.grid(row=6, column=1, ipadx=5, ipady=5)
        etiqueta_imagen_nuevo = Label(frame_ep, text="Imagen Nueva", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
        etiqueta_imagen_nuevo.grid(row=7, column=0, ipadx=5, ipady=5)
        input_imagen_nuevo = Entry(frame_ep, font=styles.ENTRADAS_DE_TEXTO)
        input_imagen_nuevo.grid(row=7, column=1, ipadx=5, ipady=5)

        etiqueta_duracion_antiguo = Label(frame_ep, text="Duracion Antigua", background=styles.BG_ETIQUETA,
                                          font=styles.TEXTOS)
        etiqueta_duracion_antiguo.grid(row=8, column=0, ipadx=5, ipady=5)
        input_duracion_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_duracion),
                                       state="readonly", font=styles.ENTRADAS_DE_TEXTO)
        input_duracion_antiguo.grid(row=8, column=1, ipadx=5, ipady=5)
        etiqueta_duracion_nuevo = Label(frame_ep, text="Duracion Nueva", background=styles.BG_ETIQUETA,
                                        font=styles.TEXTOS)
        etiqueta_duracion_nuevo.grid(row=9, column=0, ipadx=5, ipady=5)
        input_duracion_nuevo = Entry(frame_ep, font=styles.ENTRADAS_DE_TEXTO)
        input_duracion_nuevo.grid(row=9, column=1, ipadx=5, ipady=5)

        etiqueta_anio_antiguo = Label(frame_ep, text="Año antiguo", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
        etiqueta_anio_antiguo.grid(row=10, column=0, ipadx=5, ipady=5)
        input_anio_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_anio), state="readonly",
                                   font=styles.ENTRADAS_DE_TEXTO)
        input_anio_antiguo.grid(row=10, column=1, ipadx=5, ipady=5)
        etiqueta_anio_nuevo = Label(frame_ep, text="Año Nuevo", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
        etiqueta_anio_nuevo.grid(row=11, column=0, ipadx=5, ipady=5)
        input_anio_nuevo = Entry(frame_ep, font=styles.ENTRADAS_DE_TEXTO)
        input_anio_nuevo.grid(row=11, column=1, ipadx=5, ipady=5)

        etiqueta_director_antiguo = Label(frame_ep, text="Director Antiguo", background=styles.BG_ETIQUETA,
                                          font=styles.TEXTOS)
        etiqueta_director_antiguo.grid(row=12, column=0, ipadx=5, ipady=5)
        input_director_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_director),
                                       state="readonly", font=styles.ENTRADAS_DE_TEXTO)
        input_director_antiguo.grid(row=12, column=1, ipadx=5, ipady=5)
        etiqueta_director_nuevo = Label(frame_ep, text="Director Nuevo", background=styles.BG_ETIQUETA,
                                        font=styles.TEXTOS)
        etiqueta_director_nuevo.grid(row=13, column=0, ipadx=5, ipady=5)
        input_director_nuevo = Entry(frame_ep, font=styles.ENTRADAS_DE_TEXTO)
        input_director_nuevo.grid(row=13, column=1, ipadx=5, ipady=5)

        #Boton de salir
        boton_salir = Button(frame_ep, text="Salir", foreground=styles.FG_BOTON,
                             activeforeground=styles.AFG_BOTON,
                             activebackground=styles.ABG_BOTON_SALIR, command=lambda: ventana_editar.destroy())
        boton_salir.grid(row=15, sticky=W + E, columnspan=2)

        # Función del botón de actualizar
        def actualiza():
            #Si se introduce un campo nuevo se coge, si se deja en blanco se coge el valor del campo antiguo
            titulo = input_titulo_nuevo.get() if input_titulo_nuevo.get() != "" else old_titulo
            categoria = input_categoria_nuevo.get() if input_categoria_nuevo.get() != "" else old_categoria
            imagen = input_imagen_nuevo.get() if input_imagen_nuevo.get() != "" else old_imagen
            duracion = input_duracion_nuevo.get() if input_duracion_nuevo.get() != "" else old_duracion
            anio = input_anio_nuevo.get() if input_anio_nuevo.get() != "" else old_anio
            director = input_director_nuevo.get() if input_director_nuevo.get() != "" else old_director

            try:
                # Comprobación de que los datos introducidos sean casteables al tipo de dato requerido por la BBDD y
                # llamada al método update que actualiza el registro
                db.session.query(Pelicula).filter(Pelicula.id == tabla.item(tabla.selection())["text"]).update(
                    {
                        Pelicula.titulo: str(titulo),
                        Pelicula.categoria: str(categoria),
                        Pelicula.imagen: str(imagen),
                        Pelicula.duracion: float(duracion),
                        Pelicula.anio: int(anio),
                        Pelicula.director: str(director)
                    }
                )
            except:
                mensaje["fg"] = "red"
                mensaje["text"] = "Los datos introducidos no son correctos"
            else:
                # Si no hay error guardamos cambios, cerramos la ventana y volvemos a mostrar los registros
                db.session.commit()
                ventana_editar.destroy()
                get_peliculas()
                mensaje["fg"] = "blue"
                mensaje["text"] = f"Pelicula {old_titulo} actualizada"

        s = ttk.Style()
        s.configure("my.TButton")

        #Botón actualizar
        boton_actualizar = Button(frame_ep, text="Actualizar Pelicula", foreground=styles.FG_BOTON,
                                  activeforeground=styles.AFG_BOTON,
                                  activebackground=styles.ABG_BOTON, command=actualiza)
        boton_actualizar.grid(row=14, columnspan=2, sticky=W + E)

    # Aquí terminamos de configurar las opciones de la edición de películas
    #Configuracion de la ventana
    ventana_admin = Toplevel()  # Crear una ventana por delante de la principal
    ventana_admin.config(width=400, height=320, background=styles.BG_VENTANA)
    ventana_admin.resizable(False, False)
    ventana_admin.title("Edición de Películas")  # Titulo de la ventana

    mensaje = Label(ventana_admin, text="", fg="red", background=styles.BG_VENTANA)
    mensaje.grid(column=0, row=1, columnspan=2, sticky=W + E)

    #Creación de la tabla
    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                    font=styles.TABLAS)  # Se modifica la fuente de la tabla
    style.configure("mystyle.Treeview.Heading",
                    font=styles.TABLAS_CABECERAS)  # Se modifica la fuente de las cabeceras
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    # Estructura de la tabla
    tabla = ttk.Treeview(ventana_admin, height=10, columns=["#0", "#1", "#2", "#3", "#4", "#5", "#6"],
                         style="mystyle.Treeview")
    tabla.grid(row=0, column=0, ipadx=5, ipady=5, padx=10, pady=10)
    tabla.heading(column="#0", text="ID", anchor=CENTER)
    tabla.heading(column="#1", text="Titulo", anchor=CENTER)
    tabla.heading(column="#2", text="Categoria", anchor=CENTER)
    tabla.heading(column="#3", text="Imagen", anchor=CENTER)
    tabla.heading(column="#4", text="Duracion", anchor=CENTER)
    tabla.heading(column="#5", text="Año", anchor=CENTER)
    tabla.heading(column="#6", text="Director", anchor=CENTER)

    #Llamada a la función que introduce los datos en la tabla
    get_peliculas()

    #Botonos de acción de la tabla
    boton_eliminar = Button(ventana_admin, text="Eliminar", foreground=styles.FG_BOTON,
                            activeforeground=styles.AFG_BOTON,
                            activebackground=styles.ABG_BOTON, command=eliminar)
    boton_eliminar.grid(column=0, row=2, sticky=W + E)

    boton_editar = Button(ventana_admin, text="Editar", foreground=styles.FG_BOTON,
                          activeforeground=styles.AFG_BOTON,
                          activebackground=styles.ABG_BOTON, command=editar)
    boton_editar.grid(column=0, row=3, sticky=W + E)

    boton_salir = Button(ventana_admin, text="Salir", foreground=styles.FG_BOTON,
                         activeforeground=styles.AFG_BOTON,
                         activebackground=styles.ABG_BOTON_SALIR, command=lambda: ventana_admin.destroy())
    boton_salir.grid(column=0, row=4, sticky=W + E)


# -----------------------------------Series------------------------------------------------(Lo mismo que con las pelis)

def add_serie():
    titulo_serie = StringVar()
    categoria_serie = StringVar()
    imagen_serie = StringVar()
    temporadas_serie = StringVar()
    capitulos_serie = StringVar()
    duracionCapitulos_serie = StringVar()

    def registrar_serie():
        if len(tituloEntry.get()) and len(categoriaEntry.get()) and len(imagenEntry.get()) and \
                len(temporadasEntry.get()) and len(capitulosEntry.get()) and len(duracion_capitulos_serieEntry.get()):
            try:
                serie = Serie(
                    str(tituloEntry.get()),
                    str(categoriaEntry.get()),
                    str(imagenEntry.get()),
                    int(temporadasEntry.get()),
                    int(capitulosEntry.get()),
                    float(duracion_capitulos_serieEntry.get())
                )
            except:
                mensaje["fg"] = "red"
                mensaje["text"] = "Los datos introducidos no son válidos"
            else:
                db.session.add(serie)
                db.session.commit()
                mensaje["fg"] = "blue"
                mensaje["text"] = f"Serie {tituloEntry.get()} añadida con exito"
                titulo_serie.set("")
                categoria_serie.set("")
                imagen_serie.set("")
                temporadas_serie.set("")
                capitulos_serie.set("")
                duracionCapitulos_serie.set("")
        else:
            mensaje["fg"] = "red"
            mensaje["text"] = "Debe introducir todos los datos"

    ventana_admin = Toplevel()  # Crear una ventana por delante de la principal
    ventana_admin.config(width=400, height=320, background=styles.BG_VENTANA)
    ventana_admin.title("Registro de series")  # Titulo de la ventana
    ventana_admin.resizable(False, False)

    tituloSerie = ttk.Label(ventana_admin, text="Titulo", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
    tituloSerie.grid(column=0, row=1, ipadx=5, ipady=5, padx=10, pady=10)
    categoriaSerie = Label(ventana_admin, text="Categoria", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
    categoriaSerie.grid(column=0, row=2, ipadx=5, ipady=5, padx=10, pady=10)
    imagenSerie = Label(ventana_admin, text="Imagen", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
    imagenSerie.grid(column=0, row=3, ipadx=5, ipady=5, padx=10, pady=10)
    temporadasSerie = Label(ventana_admin, text="Temporadas", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
    temporadasSerie.grid(column=0, row=4, ipadx=5, ipady=5, padx=10, pady=10)
    capitulosSerie = Label(ventana_admin, text="Capitulos", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
    capitulosSerie.grid(column=0, row=5, ipadx=5, ipady=5, padx=10, pady=10)
    duracion_capitulos_serie = Label(ventana_admin, text="Duracion Capitulos", background=styles.BG_ETIQUETA,
                                     font=styles.TEXTOS)
    duracion_capitulos_serie.grid(column=0, row=6, ipadx=5, ipady=5, padx=10, pady=10)

    tituloEntry = Entry(ventana_admin, textvariable=titulo_serie, font=styles.ENTRADAS_DE_TEXTO)
    tituloEntry.grid(column=1, row=1)
    categoriaEntry = Entry(ventana_admin, textvariable=categoria_serie, font=styles.ENTRADAS_DE_TEXTO)
    categoriaEntry.grid(column=1, row=2)
    imagenEntry = Entry(ventana_admin, textvariable=imagen_serie, font=styles.ENTRADAS_DE_TEXTO)
    imagenEntry.grid(column=1, row=3)
    temporadasEntry = Entry(ventana_admin, textvariable=temporadas_serie, font=styles.ENTRADAS_DE_TEXTO)
    temporadasEntry.grid(column=1, row=4)
    capitulosEntry = Entry(ventana_admin, textvariable=capitulos_serie, font=styles.ENTRADAS_DE_TEXTO)
    capitulosEntry.grid(column=1, row=5)
    duracion_capitulos_serieEntry = Entry(ventana_admin, textvariable=duracionCapitulos_serie,
                                          font=styles.ENTRADAS_DE_TEXTO)
    duracion_capitulos_serieEntry.grid(column=1, row=6)

    boton_registrar = Button(ventana_admin, text="Registrar", foreground=styles.FG_BOTON,
                             activeforeground=styles.AFG_BOTON,
                             activebackground=styles.ABG_BOTON, command=registrar_serie)
    boton_registrar.grid(column=0, row=8, sticky=W + E, ipadx=5, ipady=5, padx=5, pady=5, columnspan=1)

    boton_salir = Button(ventana_admin, text="Salir", foreground=styles.FG_BOTON,
                         activeforeground=styles.AFG_BOTON,
                         activebackground=styles.ABG_BOTON_SALIR, command=lambda: ventana_admin.destroy())
    boton_salir.grid(column=1, row=8, sticky=W + E, ipadx=5, ipady=5, padx=5, pady=5, columnspan=1)

    mensaje = Label(ventana_admin, text="", fg="red", background=styles.BG_VENTANA)
    mensaje.grid(column=0, row=7, columnspan=2, sticky=W + E)


def editar_Serie():
    def eliminar():

        mensaje["text"] = ""
        try:
            tabla.item(tabla.selection())["values"][0]
        except IndexError:
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
        except IndexError:
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
        ventana_editar.title("Edicion de series")
        ventana_editar.config(width=400, height=320, background=styles.BG_VENTANA)
        ventana_editar.resizable(False, False)

        # Configuración ventana editar

        cabecera = Label(ventana_editar, text="Editar Serie", font=styles.ENCABEZADOS,
                         background=styles.BG_ETIQUETA, anchor=CENTER)
        cabecera.grid(column=0, row=0, padx=10, pady=10)

        frame_ep = LabelFrame(ventana_editar, text="Editar serie", font=styles.TEXTOS, background=styles.BG_ETIQUETA)
        frame_ep.grid(row=1, column=0, columnspan=2, pady=30, padx=30, ipadx=5, ipady=5)

        etiqueta_titulo_antiguo = Label(frame_ep, text="Título antiguo", background=styles.BG_ETIQUETA,
                                        font=styles.TEXTOS)
        etiqueta_titulo_antiguo.grid(row=2, column=0, ipadx=5, ipady=5)
        input_titulo_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_titulo),
                                     state="readonly", font=styles.ENTRADAS_DE_TEXTO)
        input_titulo_antiguo.grid(row=2, column=1, ipadx=5, ipady=5)
        etiqueta_titulo_nuevo = Label(frame_ep, text="Título nuevo", background=styles.BG_ETIQUETA,
                                      font=styles.TEXTOS)
        etiqueta_titulo_nuevo.grid(row=3, column=0, ipadx=5, ipady=5)
        input_titulo_nuevo = Entry(frame_ep, font=styles.ENTRADAS_DE_TEXTO)
        input_titulo_nuevo.grid(row=3, column=1, ipadx=5, ipady=5)

        etiqueta_categoria_antiguo = Label(frame_ep, text="Categoría Antigua", background=styles.BG_ETIQUETA,
                                           font=styles.TEXTOS)
        etiqueta_categoria_antiguo.grid(row=4, column=0, ipadx=5, ipady=5)
        input_categoria_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_categoria),
                                        state="readonly", font=styles.ENTRADAS_DE_TEXTO)
        input_categoria_antiguo.grid(row=4, column=1, ipadx=5, ipady=5)
        etiqueta_categoria_nuevo = Label(frame_ep, text="Categoría Nueva", background=styles.BG_ETIQUETA,
                                         font=styles.TEXTOS)
        etiqueta_categoria_nuevo.grid(row=5, column=0, ipadx=5, ipady=5)
        input_categoria_nuevo = Entry(frame_ep, font=styles.ENTRADAS_DE_TEXTO)
        input_categoria_nuevo.grid(row=5, column=1, ipadx=5, ipady=5)

        etiqueta_imagen_antiguo = Label(frame_ep, text="Imagen Antigua", background=styles.BG_ETIQUETA,
                                        font=styles.TEXTOS)
        etiqueta_imagen_antiguo.grid(row=6, column=0, ipadx=5, ipady=5)
        input_imagen_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_imagen),
                                     state="readonly", font=styles.ENTRADAS_DE_TEXTO)
        input_imagen_antiguo.grid(row=6, column=1, ipadx=5, ipady=5)
        etiqueta_imagen_nuevo = Label(frame_ep, text="Imagen Nueva", background=styles.BG_ETIQUETA,
                                      font=styles.TEXTOS)
        etiqueta_imagen_nuevo.grid(row=7, column=0, ipadx=5, ipady=5)
        input_imagen_nuevo = Entry(frame_ep, font=styles.ENTRADAS_DE_TEXTO)
        input_imagen_nuevo.grid(row=7, column=1, ipadx=5, ipady=5)

        etiqueta_temporadas_antiguo = Label(frame_ep, text="Temporadas antiguo", background=styles.BG_ETIQUETA,
                                            font=styles.TEXTOS)
        etiqueta_temporadas_antiguo.grid(row=8, column=0, ipadx=5, ipady=5)
        input_temporadas_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_temporadas),
                                         state="readonly", font=styles.ENTRADAS_DE_TEXTO)
        input_temporadas_antiguo.grid(row=8, column=1, ipadx=5, ipady=5)
        etiqueta_temporadas_nuevo = Label(frame_ep, text="Temporadas nuevo", background=styles.BG_ETIQUETA,
                                          font=styles.TEXTOS)
        etiqueta_temporadas_nuevo.grid(row=9, column=0, ipadx=5, ipady=5)
        input_temporadas_nuevo = Entry(frame_ep, font=styles.ENTRADAS_DE_TEXTO)
        input_temporadas_nuevo.grid(row=9, column=1, ipadx=5, ipady=5)

        etiqueta_capitulos_antiguo = Label(frame_ep, text="Capítulos antiguo", background=styles.BG_ETIQUETA,
                                           font=styles.TEXTOS)
        etiqueta_capitulos_antiguo.grid(row=10, column=0, ipadx=5, ipady=5)
        input_capitulos_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_capitulos),
                                        state="readonly", font=styles.ENTRADAS_DE_TEXTO)
        input_capitulos_antiguo.grid(row=10, column=1, ipadx=5, ipady=5)
        etiqueta_capitulos_nuevo = Label(frame_ep, text="Capítulos nuevo", background=styles.BG_ETIQUETA,
                                         font=styles.TEXTOS)
        etiqueta_capitulos_nuevo.grid(row=11, column=0, ipadx=5, ipady=5)
        input_capitulos_nuevo = Entry(frame_ep, font=styles.ENTRADAS_DE_TEXTO)
        input_capitulos_nuevo.grid(row=11, column=1, ipadx=5, ipady=5)

        etiqueta_duracioncapitulos_antiguo = Label(frame_ep, text="Duración de capítulos antiguo",
                                                   background=styles.BG_ETIQUETA,
                                                   font=styles.TEXTOS)
        etiqueta_duracioncapitulos_antiguo.grid(row=12, column=0, ipadx=5, ipady=5)
        input_duracioncapitulos_antiguo = Entry(frame_ep,
                                                textvariable=StringVar(ventana_editar, value=old_duracion_capitulo),
                                                state="readonly", font=styles.ENTRADAS_DE_TEXTO)
        input_duracioncapitulos_antiguo.grid(row=12, column=1, ipadx=5, ipady=5)
        etiqueta_duracioncapitulos_nuevo = Label(frame_ep, text="Duración de capítulos nuevo",
                                                 background=styles.BG_ETIQUETA,
                                                 font=styles.TEXTOS)
        etiqueta_duracioncapitulos_nuevo.grid(row=13, column=0, ipadx=5, ipady=5)
        input_duracioncapitulos_nuevo = Entry(frame_ep, font=styles.ENTRADAS_DE_TEXTO)
        input_duracioncapitulos_nuevo.grid(row=13, column=1, ipadx=5, ipady=5)

        boton_salir = Button(frame_ep, text="Salir",foreground=styles.FG_BOTON,
                             activeforeground=styles.AFG_BOTON,
                             activebackground=styles.ABG_BOTON_SALIR, command=lambda: ventana_editar.destroy())
        boton_salir.grid(row=15, sticky=W + E, columnspan=2)

        def actualiza():
            titulo = input_titulo_nuevo.get() if input_titulo_nuevo.get() != "" else old_titulo
            categoria = input_categoria_nuevo.get() if input_categoria_nuevo.get() != "" else old_categoria
            imagen = input_imagen_nuevo.get() if input_imagen_nuevo.get() != "" else old_imagen
            temporadas = input_temporadas_nuevo.get() if input_temporadas_nuevo.get() != "" else old_temporadas
            capitulos = input_capitulos_nuevo.get() if input_capitulos_nuevo.get() != "" else old_capitulos
            duracion_capitulos = input_duracioncapitulos_nuevo.get() if input_duracioncapitulos_nuevo.get() != "" else old_duracion_capitulo

            try:
                db.session.query(Serie).filter(Serie.id == tabla.item(tabla.selection())["text"]).update(
                    {
                        Serie.titulo: str(titulo),
                        Serie.categoria: str(categoria),
                        Serie.imagen: str(imagen),
                        Serie.temporadas: int(temporadas),
                        Serie.capitulos: int(capitulos),
                        Serie.duracion_capitulo: float(duracion_capitulos)
                    }
                )
            except:
                mensaje["fg"] = "red"
                mensaje["text"] = "Los datos introducidos no son correctos"
            else:
                db.session.commit()
                ventana_editar.destroy()
                get_series()
                mensaje["fg"] = "blue"
                mensaje["text"] = f"Serie {old_titulo} actualizada"

        s = ttk.Style()
        s.configure("my.TButton")
        boton_actualizar = Button(frame_ep, text="Actualizar Serie", foreground=styles.FG_BOTON,
                                  activeforeground=styles.AFG_BOTON,
                                  activebackground=styles.ABG_BOTON, command=actualiza)
        boton_actualizar.grid(row=14, columnspan=2, sticky=W + E)

    # ---------------------------#
    ventana_admin = Toplevel()  # Crear una ventana por delante de la principal
    ventana_admin.config(width=400, height=320, background=styles.BG_VENTANA)
    ventana_admin.resizable(False, False)
    ventana_admin.title("Edición de Series")  # Título de la ventana

    mensaje = Label(ventana_admin, text="", fg="red", background=styles.BG_VENTANA)
    mensaje.grid(column=0, row=1, columnspan=2, sticky=W + E)

    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                    font=styles.TABLAS)  # Se modifica la fuente de la tabla
    style.configure("mystyle.Treeview.Heading",
                    font=styles.TABLAS_CABECERAS)  # Se modifica la fuente de las cabeceras
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    # Estructura de la tabla de Series
    tabla = ttk.Treeview(ventana_admin, height=10, columns=["#0", "#1", "#2", "#3", "#4", "#5", "#6"],
                         style="mystyle.Treeview")
    tabla.grid(row=0, column=0, ipadx=5, ipady=5, padx=10, pady=10)
    tabla.heading(column="#0", text="ID", anchor=CENTER)
    tabla.heading(column="#1", text="Titulo", anchor=CENTER)
    tabla.heading(column="#2", text="Categoria", anchor=CENTER)
    tabla.heading(column="#3", text="Imagen", anchor=CENTER)
    tabla.heading(column="#4", text="Temporadas", anchor=CENTER)
    tabla.heading(column="#5", text="Capitulos", anchor=CENTER)
    tabla.heading(column="#6", text="Duracion de Capitulos", anchor=CENTER)

    get_series()

    boton_eliminar = Button(ventana_admin, text="Eliminar", foreground=styles.FG_BOTON,
                            activeforeground=styles.AFG_BOTON,
                            activebackground=styles.ABG_BOTON, command=eliminar)
    boton_eliminar.grid(column=0, row=2, sticky=W + E)

    boton_editar = Button(ventana_admin, text="Editar", foreground=styles.FG_BOTON,
                          activeforeground=styles.AFG_BOTON,
                          activebackground=styles.ABG_BOTON, command=editar)
    boton_editar.grid(column=0, row=3, sticky=W + E)

    boton_salir = Button(ventana_admin, text="Salir", foreground=styles.FG_BOTON,
                         activeforeground=styles.AFG_BOTON,
                         activebackground=styles.ABG_BOTON_SALIR, command=lambda: ventana_admin.destroy())
    boton_salir.grid(column=0, row=4, sticky=W + E)
