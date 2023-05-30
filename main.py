from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import db
from models.usuarios import Usuario
from administracion_audiovisual import add_pelicula, add_serie, editar_Serie, editar_Peli
from administracion_usuarios import gestion_usuarios
from clientes_busquedas import buscar_serie, buscar_peli
from clientes_catalogos import catalogo_peliculas, catalogo_series, graficas

root = Tk()
nombreUsuario = StringVar()
contraUsuario = StringVar()


def interfazUsuario():
    # Ventana Principal
    root.title("Login Usuario")

    # Frame Principal
    mainFrame = Frame(root)
    mainFrame.pack()
    mainFrame.config(width=400, height=320, bg="lightblue")

    # Textos y titulos
    titulo = Label(mainFrame, text="Login de Usuarios", font=("Arial", 36))
    titulo.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

    nombreLabel = Label(mainFrame, text="Nombre: ")
    nombreLabel.grid(column=0, row=1)
    passLabel = Label(mainFrame, text="Contraseña: ")
    passLabel.grid(column=0, row=2)

    # Entradas de texto

    nombreUsuario.set("")
    nombreEntry = Entry(mainFrame, textvariable=nombreUsuario)
    nombreEntry.grid(column=1, row=1)

    contraUsuario.set("")
    contraEntry = Entry(mainFrame, textvariable=contraUsuario, show="*")
    contraEntry.grid(column=1, row=2)

    # Botones

    iniciarSesionButton = ttk.Button(mainFrame, text="Iniciar Sesion", command=iniciarSesion)
    iniciarSesionButton.grid(column=1, row=3, ipadx=5, ipady=5, padx=10, pady=10)

    registrarButton = ttk.Button(mainFrame, text="Registrar Usuario", command=registrarUsuario)
    registrarButton.grid(column=0, row=3, ipadx=5, ipady=5, padx=10, pady=10)

    root.mainloop()


def iniciarSesion():
    nombre = nombreUsuario.get()
    password = contraUsuario.get()
    user = db.session.query(Usuario).filter_by(nombre=nombre, contra=password).first()
    admin = db.session.query(Usuario).filter_by(nombre="a", contra="a").first()
    if user == admin:
        mb.showinfo("Conectado", "Sesion conectada en modo Administracion")
        administracion()
    elif user:
        mb.showinfo("Conectado", f"Sesion iniciada con exito en {nombre}")
        clientes(nombre)
    else:
        mb.showerror("Error", "Credenciales incorrectas, intentelo de nuevo")


def registrarUsuario():
    nombre = nombreUsuario.get()
    password = contraUsuario.get()

    if db.session.query(Usuario).filter_by(nombre=nombre).first():
        mb.showerror("Usuario existente", "Por favor escoja otro nombre")
        nombreUsuario.set("")
        contraUsuario.set("")
    else:
        nuevoUsuario = Usuario(nombre, password)
        db.session.add(nuevoUsuario)
        db.session.commit()
        mb.showinfo("Registro con exito", f"Se ha registrado el usuario {nombre} con EXITO")
        nombreUsuario.set("")
        contraUsuario.set("")


def administracion():
    # Aqui configuramos las opciones de crear los contenidos audiovisuales para el administrador

    ventana_admin = Toplevel()  # Crear una ventana por delante de la principal
    root.withdraw()
    ventana_admin.title("Modo administracion")  # Titulo de la ventana
    ventana_admin.resizable(False, False)  # Redimension de la ventana

    titulo = Label(ventana_admin, text="ADMINISTRACION", font=("Arial", 36))
    titulo.grid(column=0, row=0, padx=10, pady=10, columnspan=4, sticky=W + E)

    nombreLabel = Label(ventana_admin, text="PELICULAS")
    nombreLabel.grid(column=0, row=1)
    passLabel = Label(ventana_admin, text="SERIES")
    passLabel.grid(column=0, row=2)

    regPeli = ttk.Button(ventana_admin, text="Registrar", command=add_pelicula)
    regPeli.grid(column=1, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E)
    regSerie = ttk.Button(ventana_admin, text="Registrar", command=add_serie)
    regSerie.grid(column=1, row=2, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E)

    editarPeli = ttk.Button(ventana_admin, text="Editar", command=editar_Peli)
    editarPeli.grid(column=3, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E)
    editarSerie = ttk.Button(ventana_admin, text="Editar", command=editar_Serie)
    editarSerie.grid(column=3, row=2, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E)

    controlUsuarios = ttk.Button(ventana_admin, text="Gestion Usuarios", command=gestion_usuarios)
    controlUsuarios.grid(column=0, row=4, ipadx=5, ipady=5, padx=5, pady=5, columnspan=4, sticky=W + E)

    boton_salir = ttk.Button(ventana_admin, text="Salir", command=lambda: ventana_admin.destroy())
    boton_salir.grid(column=0, row=5, sticky=E + W, columnspan=4)


def clientes(nombre):
    # Aqui configuramos las opciones que tienen los clientes
    ventana_usuarios = Toplevel()  # Crear una ventana por delante de la principal
    root.withdraw()
    ventana_usuarios.title("Seccion de Usuarios")  # Titulo de la ventana
    ventana_usuarios.resizable(False, False)

    titulo = Label(ventana_usuarios, text=f"Usuario {nombre}", font=("Arial", 36))
    titulo.grid(column=0, row=0, padx=10, pady=10, columnspan=4, sticky=W + E)

    buscarPeli = ttk.Button(ventana_usuarios, text="Buscar Peliculas", command=buscar_peli)
    buscarPeli.grid(column=0, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

    buscarSerie = ttk.Button(ventana_usuarios, text="Buscar Series", command=buscar_serie)
    buscarSerie.grid(column=1, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

    catalogos_peliculas = ttk.Button(ventana_usuarios, text="Catalogo de peliculas", command=catalogo_peliculas)
    catalogos_peliculas.grid(column=0, row=2, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

    catalogos_series = ttk.Button(ventana_usuarios, text="Catalogo de Series", command=catalogo_series)
    catalogos_series.grid(column=1, row=2, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

    graficas_visionado = ttk.Button(ventana_usuarios, text="Graficas de visionado", command=graficas)
    graficas_visionado.grid(column=0, row=3, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=4)

    boton_salir = ttk.Button(ventana_usuarios, text="Salir", command=lambda: ventana_usuarios.destroy())
    boton_salir.grid(column=0, row=5, sticky=E + W, columnspan=4)
