from PIL import ImageTk, Image

def readImage(path, size):
        return ImageTk.PhotoImage(Image.open(path).resize(size, Image.ANTIALIAS))

def centerWindow(window,windowWidth,windowHeight):
    sreenWidth = window.winfo_screenwidth()
    sreenHeight = window.winfo_screenheight()
    x = int((sreenWidth/2) - (windowWidth/2))
    y = int((sreenHeight/2) - (windowHeight/2))
    return window.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")