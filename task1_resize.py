"""
Tarea 1 – Redimensionar imagen
Carga una imagen y la muestra a tres escalas distintas (50 %, 100 %, 150 %)
para ilustrar el efecto de cv2.resize con interpolación bilineal.
"""
import cv2
import numpy as np
from utils import cargar_img, ruta_out, pedir_imagen


def run(ruta):
    original = cargar_img(ruta)
    h, w = original.shape[:2]
    print(f"Tamaño original: {w}×{h}")

    escalas = [0.5, 1.0, 1.5]
    redimensionadas = []
    for escala in escalas:
        nw, nh = int(w * escala), int(h * escala)
        r = cv2.resize(original, (nw, nh), interpolation=cv2.INTER_LINEAR)
        redimensionadas.append(r)
        nombre = f"redimensionada_{int(escala*100)}pct.jpg"
        cv2.imwrite(ruta_out(nombre), r)
        print(f"  {int(escala*100)}% → {nw}×{nh}  →  output/{nombre}")

    # Escalar todas al mismo alto para poder mostrarlas juntas
    alto_max = max(img.shape[0] for img in redimensionadas)
    paneles = []
    for img, esc in zip(redimensionadas, escalas):
        panel = cv2.resize(img, (int(img.shape[1] * alto_max / img.shape[0]), alto_max))
        etiqueta = f"{int(esc*100)}%  ({img.shape[1]}x{img.shape[0]})"
        cv2.putText(panel, etiqueta, (8, 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        paneles.append(panel)

    comparacion = np.hstack(paneles)
    cv2.imshow("Tarea 1 · Redimensionado  50% | 100% | 150%", comparacion)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    ruta = pedir_imagen("Seleccionar imagen")
    if ruta:
        run(ruta)
