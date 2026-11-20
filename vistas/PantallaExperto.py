import tkinter as tk
from PIL import Image, ImageTk
import os

# --- TRUCO PARA ALTA RESOLUCIÓN EN WINDOWS ---
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass
# ---------------------------------------------

class PantallaExperto:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz Experto")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.salir_atajo)
        
        self.w = self.root.winfo_screenwidth()
        self.h = self.root.winfo_screenheight()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        rutas = {
            "fondo": os.path.join(base_dir, "assets", "fondo.jpg"),
            "agregar": os.path.join(base_dir, "assets", "agregar.png"),
            "editar": os.path.join(base_dir, "assets", "editar.png"),
            "cuadro": os.path.join(base_dir, "assets", "cuadro.png"),
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

        # Título (Estilo restaurado al diseño original)
        self.canvas.create_text(self.w // 2, self.h * 0.12, text="INTERFAZ EXPERTO", 
                                font=("Helvetica", 55, "bold"), fill="#1a365d")

        # ==========================================
        # PANEL DERECHO: CUADRO DE DESCRIPCIÓN
        # ==========================================
        x_cuadro = self.w * 0.52
        y_cuadro_inicio = self.h * 0.30
        y_cuadro_fin = self.h * 0.80
        ancho_cuadro = self.w * 0.90
        
        # Recuadro blanco con borde azul marino (como en el menú principal)
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
        for clave in ["agregar", "editar", "cuadro", "salir"]:
            ruta = rutas[clave]
            if os.path.exists(ruta):
                # Regresamos al tamaño de 40x40 para que encaje perfecto en el botón
                img = Image.open(ruta).resize((40, 40), Image.Resampling.LANCZOS)
                self.iconos[clave] = ImageTk.PhotoImage(img)
            else:
                self.iconos[clave] = None

        # Estilo original con contorno sólido y fondo blanco
        btn_style = {
            "font": ("Segoe UI", 16, "bold"), "bg": "#ffffff", "fg": "#1a365d",
            "activebackground": "#f1f5f9", "activeforeground": "#1a365d",
            "cursor": "hand2", "relief": "solid", "borderwidth": 2
        }

        x_botones = self.w * 0.25

        # 1. Botón Agregar Enfermedades (Ya incluye el command para abrir la nueva pantalla)
        self.btn_agregar = tk.Button(self.root, text=" AGREGAR ENFERMEDADES", command=self.abrir_enfermedades, **btn_style)
        if self.iconos["agregar"]:
            self.btn_agregar.config(image=self.iconos["agregar"], compound="left")
        self.canvas.create_window(x_botones, self.h * 0.35, window=self.btn_agregar, anchor="center", width=500, height=75)

        # 2. Botón Agregar Síntomas
        self.btn_sintomas = tk.Button(self.root, text=" AGREGAR SÍNTOMAS", command=self.abrir_sintomas, **btn_style)
        if self.iconos["editar"]:
            self.btn_sintomas.config(image=self.iconos["editar"], compound="left")
        self.canvas.create_window(x_botones, self.h * 0.50, window=self.btn_sintomas, anchor="center", width=500, height=75)

        # 3. Botón Cuadro Diagnóstico
        self.btn_cuadro = tk.Button(self.root, text=" CUADRO DIAGNÓSTICO", command=self.abrir_cuadro, **btn_style)
        if self.iconos["cuadro"]:
            self.btn_cuadro.config(image=self.iconos["cuadro"], compound="left")
        self.canvas.create_window(x_botones, self.h * 0.65, window=self.btn_cuadro, anchor="center", width=500, height=75)

        # 4. Botón Regresar
        self.btn_salir = tk.Button(self.root, command=self.salir, text=" REGRESAR", **btn_style)
        if self.iconos["salir"]:
            self.btn_salir.config(image=self.iconos["salir"], compound="left")
        self.canvas.create_window(x_botones, self.h * 0.80, window=self.btn_salir, anchor="center", width=500, height=75)

        # ==========================================
        # LÓGICA DE HOVER
        # ==========================================
        desc_enfermedades = "AGREGAR ENFERMEDADES\n\nPermite registrar nuevas enfermedades\nen la base de datos del sistema experto."
        desc_sintomas = "AGREGAR SÍNTOMAS\n\nPermite agregar o modificar los\nsíntomas asociados a los diagnósticos."
        desc_cuadro = "CUADRO DIAGNÓSTICO\n\nMuestra la relación y matriz morfológica\nentre las enfermedades y los síntomas."
        desc_salir = "REGRESAR\n\nCierra el panel de experto y regresa\nal menú principal."

        self.btn_agregar.bind("<Enter>", lambda e: self.actualizar_texto(desc_enfermedades, normal=True))
        self.btn_agregar.bind("<Leave>", lambda e: self.actualizar_texto(texto_defecto, normal=False))

        self.btn_sintomas.bind("<Enter>", lambda e: self.actualizar_texto(desc_sintomas, normal=True))
        self.btn_sintomas.bind("<Leave>", lambda e: self.actualizar_texto(texto_defecto, normal=False))

        self.btn_cuadro.bind("<Enter>", lambda e: self.actualizar_texto(desc_cuadro, normal=True))
        self.btn_cuadro.bind("<Leave>", lambda e: self.actualizar_texto(texto_defecto, normal=False))

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
    def abrir_enfermedades(self):
        # 1. Importamos tu nueva pantalla
        from PantallaEnfermedades import PantallaEnfermedades
        
        # 2. Creamos una ventana secundaria sobrepuesta
        ventana_enf = tk.Toplevel(self.root)
        
        # 3. Abrimos la interfaz en esa nueva ventana
        app_enf = PantallaEnfermedades(ventana_enf)

    def abrir_sintomas(self):
        from PantallaSintomas import PantallaSintomas
        ventana_sintomas = tk.Toplevel(self.root)
        app_sintomas = PantallaSintomas(ventana_sintomas)

    def abrir_cuadro(self):
        from PantallaCuadro import PantallaCuadro
        ventana_cuadro = tk.Toplevel(self.root)
        app_cuadro = PantallaCuadro(ventana_cuadro)

    def salir(self):
        self.root.destroy()
        
    def salir_atajo(self, event):
        self.salir()

    def salir(self):
        self.root.destroy()
        
    def salir_atajo(self, event):
        self.salir()

if __name__ == "__main__":
    root = tk.Tk()
    app = PantallaExperto(root)
    root.mainloop()