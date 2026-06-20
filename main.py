import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from datetime import datetime

from utils import FILTRO

# Importar la función run() de cada tarea
from task1_resize            import run as t1_run
from task2_channels          import run as t2_run
from task3_negative_grayscale import run as t3_run
from task4_channel_viz       import run as t4_run
from task5_shapes_text       import run as t5_run
from task6_threshold         import run as t6_run
from task7_drawing           import run as t7_run


# ── Diálogo: pide una imagen + un deslizador de umbral (solo tarea 6) ─────────

class DialogoUmbral(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Tarea 6 · Umbral inicial")
        self.resizable(False, False)
        self.grab_set()
        self.resultado = None

        ttk.Label(self, text="Imagen:").grid(row=0, column=0, padx=10, pady=8, sticky="e")
        self.var_ruta = tk.StringVar()
        ttk.Entry(self, textvariable=self.var_ruta, width=34).grid(row=0, column=1, padx=4)
        ttk.Button(self, text="…", width=3, command=self._elegir).grid(row=0, column=2, padx=4)

        ttk.Label(self, text="Umbral (0-255):").grid(row=1, column=0, padx=10, pady=6, sticky="e")
        self.var_umbral = tk.IntVar(value=127)
        ttk.Scale(self, from_=0, to=255, variable=self.var_umbral,
                  orient="horizontal", length=180).grid(row=1, column=1, sticky="w")
        ttk.Label(self, textvariable=self.var_umbral, width=4).grid(row=1, column=2)

        ttk.Button(self, text="Abrir", command=self._ok).grid(
            row=2, column=0, columnspan=3, pady=10)

    def _elegir(self):
        r = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=FILTRO)
        if r:
            self.var_ruta.set(r)

    def _ok(self):
        if not self.var_ruta.get():
            messagebox.showwarning("Falta imagen", "Selecciona una imagen primero.", parent=self)
            return
        self.resultado = {"ruta": self.var_ruta.get(), "umbral": int(self.var_umbral.get())}
        self.destroy()


# ── Aplicación principal ───────────────────────────────────────────────────────

class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Lab 07 · Procesamiento de Imágenes")
        self.root.geometry("860x580")
        self.root.resizable(True, True)
        self._construir_ui()
        self._log("Bienvenido. Selecciona una tarea para comenzar.")

    # ── Construcción de la interfaz ────────────────────────────────────────────

    def _construir_ui(self):
        # Encabezado
        cab = tk.Frame(self.root, bg="#1e3a5f", height=50)
        cab.pack(fill="x")
        tk.Label(cab, text="Lab 07 · Procesamiento de Imágenes con OpenCV",
                 bg="#1e3a5f", fg="white",
                 font=("Segoe UI", 13, "bold")).pack(side="left", padx=16, pady=10)

        # Cuerpo
        cuerpo = tk.Frame(self.root)
        cuerpo.pack(fill="both", expand=True, padx=10, pady=8)

        izq = tk.Frame(cuerpo, width=320)
        izq.pack(side="left", fill="y", padx=(0, 8))
        izq.pack_propagate(False)

        der = tk.Frame(cuerpo)
        der.pack(side="left", fill="both", expand=True)

        self._panel_tareas(izq)
        self._panel_log(der)

        # Barra de estado
        self.var_estado = tk.StringVar(value="Listo")
        tk.Label(self.root, textvariable=self.var_estado, anchor="w",
                 relief="sunken", bd=1, font=("Segoe UI", 9),
                 fg="#444").pack(fill="x", side="bottom")

    def _panel_tareas(self, padre):
        marco = ttk.LabelFrame(padre, text="Tareas", padding=(6, 4))
        marco.pack(fill="both", expand=True)
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)

        lienzo = tk.Canvas(marco, highlightthickness=0)
        sb     = ttk.Scrollbar(marco, orient="vertical", command=lienzo.yview)
        lienzo.configure(yscrollcommand=sb.set)
        sb.grid(row=0, column=1, sticky="ns")
        lienzo.grid(row=0, column=0, sticky="nsew")

        interior  = tk.Frame(lienzo)
        win_id    = lienzo.create_window((0, 0), window=interior, anchor="nw")

        interior.bind("<Configure>",
                      lambda _: lienzo.configure(scrollregion=lienzo.bbox("all")))
        lienzo.bind("<Configure>",
                    lambda e: lienzo.itemconfig(win_id, width=e.width))
        lienzo.bind_all("<MouseWheel>",
                        lambda e: lienzo.yview_scroll(int(-1*(e.delta/120)), "units"))

        TAREAS = [
            ("1. Redimensionar imagen",
             "Muestra la imagen al 50 %, 100 % y 150 % de su tamaño original.",
             self._t1),
            ("2. Canales de color",
             "Separa y muestra los canales R, G y B de una imagen.",
             self._t2),
            ("3. Negativo y escala de grises",
             "Invierte los colores y convierte la imagen a grises.",
             self._t3),
            ("4. Visualización interactiva",
             "Activa/desactiva los canales R, G, B con las teclas R/G/B.",
             self._t4),
            ("5. Detección automática de rostros",
             "Detecta caras (persona/gato) y dibuja un círculo + etiqueta.",
             self._t5),
            ("6. Umbral binario",
             "Convierte la imagen a blanco y negro con un deslizador.",
             self._t6),
            ("7. Programa de dibujo",
             "Dibuja formas libres con ratón. Z=deshacer, S=guardar.",
             self._t7),
        ]

        for nombre, desc, cmd in TAREAS:
            cont = tk.Frame(interior, relief="groove", bd=1)
            cont.pack(fill="x", pady=3, ipady=2)
            tk.Label(cont, text=nombre, font=("Segoe UI", 9, "bold"),
                     anchor="w").pack(fill="x", padx=6, pady=(4, 0))
            tk.Label(cont, text=desc, font=("Segoe UI", 8),
                     fg="#555", anchor="w", wraplength=270,
                     justify="left").pack(fill="x", padx=6)
            ttk.Button(cont, text="Ejecutar",
                       command=cmd).pack(anchor="e", padx=6, pady=4)

    def _panel_log(self, padre):
        marco = ttk.LabelFrame(padre, text="Registro de actividad", padding=6)
        marco.pack(fill="both", expand=True)
        self.txt = scrolledtext.ScrolledText(
            marco, wrap="word", font=("Consolas", 9),
            bg="#0d1117", fg="#c9d1d9", relief="flat")
        self.txt.pack(fill="both", expand=True)

    # ── Utilidades ─────────────────────────────────────────────────────────────

    def _log(self, msg):
        ts = datetime.now().strftime("%H:%M:%S")
        self.txt.insert("end", f"[{ts}] {msg}\n")
        self.txt.see("end")

    def _estado(self, msg):
        self.var_estado.set(msg)
        self.root.update_idletasks()

    def _pedir_imagen(self, titulo="Seleccionar imagen"):
        return filedialog.askopenfilename(title=titulo, filetypes=FILTRO)

    def _hilo(self, nombre, fn, *args):
        """Ejecuta fn(*args) en un hilo daemon para no bloquear la UI."""
        def _run():
            self._log(f"── {nombre} ──")
            self._estado(f"Ejecutando: {nombre}…")
            try:
                fn(*args)
                self._log("Listo.")
            except Exception as e:
                self._log(f"ERROR: {e}")
                messagebox.showerror("Error", str(e))
            finally:
                self._estado("Listo")
        threading.Thread(target=_run, daemon=True).start()

    # ── Ejecutores ─────────────────────────────────────────────────────────────

    def _t1(self):
        r = self._pedir_imagen("Tarea 1 · Seleccionar imagen")
        if r:
            self._hilo("Tarea 1: Redimensionar", t1_run, r)

    def _t2(self):
        r = self._pedir_imagen("Tarea 2 · Seleccionar imagen")
        if r:
            self._hilo("Tarea 2: Canales de color", t2_run, r)

    def _t3(self):
        r = self._pedir_imagen("Tarea 3 · Seleccionar imagen")
        if r:
            self._hilo("Tarea 3: Negativo y grises", t3_run, r)

    def _t4(self):
        r = self._pedir_imagen("Tarea 4 · Seleccionar imagen")
        if r:
            self._hilo("Tarea 4: Visualización de canales", t4_run, r)

    def _t5(self):
        r = self._pedir_imagen("Tarea 5 · Seleccionar imagen con persona o animal")
        if r:
            self._hilo("Tarea 5: Detección automática", t5_run, r)

    def _t6(self):
        dlg = DialogoUmbral(self.root)
        self.root.wait_window(dlg)
        if dlg.resultado:
            p = dlg.resultado
            self._hilo("Tarea 6: Umbral binario", t6_run, p["ruta"], p["umbral"])

    def _t7(self):
        self._hilo("Tarea 7: Programa de dibujo", t7_run)


# ── Punto de entrada ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
