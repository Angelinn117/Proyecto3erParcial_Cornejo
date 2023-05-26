import os
import tkinter as tk
import cv2

import Util.generic as utl

from tkinter import ttk, messagebox
from tkinter.font import BOLD
from matplotlib import pyplot
from mtcnn import MTCNN
from Forms.Master.form_master import MasterPanel
from Forms.Register.form_register import FormRegister

class FormLogin:

    usuario = ''
    password = ''

    # Método encargado de abrir la ventana de registro:
    def openRegisterWindow(self):
        self.ventanaRegistro = FormRegister(self.loginScreen)
        self.ventanaRegistro.mainloop()

    # Método encargado de verificar los registros para validar al usuario (nombre y contraseña):
    def loginVerification(self):

        log_User = self.usuario.get()
        log_Password = self.password.get()

        registers = os.listdir("./Registers/UserInformation_NameAndPassword/")

        if log_User in registers: 
            file = open("./Registers/UserInformation_NameAndPassword/"+ log_User, "r")  
            verification = file.read().splitlines()
            
            if log_Password in verification:
                messagebox.showinfo(message="Inicio de sesión exitoso.", title="¡Éxito!")
                MasterPanel()
            else:
                messagebox.showerror(message="Contraseña incorrecta. Por favor, vuelva a intentarlo.", title="Error")

        else:
            messagebox.showerror(message="Usuario no registrado.", title="Error")

    # Método encargado de tomar la foto con la que el usuario intentará identificarse:
    def facialLogin(self):
        cap = cv2.VideoCapture(0)
        while (True):
            ret, frame = cap.read()
            cv2.imshow('Login Facial', frame)
            if cv2.waitKey(1) == 27:
                break
        userName = self.usuario.get()
        cv2.imwrite("./Images/FacialRegisteredImages/" + userName + "LOG.jpg",
                    frame)
        cap.release()
        cv2.destroyAllWindows()

        # Método encargado en procesar la imagen (tamaño, colores, etc.) y guardarla con la etiqueta "LOG":
        def facialProcess(img, resultsList):
            data = pyplot.imread(img)
            for i in range(len(resultsList)):
                x1, y1, ancho, alto = resultsList[i]['box']
                x2, y2 = x1 + ancho, y1 + alto
                face_reg = data[y1:y2, x1:x2]
                face_reg = cv2.resize(face_reg, (150, 200),
                                      interpolation=cv2.INTER_CUBIC)  # Guardamos la imagen 150x200
                cv2.imwrite("./Images/FacialRegisteredImages/" + userName + "LOG.jpg", face_reg)
                return

        img = "./Images/FacialRegisteredImages/" + userName + "LOG.jpg"
        pixels = pyplot.imread(img)
        detector = MTCNN()
        faces = detector.detect_faces(pixels)
        facialProcess(img, faces)

        # Método encargado de analizar las imágenes mediante el algoritmo ORB (Oriented FAST and Rotated BRIEF):
        def imageComparator(img1, img2):
            orb = cv2.ORB_create()

            kpa, descr_a = orb.detectAndCompute(img1, None)
            kpb, descr_b = orb.detectAndCompute(img2, None)

            comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

            matches = comp.match(descr_a, descr_b)

            similarRegions = [i for i in matches if i.distance < 70]
            if len(matches) == 0:
                return 0
            return len(similarRegions) / len(matches)

        os.listdir("./Registers/UserInformation_NameAndPassword/")
        imgFiles = os.listdir("./Images/FacialRegisteredImages/")

        if userName + ".jpg" in imgFiles:
            face_reg = cv2.imread("./Images/FacialRegisteredImages/" + userName + ".jpg", 0)
            face_log = cv2.imread("./Images/FacialRegisteredImages/" + userName + "LOG.jpg", 0)
            similarity = imageComparator(face_reg, face_log)

            if similarity >= 0.98:
                messagebox.showinfo(message="Bienvenido. Similitud registrada: " + str(similarity), title="¡Éxito")
            else:
                messagebox.showerror(message="Rostro no identificado. Similitud registrada: " + str(similarity), title="Fallo")

        else:
            messagebox.showerror(message="Usuario no registrado.", title="Error")

    #Método constructor encargado de ejecutar la ventana de login junto a su diseño:
    def __init__(self):
        self.loginScreen = tk.Tk()
        self.loginScreen.title('Inicio de sesion')
        self.loginScreen.geometry('800x500')
        self.loginScreen.config(bg='#fcfcfc')
        self.loginScreen.resizable(width=0, height=0)
        utl.centerWindow(self.loginScreen, 800, 500)

        logo = utl.readImage("./Images/Resources/LogoAngelinn.png", (300, 300))
        # frame_logo
        frame_logo = tk.Frame(self.loginScreen, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg='#000000')
        frame_logo.pack(side="left", expand=tk.YES, fill=tk.BOTH)
        label = tk.Label(frame_logo, image=logo, bg='#000000')
        label.place(x=0, y=-15, relwidth=1, relheight=1)

        # frame_form
        frame_form = tk.Frame(self.loginScreen, bd=0, relief=tk.SOLID, bg='#fcfcfc')
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

        userLabel = tk.Label(frame_form_fill, text="Nombre de Usuario:", font=('Times', 14), fg="#666a88", bg='#fcfcfc',
                                    anchor="w")
        userLabel.pack(fill=tk.X, padx=20, pady=0)
        self.usuario = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.usuario.pack(fill=tk.X, padx=20, pady=10)

        passwordLabel = tk.Label(frame_form_fill, text="Contraseña:", font=('Times', 14), fg="#666a88", bg='#fcfcfc',
                                     anchor="w")
        passwordLabel.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.password.pack(fill=tk.X, padx=20, pady=10)
        self.password.config(show="*")

        btnIniciarSesion = tk.Button(frame_form_fill, text="Iniciar sesión", font=('Times', 15, BOLD), bg='#45474B', bd=0,
                           fg="#fff", command=self.loginVerification)
        btnIniciarSesion.pack(fill=tk.X, padx=20, pady=15)

        btnReconocimientoFacial = tk.Button(frame_form_fill, text="Reconocimiento Facial", font=('Times', 15, BOLD), bg='#45474B', bd=0,
                           fg="#fff", command=self.facialLogin)
        btnReconocimientoFacial.pack(fill=tk.X, padx=20, pady=15)

        btnReconocimientoVoz = tk.Button(frame_form_fill, text="Reconocimiento de Voz", font=('Times', 15, BOLD),
                                         bg='#45474B', bd=0, fg="#fff")
        btnReconocimientoVoz.pack(fill=tk.X, padx=20, pady=15)

        btnRegistro = tk.Button(frame_form_fill, text="Registrarse", font=('Times', 15, BOLD), bg='#45474B', bd=0,
                           fg="#fff", command=self.openRegisterWindow)
        btnRegistro.pack(fill=tk.X, padx=20, pady=15)

        # end frame_form_fill
        self.loginScreen.mainloop()
