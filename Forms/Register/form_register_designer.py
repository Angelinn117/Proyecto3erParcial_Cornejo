import tkinter as tk
from tkinter import ttk, messagebox, END
from tkinter.font import BOLD

import cv2
from matplotlib import pyplot
from mtcnn import MTCNN

import Util.generic as utl

class FormRegisterDesigner(tk.Toplevel):

    global FormRegisterDesigner
    global usuario
    global contra  # Globalizamos las variables para usarlas en otras funciones
    global usuario_entrada
    global contra_entrada
    global pantalla1

    # Método encargado de registrar usuarios únicamente con nombre de usuarios y contraseñas:
    def registrar_usuario(self):

        self.validarCampoUsuario()  # Validar el campo de usuario antes de continuar

        # Si el campo de usuario no es válido, se mostrará un mensaje de error y no se ejecutará el resto del código
        if not self.usuario_valido:
            return

        usuario_info = self.usuario.get()  # Obetnemos la informacion alamcenada en usuario
        contra_info = self.contra.get()  # Obtenemos la informacion almacenada en contra

        archivo = open("./Registers/UserInformation_NameAndPassword/"+usuario_info, "w")  # Abriremos la informacion en modo escritura
        archivo.write(usuario_info + "\n")  # escribimos la info
        archivo.write(contra_info)
        archivo.close()

        # Limpiaremos los text variable (de igual forma dan error, checar eso):
        #usuario_entrada.delete(0, END)
        #contra_entrada.delete(0, END)

        # Ahora le diremos al usuario que su registro ha sido exitoso
        messagebox.showinfo(message="Registro exitoso.", title="¡Éxito!")

    def validarCampoUsuario(self):
        self.grab_set()
        nombre_usuario = self.usuario.get()

        if nombre_usuario.strip() == "":
            messagebox.showerror(message="Por favor, ingrese un nombre de usuario.", title="Campo Vacío")
            self.usuario_valido = False  # Indicar que el usuario no es válido
        else:
            self.usuario_valido = True  # Indicar que el usuario es válido

    # Registro de datos:
    def registro(self):
        global usuario
        global contra  # Globalizamos las variables para usarlas en otras funciones
        global usuario_entrada
        global contra_entrada
        global pantalla1

    def registro_facial(self):
        self.validarCampoUsuario()  # Validar el campo de usuario antes de continuar

        # Si el campo de usuario no es válido, se mostrará un mensaje de error y no se ejecutará el resto del código
        if not self.usuario_valido:
            return

        # Resto del código de registro facial aquí
        cap = cv2.VideoCapture(0)  # Elegimos la cámara con la que vamos a hacer la detección
        while True:
            ret, frame = cap.read()  # Leemos el video
            cv2.imshow('Registro Facial', frame)  # Mostramos el video en pantalla
            if cv2.waitKey(1) == 27:  # Cuando oprimamos "Escape", se rompe el video
                break
        usuario_img = self.usuario.get()

        # Ruta estática para almacenar las imágenes
        ruta_almacenamiento = "./Imagenes/ImagenesRegistroFacial/"  # Reemplaza con la ruta deseada

        # Guardamos la última captura del video como imagen en la ruta estática
        image_path = f"{ruta_almacenamiento}/{usuario_img}.jpg"
        cv2.imwrite(image_path, frame)
        messagebox.showinfo(message="Imagen de rostro almacenada correctamente.", title="Éxito")

        # Marcan error de que no hay atributo:
        #self.usuario_entrada.delete(0, END)  # Limpiamos los text variables
        #self.contra_entrada.delete(0, END)

        cap.release()  # Cerramos
        cv2.destroyAllWindows()


        # Detección de rostro y exportación de pixeles:
        def reg_rostro(img, lista_resultados):
            data = pyplot.imread(img)
            for i in range(len(lista_resultados)):
                x1, y1, ancho, alto = lista_resultados[i]['box']
                x2, y2 = x1 + ancho, y1 + alto
                pyplot.subplot(1, len(lista_resultados), i + 1)
                pyplot.axis('off')
                cara_reg = data[y1:y2, x1:x2]
                cara_reg = cv2.resize(cara_reg, (150, 200),
                                      interpolation=cv2.INTER_CUBIC)  # Guardamos la imagen con un tamaño de 150x200
                cv2.imwrite("./Imagenes/ImagenesRegistroFacial/"+usuario_img + ".jpg", cara_reg)
                pyplot.imshow(data[y1:y2, x1:x2])


        img = "./Imagenes/ImagenesRegistroFacial/"+usuario_img + ".jpg"
        pixeles = pyplot.imread(img)
        detector = MTCNN()
        caras = detector.detect_faces(pixeles)
        reg_rostro(img, caras)

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
        self.contra = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.contra.pack(fill=tk.X, padx=20, pady=8)
        self.contra.config(show="*")

        reconocimientoFacial = tk.Button(frame_form_fill, text="Registrar Rostro", font=('Times', 15, BOLD),
                                         bg='#45474B', bd=0,
                                         fg="#fff", command= self.registro_facial)
        reconocimientoFacial.pack(fill=tk.X, padx=20, pady=13)

        # Botón "Reconomiento de Voz":
        reconocimientoVoz = tk.Button(frame_form_fill, text="Registrar Voz", font=('Times', 15, BOLD),
                                      bg='#45474B', bd=0,
                                      fg="#fff")
        reconocimientoVoz.pack(fill=tk.X, padx=20, pady=13)

        register = tk.Button(frame_form_fill, text="Realizar Registro", font=('Times', 15, BOLD), bg='#45474B', bd=0,
                             fg="#fff", command=self.registrar_usuario)
        register.pack(fill=tk.X, padx=20, pady=13)

        self.mainloop()
