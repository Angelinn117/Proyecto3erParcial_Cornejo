import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import Util.generic as utl
from Forms.Master.form_master import MasterPanel
from Forms.Login.form_login_designer import FormLoginDesigner
from Forms.Register.form_register_designer import FormRegisterDesigner


class FormRegister(FormRegisterDesigner):

    def __init__(self):
        super().__init__()
