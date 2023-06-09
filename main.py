from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from functools import partial

from database import db
from styles import styles
from models.usuarios import Usuario
from administracion_audiovisual import add_pelicula, add_serie, editar_Serie, editar_Peli
from administracion_usuarios import gestion_usuarios, graficas_usuarios, graficas_totales
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

    # Textos y títulos
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

    # Botones de iniciar y registrar usuario

    iniciarSesionButton = Button(mainFrame, text="Iniciar Sesión", foreground=styles.FG_BOTON,
                                 activeforeground=styles.AFG_BOTON,
                                 activebackground=styles.ABG_BOTON, cursor="hand2", command=iniciarSesion)
    iniciarSesionButton.grid(column=1, row=3, ipadx=5, ipady=5, padx=10, pady=10)

    registrarButton = Button(mainFrame, text="Registrar Usuario", foreground=styles.FG_BOTON,
                             activeforeground=styles.AFG_BOTON,
                             activebackground=styles.ABG_BOTON, cursor="hand2", command=registrarUsuario)

    registrarButton.grid(column=0, row=3, ipadx=5, ipady=5, padx=10, pady=10)

    # Generamos el loop para que la ventana permanezca siempre abierta
    root.mainloop()


def iniciarSesion():
    nombre = nombreUsuario.get()
    password = contraUsuario.get()
    user = db.session.query(Usuario).filter_by(nombre=nombre, contra=password).first()
    admin = db.session.query(Usuario).filter_by(nombre="admin", contra="admin").first()

    # El usuario administrador se crea por defecto por el programa, pero está en la base de datos junto con todos los
    # usuarios y en esta función se busca al igual que cualquier usuario normal

    if user == admin:
        mb.showinfo("Conectado", "Sesión conectada en modo Administración")
        nombreUsuario.set("")
        contraUsuario.set("")
        administracion()
    elif user:
        mb.showinfo("Conectado", f"Sesión iniciada con éxito como {nombre}")
        nombreUsuario.set("")
        contraUsuario.set("")
        clientes(nombre)
    else:
        mb.showerror("Error", "Credenciales incorrectas, inténtelo de nuevo")


def registrarUsuario():
    nombre = nombreUsuario.get()
    password = contraUsuario.get()

    # Comprobaciones de que el usuario escoja un nombre que no exista ya y de que los campos no los deje vacíos

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
        mb.showinfo("Registro con éxito", f"Se ha registrado el usuario {nombre} con ÉXITO")
        nombreUsuario.set("")
        contraUsuario.set("")


def salir_y_restaurar(ventana):
    # Pequeña función que minimiza y oculta la ventana principal
    ventana.destroy()
    root.deiconify()


def administracion():
    # Aquí configuramos las opciones de crear los contenidos audiovisuales para el administrador asi como la gestion
    # de usuarios y sus respectivas gráficas

    ventana_admin = Toplevel()  # Crear una ventana por delante de la principal
    root.withdraw()  # Minimizar la ventana principal
    ventana_admin.config(width=400, height=320, background=styles.BG_VENTANA)
    ventana_admin.title("Modo administración")  # Título de la ventana
    ventana_admin.resizable(False, False)  # Redimensión de la ventana

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

    regSerie = Button(ventana_admin, text="Registrar", foreground=styles.FG_BOTON,
                      activeforeground=styles.AFG_BOTON,
                      activebackground=styles.ABG_BOTON, command=add_serie)
    regSerie.grid(column=1, row=2, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E)

    editarPeli = Button(ventana_admin, text="Editar", foreground=styles.FG_BOTON,
                        activeforeground=styles.AFG_BOTON,
                        activebackground=styles.ABG_BOTON, command=editar_Peli)
    editarPeli.grid(column=3, row=1, ipadx=5, ipady=5, padx=5, pady=5, columnspan=2, sticky=W + E)

    editarSerie = Button(ventana_admin, text="Editar", foreground=styles.FG_BOTON,
                         activeforeground=styles.AFG_BOTON,
                         activebackground=styles.ABG_BOTON, command=editar_Serie)
    editarSerie.grid(column=3, row=2, ipadx=5, ipady=5, padx=5, pady=5, columnspan=2, sticky=W + E)

    controlUsuarios = Button(ventana_admin, text="Gestion Usuarios", foreground=styles.FG_BOTON,
                             activeforeground=styles.AFG_BOTON,
                             activebackground=styles.ABG_BOTON, command=gestion_usuarios)
    controlUsuarios.grid(column=0, row=4, ipadx=5, ipady=5, padx=5, pady=5, columnspan=4, sticky=W + E)

    graficasUsuarios_pelis = Button(ventana_admin, text="Graficas de Peliculas", foreground=styles.FG_BOTON,
                                    activeforeground=styles.AFG_BOTON,
                                    activebackground=styles.ABG_BOTON, command=partial(graficas_usuarios, "Peliculas"))
    graficasUsuarios_pelis.grid(column=0, row=5, ipadx=5, ipady=5, padx=5, pady=5, columnspan=1, sticky=W + E)

    graficasUsuarios_series = Button(ventana_admin, text="Graficas de Series", foreground=styles.FG_BOTON,
                                     activeforeground=styles.AFG_BOTON,
                                     activebackground=styles.ABG_BOTON, command=partial(graficas_usuarios, "Series"))
    graficasUsuarios_series.grid(column=1, row=5, ipadx=5, ipady=5, padx=5, pady=5, columnspan=1, sticky=W + E)

    graficasUsuarios_totales = Button(ventana_admin, text="Graficas totales", foreground=styles.FG_BOTON,
                                      activeforeground=styles.AFG_BOTON,
                                      activebackground=styles.ABG_BOTON, command=graficas_totales)
    graficasUsuarios_totales.grid(column=2, row=5, ipadx=5, ipady=5, padx=5, pady=5, columnspan=2, sticky=W + E)

    boton_salir = Button(ventana_admin, text="Salir", foreground=styles.FG_BOTON,
                         activeforeground=styles.AFG_BOTON,
                         activebackground=styles.ABG_BOTON_SALIR, command=partial(salir_y_restaurar, ventana_admin))
    boton_salir.grid(column=0, row=6, sticky=E + W, columnspan=4)


def clientes(nombre):
    # Aquí configuramos las opciones que tienen los clientes
    ventana_usuarios = Toplevel()  # Crear una ventana por delante de la principal
    ventana_usuarios.config(width=400, height=320, background=styles.BG_VENTANA)
    root.withdraw()  # Minimizar la ventana principal
    ventana_usuarios.title("Sección de Usuarios")  # Título de la ventana
    ventana_usuarios.resizable(False, False)

    titulo = Label(ventana_usuarios, text=f"Usuario {nombre}", background=styles.BG_ETIQUETA, font=styles.ENCABEZADOS)
    titulo.grid(column=0, row=0, padx=10, pady=10, columnspan=4, sticky=W + E)

    button_buscar_peli = Button(ventana_usuarios, text="Buscar Peliculas", foreground=styles.FG_BOTON,
                                activeforeground=styles.AFG_BOTON,
                                activebackground=styles.ABG_BOTON,
                                command=partial(buscar_audiovisual, "peliculas", nombre))
    button_buscar_peli.grid(column=0, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=W, columnspan=4)

    button_buscarSerie = Button(ventana_usuarios, text="Buscar Series", foreground=styles.FG_BOTON,
                                activeforeground=styles.AFG_BOTON,
                                activebackground=styles.ABG_BOTON,
                                command=partial(buscar_audiovisual, "series", nombre))
    button_buscarSerie.grid(column=1, row=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=E, columnspan=4)

    button_catalogos_peliculas = Button(ventana_usuarios, text="Catalogo de peliculas", foreground=styles.FG_BOTON,
                                        activeforeground=styles.AFG_BOTON,
                                        activebackground=styles.ABG_BOTON,
                                        command=partial(catalogos, "pelicula", nombre))
    button_catalogos_peliculas.grid(column=0, row=2, ipadx=5, ipady=5, padx=5, pady=5, sticky=W, columnspan=4)

    button_catalogos_series = Button(ventana_usuarios, text="Catalogo de Series", foreground=styles.FG_BOTON,
                                     activeforeground=styles.AFG_BOTON,
                                     activebackground=styles.ABG_BOTON,
                                     command=partial(catalogos, "serie", nombre))
    button_catalogos_series.grid(column=1, row=2, ipadx=5, ipady=5, padx=5, pady=5, sticky=E, columnspan=4)

    graficas_visionado = Button(ventana_usuarios, text="Graficas de visionado", foreground=styles.FG_BOTON,
                                activeforeground=styles.AFG_BOTON,
                                activebackground=styles.ABG_BOTON,
                                command=partial(grafica_vision, nombre))
    graficas_visionado.grid(column=0, row=3, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=4)

    graficas_tiempo = Button(ventana_usuarios, text="Graficas de tiempo", foreground=styles.FG_BOTON,
                             activeforeground=styles.AFG_BOTON,
                             activebackground=styles.ABG_BOTON, command=partial(grafica_tiempo, nombre))
    graficas_tiempo.grid(column=0, row=4, ipadx=5, ipady=5, padx=5, pady=5, sticky=W + E, columnspan=4)

    boton_salir = Button(ventana_usuarios, text="Salir", foreground=styles.FG_BOTON,
                         activeforeground=styles.AFG_BOTON,
                         activebackground=styles.ABG_BOTON_SALIR, command=partial(salir_y_restaurar, ventana_usuarios))
    boton_salir.grid(column=0, row=5, sticky=E + W, columnspan=4)
