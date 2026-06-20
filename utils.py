import cv2
import numpy as np
import os
from PIL import Image

OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)

FILTRO = [("Imágenes", "*.jpg *.jpeg *.png *.bmp *.avif *.avifs *.webp"),
          ("Todo", "*.*")]


def cargar_img(ruta, flags=cv2.IMREAD_COLOR):
    img = cv2.imread(ruta, flags)
    if img is not None:
        return img
    pil = Image.open(ruta)
    if flags == cv2.IMREAD_GRAYSCALE:
        return np.array(pil.convert("L"))
    return cv2.cvtColor(np.array(pil.convert("RGB")), cv2.COLOR_RGB2BGR)


def ruta_out(nombre):
    return os.path.join(OUT_DIR, nombre)


def pedir_imagen(titulo="Seleccionar imagen"):
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    ruta = filedialog.askopenfilename(title=titulo, filetypes=FILTRO)
    root.destroy()
    return ruta
