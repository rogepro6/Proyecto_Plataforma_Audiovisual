from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import chain

from database import db
from styles import styles
from models.usuarios import Usuario
from clientes_busquedas import dict_peliculas_audiovisual, dict_series_audiovisual
from clientes_catalogos import config_grafica


def add_usuario():
    def registrar_usuario():
        # Comprobación de que se rellenan ambos campos
        if len(nombre_Entry.get()) and len(pass_Entry.get()):

            usuario = Usuario(
                nombre_Entry.get(),
                pass_Entry.get(),
            )
            # Añadimos a la BBDD, guardamos, informamos mediante el mensaje y limpiamos campos
            db.session.add(usuario)
            db.session.commit()
            mensaje["fg"] = "blue"
            mensaje["text"] = f"Usuario {nombre_Entry.get()} añadido con exito"
            nombre_Entry.delete(0, "end")
            pass_Entry.delete(0, "end")

        else:
            mensaje["fg"] = "red"
            mensaje["text"] = "Debe introducir todos los datos"

    # Creacion de la ventana
    ventana_admin_usuario = Toplevel()  # Crear una ventana por delante de la principal
    ventana_admin_usuario.config(width=400, height=320, background=styles.BG_VENTANA)
    ventana_admin_usuario.title("Registro de usuarios")  # Título de la ventana
    ventana_admin_usuario.resizable(False, False)

    # Etiquetas y entradas de texto para los campos nombre y contraseña
    nombre_usuario = Label(ventana_admin_usuario, text="Nombre", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
    nombre_usuario.grid(column=0, row=1, ipadx=5, ipady=5, padx=10, pady=10)
    pass_usuario = Label(ventana_admin_usuario, text="Password", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
    pass_usuario.grid(column=0, row=2, ipadx=5, ipady=5, padx=10, pady=10)

    nombre_Entry = Entry(ventana_admin_usuario, textvariable=StringVar(), font=styles.ENTRADAS_DE_TEXTO)
    nombre_Entry.grid(column=1, row=1, ipadx=5, ipady=5, padx=10, pady=10)
    pass_Entry = Entry(ventana_admin_usuario, textvariable=StringVar(), show="*", font=styles.ENTRADAS_DE_TEXTO)
    pass_Entry.grid(column=1, row=2, ipadx=5, ipady=5, padx=10, pady=10)

    # Botones de acción
    boton_registrar = Button(ventana_admin_usuario, text="Registrar", foreground=styles.FG_BOTON,
                             activeforeground=styles.AFG_BOTON,
                             activebackground=styles.ABG_BOTON, command=registrar_usuario)
    boton_registrar.grid(column=0, row=4, sticky=W + E, columnspan=1)

    boton_salir = Button(ventana_admin_usuario, text="Salir", foreground=styles.FG_BOTON,
                         activeforeground=styles.AFG_BOTON,
                         activebackground=styles.ABG_BOTON_SALIR, command=lambda: ventana_admin_usuario.destroy())
    boton_salir.grid(column=1, row=4, sticky=W + E, columnspan=1)

    # Mensaje de confirmación o error
    mensaje = Label(ventana_admin_usuario, text="", fg="red", background=styles.BG_VENTANA)
    mensaje.grid(column=0, row=3, columnspan=2, sticky=W + E)


def gestion_usuarios():
    # Funcion que limpia los datos antiguos e introduce los nuevos en la tabla
    def get_usuarios():
        registros = tabla.get_children()

        for fila in registros:
            tabla.delete(fila)

        usuarios = db.session.query(Usuario).all()

        for usuario in usuarios:
            tabla.insert("", 0, text=usuario.id, values=(usuario.nombre, usuario.contra))

    def eliminar_usuario():
        mensaje["text"] = ""
        try:
            # Comprobacion de que se selecciona un registro
            tabla.item(tabla.selection())["values"][0]
        except IndexError:
            mensaje["fg"] = "red"
            mensaje["text"] = "Seleccione un usuario"
            return
        else:
            db.session.query(Usuario).filter(Usuario.id == tabla.item(tabla.selection())["text"]).delete()
            db.session.commit()
            nombre = tabla.item(tabla.selection())["values"][0]
            mensaje["fg"] = "blue"
            mensaje['text'] = 'Usuario {} eliminado con éxito'.format(nombre)

            get_usuarios()

    def editar_usuario():
        mensaje["text"] = ""
        try:
            # Comprobacion de que se selecciona un registro
            tabla.item(tabla.selection())["values"][0]
        except IndexError:
            mensaje["fg"] = "red"
            mensaje["text"] = "Seleccione un usuario"
            return

        old_nombre = tabla.item(tabla.selection())["values"][0]
        old_pass = tabla.item(tabla.selection())["values"][1]

        # Creacion de la ventana de edición de usuarios
        ventana_editar = Toplevel()
        ventana_editar.title("Edición de usuarios")
        ventana_editar.config(width=400, height=320, background=styles.BG_VENTANA)
        ventana_editar.resizable(False, False)

        cabecera = Label(ventana_editar, text="Editar Usuario", font=styles.ENCABEZADOS,
                         background=styles.BG_ETIQUETA, anchor=CENTER)
        cabecera.grid(column=0, row=0, padx=10, pady=10)

        frame_ep = LabelFrame(ventana_editar, text="Editar Usuario", font=styles.TEXTOS, background=styles.BG_ETIQUETA)
        frame_ep.grid(row=1, column=0, columnspan=2, pady=30, padx=30, ipadx=5, ipady=5)

        # Etiquetas y entradas de texto
        etiqueta_nombre_antiguo = Label(frame_ep, text="Nombre antiguo", background=styles.BG_ETIQUETA,
                                        font=styles.TEXTOS)
        etiqueta_nombre_antiguo.grid(row=2, column=0, ipadx=5, ipady=5)
        input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_nombre),
                                     font=styles.ENTRADAS_DE_TEXTO,
                                     state="readonly")
        input_nombre_antiguo.grid(row=2, column=1, ipadx=5, ipady=5)
        etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo", background=styles.BG_ETIQUETA,
                                      font=styles.TEXTOS)
        etiqueta_nombre_nuevo.grid(row=3, column=0, ipadx=5, ipady=5)
        input_nombre_nuevo = Entry(frame_ep, font=styles.ENTRADAS_DE_TEXTO)
        input_nombre_nuevo.grid(row=3, column=1, ipadx=5, ipady=5)

        etiqueta_pass_antiguo = Label(frame_ep, text="Contraseña Antigua", background=styles.BG_ETIQUETA,
                                      font=styles.TEXTOS)
        etiqueta_pass_antiguo.grid(row=4, column=0, ipadx=5, ipady=5)
        input_pass_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_pass),
                                   font=styles.ENTRADAS_DE_TEXTO, state="readonly")
        input_pass_antiguo.grid(row=4, column=1, ipadx=5, ipady=5)
        etiqueta_pass_nuevo = Label(frame_ep, text="Contraseña Nueva", background=styles.BG_ETIQUETA,
                                    font=styles.TEXTOS)
        etiqueta_pass_nuevo.grid(row=5, column=0, ipadx=5, ipady=5)
        input_pass_nuevo = Entry(frame_ep, show="*", font=styles.ENTRADAS_DE_TEXTO)
        input_pass_nuevo.grid(row=5, column=1, ipadx=5, ipady=5)

        # Botón de salir
        boton_salir = Button(frame_ep, text="Salir", foreground=styles.FG_BOTON,
                             activeforeground=styles.AFG_BOTON,
                             activebackground=styles.ABG_BOTON_SALIR, command=lambda: ventana_editar.destroy())
        boton_salir.grid(row=7, sticky=W + E, columnspan=2)

        def actualiza():
            # Si los campos se dejan vacíos se coge el registro anterior, en otro caso se coge el nuevo
            nombre = input_nombre_nuevo.get() if input_nombre_nuevo.get() != "" else old_nombre
            contra = input_pass_nuevo.get() if input_pass_nuevo.get() != "" else old_pass

            # Llamamos al metodo update que actualiza el registro en la BBDD
            db.session.query(Usuario).filter(Usuario.id == tabla.item(tabla.selection())["text"]).update(
                {
                    Usuario.nombre: nombre,
                    Usuario.contra: contra,
                }
            )
            # Guardamos, cerramos la ventana, y cargamos los datos en la tabla y mostramos el mensaje de confirmación
            db.session.commit()
            ventana_editar.destroy()
            get_usuarios()
            mensaje["fg"] = "blue"
            mensaje["text"] = f"Usuario {old_nombre} actualizado"

        s = ttk.Style()
        s.configure("my.TButton")

        # Botón de actualizar
        boton_actualizar = Button(frame_ep, text="Actualizar Usuario", foreground=styles.FG_BOTON,
                                  activeforeground=styles.AFG_BOTON,
                                  activebackground=styles.ABG_BOTON, command=actualiza)
        boton_actualizar.grid(row=6, columnspan=2, sticky=W + E)

    # ---------------- Aquí continuamos con la función de gestion de usuarios y creación de la tabla------------------#
    ventana_gestion_usuarios = Toplevel()
    ventana_gestion_usuarios.config(width=400, height=320, background=styles.BG_VENTANA)
    ventana_gestion_usuarios.title("Gestión de Usuarios")  # Título de la ventana
    ventana_gestion_usuarios.resizable(False, False)

    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                    font=styles.TABLAS)  # Se modifica la fuente de la tabla
    style.configure("mystyle.Treeview.Heading",
                    font=styles.TABLAS_CABECERAS)  # Se modifica la fuente de las cabeceras
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    # Estructura de la tabla de Peliculas
    tabla = ttk.Treeview(ventana_gestion_usuarios, height=10, columns=["#0", "#1", "#2"],
                         style="mystyle.Treeview")
    tabla.grid(column=0, row=0, ipadx=5, ipady=5, padx=10, pady=10)
    tabla.heading(column="#0", text="ID", anchor=CENTER)
    tabla.heading(column="#1", text="Nombre", anchor=CENTER)
    tabla.heading(column="#2", text="Contraseña", anchor=CENTER)

    mensaje = Label(ventana_gestion_usuarios, text="", fg="red", background=styles.BG_VENTANA)
    mensaje.grid(column=0, row=1, columnspan=2, sticky=W + E)

    # Botones de registrar, eliminar, editar y actualizar usuarios
    boton_registrar_usuario = Button(ventana_gestion_usuarios, text="Registrar", foreground=styles.FG_BOTON,
                                     activeforeground=styles.AFG_BOTON,
                                     activebackground=styles.ABG_BOTON, command=add_usuario)
    boton_registrar_usuario.grid(column=0, row=2, sticky=W + E)
    boton_eliminar_usuario = Button(ventana_gestion_usuarios, text="Eliminar", foreground=styles.FG_BOTON,
                                    activeforeground=styles.AFG_BOTON,
                                    activebackground=styles.ABG_BOTON, command=eliminar_usuario)
    boton_eliminar_usuario.grid(column=0, row=3, sticky=W + E)
    boton_editar_usuario = Button(ventana_gestion_usuarios, text="Editar", foreground=styles.FG_BOTON,
                                  activeforeground=styles.AFG_BOTON,
                                  activebackground=styles.ABG_BOTON, command=editar_usuario)
    boton_editar_usuario.grid(column=0, row=4, sticky=W + E)
    boton_actualizar = Button(ventana_gestion_usuarios, text="Actualizar", foreground=styles.FG_BOTON,
                              activeforeground=styles.AFG_BOTON,
                              activebackground=styles.ABG_BOTON, command=get_usuarios)
    boton_actualizar.grid(column=0, row=5, sticky=W + E)

    # Botón de salir
    boton_salir = Button(ventana_gestion_usuarios, text="Salir", foreground=styles.FG_BOTON,
                         activeforeground=styles.AFG_BOTON,
                         activebackground=styles.ABG_BOTON_SALIR, command=lambda: ventana_gestion_usuarios.destroy())
    boton_salir.grid(column=0, row=6, sticky=W + E)

    get_usuarios()


# En esta función configuramos las gráficas de sectores para ver el total de películas o series vistas por cada uno
# de los clientes y su porcentaje con respecto al resto
def graficas_usuarios(audiovisual):

    # calcular las leyendas y las cantidades de visualizaciones
    leyendas = []
    cantidades = []
    if audiovisual == "Peliculas":
        for i, x in dict_peliculas_audiovisual.items():
            if i[-7:] == "_vistas":
                leyendas.append(i[:-7])
                cantidades.append(len(x))
    elif audiovisual == "Series":
        for i, x in dict_series_audiovisual.items():
            if i[-7:] == "_vistas":
                leyendas.append(i[:-7])
                cantidades.append(len(x))

    # Comprobación de que haya cantidades
    if cantidades == [0]:
        mb.showerror("Error", "No existen graficas para mostrar")
    else:
        # Creación de la ventana para gráficas
        ventana_graficas = Toplevel()
        ventana_graficas.title(f"{audiovisual} vistas por los Usuarios")  # Titulo de la ventana
        ventana_graficas.resizable(False, False)

        # Creación de la gráfica de sectores
        fig, ax = plt.subplots()
        ax.pie(cantidades, autopct='%1.1f%%', shadow=True)  # Añadimos el % de cada usuario
        ax.legend(leyendas, loc='lower right')

        # Aplicar la configuración
        config_grafica(fig, ventana_graficas)


# En esta función configuramos la gráfica de visionados totales de ambas categorías de cada uno de los clientes que
# han visto al menos una película o serie
def graficas_totales():
    # Creamos un diccionario combinado para calcular los visionados totales
    dict_combinado = defaultdict(list)
    for k, v in chain(dict_peliculas_audiovisual.items(), dict_series_audiovisual.items()):
        dict_combinado[k].append(v)

    # Calculamos los datos de las gráficas
    nombres_usuario = []
    cantidades_vistas = []
    for k, items in dict_combinado.items():
        total = 0
        if k[-7:] == "_vistas":
            for item in items:
                total += len(item)
            cantidades_vistas.append(total)
            nombres_usuario.append(k[:-7])

    try:
        # Generamos la gráfica y configuramos sus títulos y ejes
        fig, ax = plt.subplots()
        ax.bar(nombres_usuario, cantidades_vistas)
        ax.set_title('Cantidades vistas por todos los usuarios', loc="left",
                     fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
        ax.set_ylabel("Numero de vistas", fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
        ax.set_yticks(range(0, max(cantidades_vistas) + 1))  # Línea propensa de error si no hay ninguna cantidad

    except ValueError:
        mb.showerror("Error", "No existen graficas para mostrar")
    else:
        # Creación de la ventana para gráficas
        ventana_graficas = Toplevel()
        ventana_graficas.title("Gráficas totales")  # Título de la ventana
        ventana_graficas.resizable(False, False)

        # Aplicar la configuración
        config_grafica(fig, ventana_graficas)
