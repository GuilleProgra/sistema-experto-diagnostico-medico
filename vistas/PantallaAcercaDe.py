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

class PantallaAcercaDe:
    def __init__(self, root):
        self.root = root
        self.root.title("Acerca del Sistema - ITZ")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.regresar_atajo)
        
        self.w = self.root.winfo_screenwidth()
        self.h = self.root.winfo_screenheight()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        rutas = {
            "fondo": os.path.join(base_dir, "assets", "fondo.jpg"),
            "logo_medicina": os.path.join(base_dir, "assets", "logo_medicina.png"),
            "autores": os.path.join(base_dir, "assets", "autores.png"),
            "regresar": os.path.join(base_dir, "assets", "regresar.png")
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

        centro_x = self.w // 2

        # 1. Título movido un poco más arriba (12% de la pantalla)
        self.canvas.create_text(centro_x, self.h * 0.12, text="ACERCA DEL SISTEMA", 
                                font=("Helvetica", 55, "bold"), fill="#1a365d")

        # 2. Logo movido hacia arriba (35% de la pantalla) y un poco más pequeño
        try:
            img_med = Image.open(rutas["logo_medicina"])
            aspect_ratio_med = img_med.width / img_med.height
            nuevo_alto_med = 230 
            nuevo_ancho_med = int(nuevo_alto_med * aspect_ratio_med) 
            
            img_med = img_med.resize((nuevo_ancho_med, nuevo_alto_med), Image.Resampling.LANCZOS)
            self.logo_med = ImageTk.PhotoImage(img_med)
            self.canvas.create_image(centro_x, self.h * 0.35, image=self.logo_med, anchor="center")
        except Exception as e:
            print(f"Error cargando logo medicina: {e}")

        # 3. Texto descriptivo subido al 62% y letra reducida a 20
        texto_info = (
            "Versión 1.0\n\n"
            "Este software es para uso exclusivo de la materia de Inteligencia Artificial\n"
            "de la carrera de Ingeniería en Sistemas Computacionales.\n\n"
            "Todo aquel que realice mal uso de la aplicación será sancionado."
        )
        self.canvas.create_text(centro_x, self.h * 0.62, text=texto_info, 
                                font=("Segoe UI", 20), fill="#1a365d", justify="center")

        # Cargar iconos
        self.iconos = {}
        for clave in ["autores", "regresar"]:
            ruta = rutas[clave]
            if os.path.exists(ruta):
                img = Image.open(ruta).resize((40, 40), Image.Resampling.LANCZOS)
                self.iconos[clave] = ImageTk.PhotoImage(img)
            else:
                self.iconos[clave] = None

        # Estilos de botones
        btn_style_secundario = {
            "font": ("Segoe UI", 16, "bold"), "bg": "#ffffff", "fg": "#1a365d",
            "activebackground": "#f1f5f9", "activeforeground": "#1a365d",
            "cursor": "hand2", "relief": "solid", "borderwidth": 2
        }

        btn_style_primario = {
            "font": ("Segoe UI", 16, "bold"), "bg": "#1a365d", "fg": "#ffffff",
            "activebackground": "#2b6cb0", "activeforeground": "#ffffff",
            "cursor": "hand2", "relief": "solid", "borderwidth": 2
        }

        # 4. Botones bajados al 88% de la pantalla para dar mucho más espacio
        kwargs_autores = {"text": " AUTORES", "width": 18}
        if self.iconos["autores"]: 
            kwargs_autores.update({"image": self.iconos["autores"], "compound": "left", "width": 240, "height": 65})
        btn_autores = tk.Button(self.root, command=self.mostrar_autores, **btn_style_secundario, **kwargs_autores)
        self.canvas.create_window(self.w * 0.10, self.h * 0.88, window=btn_autores, anchor="w")

        kwargs_regresar = {"text": " REGRESAR", "width": 18}
        if self.iconos["regresar"]: 
            kwargs_regresar.update({"image": self.iconos["regresar"], "compound": "left", "width": 240, "height": 65})
        btn_regresar = tk.Button(self.root, command=self.regresar, **btn_style_primario, **kwargs_regresar)
        self.canvas.create_window(self.w * 0.90, self.h * 0.88, window=btn_regresar, anchor="e")

    def mostrar_autores(self):

        from PantallaAutores import PantallaAutores
        
        ventana_autores = tk.Toplevel(self.root)
        
        app_autores = PantallaAutores(ventana_autores)

    def regresar(self):
        # Esta línea destruirá la ventana secundaria y volverá a la principal
        self.root.destroy()
        
    def regresar_atajo(self, event):
        self.regresar()

if __name__ == "__main__":
    root = tk.Tk()
    app = PantallaAcercaDe(root)
    root.mainloop()