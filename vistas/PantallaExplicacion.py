import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception: pass

class PantallaExplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Módulo de Explicación")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.salir())
        
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.assets_dir = os.path.join(base_dir, "assets")
        
        self.canvas = tk.Canvas(self.root, width=self.w, height=self.h, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.dibujar_fondo()
        self.cargar_iconos()
        self.crear_interfaz()

    def cargar_iconos(self):
        self.iconos = {}
        ruta_salir = os.path.join(self.assets_dir, "salir.png")
        if os.path.exists(ruta_salir):
            img = Image.open(ruta_salir).resize((30, 30), Image.Resampling.LANCZOS)
            self.iconos["salir"] = ImageTk.PhotoImage(img)
        else:
            self.iconos["salir"] = None

    def dibujar_fondo(self):
        try:
            img_fondo = Image.open(os.path.join(self.assets_dir, "fondo.jpg")).resize((self.w, self.h), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(img_fondo)
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except:
            self.canvas.config(bg="#e2e8f0")
            
        self.canvas.create_text(self.w // 2, self.h * 0.08, text="MÓDULO DE EXPLICACIÓN", font=("Helvetica", 40, "bold"), fill="#1a365d")

    def crear_interfaz(self):
        # Contenedor principal
        frame_principal = tk.Frame(self.canvas, bg="#f8fafc", highlightbackground="#1a365d", highlightthickness=3)
        self.canvas.create_window(self.w//2, self.h//2 + 30, window=frame_principal, width=self.w * 0.85, height=self.h * 0.78)

        lbl_style = {"bg": "#f8fafc", "fg": "#1a365d", "font": ("Segoe UI", 12, "bold")}

        # ================= SECCIÓN SUPERIOR =================
        frame_sup = tk.Frame(frame_principal, bg="#f8fafc")
        frame_sup.pack(fill="x", pady=20, padx=40)

        tk.Label(frame_sup, text="Bitácora de Razonamiento del Motor de Inferencia:", **lbl_style).pack(anchor="w")

        # ================= SECCIÓN CENTRAL (Caja de Texto/Consola) =================
        frame_central = tk.Frame(frame_principal, bg="#f8fafc")
        frame_central.pack(fill="both", expand=True, padx=40, pady=10)

        # Scrollbar para el texto
        scroll = tk.Scrollbar(frame_central)
        scroll.pack(side="right", fill="y")

        # Caja de texto (tipo consola)
        self.txt_explicacion = tk.Text(frame_central, font=("Consolas", 12), bg="#1e293b", fg="#f8fafc", 
                                       yscrollcommand=scroll.set, wrap="word", padx=15, pady=15)
        self.txt_explicacion.pack(side="left", fill="both", expand=True)
        scroll.config(command=self.txt_explicacion.yview)

        # Texto de relleno (Placeholder)
        texto_inicial = (
            "=======================================================================\n"
            "                 SISTEMA EXPERTO DE DIAGNÓSTICO MÉDICO                 \n"
            "=======================================================================\n\n"
            "Estado: Esperando consulta...\n\n"
            "> Aún no se ha realizado ninguna inferencia en esta sesión.\n\n"
            "En este módulo se detallará el paso a paso de las reglas de producción\n"
            "que se activen durante la Búsqueda Hacia Adelante, mostrando los pesos\n"
            "calculados y el porcentaje de probabilidad final de la hipótesis.\n"
        )
        self.txt_explicacion.insert(tk.END, texto_inicial)
        self.txt_explicacion.config(state="disabled") # Bloquear escritura para que sea solo lectura

        # ================= SECCIÓN INFERIOR (Botón Salir) =================
        frame_inf = tk.Frame(frame_principal, bg="#f8fafc")
        frame_inf.pack(fill="x", pady=25, padx=40)

        btn_salir = tk.Button(frame_inf, text=" SALIR", command=self.salir, 
                              font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1a365d", 
                              cursor="hand2", relief="solid", borderwidth=2)
        if self.iconos["salir"]: 
            btn_salir.config(image=self.iconos["salir"], compound="left", padx=5)
            
        btn_salir.pack(side="right", ipadx=15, ipady=8)

    def salir(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PantallaExplicacion(root)
    root.mainloop()