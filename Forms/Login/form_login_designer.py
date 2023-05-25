import os
import tkinter as tk
import cv2
from tkinter import ttk, messagebox
from tkinter.font import BOLD

from matplotlib import pyplot
from mtcnn import MTCNN

import Util.generic as utl
from Forms.Master.form_master import MasterPanel
from Forms.Register.form_register_designer import FormRegisterDesigner

class FormLoginDesigner:

    usuario = ''
    password = ''

    def verificar(self):
        pass

    # Método encargado de verificar los registros para validar al usuario (nombre y contraseña):
    def verificacion_login(self):

        log_usuario = self.usuario.get()
        log_contra = self.password.get()

        #Seguir checando estas cosas que marcan error:
        #usuario_entrada2.delete(0, END)
        #contra_entrada2.delete(0, END)

        registers = os.listdir("./Registers/UserInformation_NameAndPassword/")  # Vamos a importar la lista de archivos con la libreria os
        if log_usuario in registers:  # Comparamos los archivos con el que nos interesa
            archivo2 = open("./Registers/UserInformation_NameAndPassword/"+log_usuario, "r")  # Abrimos el archivo en modo lectura
            verificacion = archivo2.read().splitlines()  # leera las lineas dentro del archivo ignorando el resto
            if log_contra in verificacion:
                messagebox.showinfo(message="Inicio de sesión exitoso.", title="¡Éxito!")
                MasterPanel()
            else:
                messagebox.showerror(message="Contraseña incorrecta. Por favor, vuelva a intentarlo.", title="Error")

        else:
            messagebox.showerror(message="Usuario no registrado.", title="Error")

    def login_facial(self):
        # ------------------------------Vamos a capturar el rostro-----------------------------------------------------
        cap = cv2.VideoCapture(0)  # Elegimos la camara con la que vamos a hacer la deteccion
        while (True):
            ret, frame = cap.read()  # Leemos el video
            cv2.imshow('Login Facial', frame)  # Mostramos el video en pantalla
            if cv2.waitKey(1) == 27:  # Cuando oprimamos "Escape" rompe el video
                break
        usuario_login = self.usuario.get()  # Con esta variable vamos a guardar la foto pero con otro nombre para no sobreescribir
        cv2.imwrite("./Imagenes/ImagenesRegistroFacial/" + usuario_login + "LOG.jpg",
                    frame)  # Guardamos la ultima caputra del video como imagen y asignamos el nombre del usuario
        cap.release()  # Cerramos
        cv2.destroyAllWindows()

        def log_rostro(img, lista_resultados):
            data = pyplot.imread(img)
            for i in range(len(lista_resultados)):
                x1, y1, ancho, alto = lista_resultados[i]['box']
                x2, y2 = x1 + ancho, y1 + alto
                pyplot.subplot(1, len(lista_resultados), i + 1)
                pyplot.axis('off')
                cara_reg = data[y1:y2, x1:x2]
                cara_reg = cv2.resize(cara_reg, (150, 200),
                                      interpolation=cv2.INTER_CUBIC)  # Guardamos la imagen 150x200
                cv2.imwrite("./Imagenes/ImagenesRegistroFacial/" + usuario_login + "LOG.jpg", cara_reg)
                return pyplot.imshow(data[y1:y2, x1:x2])


        # -------------------------- Detectamos el rostro-------------------------------------------------------

        img = "./Imagenes/ImagenesRegistroFacial/" + usuario_login + "LOG.jpg"
        pixeles = pyplot.imread(img)
        detector = MTCNN()
        caras = detector.detect_faces(pixeles)
        log_rostro(img, caras)

        # -------------------------- Funcion para comparar los rostros --------------------------------------------
        def orb_sim(img1, img2):
            orb = cv2.ORB_create()  # Creamos el objeto de comparacion

            kpa, descr_a = orb.detectAndCompute(img1, None)  # Creamos descriptor 1 y extraemos puntos claves
            kpb, descr_b = orb.detectAndCompute(img2, None)  # Creamos descriptor 2 y extraemos puntos claves

            comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)  # Creamos comparador de fuerza

            matches = comp.match(descr_a, descr_b)  # Aplicamos el comparador a los descriptores

            regiones_similares = [i for i in matches if
                                  i.distance < 70]  # Extraemos las regiones similares en base a los puntos claves
            if len(matches) == 0:
                return 0
            return len(regiones_similares) / len(matches)  # Exportamos el porcentaje de similitud

        # ---------------------------- Importamos las imagenes y llamamos la funcion de comparacion ---------------------------------
        os.listdir("./Registers/UserInformation_NameAndPassword/")
        im_archivos = os.listdir("./Imagenes/ImagenesRegistroFacial/")  # Vamos a importar la lista de archivos con la libreria os
        if usuario_login + ".jpg" in im_archivos:  # Comparamos los archivos con el que nos interesa
            rostro_reg = cv2.imread("./Imagenes/ImagenesRegistroFacial/" + usuario_login + ".jpg", 0)  # Importamos el rostro del registro
            rostro_log = cv2.imread("./Imagenes/ImagenesRegistroFacial/" + usuario_login + "LOG.jpg", 0)  # Importamos el rostro del inicio de sesion
            similitud = orb_sim(rostro_reg, rostro_log)
            if similitud >= 0.95:
                messagebox.showinfo(message="Bienvenido. Similitud registrada: " + str(similitud), title="¡Éxito")
            else:
                messagebox.showerror(message="Rostro no identificado. Similitud registrada: " + str(similitud), title="Fallo")

        else:
            messagebox.showerror(message="Usuario no registrado.", title="Error")

    #Método constructor encargado de ejecutar la ventana de login junto a su diseño:
    def __init__(self):
        self.loginScreen = tk.Tk()
        self.loginScreen.title('Inicio de sesion')
        self.loginScreen.geometry('800x500')
        self.loginScreen.config(bg='#fcfcfc')
        self.loginScreen.resizable(width=0, height=0)
        utl.centrar_ventana(self.loginScreen, 800, 500)

        logo = utl.leer_imagen("./Imagenes/LogoAngelinn.png", (300, 300))
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
                           fg="#fff", command=self.verificacion_login)
        btnIniciarSesion.pack(fill=tk.X, padx=20, pady=15)

        btnReconocimientoFacial = tk.Button(frame_form_fill, text="Reconocimiento Facial", font=('Times', 15, BOLD), bg='#45474B', bd=0,
                           fg="#fff", command=self.login_facial)
        btnReconocimientoFacial.pack(fill=tk.X, padx=20, pady=15)

        btnReconocimientoVoz = tk.Button(frame_form_fill, text="Reconocimiento de Voz", font=('Times', 15, BOLD),
                                         bg='#45474B', bd=0, fg="#fff")
        btnReconocimientoVoz.pack(fill=tk.X, padx=20, pady=15)

        btnRegistro = tk.Button(frame_form_fill, text="Registrarse", font=('Times', 15, BOLD), bg='#45474B', bd=0,
                           fg="#fff", command=self.abrirVentanaRegistro)
        btnRegistro.pack(fill=tk.X, padx=20, pady=15)

        # end frame_form_fill
        self.loginScreen.mainloop()