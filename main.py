import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import cv2
import numpy as np
import os
import threading
from datetime import datetime

IMG_DIR = "images"
OUT_DIR = "output"
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)


# ── Helpers ────────────────────────────────────────────────────────────────────

def ruta_salida(nombre):
    return os.path.join(OUT_DIR, nombre)


def cargar_imagen(ruta, flags=cv2.IMREAD_COLOR):
    img = cv2.imread(ruta, flags)
    if img is None:
        raise FileNotFoundError(f"No se pudo abrir: {ruta}")
    return img


# ── Lógica de cada tarea ───────────────────────────────────────────────────────

def tarea1_redimensionar(rutas, log):
    imgs = [cargar_imagen(r) for r in rutas]
    dims = [img.shape[:2] for img in imgs]
    max_h = max(h for h, _ in dims)
    max_w = max(w for _, w in dims)
    log(f"Tamaños originales: {[f'{w}×{h}' for h,w in dims]}")
    log(f"Tamaño objetivo (el mayor): {max_w}×{max_h}")
    salidas = []
    for i, img in enumerate(imgs):
        r = cv2.resize(img, (max_w, max_h), interpolation=cv2.INTER_LINEAR)
        nombre = f"redimensionada{i+1}.jpg"
        cv2.imwrite(ruta_salida(nombre), r)
        salidas.append(r)
        log(f"  → output/{nombre}")
    fila = np.hstack(salidas)
    cv2.imshow("Tarea 1 · Imágenes redimensionadas", fila)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return salidas


def tarea2_combinar_canales(log):
    r1 = ruta_salida("redimensionada1.jpg")
    r2 = ruta_salida("redimensionada2.jpg")
    r3 = ruta_salida("redimensionada3.jpg")
    for r in (r1, r2, r3):
        if not os.path.exists(r):
            raise FileNotFoundError("Primero ejecuta la Tarea 1.")
    i1, i2, i3 = cargar_imagen(r1), cargar_imagen(r2), cargar_imagen(r3)
    _, _, rch = cv2.split(i1)
    _, gch, _ = cv2.split(i2)
    bch, _, _ = cv2.split(i3)
    combinada = cv2.merge([bch, gch, rch])
    cv2.imwrite(ruta_salida("canales_combinados.jpg"), combinada)
    log("Canal R → imagen 1 | Canal G → imagen 2 | Canal B → imagen 3")
    log("  → output/canales_combinados.jpg")
    cv2.imshow("Tarea 2 · Canales combinados", combinada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def tarea3_negativo_grises(log):
    src = ruta_salida("canales_combinados.jpg")
    if not os.path.exists(src):
        raise FileNotFoundError("Primero ejecuta la Tarea 2.")
    combinada = cargar_imagen(src)
    negativo = 255 - combinada
    cv2.imwrite(ruta_salida("negativo.png"), negativo)
    log("  → output/negativo.png")
    gris = cv2.imread(ruta_salida("negativo.png"), cv2.IMREAD_GRAYSCALE)
    cv2.imwrite(ruta_salida("escala_grises.png"), gris)
    log("  → output/escala_grises.png")
    cv2.imshow("Tarea 3 · Original", combinada)
    cv2.imshow("Tarea 3 · Negativo", negativo)
    cv2.imshow("Tarea 3 · Escala de grises", gris)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def tarea4_visualizacion_canales(log):
    src = ruta_salida("canales_combinados.jpg")
    if not os.path.exists(src):
        raise FileNotFoundError("Primero ejecuta la Tarea 2.")
    img = cargar_imagen(src)
    bch, gch, rch = cv2.split(img)
    estado = [True, True, True]  # R G B
    TITULO = "Tarea 4  |  R=rojo  G=verde  B=azul  Q=salir"
    cv2.namedWindow(TITULO, cv2.WINDOW_NORMAL)
    log("Ventana abierta. Presiona R/G/B para alternar canales, Q para salir.")
    while True:
        zeros = np.zeros_like(rch)
        frame = cv2.merge([
            bch if estado[2] else zeros,
            gch if estado[1] else zeros,
            rch if estado[0] else zeros,
        ])
        barra = np.full((30, frame.shape[1], 3), 30, dtype=np.uint8)
        etiqueta = (f"[R] {'ON ' if estado[0] else 'OFF'}   "
                    f"[G] {'ON ' if estado[1] else 'OFF'}   "
                    f"[B] {'ON ' if estado[2] else 'OFF'}")
        cv2.putText(barra, etiqueta, (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (220, 220, 220), 1)
        cv2.imshow(TITULO, np.vstack([frame, barra]))
        tecla = cv2.waitKey(30) & 0xFF
        if tecla == ord('r'):
            estado[0] = not estado[0]
        elif tecla == ord('g'):
            estado[1] = not estado[1]
        elif tecla == ord('b'):
            estado[2] = not estado[2]
        elif tecla in (ord('q'), 27):
            break
    cv2.destroyAllWindows()


def tarea5_formas_texto(ruta, cx, cy, radio, etiqueta, log):
    img = cargar_imagen(ruta)
    out = img.copy()
    cv2.circle(out, (cx, cy), radio, (0, 220, 0), 3)
    tx, ty = cx - 40, cy - radio - 12
    cv2.putText(out, etiqueta, (tx, ty),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4)
    cv2.putText(out, etiqueta, (tx, ty),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 220, 0), 2)
    cv2.imwrite(ruta_salida("figura_etiquetada.jpg"), out)
    log("  → output/figura_etiquetada.jpg")
    cv2.imshow("Tarea 5 · Original", img)
    cv2.imshow("Tarea 5 · Con círculo y texto", out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def tarea6_umbral(ruta, valor_umbral, log):
    img = cargar_imagen(ruta, cv2.IMREAD_GRAYSCALE)

    def nada(_):
        pass

    cv2.namedWindow("Tarea 6 · Umbral binario")
    cv2.createTrackbar("Umbral", "Tarea 6 · Umbral binario", valor_umbral, 255, nada)
    log(f"Umbral inicial: {valor_umbral}. Ajusta con el deslizador. Q para guardar y salir.")
    while True:
        t = cv2.getTrackbarPos("Umbral", "Tarea 6 · Umbral binario")
        _, binaria = cv2.threshold(img, t, 255, cv2.THRESH_BINARY)
        lado = np.hstack([img, binaria])
        cv2.imshow("Tarea 6 · Umbral binario", lado)
        tecla = cv2.waitKey(30) & 0xFF
        if tecla in (ord('q'), 27):
            cv2.imwrite(ruta_salida("umbral_binario.png"), binaria)
            log(f"Guardado con umbral={t} → output/umbral_binario.png")
            break
    cv2.destroyAllWindows()


def tarea7_dibujo_interactivo(log):
    canvas = np.full((600, 800, 3), 255, dtype=np.uint8)
    historial = []
    estado = {"forma": "rectangulo", "color": (0, 0, 0),
               "grosor": 2, "dibujando": False, "sx": 0, "sy": 0}
    COLORES = {
        ord('1'): ((0,   0,   0),   "Negro"),
        ord('2'): ((0,   0, 255),   "Rojo"),
        ord('3'): ((0, 200,   0),   "Verde"),
        ord('4'): ((255, 0,   0),   "Azul"),
        ord('5'): ((0, 180, 255),   "Amarillo"),
        ord('6'): ((255, 0, 255),   "Magenta"),
    }

    def dibujar(img, sx, sy, x, y):
        f = estado["forma"]
        c = estado["color"]
        g = estado["grosor"]
        if f == "rectangulo":
            cv2.rectangle(img, (sx, sy), (x, y), c, g)
        elif f == "circulo":
            r = int(np.hypot(x - sx, y - sy))
            cv2.circle(img, (sx, sy), r, c, g)
        elif f == "linea":
            cv2.line(img, (sx, sy), (x, y), c, g)

    def mouse(event, x, y, flags, _):
        if event == cv2.EVENT_LBUTTONDOWN:
            historial.append(canvas.copy())
            estado["dibujando"] = True
            estado["sx"], estado["sy"] = x, y
        elif event == cv2.EVENT_MOUSEMOVE and estado["dibujando"]:
            if estado["forma"] == "lapiz":
                cv2.line(canvas, (estado["sx"], estado["sy"]),
                         (x, y), estado["color"], estado["grosor"])
                estado["sx"], estado["sy"] = x, y
            else:
                tmp = canvas.copy()
                dibujar(tmp, estado["sx"], estado["sy"], x, y)
                barra = _barra_estado(tmp)
                cv2.imshow(TITULO, barra)
        elif event == cv2.EVENT_LBUTTONUP and estado["dibujando"]:
            estado["dibujando"] = False
            if estado["forma"] != "lapiz":
                dibujar(canvas, estado["sx"], estado["sy"], x, y)

    def _barra_estado(img):
        b = np.full((36, img.shape[1], 3), 35, dtype=np.uint8)
        txt = ("[R]rect [C]circ [L]linea [F]lapiz | "
               "[1-6]color | [+/-]grosor | [Z]deshacer | [S]guardar | [ESC]salir  "
               f"Forma:{estado['forma']}  Grosor:{estado['grosor']}")
        cv2.putText(b, txt, (6, 23), cv2.FONT_HERSHEY_SIMPLEX, 0.38,
                    (200, 200, 200), 1)
        swatch = np.full((20, 20, 3), estado["color"], dtype=np.uint8)
        b[8:28, img.shape[1]-28:img.shape[1]-8] = swatch
        return np.vstack([img, b])

    TITULO = "Tarea 7 · Programa de dibujo"
    cv2.namedWindow(TITULO, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(TITULO, mouse)
    log("Ventana de dibujo abierta. R/C/L/F forma | 1-6 color | +/- grosor | Z deshacer | S guardar | ESC salir")

    while True:
        cv2.imshow(TITULO, _barra_estado(canvas))
        tecla = cv2.waitKey(20) & 0xFF
        if tecla == ord('r'):
            estado["forma"] = "rectangulo"
        elif tecla == ord('c'):
            estado["forma"] = "circulo"
        elif tecla == ord('l'):
            estado["forma"] = "linea"
        elif tecla == ord('f'):
            estado["forma"] = "lapiz"
        elif tecla in COLORES:
            estado["color"], nombre = COLORES[tecla]
            log(f"Color: {nombre}")
        elif tecla in (ord('+'), ord('=')):
            estado["grosor"] = min(estado["grosor"] + 1, 30)
        elif tecla == ord('-'):
            estado["grosor"] = max(estado["grosor"] - 1, 1)
        elif tecla == ord('z'):
            if historial:
                canvas[:] = historial.pop()
                log("Deshacer")
        elif tecla == ord('s'):
            cv2.imwrite(ruta_salida("dibujo.png"), canvas)
            log("Guardado → output/dibujo.png")
        elif tecla == 27:
            break
    cv2.destroyAllWindows()


# ── Diálogos auxiliares ────────────────────────────────────────────────────────

class DialogoTarea5(tk.Toplevel):
    """Pide la imagen y los parámetros del círculo para la Tarea 5."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Tarea 5 · Parámetros")
        self.resizable(False, False)
        self.grab_set()
        self.resultado = None

        ttk.Label(self, text="Imagen:").grid(row=0, column=0, padx=10, pady=6, sticky="e")
        self.var_ruta = tk.StringVar()
        ttk.Entry(self, textvariable=self.var_ruta, width=34).grid(row=0, column=1, padx=4)
        ttk.Button(self, text="…", width=3,
                   command=self._elegir).grid(row=0, column=2, padx=4)

        campos = [("Centro X:", "cx", "200"), ("Centro Y:", "cy", "150"),
                  ("Radio:", "radio", "95"), ("Etiqueta:", "etiq", "Persona")]
        self.vars = {}
        for i, (lbl, key, val) in enumerate(campos, start=1):
            ttk.Label(self, text=lbl).grid(row=i, column=0, padx=10, pady=4, sticky="e")
            v = tk.StringVar(value=val)
            ttk.Entry(self, textvariable=v, width=14).grid(row=i, column=1, sticky="w", padx=4)
            self.vars[key] = v

        ttk.Button(self, text="Ejecutar", command=self._ok).grid(
            row=5, column=0, columnspan=3, pady=10)

    def _elegir(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp"), ("Todo", "*.*")])
        if ruta:
            self.var_ruta.set(ruta)

    def _ok(self):
        try:
            self.resultado = {
                "ruta": self.var_ruta.get(),
                "cx": int(self.vars["cx"].get()),
                "cy": int(self.vars["cy"].get()),
                "radio": int(self.vars["radio"].get()),
                "etiq": self.vars["etiq"].get(),
            }
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Los valores numéricos son inválidos.", parent=self)


class DialogoTarea6(tk.Toplevel):
    """Pide la imagen y el umbral inicial para la Tarea 6."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Tarea 6 · Parámetros")
        self.resizable(False, False)
        self.grab_set()
        self.resultado = None

        ttk.Label(self, text="Imagen:").grid(row=0, column=0, padx=10, pady=6, sticky="e")
        self.var_ruta = tk.StringVar()
        ttk.Entry(self, textvariable=self.var_ruta, width=34).grid(row=0, column=1, padx=4)
        ttk.Button(self, text="…", width=3,
                   command=self._elegir).grid(row=0, column=2, padx=4)

        ttk.Label(self, text="Umbral inicial (0-255):").grid(
            row=1, column=0, padx=10, pady=4, sticky="e")
        self.var_umbral = tk.IntVar(value=127)
        ttk.Scale(self, from_=0, to=255, variable=self.var_umbral,
                  orient="horizontal", length=200).grid(row=1, column=1, sticky="w")
        ttk.Label(self, textvariable=self.var_umbral).grid(row=1, column=2)

        ttk.Button(self, text="Ejecutar", command=self._ok).grid(
            row=2, column=0, columnspan=3, pady=10)

    def _elegir(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp"), ("Todo", "*.*")])
        if ruta:
            self.var_ruta.set(ruta)

    def _ok(self):
        self.resultado = {"ruta": self.var_ruta.get(),
                          "umbral": int(self.var_umbral.get())}
        self.destroy()


# ── Aplicación principal ───────────────────────────────────────────────────────

class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Lab 07 · Procesamiento de Imágenes")
        self.root.geometry("920x640")
        self.root.resizable(True, True)

        self.rutas = [tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self._construir_ui()
        self._log("Bienvenido. Carga las tres imágenes y selecciona una tarea.")

    # ── UI ─────────────────────────────────────────────────────────────────────

    def _construir_ui(self):
        # ── Encabezado ──────────────────────────────────────────────────────────
        cabecera = tk.Frame(self.root, bg="#1e3a5f", height=54)
        cabecera.pack(fill="x")
        tk.Label(cabecera, text="Lab 07 · Procesamiento de Imágenes con OpenCV",
                 bg="#1e3a5f", fg="white",
                 font=("Segoe UI", 14, "bold")).pack(side="left", padx=18, pady=10)

        # ── Cuerpo principal ─────────────────────────────────────────────────
        cuerpo = tk.Frame(self.root)
        cuerpo.pack(fill="both", expand=True, padx=12, pady=8)

        # Panel izquierdo
        izq = tk.Frame(cuerpo, width=340)
        izq.pack(side="left", fill="y", padx=(0, 8))
        izq.pack_propagate(False)

        # Panel derecho (log)
        der = tk.Frame(cuerpo)
        der.pack(side="left", fill="both", expand=True)

        self._panel_imagenes(izq)
        self._panel_tareas(izq)
        self._panel_log(der)

        # ── Barra de estado ──────────────────────────────────────────────────
        self.var_estado = tk.StringVar(value="Listo")
        barra = tk.Label(self.root, textvariable=self.var_estado,
                         anchor="w", relief="sunken", bd=1,
                         font=("Segoe UI", 9), fg="#444")
        barra.pack(fill="x", side="bottom")

    def _panel_imagenes(self, padre):
        marco = ttk.LabelFrame(padre, text="Imágenes de entrada", padding=6)
        marco.pack(fill="x", pady=(0, 8))

        etiquetas = ["Imagen 1", "Imagen 2", "Imagen 3"]
        for i, etq in enumerate(etiquetas):
            fila = tk.Frame(marco)
            fila.pack(fill="x", pady=2)
            tk.Label(fila, text=etq, width=9, anchor="w",
                     font=("Segoe UI", 9)).pack(side="left")
            ttk.Entry(fila, textvariable=self.rutas[i],
                      width=22, font=("Segoe UI", 8)).pack(side="left", padx=4)
            ttk.Button(fila, text="…", width=3,
                       command=lambda idx=i: self._cargar_imagen(idx)
                       ).pack(side="left")

    def _panel_tareas(self, padre):
        marco = ttk.LabelFrame(padre, text="Tareas", padding=6)
        marco.pack(fill="both", expand=True)

        tareas = [
            ("1. Redimensionar imágenes",
             "Ajusta las 3 imágenes al tamaño de la más grande.",
             self._ejecutar_t1),
            ("2. Combinar canales de color",
             "R de img1 · G de img2 · B de img3.",
             self._ejecutar_t2),
            ("3. Negativo y escala de grises",
             "Invierte los colores y convierte a grises.",
             self._ejecutar_t3),
            ("4. Visualización de canales",
             "Activa/desactiva R, G, B con el teclado.",
             self._ejecutar_t4),
            ("5. Dibujar formas y texto",
             "Dibuja un círculo alrededor de la cara.",
             self._ejecutar_t5),
            ("6. Umbral binario",
             "Convierte la imagen a blanco y negro.",
             self._ejecutar_t6),
            ("7. Programa de dibujo",
             "Dibuja formas con ratón y teclado.",
             self._ejecutar_t7),
        ]

        for nombre, desc, cmd in tareas:
            contenedor = tk.Frame(marco, relief="groove", bd=1)
            contenedor.pack(fill="x", pady=3, ipady=2)
            tk.Label(contenedor, text=nombre, font=("Segoe UI", 9, "bold"),
                     anchor="w").pack(fill="x", padx=6, pady=(4, 0))
            tk.Label(contenedor, text=desc, font=("Segoe UI", 8),
                     fg="#555", anchor="w").pack(fill="x", padx=6)
            ttk.Button(contenedor, text="Ejecutar",
                       command=cmd).pack(anchor="e", padx=6, pady=4)

    def _panel_log(self, padre):
        marco = ttk.LabelFrame(padre, text="Registro de actividad", padding=6)
        marco.pack(fill="both", expand=True)
        self.txt_log = scrolledtext.ScrolledText(
            marco, wrap="word", font=("Consolas", 9),
            bg="#0d1117", fg="#c9d1d9", insertbackground="white",
            state="normal", relief="flat")
        self.txt_log.pack(fill="both", expand=True)

    # ── Utilidades UI ──────────────────────────────────────────────────────────

    def _cargar_imagen(self, idx):
        ruta = filedialog.askopenfilename(
            title=f"Seleccionar imagen {idx + 1}",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp"), ("Todo", "*.*")])
        if ruta:
            self.rutas[idx].set(ruta)
            self._log(f"Imagen {idx + 1} cargada: {os.path.basename(ruta)}")

    def _log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        self.txt_log.insert("end", f"[{ts}] {msg}\n")
        self.txt_log.see("end")

    def _estado(self, msg):
        self.var_estado.set(msg)
        self.root.update_idletasks()

    def _tres_rutas(self):
        rutas = [v.get() for v in self.rutas]
        vacias = [i + 1 for i, r in enumerate(rutas) if not r]
        if vacias:
            messagebox.showwarning(
                "Faltan imágenes",
                f"Carga las imágenes {vacias} antes de continuar.")
            return None
        return rutas

    def _en_hilo(self, fn, *args):
        """Ejecuta fn en un hilo para no bloquear tkinter."""
        def _run():
            try:
                self._estado("Ejecutando…")
                fn(*args)
                self._estado("Listo")
            except Exception as e:
                self._log(f"ERROR: {e}")
                self._estado("Error")
                messagebox.showerror("Error", str(e))
        threading.Thread(target=_run, daemon=True).start()

    # ── Ejecutores de tareas ───────────────────────────────────────────────────

    def _ejecutar_t1(self):
        rutas = self._tres_rutas()
        if rutas:
            self._log("── Tarea 1: Redimensionar imágenes ──")
            self._en_hilo(tarea1_redimensionar, rutas, self._log)

    def _ejecutar_t2(self):
        self._log("── Tarea 2: Combinar canales de color ──")
        self._en_hilo(tarea2_combinar_canales, self._log)

    def _ejecutar_t3(self):
        self._log("── Tarea 3: Negativo y escala de grises ──")
        self._en_hilo(tarea3_negativo_grises, self._log)

    def _ejecutar_t4(self):
        self._log("── Tarea 4: Visualización interactiva de canales ──")
        self._en_hilo(tarea4_visualizacion_canales, self._log)

    def _ejecutar_t5(self):
        dlg = DialogoTarea5(self.root)
        self.root.wait_window(dlg)
        if dlg.resultado:
            p = dlg.resultado
            self._log("── Tarea 5: Dibujar formas y texto ──")
            self._en_hilo(tarea5_formas_texto,
                          p["ruta"], p["cx"], p["cy"], p["radio"], p["etiq"],
                          self._log)

    def _ejecutar_t6(self):
        dlg = DialogoTarea6(self.root)
        self.root.wait_window(dlg)
        if dlg.resultado:
            p = dlg.resultado
            self._log("── Tarea 6: Umbral binario ──")
            self._en_hilo(tarea6_umbral, p["ruta"], p["umbral"], self._log)

    def _ejecutar_t7(self):
        self._log("── Tarea 7: Programa de dibujo interactivo ──")
        self._en_hilo(tarea7_dibujo_interactivo, self._log)


# ── Punto de entrada ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
