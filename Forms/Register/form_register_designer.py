import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import Util.generic as utl


class FormRegisterDesigner(tk.Toplevel):

    def validarCampoUsuario(self):
        self.grab_set()
        nombre_usuario = self.usuario.get()

        if nombre_usuario.strip() == "":
            messagebox.showerror(message="Por favor, ingrese un nombre de usuario.", title="Campo Vacío")
            return

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ventana de Registro")
        self.resizable(width=0, height=0)
        utl.centrar_ventana(self, 600, 400)

        logo = utl.leer_imagen("./Imagenes/UserLogo.png", (220, 220))
        # frame_logo
        frame_logo = tk.Frame(self, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg='#000000')
        frame_logo.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo, bg='#000000')
        label.place(x=0, y=-15, relwidth=1, relheight=1)

        # frame_form
        frame_form = tk.Frame(self, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)
        # frame_form

        # frame_form_top
        frame_form_top = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="Nuevo registro", font=('Times', 26), fg="#000000", bg='#fcfcfc',
                         pady=10)
        title.pack(expand=tk.YES, fill=tk.BOTH)
        # end frame_form_top

        # frame_form_fill
        frame_form_fill = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        etiqueta_usuario = tk.Label(frame_form_fill, text="Nombre de Usuario:", font=('Times', 14), fg="#666a88",
                                    bg='#fcfcfc',
                                    anchor="w")
        etiqueta_usuario.pack(fill=tk.X, padx=20, pady=0)
        self.usuario = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.usuario.pack(fill=tk.X, padx=20, pady=5)

        etiqueta_password = tk.Label(frame_form_fill, text="Contraseña:", font=('Times', 14), fg="#666a88",
                                     bg='#fcfcfc',
                                     anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.password.pack(fill=tk.X, padx=20, pady=8)
        self.password.config(show="*")

        reconocimientoFacial = tk.Button(frame_form_fill, text="Registrar Rostro", font=('Times', 15, BOLD),
                                         bg='#45474B', bd=0,
                                         fg="#fff")
        reconocimientoFacial.pack(fill=tk.X, padx=20, pady=13)

        # Botón "Reconomiento de Voz":
        reconocimientoVoz = tk.Button(frame_form_fill, text="Registrar Voz", font=('Times', 15, BOLD),
                                      bg='#45474B', bd=0,
                                      fg="#fff")
        reconocimientoVoz.pack(fill=tk.X, padx=20, pady=13)

        register = tk.Button(frame_form_fill, text="Realizar Registro", font=('Times', 15, BOLD), bg='#45474B', bd=0,
                             fg="#fff", command=self.validarCampoUsuario)
        register.pack(fill=tk.X, padx=20, pady=13)

        self.mainloop()
