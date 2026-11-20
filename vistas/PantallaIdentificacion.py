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
except Exception:
    pass

class PantallaIdentificacion:
    def __init__(self, root, resultados, callback_continuar, callback_salir_menu):
        self.root = root
        self.resultados = resultados
        self.callback_continuar = callback_continuar
        self.callback_salir_menu = callback_salir_menu
        
        self.root.title("Identificación del Sistema Experto")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.salir_al_menu())
        
        self.w = self.root.winfo_screenwidth()
        self.h = self.root.winfo_screenheight()
        self.assets_dir = os.path.join(base_dir, "assets")
        
        self.canvas = tk.Canvas(self.root, width=self.w, height=self.h, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.cargar_iconos()
        self.dibujar_fondo()
        self.crear_interfaz()

    def cargar_iconos(self):
        self.iconos = {}
        archivos = {
            "si": "si.png",
            "no": "no.png",
            "regresar": "regresar_azul.png",
            "salir": "salir.png"
        }
        for clave, nombre in archivos.items():
            ruta = os.path.join(self.assets_dir, nombre)
            if os.path.exists(ruta):
                img = Image.open(ruta).resize((28, 28), Image.Resampling.LANCZOS)
                self.iconos[clave] = ImageTk.PhotoImage(img)
            else:
                self.iconos[clave] = None

    def dibujar_fondo(self):
        # Usa fondo2.jpg si existe para distinguir la pantalla, o fondo.jpg por defecto
        ruta_f2 = os.path.join(self.assets_dir, "fondo2.jpg")
        ruta_f1 = os.path.join(self.assets_dir, "fondo.jpg")
        ruta_usar = ruta_f2 if os.path.exists(ruta_f2) else ruta_f1
        
        try:
            img_fondo = Image.open(ruta_usar).resize((self.w, self.h), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(img_fondo)
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception:
            self.canvas.config(bg="#e2e8f0")
            
        self.canvas.create_text(
            self.w // 2, self.h * 0.08, 
            text="RESULTADO DE LA INFERENCIA DIRECTA", 
            font=("Helvetica", 38, "bold"), fill="#1a365d"
        )

    def crear_interfaz(self):
        # Cuadro central estilizado (equivalente a la ventana central de la Fig. 2)
        frame_central = tk.Frame(
            self.canvas, bg="#f8fafc", 
            highlightbackground="#1a365d", highlightthickness=3
        )
        self.canvas.create_window(
            self.w // 2, self.h * 0.48, 
            window=frame_central, width=self.w * 0.65, height=self.h * 0.66
        )

        # Barra superior decorativa del cuadro central
        barra_titulo = tk.Frame(frame_central, bg="#1a365d", height=42)
        barra_titulo.pack(fill="x")
        tk.Label(
            barra_titulo, text="  Diagnóstico Probabilístico - Sistema Experto", 
            bg="#1a365d", fg="#ffffff", font=("Segoe UI", 13, "bold")
        ).pack(side="left", pady=8, padx=10)

        cuerpo = tk.Frame(frame_central, bg="#f8fafc")
        cuerpo.pack(fill="both", expand=True, padx=35, pady=20)

        # Encabezado de coincidencias (Fig. 2)
        tk.Label(
            cuerpo, 
            text="Las características que se dieron coinciden con las siguientes enfermedades:", 
            bg="#f8fafc", fg="#475569", font=("Segoe UI", 13, "italic")
        ).pack(anchor="w", pady=(0, 10))

        # Enfermedad principal más probable (Diapositiva 12)
        principal = self.resultados[0]
        frame_ganador = tk.Frame(cuerpo, bg="#e0f2fe", highlightbackground="#0284c7", highlightthickness=2)
        frame_ganador.pack(fill="x", pady=8, ipady=8)
        
        texto_ganador = f"La enfermedad más probable es {principal['nombre']} con un {principal['porcentaje']}% de exactitud"
        tk.Label(
            frame_ganador, text=texto_ganador, 
            bg="#e0f2fe", fg="#0369a1", font=("Segoe UI", 16, "bold")
        ).pack(anchor="center")

        # Subtítulo de siguientes probabilidades (Mínimo 5 probabilidades en total)
        tk.Label(
            cuerpo, text="Pero también pueden ser (orden descendente de certeza):", 
            bg="#f8fafc", fg="#1a365d", font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", pady=(15, 5))

        # Contenedor para enlistar las probabilidades (Mostramos el Top 6 para asegurar mínimo 5)
        frame_lista = tk.Frame(cuerpo, bg="#ffffff", highlightbackground="#cbd5e1", highlightthickness=1)
        frame_lista.pack(fill="both", expand=True, pady=5)

        # Empezamos desde el índice 1 (el segundo lugar) para no repetir al ganador
        top_mostrar = self.resultados[1:6] if len(self.resultados) >= 2 else []
        for idx, item in enumerate(top_mostrar, start=1):
            fila = tk.Frame(frame_lista, bg="#ffffff" if idx % 2 != 0 else "#f1f5f9")
            fila.pack(fill="x", padx=15, pady=4)
            
            color_texto = "#1a365d" if idx == 1 else "#334155"
            peso_fuente = "bold" if idx == 1 else "normal"
            
            lbl_nom = tk.Label(
                fila, text=f"{idx}. {item['nombre']}", 
                bg=fila["bg"], fg=color_texto, font=("Segoe UI", 12, peso_fuente), width=35, anchor="w"
            )
            lbl_nom.pack(side="left")

            lbl_calc = tk.Label(
                fila, text=f"({item['total']} / {item['suma_total']} pts)", 
                bg=fila["bg"], fg="#64748b", font=("Segoe UI", 10)
            )
            lbl_calc.pack(side="left", padx=10)

            lbl_porc = tk.Label(
                fila, text=f"con un {item['porcentaje']}% de exactitud / certeza", 
                bg=fila["bg"], fg="#dc2626" if idx == 1 else "#0f766e", font=("Segoe UI", 12, "bold")
            )
            lbl_porc.pack(side="right")

        # ================= SECCIÓN: ¿DESEAS CONTINUAR INFIRIENDO? (Fig. 2) =================
        frame_pregunta = tk.Frame(cuerpo, bg="#f8fafc")
        frame_pregunta.pack(fill="x", pady=(15, 5))

        tk.Label(
            frame_pregunta, text="¿Deseas Continuar Infiriendo?", 
            bg="#f8fafc", fg="#1a365d", font=("Segoe UI", 14, "bold")
        ).pack(anchor="center", pady=(0, 10))

        frame_btns_sino = tk.Frame(frame_pregunta, bg="#f8fafc")
        frame_btns_sino.pack(anchor="center")

        btn_si = tk.Button(
            frame_btns_sino, text=" Sí", command=self.continuar_infiriendo,
            font=("Segoe UI", 12, "bold"), bg="#1a365d", fg="#ffffff",
            cursor="hand2", relief="solid", borderwidth=2
        )
        if self.iconos["si"]:
            btn_si.config(image=self.iconos["si"], compound="left", padx=8)
        btn_si.pack(side="left", padx=20, ipadx=30, ipady=6)

        btn_no = tk.Button(
            frame_btns_sino, text=" No", command=self.salir_al_menu,
            font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1a365d",
            cursor="hand2", relief="solid", borderwidth=2
        )
        if self.iconos["no"]:
            btn_no.config(image=self.iconos["no"], compound="left", padx=8)
        btn_no.pack(side="left", padx=20, ipadx=30, ipady=6)

        # ================= BOTÓN REGRESAR EN LA ESQUINA INFERIOR DERECHA (Fig. 2) =================
        btn_regresar = tk.Button(
            self.root, text=" REGRESAR", command=self.salir_al_menu,
            font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1a365d",
            cursor="hand2", relief="solid", borderwidth=2
        )
        icono_reg = self.iconos["regresar"] or self.iconos["salir"]
        if icono_reg:
            btn_regresar.config(image=icono_reg, compound="left", padx=8)
            
        self.canvas.create_window(
            self.w * 0.85, self.h * 0.89, 
            window=btn_regresar, width=180, height=55
        )

    def continuar_infiriendo(self):
        """Cierra esta pantalla y regresa a Búsqueda Hacia Adelante limpiando la lista."""
        self.root.destroy()
        if self.callback_continuar:
            self.callback_continuar()

    def salir_al_menu(self):
        """Cierra tanto esta pantalla como la de Búsqueda Hacia Adelante y regresa al Menú Usuario."""
        self.root.destroy()
        if self.callback_salir_menu:
            self.callback_salir_menu()