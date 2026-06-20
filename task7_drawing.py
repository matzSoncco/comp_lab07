"""
Tarea 7 – Programa de dibujo interactivo
Ratón: clic y arrastra para dibujar.
Teclado:
  R = rectángulo  C = círculo  L = línea  F = lápiz libre
  1-6 = color     + / - = grosor     Z = deshacer     S = guardar     ESC = salir
"""
import cv2
import numpy as np
from utils import ruta_out

COLORES = {
    ord('1'): ((0,   0,   0),   "Negro"),
    ord('2'): ((0,   0, 255),   "Rojo"),
    ord('3'): ((0, 200,   0),   "Verde"),
    ord('4'): ((255, 0,   0),   "Azul"),
    ord('5'): ((0, 180, 255),   "Amarillo"),
    ord('6'): ((255, 0, 255),   "Magenta"),
}


def run():
    canvas    = np.full((600, 800, 3), 255, dtype=np.uint8)
    historial = []
    est = {"forma": "rectangulo", "color": (0, 0, 0),
           "grosor": 2, "activo": False, "sx": 0, "sy": 0}

    def _dibujar(img, x, y):
        f, c, g = est["forma"], est["color"], est["grosor"]
        sx, sy  = est["sx"], est["sy"]
        if f == "rectangulo":
            cv2.rectangle(img, (sx, sy), (x, y), c, g)
        elif f == "circulo":
            cv2.circle(img, (sx, sy), int(np.hypot(x - sx, y - sy)), c, g)
        elif f == "linea":
            cv2.line(img, (sx, sy), (x, y), c, g)

    def _barra(img):
        b = np.full((38, img.shape[1], 3), 30, dtype=np.uint8)
        txt = ("[R]rect [C]circ [L]línea [F]lápiz  "
               "[1-6]color  [+/-]grosor  [Z]deshacer  [S]guardar  [ESC]salir  "
               f"| Forma: {est['forma']}  Grosor: {est['grosor']}")
        cv2.putText(b, txt, (6, 25), cv2.FONT_HERSHEY_SIMPLEX,
                    0.38, (200, 200, 200), 1)
        swatch = np.full((22, 22, 3), est["color"], dtype=np.uint8)
        b[8:30, img.shape[1] - 30: img.shape[1] - 8] = swatch
        return np.vstack([img, b])

    def _mouse(event, x, y, *_):
        if event == cv2.EVENT_LBUTTONDOWN:
            historial.append(canvas.copy())
            est["activo"] = True
            est["sx"], est["sy"] = x, y

        elif event == cv2.EVENT_MOUSEMOVE and est["activo"]:
            if est["forma"] == "lapiz":
                cv2.line(canvas, (est["sx"], est["sy"]), (x, y),
                         est["color"], est["grosor"])
                est["sx"], est["sy"] = x, y
            else:
                tmp = canvas.copy()
                _dibujar(tmp, x, y)
                cv2.imshow(TITULO, _barra(tmp))

        elif event == cv2.EVENT_LBUTTONUP and est["activo"]:
            est["activo"] = False
            if est["forma"] != "lapiz":
                _dibujar(canvas, x, y)

    TITULO = "Tarea 7 · Programa de dibujo"
    cv2.namedWindow(TITULO, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(TITULO, _mouse)

    while True:
        cv2.imshow(TITULO, _barra(canvas))
        tecla = cv2.waitKey(20) & 0xFF

        if   tecla == ord('r'): est["forma"] = "rectangulo"
        elif tecla == ord('c'): est["forma"] = "circulo"
        elif tecla == ord('l'): est["forma"] = "linea"
        elif tecla == ord('f'): est["forma"] = "lapiz"
        elif tecla in COLORES:
            est["color"], nombre = COLORES[tecla]
            print(f"Color: {nombre}")
        elif tecla in (ord('+'), ord('=')):
            est["grosor"] = min(est["grosor"] + 1, 30)
        elif tecla == ord('-'):
            est["grosor"] = max(est["grosor"] - 1, 1)
        elif tecla == ord('z'):
            if historial:
                canvas[:] = historial.pop()
                print("Deshacer")
        elif tecla == ord('s'):
            cv2.imwrite(ruta_out("dibujo.png"), canvas)
            print("Guardado → output/dibujo.png")
        elif tecla == 27:
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
