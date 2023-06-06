from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from functools import partial
import db
from styles import styles
from models.usuarios import Usuario
from administracion_audiovisual import add_pelicula, add_serie, editar_Serie, editar_Peli
from administracion_usuarios import gestion_usuarios, graficas_usuarios
from clientes_busquedas import buscar_audiovisual
from clientes_catalogos import catalogos, grafica_tiempo, grafica_vision

root = Tk()
nombreUsuario = StringVar()
contraUsuario = StringVar()


def interfazUsuario():
    # Ventana Principal
    root.title("Login Usuarios")
    root.resizable(False, False)

    # Frame Principal
    mainFrame = Frame(root)
    mainFrame.pack()
    mainFrame.config(width=400, height=320, background=styles.BG_VENTANA)

    # Textos y titulos
    titulo = ttk.Label(mainFrame, text="PLATAFORMA AUDIOVISUAL", font=styles.ENCABEZADOS,
                       background=styles.BG_ETIQUETA)
    titulo.grid(column=0, row=0, padx=10, pady=10, columnspan=2)

    nombreLabel = ttk.Label(mainFrame, text="Nombre ", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
    nombreLabel.grid(column=0, row=1)

    passLabel = ttk.Label(mainFrame, text="Contraseña ", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
    passLabel.grid(column=0, row=2)

    # Entradas de texto

    nombreUsuario.set("")
    nombreEntry = Entry(mainFrame, textvariable=nombreUsuario, font=styles.ENTRADAS_DE_TEXTO)
    nombreEntry.grid(column=1, row=1)

    contraUsuario.set("")
    contraEntry = Entry(mainFrame, textvariable=contraUsuario, font=styles.ENTRADAS_DE_TEXTO, show="*")
    contraEntry.grid(column=1, row=2)

    # Botones

    iniciarSesionButton = Button(mainFrame, text="Iniciar Sesion", foreground=styles.FG_BOTON,
                                 activeforeground=styles.AFG_BOTON,
                                 activebackground=styles.ABG_BOTON, command=iniciarSesion)
    iniciarSesionButton.grid(column=1, row=3, ipadx=5, ipady=5, padx=10, pady=10)

    registrarButton = Button(mainFrame, text="Registrar Usuario", foreground=styles.FG_BOTON,
                             activeforeground=styles.AFG_BOTON,
                             activebackground=styles.ABG_BOTON, command=registrarUsuario)

    registrarButton.grid(column=0, row=3, ipadx=5, ipady=5, padx=10, pady=10)

    root.mainloop()


def iniciarSesion():
    nombre = nombreUsuario.get()
    password = contraUsuario.get()
    user = db.session.query(Usuario).filter_by(nombre=nombre, contra=password).first()
    admin = db.session.query(Usuario).filter_by(nombre="a", contra="a").first()
    if user == admin:
        mb.showinfo("Conectado", "Sesion conectada en modo Administracion")
        nombreUsuario.set("")
        contraUsuario.set("")
        administracion()
    elif user:
        mb.showinfo("Conectado", f"Sesion iniciada con exito como {nombre}")
        nombreUsuario.set("")
        contraUsuario.set("")
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
    elif len(nombre) == 0 or len(password) == 0:
        mb.showerror("Ausencia de datos", "Introduzca nombre y contraseña")
        nombreUsuario.set("")
        contraUsuario.set("")
    else:
        nuevoUsuario = Usuario(nombre, password)
        db.session.add(nuevoUsuario)
        db.session.commit()
        mb.showinfo("Registro con exito", f"Se ha registrado el usuario {nombre} con EXITO")
        nombreUsuario.set("")
        contraUsuario.set("")


def salir_y_restaurar(ventana):
    ventana.destroy()
    root.deiconify()


def administracion():
    # Aqui configuramos las opciones de crear los contenidos audiovisuales para el administrador

    ventana_admin = Toplevel()  # Crear una ventana por delante de la principal
    root.withdraw()
    ventana_admin.config(width=400, height=320, background=styles.BG_VENTANA)
    ventana_admin.title("Modo administracion")  # Titulo de la ventana
    ventana_admin.resizable(False, False)  # Redimension de la ventana

    titulo = ttk.Label(ventana_admin, text="ADMINISTRACION", background=styles.BG_ETIQUETA, font=styles.ENCABEZADOS)
    titulo.grid(column=0, row=0, padx=10, pady=10, columnspan=4, sticky=W + E)

    nombreLabel = ttk.Label(ventana_admin, text="PELICULAS", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
    nombreLabel.grid(column=0, row=1)
    passLabel = ttk.Label(ventana_admin, text="SERIES", background=styles.BG_ETIQUETA, font=styles.TEXTOS)
    passLabel.grid(column=0, row=2)

    regPeli = Button(ventana_admin, text="Registrar", foreground=styles.FG_BOTON,
                     activeforeground=styles.AFG_BOTON,
                     activebackground=styles.ABG_BOTON, command=add_pelicula)
    regPeli.grid(column=1, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E)
    regSerie = ttk.Button(ventana_admin, text="Registrar", command=add_serie)
    regSerie.grid(column=1, row=2, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E)

    editarPeli = ttk.Button(ventana_admin, text="Editar", command=editar_Peli)
    editarPeli.grid(column=3, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E)
    editarSerie = ttk.Button(ventana_admin, text="Editar", command=editar_Serie)
    editarSerie.grid(column=3, row=2, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E)

    controlUsuarios = ttk.Button(ventana_admin, text="Gestion Usuarios", command=gestion_usuarios)
    controlUsuarios.grid(column=0, row=4, ipadx=5, ipady=5, padx=5, pady=5, columnspan=4, sticky=W + E)

    graficasUsuarios = ttk.Button(ventana_admin, text="Graficas de Usuarios", command=graficas_usuarios)
    graficasUsuarios.grid(column=0, row=5, ipadx=5, ipady=5, padx=5, pady=5, columnspan=4, sticky=W + E)

    boton_salir = ttk.Button(ventana_admin, text="Salir", command=partial(salir_y_restaurar, ventana_admin))
    boton_salir.grid(column=0, row=6, sticky=E + W, columnspan=4)


def clientes(nombre):
    # Aqui configuramos las opciones que tienen los clientes
    ventana_usuarios = Toplevel()  # Crear una ventana por delante de la principal
    root.withdraw()
    ventana_usuarios.title("Seccion de Usuarios")  # Titulo de la ventana
    ventana_usuarios.resizable(False, False)

    titulo = Label(ventana_usuarios, text=f"Usuario {nombre}", font=("Arial", 36))
    titulo.grid(column=0, row=0, padx=10, pady=10, columnspan=4, sticky=W + E)

    button_buscar_peli = ttk.Button(ventana_usuarios, text="Buscar Peliculas",
                                    command=partial(buscar_audiovisual, "peliculas", nombre))
    button_buscar_peli.grid(column=0, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

    button_buscarSerie = ttk.Button(ventana_usuarios, text="Buscar Series",
                                    command=partial(buscar_audiovisual, "series", nombre))
    button_buscarSerie.grid(column=1, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

    button_catalogos_peliculas = ttk.Button(ventana_usuarios, text="Catalogo de peliculas",
                                            command=partial(catalogos, "pelicula", nombre))
    button_catalogos_peliculas.grid(column=0, row=2, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

    button_catalogos_series = ttk.Button(ventana_usuarios, text="Catalogo de Series",
                                         command=partial(catalogos, "serie", nombre))
    button_catalogos_series.grid(column=1, row=2, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=1)

    graficas_visionado = ttk.Button(ventana_usuarios, text="Graficas de visionado",
                                    command=partial(grafica_vision, nombre))
    graficas_visionado.grid(column=0, row=3, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=4)

    graficas_tiempo = ttk.Button(ventana_usuarios, text="Graficas de tiempo", command=partial(grafica_tiempo, nombre))
    graficas_tiempo.grid(column=0, row=4, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=4)

    boton_salir = ttk.Button(ventana_usuarios, text="Salir", command=partial(salir_y_restaurar, ventana_usuarios))
    boton_salir.grid(column=0, row=5, sticky=E + W, columnspan=4)
