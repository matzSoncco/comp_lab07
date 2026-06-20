"""
Tarea 3 – Negativo y escala de grises
Abre una imagen, invierte sus valores (negativo) y luego la convierte a grises.
"""
import cv2
import numpy as np
from utils import cargar_img, ruta_out, pedir_imagen


def run(ruta):
    original = cargar_img(ruta)

    # Negativo: invertir cada valor de píxel
    negativo = 255 - original
    cv2.imwrite(ruta_out("negativo.png"), negativo)
    print("  → output/negativo.png")

    # Escala de grises del negativo
    gris = cv2.cvtColor(negativo, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(ruta_out("escala_grises.png"), gris)
    print("  → output/escala_grises.png")

    # Mostrar los 3 estados
    gris_bgr = cv2.cvtColor(gris, cv2.COLOR_GRAY2BGR)
    h = max(original.shape[0], negativo.shape[0], gris_bgr.shape[0])
    w = original.shape[1]

    def pad(img):
        return cv2.copyMakeBorder(img, 0, h - img.shape[0], 0, 0,
                                  cv2.BORDER_CONSTANT, value=0)

    comparacion = np.hstack([pad(original), pad(negativo), pad(gris_bgr)])
    for i, lbl in enumerate(["Original", "Negativo", "Escala de grises"]):
        cv2.putText(comparacion, lbl, (i * w + 10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Tarea 3 · Original | Negativo | Grises", comparacion)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    ruta = pedir_imagen("Seleccionar imagen")
    if ruta:
        run(ruta)
