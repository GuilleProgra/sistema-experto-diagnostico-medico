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

class PantallaAutores:
    def __init__(self, root):
        self.root = root
        self.root.title("Autores del Sistema - ITZ")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.regresar_atajo)
        
        self.w = self.root.winfo_screenwidth()
        self.h = self.root.winfo_screenheight()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        rutas = {
            "fondo": os.path.join(base_dir, "assets", "fondo.jpg"),
            "selfie": os.path.join(base_dir, "assets", "selfie.jpeg"),
            "mascota": os.path.join(base_dir, "assets", "mascota.jpeg"),
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
        x_imagenes = self.w * 0.22 # Posición X para las fotos
        x_textos = self.w * 0.35   # Posición X para los textos
        
        # Altura dinámica para las fotos (28% de la pantalla para que queden largas pero no choquen)
        alto_fotos = int(self.h * 0.28) 

        # 1. Título
        self.canvas.create_text(centro_x, self.h * 0.12, text="AUTORES DEL SISTEMA", 
                                font=("Helvetica", 55, "bold"), fill="#1a365d")

        # 2. Foto Tuya (Selfie) con Proporción Corregida
        y_selfie = self.h * 0.35
        try:
            img_selfie = Image.open(rutas["selfie"])
            # Calcular ancho para NO deformar
            aspect_ratio_selfie = img_selfie.width / img_selfie.height
            ancho_selfie = int(alto_fotos * aspect_ratio_selfie)
            
            img_selfie = img_selfie.resize((ancho_selfie, alto_fotos), Image.Resampling.LANCZOS)
            self.foto_selfie = ImageTk.PhotoImage(img_selfie)
            
            # Dibujar un marco estético ajustado al nuevo ancho
            margen = 3
            self.canvas.create_rectangle(x_imagenes - (ancho_selfie/2) - margen, y_selfie - (alto_fotos/2) - margen, 
                                         x_imagenes + (ancho_selfie/2) + margen, y_selfie + (alto_fotos/2) + margen, 
                                         outline="#1a365d", width=3, fill="#ffffff")
            self.canvas.create_image(x_imagenes, y_selfie, image=self.foto_selfie, anchor="center")
        except Exception as e:
            print(f"Error cargando selfie: {e}")

        # 3. Datos Tuyos
        datos_autor = (
            "Nombre: Joshua Yael Guillermo Ocampo\n"
            "Dirección: Galeana, Morelos\n"
            "Teléfono: 734 142 5386\n"
            "E-mail: joshua.ocampo.yg16@gmail.com"
        )
        self.canvas.create_text(x_textos, y_selfie, text=datos_autor, 
                                font=("Segoe UI", 20), fill="#1a365d", justify="left", anchor="w")

        # 4. Foto de tu Mascota (Max) con Proporción Corregida
        y_mascota = self.h * 0.67
        try:
            img_mascota = Image.open(rutas["mascota"])
            # Calcular ancho para NO deformar
            aspect_ratio_mascota = img_mascota.width / img_mascota.height
            ancho_mascota = int(alto_fotos * aspect_ratio_mascota)
            
            img_mascota = img_mascota.resize((ancho_mascota, alto_fotos), Image.Resampling.LANCZOS)
            self.foto_mascota = ImageTk.PhotoImage(img_mascota)
            
            # Dibujar un marco estético ajustado
            self.canvas.create_rectangle(x_imagenes - (ancho_mascota/2) - margen, y_mascota - (alto_fotos/2) - margen, 
                                         x_imagenes + (ancho_mascota/2) + margen, y_mascota + (alto_fotos/2) + margen, 
                                         outline="#1a365d", width=3, fill="#ffffff")
            self.canvas.create_image(x_imagenes, y_mascota, image=self.foto_mascota, anchor="center")
        except Exception as e:
            print(f"Error cargando mascota: {e}")

        # 5. Datos de la Mascota
        datos_mascota = (
            "Mascota: Taco\n"
            "Raza: Cruza de Chihuahua\n"
            "Edad: 4 años \n"
            "Rol: Soporte Emocional del Proyecto"
        )
        self.canvas.create_text(x_textos, y_mascota, text=datos_mascota, 
                                font=("Segoe UI", 20), fill="#1a365d", justify="left", anchor="w")

        # Cargar icono de regresar
        self.icono_regresar = None
        if os.path.exists(rutas["regresar"]):
            img_reg = Image.open(rutas["regresar"]).resize((40, 40), Image.Resampling.LANCZOS)
            self.icono_regresar = ImageTk.PhotoImage(img_reg)

        # Estilo del botón
        btn_style_primario = {
            "font": ("Segoe UI", 16, "bold"), "bg": "#1a365d", "fg": "#ffffff",
            "activebackground": "#2b6cb0", "activeforeground": "#ffffff",
            "cursor": "hand2", "relief": "solid", "borderwidth": 2
        }

        # 6. Botón Regresar
        kwargs_regresar = {"text": " REGRESAR", "width": 18}
        if self.icono_regresar: 
            kwargs_regresar.update({"image": self.icono_regresar, "compound": "left", "width": 240, "height": 65})
        
        btn_regresar = tk.Button(self.root, command=self.regresar, **btn_style_primario, **kwargs_regresar)
        self.canvas.create_window(self.w * 0.90, self.h * 0.88, window=btn_regresar, anchor="e")


    def regresar(self):
        self.root.destroy()
        
    def regresar_atajo(self, event):
        self.regresar()

if __name__ == "__main__":
    root = tk.Tk()
    app = PantallaAutores(root)
    root.mainloop()