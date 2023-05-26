import tkinter as tk
import cv2
import Util.generic as utl

from tkinter import ttk, messagebox
from tkinter.font import BOLD
from matplotlib import pyplot
from mtcnn import MTCNN

class FormRegister(tk.Toplevel):

    # Método encargado de registrar usuarios únicamente con nombre de usuarios y contraseñas:
    def userRegister(self):

        self.fieldsValidation()

        if not self.validUser:
            return

        nameUser = self.usuario.get()
        passwordUser = self.password.get()

        file = open("./Registers/UserInformation_NameAndPassword/" + nameUser, "w")
        file.write(nameUser + "\n" + passwordUser)
        file.close()

        messagebox.showinfo(message="Registro exitoso.", title="¡Éxito!")
        self.destroy()

    # Método encargado de no permitir campos vacios en "Nombre" y "Contraseña" del registro:
    def fieldsValidation(self):
        self.grab_set()
        userName = self.usuario.get()
        userPassword = self.password.get()

        if userName.strip() == "" or userPassword.strip() == "":
            messagebox.showerror(message="Por favor, ingrese todos los campos.", title="Campo Vacío")
            self.validUser = False
            self.validPassword = False
        else:
            self.validUser = True
            self.validPassword = True

    # Método encargado de detectar y almacenar rostros de los usuarios:
    def facialRegistration(self):
        self.fieldsValidation()

        if not self.validUser:
            return

        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            cv2.imshow('Registro Facial', frame)
            if cv2.waitKey(1) == 27:
                break
        userName = self.usuario.get()

        pathUsersImages = "./Images/FacialRegisteredImages/"

        image_path = f"{pathUsersImages}/{userName}.jpg"
        cv2.imwrite(image_path, frame)
        messagebox.showinfo(message="Imagen de rostro almacenada correctamente.", title="Éxito")

        cap.release()
        cv2.destroyAllWindows()

        # Detección de rostro y exportación de pixeles:
        def facialDetection(img, resultsList):
            data = pyplot.imread(img)
            for i in range(len(resultsList)):
                x1, y1, width, height = resultsList[i]['box']
                x2, y2 = x1 + width, y1 + height
                pyplot.subplot(1, len(resultsList), i + 1)
                pyplot.axis('off')
                faceRegister = data[y1:y2, x1:x2]
                faceRegister = cv2.resize(faceRegister, (150, 200), interpolation=cv2.INTER_CUBIC)
                cv2.imwrite("./Images/FacialRegisteredImages/" + userName + ".jpg", faceRegister)
                pyplot.imshow(data[y1:y2, x1:x2])

        img = "./Images/FacialRegisteredImages/" + userName + ".jpg"
        pixels = pyplot.imread(img)
        detector = MTCNN()
        faces = detector.detect_faces(pixels)
        facialDetection(img, faces)

        self.userRegister()

    # Método constructor encargado de ejecutar la ventana de registro junto a su diseño y componentes:
    def __init__(self, parent):

        super().__init__(parent)
        self.title("Ventana de Registro")
        self.resizable(width=0, height=0)
        utl.centerWindow(self, 600, 400)

        logo = utl.readImage("./Images/Resources/UserLogo.png", (220, 220))
        # frame_logo
        frame_logo = tk.Frame(self, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg='#000000')
        frame_logo.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo, bg='#000000')
        label.place(x=0, y=-15, relwidth=1, relheight=1)

        # frame_form
        frame_form = tk.Frame(self, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        # frame_form_top
        frame_form_top = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="Nuevo registro", font=('Times', 26), fg="#000000", bg='#fcfcfc',
                         pady=10)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        # frame_form_fill
        frame_form_fill = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        userLabel = tk.Label(frame_form_fill, text="Nombre de Usuario:", font=('Times', 14), fg="#666a88",
                             bg='#fcfcfc',
                             anchor="w")
        userLabel.pack(fill=tk.X, padx=20, pady=0)
        self.usuario = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.usuario.pack(fill=tk.X, padx=20, pady=5)

        passwordLabel = tk.Label(frame_form_fill, text="Contraseña:", font=('Times', 14), fg="#666a88",
                                 bg='#fcfcfc',
                                 anchor="w")
        passwordLabel.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.password.pack(fill=tk.X, padx=20, pady=8)
        self.password.config(show="*")

        btnReconocimientoFacial = tk.Button(frame_form_fill, text="Registrar Rostro", font=('Times', 15, BOLD),
                                            bg='#45474B', bd=0,
                                            fg="#fff", command=self.facialRegistration)
        btnReconocimientoFacial.pack(fill=tk.X, padx=20, pady=13)

        btnReconocimientoVoz = tk.Button(frame_form_fill, text="Registrar Voz", font=('Times', 15, BOLD),
                                         bg='#45474B', bd=0,
                                         fg="#fff")
        btnReconocimientoVoz.pack(fill=tk.X, padx=20, pady=13)

        btnRegister = tk.Button(frame_form_fill, text="Realizar Registro", font=('Times', 15, BOLD), bg='#45474B', bd=0,
                                fg="#fff", command=self.userRegister)
        btnRegister.pack(fill=tk.X, padx=20, pady=13)

        self.mainloop()
