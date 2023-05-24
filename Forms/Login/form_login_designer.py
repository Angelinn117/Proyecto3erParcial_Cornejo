import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import Util.generic as utl
from Forms.Master.form_master import MasterPanel
from Forms.Register.form_register_designer import FormRegisterDesigner

class FormLoginDesigner:

    global FormLoginDesigner
    global usuario
    global password


    def verificar(self):
        pass

    def verificacion_login(self):

        log_usuario = self.usuario.get()
        log_contra = self.password.get()

        #Seguir checando estas cosas que marcan error:
        #usuario_entrada2.delete(0, END)
        #contra_entrada2.delete(0, END)

        lista_archivos = os.listdir("./Registers/UserInformation_NameAndPassword/")  # Vamos a importar la lista de archivos con la libreria os
        if log_usuario in lista_archivos:  # Comparamos los archivos con el que nos interesa
            archivo2 = open("./Registers/UserInformation_NameAndPassword/"+log_usuario, "r")  # Abrimos el archivo en modo lectura
            verificacion = archivo2.read().splitlines()  # leera las lineas dentro del archivo ignorando el resto
            if log_contra in verificacion:
                messagebox.showinfo(message="Inicio de sesión exitoso.", title="¡Éxito!")
                MasterPanel()
            else:
                messagebox.showerror(message="Contraseña incorrecta.", title="Error")

        else:
            messagebox.showerror(message="Usuario no registrado.", title="Error")

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title('Inicio de sesion')
        self.ventana.geometry('800x500')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)
        utl.centrar_ventana(self.ventana, 800, 500)

        logo = utl.leer_imagen("./Imagenes/LogoAngelinn.png", (300, 300))
        # frame_logo
        frame_logo = tk.Frame(self.ventana, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg='#000000')
        frame_logo.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo, bg='#000000')
        label.place(x=0, y=-15, relwidth=1, relheight=1)

        # frame_form
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)
        # frame_form

        # frame_form_top
        frame_form_top = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="Inicio de sesión", font=('Times', 30), fg="#000000", bg='#fcfcfc',
                         pady=10)
        title.pack(expand=tk.YES, fill=tk.BOTH)
        # end frame_form_top

        # frame_form_fill
        frame_form_fill = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        etiqueta_usuario = tk.Label(frame_form_fill, text="Nombre de Usuario:", font=('Times', 14), fg="#666a88", bg='#fcfcfc',
                                    anchor="w")
        etiqueta_usuario.pack(fill=tk.X, padx=20, pady=0)
        self.usuario = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.usuario.pack(fill=tk.X, padx=20, pady=10)

        etiqueta_password = tk.Label(frame_form_fill, text="Contraseña:", font=('Times', 14), fg="#666a88", bg='#fcfcfc',
                                     anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.password.pack(fill=tk.X, padx=20, pady=10)
        self.password.config(show="*")

        inicio = tk.Button(frame_form_fill, text="Iniciar sesión", font=('Times', 15, BOLD), bg='#45474B', bd=0,
                           fg="#fff", command=self.verificacion_login)
        inicio.pack(fill=tk.X, padx=20, pady=15)


        #CODIGO EXPERIMENTAL (Le falta el "Command" para indicarle que hacer al pulsar el botón:
        #Botón "Reconocimiento Facial":
        reconocimientoFacial = tk.Button(frame_form_fill, text="Reconocimiento Facial", font=('Times', 15, BOLD), bg='#45474B', bd=0,
                           fg="#fff")
        reconocimientoFacial.pack(fill=tk.X, padx=20, pady=15)


        #Botón "Reconomiento de Voz":
        reconocimientoVoz = tk.Button(frame_form_fill, text="Reconocimiento de Voz", font=('Times', 15, BOLD),
                                         bg='#45474B', bd=0,
                                         fg="#fff")
        reconocimientoVoz.pack(fill=tk.X, padx=20, pady=15)

        register = tk.Button(frame_form_fill, text="Registrarse", font=('Times', 15, BOLD), bg='#45474B', bd=0,
                           fg="#fff", command=self.abrirVentanaRegistro)
        register.pack(fill=tk.X, padx=20, pady=15)

        # end frame_form_fill
        self.ventana.mainloop()