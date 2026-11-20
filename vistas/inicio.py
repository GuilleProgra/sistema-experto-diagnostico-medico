import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

class PantallaBienvenida:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto - ITZ")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.salir_atajo)
        
        self.w = self.root.winfo_screenwidth()
        self.h = self.root.winfo_screenheight()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        rutas = {
            "fondo": os.path.join(base_dir, "assets", "fondo.jpg"),
            "logo_medicina": os.path.join(base_dir, "assets", "logo_medicina.png"),
            "logo_zaca": os.path.join(base_dir, "assets", "logo_zaca.png")
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

        # Cargar Logo Medicina (Izquierda)
        try:
            img_med = Image.open(rutas["logo_medicina"])
            aspect_ratio_med = img_med.width / img_med.height
            nuevo_alto_med = 200 
            nuevo_ancho_med = int(nuevo_alto_med * aspect_ratio_med) 
            
            img_med = img_med.resize((nuevo_ancho_med, nuevo_alto_med), Image.Resampling.LANCZOS)
            self.logo_med = ImageTk.PhotoImage(img_med)
            self.canvas.create_image(60, 40, image=self.logo_med, anchor="nw") 
        except Exception as e:
            print(f"Error cargando logo medicina: {e}")

        # Cargar Logo ITZ (Derecha)
        try:
            img_itz = Image.open(rutas["logo_zaca"])
            aspect_ratio_itz = img_itz.width / img_itz.height
            nuevo_alto_itz = 130
            nuevo_ancho_itz = int(nuevo_alto_itz * aspect_ratio_itz)
            
            img_itz = img_itz.resize((nuevo_ancho_itz, nuevo_alto_itz), Image.Resampling.LANCZOS)
            self.logo_itz = ImageTk.PhotoImage(img_itz)
            self.canvas.create_image(self.w - 60, 70, image=self.logo_itz, anchor="ne") 
        except Exception as e:
            print(f"Error cargando logo zaca: {e}")

        # Textos centrales (Más grandes)
        centro_x = self.w // 2
        self.canvas.create_text(centro_x, self.h * 0.20, text="ITZ", font=("Helvetica", 45, "bold"), fill="#1a365d")
        
        titulo = "SISTEMA EXPERTO\nPARA EL DIAGNÓSTICO\nDE ENFERMEDADES"
        self.canvas.create_text(centro_x, self.h * 0.45, text=titulo, font=("Helvetica", 55, "bold"), fill="#1a365d", justify="center")

        # Cargar iconos (Renderizados a 40x40 para mayor claridad)
        rutas_iconos = {
            "salir": os.path.join(base_dir, "assets", "salir.png"),
            "info": os.path.join(base_dir, "assets", "info.png"),
            "entrar": os.path.join(base_dir, "assets", "entrar.png")
        }
        
        self.iconos = {}
        for clave, ruta in rutas_iconos.items():
            if os.path.exists(ruta):
                img = Image.open(ruta).resize((40, 40), Image.Resampling.LANCZOS)
                self.iconos[clave] = ImageTk.PhotoImage(img)
            else:
                self.iconos[clave] = None

        # Estilos de botones (Con contorno sólido tipo "Solid" y borde de 2px, y fuente en 16pt)
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

        # Botones (Tamaño aumentado a 240 de ancho y 65 de alto)
        kwargs_salir = {"text": " SALIR", "width": 18}
        if self.iconos["salir"]: kwargs_salir.update({"image": self.iconos["salir"], "compound": "left", "width": 240, "height": 65})
        btn_salir = tk.Button(self.root, command=self.salir, **btn_style_secundario, **kwargs_salir)
        self.canvas.create_window(self.w * 0.10, self.h * 0.85, window=btn_salir, anchor="w")

        kwargs_info = {"text": " ACERCA DE", "width": 18}
        if self.iconos["info"]: kwargs_info.update({"image": self.iconos["info"], "compound": "left", "width": 240, "height": 65})
        btn_acerca = tk.Button(self.root, command=self.acerca_de, **btn_style_secundario, **kwargs_info)
        self.canvas.create_window(self.w * 0.90, self.h * 0.72, window=btn_acerca, anchor="e")

        kwargs_entrar = {"text": " ENTRAR", "width": 18}
        if self.iconos["entrar"]: kwargs_entrar.update({"image": self.iconos["entrar"], "compound": "left", "width": 240, "height": 65})
        btn_entrar = tk.Button(self.root, command=self.entrar, **btn_style_primario, **kwargs_entrar)
        self.canvas.create_window(self.w * 0.90, self.h * 0.85, window=btn_entrar, anchor="e")

    def salir(self):
        if messagebox.askyesno("Salir", "¿Estás seguro que deseas salir?"):
            self.root.destroy()
            
    def salir_atajo(self, event):
        self.salir()

    def acerca_de(self):
        from PantallaAcercaDe import PantallaAcercaDe
        ventana_secundaria = tk.Toplevel(self.root)
        app_acerca = PantallaAcercaDe(ventana_secundaria)

    def entrar(self):
        # 1. Importamos la pantalla del menú principal
        from PantallaMenuPrincipal import PantallaMenuPrincipal
        
        # 2. Creamos una nueva ventana sobrepuesta (Toplevel)
        ventana_menu = tk.Toplevel(self.root)
        
        # 3. Abrimos la interfaz en esa nueva ventana
        app_menu = PantallaMenuPrincipal(ventana_menu)

if __name__ == "__main__":
    root = tk.Tk()
    app = PantallaBienvenida(root)
    root.mainloop()