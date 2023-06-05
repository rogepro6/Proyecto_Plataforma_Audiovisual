from tkinter import *
from tkinter import ttk
from math import ceil
import db
from models.usuarios import Usuario
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from clientes_busquedas import dict_peliculas_audiovisual, dict_series_audiovisual
from clientes_catalogos import config_grafica


def add_usuario():
    def registrar_usuario():
        if len(nombre_Entry.get()) and len(pass_Entry.get()):

            usuario = Usuario(
                nombre_Entry.get(),
                pass_Entry.get(),
            )
            db.session.add(usuario)
            db.session.commit()
            mensaje["fg"] = "blue"
            mensaje["text"] = f"Usuario {nombre_Entry.get()} añadido con exito"
        else:
            mensaje["fg"] = "red"
            mensaje["text"] = "Debe introducir todos los datos"

    ventana_admin_usuario = Toplevel()  # Crear una ventana por delante de la principal
    ventana_admin_usuario.title("Registro de usuarios")  # Titulo de la ventana
    ventana_admin_usuario.resizable(False, False)

    nombre_usuario = Label(ventana_admin_usuario, text="Nombre")
    nombre_usuario.grid(column=0, row=1)
    pass_usuario = Label(ventana_admin_usuario, text="Password")
    pass_usuario.grid(column=0, row=2)

    nombre_Entry = Entry(ventana_admin_usuario, textvariable=StringVar())
    nombre_Entry.grid(column=1, row=1)
    pass_Entry = Entry(ventana_admin_usuario, textvariable=StringVar())
    pass_Entry.grid(column=1, row=2)

    boton_registrar = ttk.Button(ventana_admin_usuario, text="Registrar", command=registrar_usuario)
    boton_registrar.grid(column=0, row=4, sticky=W + E, columnspan=1)

    boton_salir = ttk.Button(ventana_admin_usuario, text="Salir", command=lambda: ventana_admin_usuario.destroy())
    boton_salir.grid(column=1, row=4, sticky=W + E, columnspan=1)

    mensaje = Label(ventana_admin_usuario, text="", fg="red")
    mensaje.grid(column=0, row=3, columnspan=2, sticky=W + E)


def gestion_usuarios():
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
            tabla.item(tabla.selection())["values"][0]
        except IndexError as e:
            mensaje["fg"] = "red"
            mensaje["text"] = "Seleccione un usuario"
            return
        db.session.query(Usuario).filter(Usuario.id == tabla.item(tabla.selection())["text"]).delete()
        db.session.commit()
        nombre = tabla.item(tabla.selection())["values"][0]
        mensaje["fg"] = "blue"
        mensaje['text'] = 'Usuario {} eliminado con éxito'.format(nombre)

        get_usuarios()

    def editar_usuario():

        mensaje["text"] = ""

        try:
            tabla.item(tabla.selection())["values"][0]
        except IndexError as e:
            mensaje["fg"] = "red"
            mensaje["text"] = "Seleccione un usuario"
            return

        old_nombre = tabla.item(tabla.selection())["values"][0]
        old_pass = tabla.item(tabla.selection())["values"][1]

        ventana_editar = Toplevel()
        ventana_editar.title = "Edicion de usuarios"
        ventana_editar.resizable(False, False)

        cabecera = Label(ventana_editar, text="Editar Usuario", font=("calibri", 40, "bold"))
        cabecera.grid(column=0, row=0)

        frame_ep = LabelFrame(ventana_editar, text="Editar Usuario")
        frame_ep.grid(row=1, column=0, columnspan=2, pady=30, padx=30)

        etiqueta_nombre_antiguo = Label(frame_ep, text="Nombre antiguo")
        etiqueta_nombre_antiguo.grid(row=2, column=0)
        input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_nombre),
                                     state="readonly")
        input_nombre_antiguo.grid(row=2, column=1)
        etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo:")
        etiqueta_nombre_nuevo.grid(row=3, column=0)
        input_nombre_nuevo = Entry(frame_ep)
        input_nombre_nuevo.grid(row=3, column=1)

        etiqueta_pass_antiguo = Label(frame_ep, text="Categoria Antigua")
        etiqueta_pass_antiguo.grid(row=4, column=0)
        input_pass_antiguo = Entry(frame_ep, textvariable=StringVar(ventana_editar, value=old_pass), state="readonly")
        input_pass_antiguo.grid(row=4, column=1)
        etiqueta_pass_nuevo = Label(frame_ep, text="Contraseña Nueva:")
        etiqueta_pass_nuevo.grid(row=5, column=0)
        input_pass_nuevo = Entry(frame_ep)
        input_pass_nuevo.grid(row=5, column=1)

        boton_salir = ttk.Button(frame_ep, text="Salir", command=lambda: ventana_editar.destroy())
        boton_salir.grid(row=7, sticky=W + E, columnspan=2)

        def actualiza():

            nombre = input_nombre_nuevo.get() if input_nombre_nuevo.get() != "" else old_nombre
            contra = input_pass_nuevo.get() if input_pass_nuevo.get() != "" else old_pass

            db.session.query(Usuario).filter(Usuario.id == tabla.item(tabla.selection())["text"]).update(
                {
                    Usuario.nombre: nombre,
                    Usuario.contra: contra,
                }
            )
            db.session.commit()
            ventana_editar.destroy()
            get_usuarios()
            mensaje["fg"] = "blue"
            mensaje["text"] = f"Usuario {old_nombre} actualizado"

        s = ttk.Style()
        s.configure("my.TButton")
        boton_actualizar = ttk.Button(frame_ep, text="Actualizar Usuario", command=actualiza)
        boton_actualizar.grid(row=6, columnspan=2, sticky=W + E)

    # ---------------------------#
    ventana_gestion_usuarios = Toplevel()
    ventana_gestion_usuarios.title("Gestion de Usuarios")  # Titulo de la ventana
    ventana_gestion_usuarios.resizable(False, False)

    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                    font=('Calibri', 10))  # Se modifica la fuente de la tabla
    style.configure("mystyle.Treeview.Heading",
                    font=('Calibri', 10, 'bold'))  # Se modifica la fuente de las cabeceras
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    # Estructura de la tabla de Peliculas
    tabla = ttk.Treeview(ventana_gestion_usuarios, height=10, columns=["#0", "#1", "#2"],
                         style="mystyle.Treeview")
    tabla.grid(column=0, row=0)
    tabla.heading(column="#0", text="ID", anchor=CENTER)
    tabla.heading(column="#1", text="Nombre", anchor=CENTER)
    tabla.heading(column="#2", text="Contraseña", anchor=CENTER)

    mensaje = Label(ventana_gestion_usuarios, text="", fg="red")
    mensaje.grid(column=0, row=1, columnspan=2, sticky=W + E)

    boton_registrar_usuario = ttk.Button(ventana_gestion_usuarios, text="Registrar", command=add_usuario)
    boton_registrar_usuario.grid(column=0, row=2, sticky=W + E)
    boton_registrar_usuario = ttk.Button(ventana_gestion_usuarios, text="Eliminar", command=eliminar_usuario)
    boton_registrar_usuario.grid(column=0, row=3, sticky=W + E)
    boton_registrar_usuario = ttk.Button(ventana_gestion_usuarios, text="Editar", command=editar_usuario)
    boton_registrar_usuario.grid(column=0, row=4, sticky=W + E)
    boton_actualizar = ttk.Button(ventana_gestion_usuarios, text="Actualizar", command=get_usuarios)
    boton_actualizar.grid(column=0, row=5, sticky=W + E)

    boton_salir = ttk.Button(ventana_gestion_usuarios, text="Salir", command=lambda: ventana_gestion_usuarios.destroy())
    boton_salir.grid(column=0, row=6, sticky=W + E)

    get_usuarios()


def graficas_usuarios():
    # revision de esta funcion
    # Creacion de la ventana para graficas
    ventana_graficas = Toplevel()
    ventana_graficas.title("Graficas de Usuarios")  # Titulo de la ventana
    ventana_graficas.resizable(False, False)

    # calcular las leyendas
    leyendas = []
    cantidad_vistas = []
    for i, x in dict_peliculas_audiovisual.items():
        leyendas.append(i[:-7])
        cantidad_vistas.append(len(x))

    fig, ax = plt.subplots()
    ax.pie(cantidad_vistas)
    ax.legend(leyendas, loc='upper right')

    config_grafica(fig, ventana_graficas)
