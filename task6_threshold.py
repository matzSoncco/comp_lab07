"""
Tarea 6 – Umbral binario interactivo
Mueve el deslizador para ajustar el umbral. Q para guardar y salir.
"""
import cv2
import numpy as np
from utils import cargar_img, ruta_out, pedir_imagen


def run(ruta, umbral_inicial=127):
    img_color = cargar_img(ruta)
    gris = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    TITULO = "Tarea 6 · Umbral binario  |  Q = guardar y salir"
    cv2.namedWindow(TITULO, cv2.WINDOW_NORMAL)
    cv2.createTrackbar("Umbral", TITULO, umbral_inicial, 255, lambda _: None)

    while True:
        t = cv2.getTrackbarPos("Umbral", TITULO)
        _, binaria = cv2.threshold(gris, t, 255, cv2.THRESH_BINARY)

        # Mostrar original en grises y resultado lado a lado
        lado = np.hstack([gris, binaria])
        cv2.putText(lado, "Original (gris)", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, 180, 2)
        cv2.putText(lado, f"Binaria (umbral={t})", (gris.shape[1] + 10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, 180, 2)
        cv2.imshow(TITULO, lado)

        tecla = cv2.waitKey(30) & 0xFF
        if tecla in (ord('q'), 27):
            cv2.imwrite(ruta_out("umbral_binario.png"), binaria)
            print(f"Guardado con umbral={t} → output/umbral_binario.png")
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    ruta = pedir_imagen("Seleccionar imagen")
    if ruta:
        run(ruta)
