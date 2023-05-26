import tkinter as tk
from tkinter.font import BOLD
import Util.generic as utl

class MasterPanel:

    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title('Master panel')
        w, h = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        self.window.geometry("%dx%d+0+0" % (w, h))
        self.window.config(bg='#fcfcfc')
        self.window.resizable(width=0, height=0)

        logo = utl.readImage("./Images/Resources/BienvenidaCanina.jpeg", (600, 600))

        label = tk.Label(self.window, image=logo, bg='#000000')
        label.place(x=0, y=0, relwidth=1, relheight=1)

        self.window.mainloop()