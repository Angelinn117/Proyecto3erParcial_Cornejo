import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import Util.generic as utl
from Forms.Master.form_master import MasterPanel
from Forms.Login.form_login_designer import FormLoginDesigner
from Forms.Register.form_register_designer import FormRegisterDesigner

class FormLogin (FormLoginDesigner):

    def verificar(self):
        usu = self.usuario.get()
        password = self.password.get()
        if (usu == "root" and password == "1234"):
            self.ventana.destroy()
            MasterPanel()
        else:
            messagebox.showerror(message="Datos incorrectos. Por favor, inténtelo de nuevo.", title="Aviso")

    def abrirVentanaRegistro(self):
        self.ventanaRegistro = FormRegisterDesigner(self.ventana)
        self.ventanaRegistro.mainloop()

    def __init__(self):
        super().__init__()

