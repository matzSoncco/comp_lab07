"""
Tarea 5 – Detección automática de rostros/gatos y etiquetado
Usa clasificadores Haar de OpenCV para detectar caras humanas o de gato.
Si no detecta nada, dibuja un círculo central como respaldo.
"""
import cv2
from utils import cargar_img, ruta_out, pedir_imagen

CARA_HUMANA  = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
CARA_GATO    = cv2.data.haarcascades + "haarcascade_frontalcatface_extended.xml"


def _detectar(img_gris, cascade_path, escala=1.1, vecinos=5, min_px=60):
    cascade = cv2.CascadeClassifier(cascade_path)
    return cascade.detectMultiScale(
        img_gris, scaleFactor=escala, minNeighbors=vecinos,
        minSize=(min_px, min_px))


def run(ruta):
    img   = cargar_img(ruta)
    gris  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    salida = img.copy()

    # 1) intentar rostro humano
    rostros = _detectar(gris, CARA_HUMANA)
    if len(rostros):
        etiqueta = "Persona"
        detecciones = rostros
    else:
        # 2) intentar cara de gato
        gatos = _detectar(gris, CARA_GATO, escala=1.05, vecinos=3, min_px=40)
        if len(gatos):
            etiqueta = "Gato"
            detecciones = gatos
        else:
            # 3) respaldo: círculo central
            print("No se detectó rostro. Dibujando círculo central.")
            h, w = img.shape[:2]
            cx, cy = w // 2, h // 3
            radio  = min(w, h) // 5
            detecciones = [(cx - radio, cy - radio, radio * 2, radio * 2)]
            etiqueta = "Figura"

    for (x, y, w, h) in detecciones:
        cx = x + w // 2
        cy = y + h // 2
        radio = max(w, h) // 2 + 10
        cv2.circle(salida, (cx, cy), radio, (0, 220, 0), 3)
        # sombra negra + texto verde
        cv2.putText(salida, etiqueta, (x, y - 14),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 4)
        cv2.putText(salida, etiqueta, (x, y - 14),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 220, 0), 2)

    print(f"Detectado: {etiqueta}  ({len(detecciones)} zona/s)")
    cv2.imwrite(ruta_out("figura_etiquetada.jpg"), salida)
    print("  → output/figura_etiquetada.jpg")

    cv2.imshow("Tarea 5 · Original", img)
    cv2.imshow("Tarea 5 · Detección automática", salida)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    ruta = pedir_imagen("Seleccionar imagen con persona o animal")
    if ruta:
        run(ruta)
