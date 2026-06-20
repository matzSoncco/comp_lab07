"""
Tarea 4 – Visualización interactiva de canales
Presiona R / G / B para activar o desactivar cada canal. Q para salir.
"""
import cv2
import numpy as np
from utils import cargar_img, pedir_imagen


def run(ruta):
    img = cargar_img(ruta)
    b_ch, g_ch, r_ch = cv2.split(img)
    activos = [True, True, True]   # R, G, B
    TITULO = "Tarea 4  |  R = rojo   G = verde   B = azul   Q = salir"
    cv2.namedWindow(TITULO, cv2.WINDOW_NORMAL)

    while True:
        zeros = np.zeros_like(r_ch)
        frame = cv2.merge([
            b_ch if activos[2] else zeros,
            g_ch if activos[1] else zeros,
            r_ch if activos[0] else zeros,
        ])

        barra = np.full((32, frame.shape[1], 3), 28, dtype=np.uint8)
        txt = (f"[R] {'ON ' if activos[0] else 'OFF'}   "
               f"[G] {'ON ' if activos[1] else 'OFF'}   "
               f"[B] {'ON ' if activos[2] else 'OFF'}")
        cv2.putText(barra, txt, (10, 22),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        cv2.imshow(TITULO, np.vstack([frame, barra]))

        tecla = cv2.waitKey(30) & 0xFF
        if tecla == ord('r'):
            activos[0] = not activos[0]
        elif tecla == ord('g'):
            activos[1] = not activos[1]
        elif tecla == ord('b'):
            activos[2] = not activos[2]
        elif tecla in (ord('q'), 27):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    ruta = pedir_imagen("Seleccionar imagen")
    if ruta:
        run(ruta)
