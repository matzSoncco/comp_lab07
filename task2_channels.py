"""
Tarea 2 – Separación y combinación de canales de color
Carga una imagen y muestra sus canales R, G y B por separado en falso color,
luego guarda la imagen con los canales recombinados en un orden distinto (BGR→RGB)
para crear un efecto visual diferente.
"""
import cv2
import numpy as np
from utils import cargar_img, ruta_out, pedir_imagen


def run(ruta):
    img = cargar_img(ruta)
    b, g, r = cv2.split(img)
    zeros   = np.zeros_like(b)

    # Cada canal en falso color (solo ese canal activo)
    solo_r = cv2.merge([zeros, zeros, r])
    solo_g = cv2.merge([zeros, g,     zeros])
    solo_b = cv2.merge([b,     zeros, zeros])

    # Nueva imagen recombinando canales en orden invertido (R→B, G→G, B→R)
    combinada = cv2.merge([r, g, b])   # intercambia R↔B

    cv2.imwrite(ruta_out("canal_rojo.jpg"),     solo_r)
    cv2.imwrite(ruta_out("canal_verde.jpg"),    solo_g)
    cv2.imwrite(ruta_out("canal_azul.jpg"),     solo_b)
    cv2.imwrite(ruta_out("canales_combinados.jpg"), combinada)
    print("  → output/canal_rojo.jpg")
    print("  → output/canal_verde.jpg")
    print("  → output/canal_azul.jpg")
    print("  → output/canales_combinados.jpg  (R↔B intercambiados)")

    h, w = img.shape[:2]
    etiquetas = ["Original", "Canal R", "Canal G", "Canal B", "Recombinada (R↔B)"]
    imagenes  = [img, solo_r, solo_g, solo_b, combinada]

    # Redimensionar todas al mismo alto antes de juntar
    alto = 300
    paneles = []
    for im, lbl in zip(imagenes, etiquetas):
        escala = alto / im.shape[0]
        panel  = cv2.resize(im, (int(im.shape[1] * escala), alto))
        cv2.putText(panel, lbl, (6, 22),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
        paneles.append(panel)

    fila = np.hstack(paneles)
    cv2.imshow("Tarea 2 · Canales de color", fila)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return combinada


if __name__ == "__main__":
    ruta = pedir_imagen("Seleccionar imagen")
    if ruta:
        run(ruta)
