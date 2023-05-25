from Forms.Login.form_login_designer import FormLoginDesigner
from Forms.Register.form_register_designer import FormRegisterDesigner

class FormLogin (FormLoginDesigner):

    # Método encargado de abrir la ventana de registro:
    def abrirVentanaRegistro(self):
        self.ventanaRegistro = FormRegisterDesigner(self.loginScreen)
        self.ventanaRegistro.mainloop()

    def __init__(self):
        super().__init__()

