from tkinter import *
from tkinter import ttk
from functools import partial

from database import db
from styles import styles
from models.audiovisual import Pelicula, Serie

# Creamos dos diccionarios (uno para películas y otro para series) que cada uno tendrá el siguiente formato:

# {"nombre de usuario_vistas":[lista de nombres de películas/series que ha visto el usuario],
# "nombre de usuario_favoritos":[lista de nombres de películas/series que quiere ver el usuario más adelante]}

# Cada una de estas claves se iran generando a medida que los nuevos usuarios añadan más contenidos

dict_peliculas_audiovisual = {}
dict_series_audiovisual = {}


# Función dedicada a mostrar y añadir a cada uno de los diccionarios los registros que el usuario considere oportuno
# La función recibe 3 parámetros (los resultados aplicados a la búsqueda que realiza en la siguiente función
# (buscar_audiovisual), el tipo de audiovisual(película o serie) y el nombre del usuario

def mostrar_resultados(resultados, audiovisual, nombre):
    # Función que recibe dos parámetros, tipo de audiovisual(película o serie) y el nombre del usuario
    def favoritos(tipo, nombre_cliente):
        mensaje["text"] = ""
        try:
            # Comprobación de que se seleccione un registro
            titulo = tabla.item(tabla.selection())["values"][0]
        except IndexError:
            mensaje["fg"] = "red"
            mensaje["text"] = "Seleccione un registro"
            return

        if tipo == "peliculas":
            try:
                # Comprobación de que el registro no este ya en el diccionario
                if titulo in dict_peliculas_audiovisual[str(nombre_cliente) + "_favoritos"]:
                    mensaje["fg"] = "red"
                    mensaje["text"] = "La película ya esta en favoritos"
                    return
                else:
                    # Intentamos añadir el registro al diccionario con la clave ya creada
                    dict_peliculas_audiovisual[str(nombre_cliente) + "_favoritos"].append(titulo)
                    mensaje["fg"] = "blue"
                    mensaje["text"] = f"Película {titulo} añadida a favoritos"
            except:
                # En el caso de que la clave no hubiera sido creada (para el primer registro), primero se crea y
                # luego se introduce el registro
                dict_peliculas_audiovisual[str(nombre_cliente) + "_favoritos"] = []
                dict_peliculas_audiovisual[str(nombre_cliente) + "_favoritos"].append(titulo)
                mensaje["fg"] = "blue"
                mensaje["text"] = f"Película {titulo} añadida a favoritos"

        elif tipo == "series":
            try:
                # Comprobación de que el registro no este ya en el diccionario
                if titulo in dict_series_audiovisual[str(nombre_cliente) + "_favoritos"]:
                    mensaje["fg"] = "red"
                    mensaje["text"] = "La serie ya esta en favoritos"
                    return
                else:
                    # Intentamos añadir el registro al diccionario con la clave ya creada
                    dict_series_audiovisual[str(nombre_cliente) + "_favoritos"].append(titulo)
                    mensaje["fg"] = "blue"
                    mensaje["text"] = f"Serie {titulo} añadida a favoritos"
            except:
                # En el caso de que la clave no hubiera sido creada (para el primer registro), primero se crea y
                # luego se introduce el registro
                dict_series_audiovisual[str(nombre_cliente) + "_favoritos"] = []
                dict_series_audiovisual[str(nombre_cliente) + "_favoritos"].append(titulo)
                mensaje["fg"] = "blue"
                mensaje["text"] = f"Serie {titulo} añadida a favoritos"

    # Misma función que favoritos, pero para las películas y series vistas
    def vistas(tipo, nombre_cliente):
        mensaje["text"] = ""
        try:
            titulo = tabla.item(tabla.selection())["values"][0]
        except IndexError:
            mensaje["fg"] = "red"
            mensaje["text"] = "Selecciona un registro"
            return
        if tipo == "peliculas":
            try:
                if titulo in dict_peliculas_audiovisual[str(nombre_cliente) + "_vistas"]:
                    mensaje["fg"] = "red"
                    mensaje["text"] = "La película ya esta en vistas"
                    return
                else:
                    dict_peliculas_audiovisual[str(nombre_cliente) + "_vistas"].append(titulo)
                    mensaje["fg"] = "blue"
                    mensaje["text"] = f"Película {titulo} añadida a vistas"
            except:
                dict_peliculas_audiovisual[str(nombre_cliente) + "_vistas"] = []
                dict_peliculas_audiovisual[str(nombre_cliente) + "_vistas"].append(titulo)
                mensaje["fg"] = "blue"
                mensaje["text"] = f"Película {titulo} añadida a vistas"
        if tipo == "series":
            try:
                if titulo in dict_series_audiovisual[str(nombre_cliente) + "_vistas"]:
                    mensaje["fg"] = "red"
                    mensaje["text"] = "La serie ya esta en vistas"
                    return
                else:
                    dict_series_audiovisual[str(nombre_cliente) + "_vistas"].append(titulo)
                    mensaje["fg"] = "blue"
                    mensaje["text"] = f"Serie {titulo} añadida a vistas"
            except:
                dict_series_audiovisual[str(nombre_cliente) + "_vistas"] = []
                dict_series_audiovisual[str(nombre_cliente) + "_vistas"].append(titulo)
                mensaje["fg"] = "blue"
                mensaje["text"] = f"Serie {titulo} añadida a vistas"

    # Creamos la ventana de los resultados de la búsqueda
    ventana_resultados_busqueda = Toplevel()
    ventana_resultados_busqueda.config(width=400, height=320, background=styles.BG_VENTANA)
    ventana_resultados_busqueda.title("Resultados busqueda")  # Título de la ventana
    ventana_resultados_busqueda.resizable(False, False)

    # Creamos la tabla para introducir los registros
    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                    font=styles.TABLAS)  # Se modifica la fuente de la tabla
    style.configure("mystyle.Treeview.Heading",
                    font=styles.TABLAS_CABECERAS)  # Se modifica la fuente de las cabeceras
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    # Estructura de la tabla de Peliculas
    tabla = ttk.Treeview(ventana_resultados_busqueda, height=10, columns=["#0", "#1", "#2", "#3", "#4", "#5", "#6"],
                         style="mystyle.Treeview")

    # Si la función se invoca con el audiovisual en películas, los encabezados serán los de las películas...
    if audiovisual == "peliculas":

        tabla.grid(row=0, column=0, ipadx=5, ipady=5, padx=10, pady=10)
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

        # Botones de llamada a las funciones de añadir a vistas y favoritas
        boton_favoritas = Button(ventana_resultados_busqueda, text="Añadir a favoritas", foreground=styles.FG_BOTON,
                                 activeforeground=styles.AFG_BOTON,
                                 activebackground=styles.ABG_BOTON,
                                 command=partial(favoritos, "peliculas", nombre))
        boton_favoritas.grid(row=2, column=0, columnspan=2, sticky=W + E)

        boton_vistas = Button(ventana_resultados_busqueda, text="Pelicula vista", foreground=styles.FG_BOTON,
                              activeforeground=styles.AFG_BOTON,
                              activebackground=styles.ABG_BOTON,
                              command=partial(vistas, "peliculas", nombre))
        boton_vistas.grid(row=3, column=0, columnspan=2, sticky=W + E)

        # Botón de salir y mensaje de confirmación o error
        boton_salir = Button(ventana_resultados_busqueda, text="Salir", foreground=styles.FG_BOTON,
                             activeforeground=styles.AFG_BOTON,
                             activebackground=styles.ABG_BOTON_SALIR,
                             command=lambda: ventana_resultados_busqueda.destroy())
        boton_salir.grid(row=4, column=0, columnspan=2, sticky=W + E)

        mensaje = Label(ventana_resultados_busqueda, text="", fg="red", background=styles.BG_VENTANA)
        mensaje.grid(row=1, column=0, columnspan=2, sticky=W + E)

    # Si la función se invoca con el audiovisual en series, los encabezados serán los de las series...
    if audiovisual == "series":

        tabla.grid(row=0, column=0, ipadx=5, ipady=5, padx=10, pady=10)
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

        # Botones de llamada a las funciones de añadir a vistas y favoritas
        boton_favoritas = Button(ventana_resultados_busqueda, text="Añadir a favoritas", foreground=styles.FG_BOTON,
                                 activeforeground=styles.AFG_BOTON,
                                 activebackground=styles.ABG_BOTON,
                                 command=partial(favoritos, "series", nombre))
        boton_favoritas.grid(row=2, column=0, columnspan=2, sticky=W + E)

        boton_vistas = Button(ventana_resultados_busqueda, text="Serie vista", foreground=styles.FG_BOTON,
                              activeforeground=styles.AFG_BOTON,
                              activebackground=styles.ABG_BOTON,
                              command=partial(vistas, "series", nombre))
        boton_vistas.grid(row=3, column=0, columnspan=2, sticky=W + E)

        # Botón de salir y mensaje de confirmación o error
        boton_salir = Button(ventana_resultados_busqueda, text="Salir", foreground=styles.FG_BOTON,
                             activeforeground=styles.AFG_BOTON,
                             activebackground=styles.ABG_BOTON_SALIR,
                             command=lambda: ventana_resultados_busqueda.destroy())
        boton_salir.grid(row=4, column=0, columnspan=2, sticky=W + E)

        mensaje = Label(ventana_resultados_busqueda, text="", fg="red", background=styles.BG_VENTANA)
        mensaje.grid(row=1, column=0, columnspan=2, sticky=W + E)


# Esta es la función encargada de realizar las búsquedas en la BBDD por título y categoría
# Recibe el tipo de búsqueda (película o serie) y el nombre del usuario
def buscar_audiovisual(audiovisual, nombre):

    def busqueda(tipo, nombre_cliente):
        if busqueda_entry.get() == "":
            mensaje["fg"] = "red"
            mensaje["text"] = "Seleccione una busqueda"
        else:
            # Dependiendo del tipo de búsqueda y del radiobutton(título o categoría) seleccionado hacemos una
            # consulta u otra a la BBDD e invocamos a la función de mostrar los resultados con esos parámetros
            if tipo == "peliculas":
                if modo_busqueda.get() == "titulo":
                    resultados = db.session.query(Pelicula).filter_by(titulo=busqueda_entry.get())
                    mostrar_resultados(resultados, tipo, nombre_cliente)
                elif modo_busqueda.get() == "categoria":
                    resultados = db.session.query(Pelicula).filter_by(categoria=busqueda_entry.get())
                    mostrar_resultados(resultados, tipo, nombre_cliente)
            elif tipo == "series":
                if modo_busqueda.get() == "titulo":
                    resultados = db.session.query(Serie).filter_by(titulo=busqueda_entry.get())
                    mostrar_resultados(resultados, tipo, nombre_cliente)
                elif modo_busqueda.get() == "categoria":
                    resultados = db.session.query(Serie).filter_by(categoria=busqueda_entry.get())
                    mostrar_resultados(resultados, tipo, nombre_cliente)

    # Creación de la ventana de buscar
    ventana_buscar = Toplevel()  # Crear una ventana por delante de la principal
    ventana_buscar.config(width=400, height=320, background=styles.BG_VENTANA)
    ventana_buscar.title(f"Buscador de {audiovisual}")  # Título de la ventana
    ventana_buscar.resizable(False, False)

    modo_label = Label(ventana_buscar, text="Modo de Busqueda", background=styles.BG_ETIQUETA,
                       font=styles.TEXTOS, anchor=CENTER)
    modo_label.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

    # Creación del radiobutton donde se escoge el tipo de búsqueda
    modo_busqueda = StringVar()
    modo_busqueda.set(value=1)
    radiobutton1 = Radiobutton(ventana_buscar, text="Titulo", variable=modo_busqueda, value="titulo",
                               font=styles.TEXTOS,
                               background=styles.BG_ETIQUETA)
    radiobutton1.grid(row=1, column=0, padx=10, pady=10)
    radiobutton2 = Radiobutton(ventana_buscar, text="Categoría", variable=modo_busqueda, value="categoria",
                               font=styles.TEXTOS,
                               background=styles.BG_ETIQUETA)
    radiobutton2.grid(row=1, column=1, padx=10, pady=10)

    busqueda_entry = Entry(ventana_buscar, font=styles.ENTRADAS_DE_TEXTO)
    busqueda_entry.grid(row=2, column=0, padx=10, pady=10, columnspan=2, sticky=W + E)

    boton_buscar = Button(ventana_buscar, text="Buscar", foreground=styles.FG_BOTON,
                          activeforeground=styles.AFG_BOTON,
                          activebackground=styles.ABG_BOTON, command=partial(busqueda, audiovisual, nombre))
    boton_buscar.grid(row=4, column=0, columnspan=2, sticky=W + E)

    # Botón de salir y mensaje de confirmación o error
    boton_salir = Button(ventana_buscar, text="Salir", foreground=styles.FG_BOTON,
                         activeforeground=styles.AFG_BOTON,
                         activebackground=styles.ABG_BOTON_SALIR, command=lambda: ventana_buscar.destroy())
    boton_salir.grid(row=5, column=0, columnspan=2, sticky=W + E)

    mensaje = Label(ventana_buscar, text="", fg="red", background=styles.BG_VENTANA)
    mensaje.grid(column=0, row=3, columnspan=2, sticky=W + E)
