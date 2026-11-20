import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# --- TRUCO PARA ALTA RESOLUCIÓN EN WINDOWS ---
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass
# ---------------------------------------------

class PantallaUsuario:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Interfaz Usuario - SE")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.salir_atajo)
        
        self.w = self.root.winfo_screenwidth()
        self.h = self.root.winfo_screenheight()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        rutas = {
            "fondo": os.path.join(base_dir, "assets", "fondo.jpg"),
            "atras": os.path.join(base_dir, "assets", "atras.png"),
            "adelante": os.path.join(base_dir, "assets", "adelante.png"),
            "explicacion": os.path.join(base_dir, "assets", "explicacion.png"),
            "salir": os.path.join(base_dir, "assets", "salir.png")
        }

        self.canvas = tk.Canvas(self.root, width=self.w, height=self.h, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Cargar Fondo
        try:
            img_fondo = Image.open(rutas["fondo"]).resize((self.w, self.h), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(img_fondo)
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error cargando fondo: {e}")

        # Título
        self.canvas.create_text(self.w // 2, self.h * 0.12, text="MENÚ INTERFAZ USUARIO", 
                                font=("Helvetica", 55, "bold"), fill="#1a365d")

        # ==========================================
        # PANEL DERECHO: CUADRO DE DESCRIPCIÓN
        # ==========================================
        x_cuadro = self.w * 0.52
        y_cuadro_inicio = self.h * 0.30
        y_cuadro_fin = self.h * 0.85
        ancho_cuadro = self.w * 0.90
        
        self.canvas.create_rectangle(x_cuadro, y_cuadro_inicio, ancho_cuadro, y_cuadro_fin, 
                                     outline="#1a365d", width=3, fill="#f8fafc")
        
        texto_defecto = "Pasa el ratón sobre una opción de la\nizquierda para ver su descripción aquí."
        
        self.texto_descripcion = self.canvas.create_text(
            (x_cuadro + ancho_cuadro) / 2, (y_cuadro_inicio + y_cuadro_fin) / 2, 
            text=texto_defecto, font=("Segoe UI", 18, "italic"), fill="#475569", justify="center", width=700
        )

        # ==========================================
        # PANEL IZQUIERDO: BOTONES E ICONOS
        # ==========================================
        self.iconos = {}
        for clave in ["atras", "adelante", "explicacion", "salir"]:
            ruta = rutas[clave]
            if os.path.exists(ruta):
                img = Image.open(ruta).resize((40, 40), Image.Resampling.LANCZOS)
                self.iconos[clave] = ImageTk.PhotoImage(img)
            else:
                self.iconos[clave] = None

        btn_style = {
            "font": ("Segoe UI", 16, "bold"), "bg": "#ffffff", "fg": "#1a365d",
            "activebackground": "#f1f5f9", "activeforeground": "#1a365d",
            "cursor": "hand2", "relief": "solid", "borderwidth": 2
        }

        x_botones = self.w * 0.25

        # 1. Botón Búsqueda Hacia Atrás
        self.btn_atras = tk.Button(self.root, text=" BÚSQUEDA HACIA ATRÁS", command=self.abrir_busqueda_atras, **btn_style)
        if self.iconos["atras"]:
            self.btn_atras.config(image=self.iconos["atras"], compound="left")
        self.canvas.create_window(x_botones, self.h * 0.35, window=self.btn_atras, anchor="center", width=520, height=75)

        # 2. Botón Búsqueda Hacia Adelante
        self.btn_adelante = tk.Button(self.root, text=" BÚSQUEDA HACIA ADELANTE", command=self.abrir_busqueda_adelante, **btn_style)
        if self.iconos["adelante"]:
            self.btn_adelante.config(image=self.iconos["adelante"], compound="left")
        self.canvas.create_window(x_botones, self.h * 0.50, window=self.btn_adelante, anchor="center", width=520, height=75)

        # 3. Botón Módulo de Explicación
        self.btn_explicacion = tk.Button(self.root, text=" MÓDULO DE EXPLICACIÓN", command=self.abrir_explicacion, **btn_style)
        if self.iconos["explicacion"]:
            self.btn_explicacion.config(image=self.iconos["explicacion"], compound="left")
        self.canvas.create_window(x_botones, self.h * 0.65, window=self.btn_explicacion, anchor="center", width=520, height=75)

        # 4. Botón Salir (Regresar)
        self.btn_salir = tk.Button(self.root, command=self.salir, text=" SALIR", **btn_style)
        if self.iconos["salir"]:
            self.btn_salir.config(image=self.iconos["salir"], compound="left")
        self.canvas.create_window(x_botones, self.h * 0.80, window=self.btn_salir, anchor="center", width=500, height=75)

        # ==========================================
        # LÓGICA DE HOVER (Descripciones breves)
        # ==========================================
        desc_atras = "BÚSQUEDA HACIA ATRÁS\n\nParte de una hipótesis o enfermedad específica para verificar si el paciente cumple con los síntomas que la confirman."
        desc_adelante = "BÚSQUEDA HACIA ADELANTE\n\nPermite seleccionar los síntomas que presenta el paciente para inferir y calcular qué enfermedad padece."
        desc_explicacion = "MÓDULO DE EXPLICACIÓN\n\nMuestra el razonamiento, las reglas activadas y los porcentajes utilizados por el sistema experto para llegar al diagnóstico."
        desc_salir = "SALIR\n\nCierra el menú de usuario y regresa al Menú Principal del Sistema Experto."

        self.btn_atras.bind("<Enter>", lambda e: self.actualizar_texto(desc_atras, normal=True))
        self.btn_atras.bind("<Leave>", lambda e: self.actualizar_texto(texto_defecto, normal=False))

        self.btn_adelante.bind("<Enter>", lambda e: self.actualizar_texto(desc_adelante, normal=True))
        self.btn_adelante.bind("<Leave>", lambda e: self.actualizar_texto(texto_defecto, normal=False))

        self.btn_explicacion.bind("<Enter>", lambda e: self.actualizar_texto(desc_explicacion, normal=True))
        self.btn_explicacion.bind("<Leave>", lambda e: self.actualizar_texto(texto_defecto, normal=False))

        self.btn_salir.bind("<Enter>", lambda e: self.actualizar_texto(desc_salir, normal=True))
        self.btn_salir.bind("<Leave>", lambda e: self.actualizar_texto(texto_defecto, normal=False))

    def actualizar_texto(self, texto, normal):
        if normal:
            self.canvas.itemconfig(self.texto_descripcion, text=texto, font=("Segoe UI", 16, "bold"), fill="#1a365d")
        else:
            self.canvas.itemconfig(self.texto_descripcion, text=texto, font=("Segoe UI", 18, "italic"), fill="#475569")

    # ==========================================
    # FUNCIONES DE NAVEGACIÓN
    # ==========================================
    def abrir_busqueda_atras(self):
        from PantallaAtras import PantallaAtras
        ventana_atras = tk.Toplevel(self.root)
        app_atras = PantallaAtras(ventana_atras)

    def abrir_busqueda_adelante(self):
        from PantallaAdelante import PantallaAdelante
        ventana_adelante = tk.Toplevel(self.root)
        app_adelante = PantallaAdelante(ventana_adelante)

    def abrir_explicacion(self):
        from PantallaExplicacion import PantallaExplicacion
        ventana_explicacion = tk.Toplevel(self.root)
        app_explicacion = PantallaExplicacion(ventana_explicacion)

    def salir(self):
        self.root.destroy()
        
    def salir_atajo(self, event):
        self.salir()

if __name__ == "__main__":
    root = tk.Tk()
    app = PantallaUsuario(root)
    root.mainloop()