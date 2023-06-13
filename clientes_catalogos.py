from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from functools import partial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from database import db
from styles import styles
from models.audiovisual import Pelicula, Serie
from clientes_busquedas import dict_peliculas_audiovisual, dict_series_audiovisual


def mostrar_catalogos(resultados, audiovisual, nombre, tipo=None):

    #Creacion de la ventana y configuración
    ventana_mostrar = Toplevel()
    ventana_mostrar.config(width=400, height=320, background=styles.BG_VENTANA)
    ventana_mostrar.title("Resultados busqueda")  # Título de la ventana
    ventana_mostrar.resizable(False, False)

    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                    font=styles.TABLAS)  # Se modifica la fuente de la tabla
    style.configure("mystyle.Treeview.Heading",
                    font=styles.TABLAS_CABECERAS)  # Se modifica la fuente de las cabeceras
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    # Estructura de la tabla general
    tabla = ttk.Treeview(ventana_mostrar, height=10, columns=["#0", "#1", "#2", "#3", "#4", "#5", "#6"],
                         style="mystyle.Treeview")
    tabla.grid(row=0, column=0, ipadx=5, ipady=5, padx=10, pady=10)
    tabla.heading(column="#0", text="ID", anchor=CENTER)
    tabla.heading(column="#1", text="Titulo", anchor=CENTER)
    tabla.heading(column="#2", text="Categoria", anchor=CENTER)
    tabla.heading(column="#3", text="Imagen", anchor=CENTER)

    def ver_imagen():
        # Función que muestra en la pantalla la imagen de la carpeta recursos de cada película o serie
        try:
            foto = tabla.item(tabla.selection())["values"][2]
            nombre_registro = tabla.item(tabla.selection())["values"][0]
        except IndexError:
            mensaje["fg"] = "red"
            mensaje["text"] = "Seleccione un registro"
        else:
            ventana_imagen = Toplevel()
            ventana_imagen.title(f"Imagen de portada de {nombre_registro}")  # Título de la ventana
            ventana_imagen.config(width=400, height=320, background=styles.BG_VENTANA)
            ventana_imagen.resizable(True, True)
            img = PhotoImage(file=f"recursos/{str(foto)}")
            label_imagen = Label(ventana_imagen, image=img)
            label_imagen.pack()
            ventana_imagen.mainloop()

    def eliminar(diccionario, tipo, nombre):
        # Función para eliminar los registros de cada una de las listas de los usuarios
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
        # Parte de la tabla asociado a las películas
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
        # Parte de la tabla asociado a las series
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

    imagen_portada = Button(ventana_mostrar, text="Ver imagen", foreground=styles.FG_BOTON,
                            activeforeground=styles.AFG_BOTON,
                            activebackground=styles.ABG_BOTON, command=ver_imagen)
    imagen_portada.grid(row=3, column=0, columnspan=3, sticky=W + E)

    boton_salir = Button(ventana_mostrar, text="Salir", foreground=styles.FG_BOTON,
                         activeforeground=styles.AFG_BOTON,
                         activebackground=styles.ABG_BOTON_SALIR,
                         command=lambda: ventana_mostrar.destroy())
    boton_salir.grid(row=4, column=0, columnspan=3, sticky=W + E)


def catalogo_completo(audiovisual, nombre):
    # Esta función llama a la función mostrar_catálogos enviando todas las películas o series de la BBDD
    if audiovisual == "Pelicula":
        peliculas = db.session.query(Pelicula).all()
        mostrar_catalogos(peliculas, "Pelicula", nombre)
    elif audiovisual == "Serie":
        series = db.session.query(Serie).all()
        mostrar_catalogos(series, "Serie", nombre)


def listas_usuarios(audiovisual, tipo, nombre):
    # Esta función es encargada de llamar a la función mostrar_catálogos con los parámetros requeridos
    if audiovisual == "Pelicula":
        peliculas = []
        try:
            titulos = dict_peliculas_audiovisual[str(nombre) + tipo]
            for i in titulos:
                peliculas.append(db.session.query(Pelicula).filter(Pelicula.titulo == i).first())
            mostrar_catalogos(peliculas, "Pelicula", nombre, tipo=tipo)
        except KeyError:
            mb.showwarning("Error", "No tiene ninguna película en esta sección")
    elif audiovisual == "Serie":
        series = []
        try:
            titulos = dict_series_audiovisual[str(nombre) + tipo]
            for i in titulos:
                series.append(db.session.query(Serie).filter(Serie.titulo == i).first())
            mostrar_catalogos(series, "Serie", nombre, tipo=tipo)
        except KeyError:
            mb.showwarning("Error", "No tiene ninguna serie en esta sección")


def config_grafica(grafica, ventana):
    # Esta función la llaman todas las demás gráficas del programa y lo que hace es recibir la propia gráfica y la
    # ventana donde será colocada y las coloca en el área de trabajo y crea una barra de iconos que deja realizar
    # algunos ajustes sobre la gráfica
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
        # Líneas propensas de error si el usuario intenta visualizar las gráficas sin haber introducido ninguna
        # película y serie en la sección de vistas
        pelis_vistas = dict_peliculas_audiovisual[str(nombre) + "_vistas"]  # linea propensa de error
        series_vistas = dict_series_audiovisual[str(nombre) + "_vistas"]  # linea propensa de error
    except KeyError:
        mb.showwarning("Error", "No existen estadísticas para mostrar. Debe haber visto al menos una de cada para "
                                "mostrar sus graficas")
    else:
        # Si no hay error calculamos el tamaño de cada lista (series y pelis)
        numero_pelis = len(pelis_vistas)
        numero_series = len(series_vistas)

        # Creamos la ventana
        ventana_grafica = Toplevel()  # Crear una ventana por delante de la principal
        ventana_grafica.title(f"Grafica de visiones de {nombre}")  # Titulo de la ventana
        ventana_grafica.resizable(True, True)

        # Aquí comprobamos que lista es más grande para luego establecer el rango del eje Y de la gráfica
        if numero_series >= numero_pelis:
            rango = numero_series
        else:
            rango = numero_pelis

        # Configuración de la gráfica
        fig, ax = plt.subplots()
        ax.bar(["Series", "Peliculas"], [numero_series, numero_pelis], color="indianred")
        ax.set_title('Cantidades vistas', loc="left",
                     fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
        ax.set_ylabel("Numero de vistas", fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
        ax.set_yticks(range(0, rango + 1))

        config_grafica(fig, ventana_grafica)


def grafica_tiempo(nombre):
    try:
        # Líneas propensas de error si el usuario intenta visualizar las gráficas sin haber introducido ninguna
        # película y serie en la sección de vistas
        pelis_vistas = dict_peliculas_audiovisual[str(nombre) + "_vistas"]
        series_vistas = dict_series_audiovisual[str(nombre) + "_vistas"]
    except KeyError:
        mb.showwarning("Error", "No existen estadísticas para mostrar. Debe haber visto al menos una de cada para "
                                "mostrar sus graficas")
    else:
        # Si no hay error creamos las variables acumuladas de tiempo
        duracion_peliculas_vistas = 0
        duracion_series_vistas = 0

        #Creamos la ventana
        ventana_grafica = Toplevel()  # Crear una ventana por delante de la principal
        ventana_grafica.title(f"Grafica de tiempo de {nombre}")  # Título de la ventana
        ventana_grafica.resizable(True, True)

        # Calcular las métricas; para las películas simplemente sumamos su duración y para las series suponemos que
        # cuando el usuario la marca como vista es que ha visto la serie entera asi que multiplicamos la duración del
        # capítulo por el número de capítulos y por el número de temporadas
        for i in pelis_vistas:
            pelicula = db.session.query(Pelicula).filter(Pelicula.titulo == i).first()
            duracion_peliculas_vistas += pelicula.duracion

        for i in series_vistas:
            serie = db.session.query(Serie).filter(Serie.titulo == i).first()
            duracion_series_vistas += (serie.duracion_capitulo * serie.capitulos * serie.temporadas)

        duracion_peliculas_vistas /= 60  # Conversion a horas para la gráfica
        duracion_series_vistas /= 60  # Conversion a horas para la gráfica

        # Configuración de la gráfica
        fig, ax = plt.subplots()
        ax.barh(["Series", "Peliculas"], [duracion_series_vistas, duracion_peliculas_vistas], color="indianred")
        ax.set_title('Tiempo de visionado', loc="left",
                     fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
        ax.set_xlabel("Horas", fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})

        config_grafica(fig, ventana_grafica)


def catalogos(audiovisual, nombre):
    # Función que recibe dos parámetros, el tipo de audiovisual(película o serie) y el nombre del usuario. La
    # función se llama desde el main
    if audiovisual == "pelicula":

        # Creación de la ventana y configuración
        ventana_catalogo_peliculas = Toplevel()  # Crear una ventana por delante de la principal
        ventana_catalogo_peliculas.config(width=400, height=320, background=styles.BG_VENTANA)
        ventana_catalogo_peliculas.title(f"Catalogo de peliculas de {nombre}")  # Título de la ventana
        ventana_catalogo_peliculas.resizable(False, False)

        # Etiquetas y botones
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

        # Creación de la ventana y configuración
        ventana_catalogo_series = Toplevel()  # Crear una ventana por delante de la principal
        ventana_catalogo_series.title(f"Catalogo de series de {nombre}")  # Titulo de la ventana
        ventana_catalogo_series.config(width=400, height=320, background=styles.BG_VENTANA)
        ventana_catalogo_series.resizable(False, False)

        # Etiquetas y botones
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
