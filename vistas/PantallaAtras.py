import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# Importamos las consultas para llenar la lista de enfermedades y traer sus síntomas
from db.consultas_enfermedades import obtener_todos_registros as get_enf
from db.consultas_cuadro import obtener_sintomas_por_enfermedad

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception: pass

class PantallaAtras:
    def __init__(self, root):
        self.root = root
        self.root.title("Búsqueda Hacia Atrás")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.salir())
        
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.assets_dir = os.path.join(base_dir, "assets")
        
        self.canvas = tk.Canvas(self.root, width=self.w, height=self.h, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.dibujar_fondo()
        self.dict_enf = {}

        self.cargar_iconos()
        self.crear_interfaz()
        self.cargar_datos_combos()

    def cargar_iconos(self):
        self.iconos = {}
        # Ahora solo cargamos el icono de salir para esta pantalla
        archivos = {
            "salir": "salir.png"
        }
        for clave, nombre_archivo in archivos.items():
            ruta = os.path.join(self.assets_dir, nombre_archivo)
            if os.path.exists(ruta):
                img = Image.open(ruta).resize((30, 30), Image.Resampling.LANCZOS)
                self.iconos[clave] = ImageTk.PhotoImage(img)
            else:
                self.iconos[clave] = None

    def dibujar_fondo(self):
        try:
            img_fondo = Image.open(os.path.join(self.assets_dir, "fondo.jpg")).resize((self.w, self.h), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(img_fondo)
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except:
            self.canvas.config(bg="#e2e8f0")
            
        self.canvas.create_text(self.w // 2, self.h * 0.08, text="BÚSQUEDA HACIA ATRÁS", font=("Helvetica", 40, "bold"), fill="#dc2626")

    def crear_interfaz(self):
        frame_principal = tk.Frame(self.canvas, bg="#f8fafc", highlightbackground="#1a365d", highlightthickness=3)
        self.canvas.create_window(self.w//2, self.h//2 + 30, window=frame_principal, width=self.w * 0.85, height=self.h * 0.78)

        lbl_style = {"bg": "#f8fafc", "fg": "#1a365d", "font": ("Segoe UI", 12, "bold")}
        combo_style = {"font": ("Segoe UI", 12), "state": "readonly"}

        # ================= SECCIÓN SUPERIOR (Hipótesis) =================
        frame_sup = tk.Frame(frame_principal, bg="#f8fafc")
        frame_sup.pack(fill="x", pady=20, padx=40)

        tk.Label(frame_sup, text="1. Seleccione la Hipótesis a evaluar (Enfermedad):", **lbl_style).pack(anchor="w")
        
        self.cb_enfermedad = ttk.Combobox(frame_sup, width=70, **combo_style)
        self.cb_enfermedad.pack(anchor="w", pady=10, ipady=4)
        self.cb_enfermedad.bind("<<ComboboxSelected>>", self.cargar_sintomas_esperados)

        # ================= SECCIÓN CENTRAL (Tabla de características esperadas) =================
        frame_central = tk.Frame(frame_principal, bg="#f8fafc")
        frame_central.pack(fill="both", expand=True, padx=40, pady=10)

        tk.Label(frame_central, text="2. Características requeridas para confirmar la hipótesis:", **lbl_style).pack(anchor="w")

        frame_tabla = tk.Frame(frame_central, bg="#f8fafc")
        frame_tabla.pack(fill="both", expand=True, pady=5)

        self.tabla = ttk.Treeview(frame_tabla, columns=("ID_Sin", "Síntoma", "Peso"), show="headings")
        self.tabla.heading("ID_Sin", text="ID")
        self.tabla.heading("Síntoma", text="Síntoma")
        self.tabla.heading("Peso", text="Peso (%)")
        
        self.tabla.column("ID_Sin", width=50, anchor="center")
        self.tabla.column("Síntoma", width=600)
        self.tabla.column("Peso", width=100, anchor="center")
        self.tabla.pack(side="left", fill="both", expand=True)

        # ================= SECCIÓN INFERIOR (Botón Salir) =================
        frame_inf = tk.Frame(frame_principal, bg="#f8fafc")
        frame_inf.pack(fill="x", pady=25, padx=40)

        # Botón SALIR (Alineado a la derecha)
        btn_salir = tk.Button(frame_inf, text=" SALIR", command=self.salir, 
                              font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1a365d", 
                              cursor="hand2", relief="solid", borderwidth=2)
        if self.iconos["salir"]: 
            btn_salir.config(image=self.iconos["salir"], compound="left", padx=5)
            
        btn_salir.pack(side="right", ipadx=15, ipady=8)

    def cargar_datos_combos(self):
        enf_data = get_enf()
        nombres_enf = []
        for reg in enf_data:
            self.dict_enf[reg[1]] = reg[0] # Guardamos Nombre: ID
            nombres_enf.append(reg[1])
            
        self.cb_enfermedad['values'] = nombres_enf
        if nombres_enf:
            self.cb_enfermedad.current(0)
            self.cargar_sintomas_esperados(None)

    def cargar_sintomas_esperados(self, event):
        """Limpia la tabla y carga los síntomas que pertenecen a la enfermedad seleccionada."""
        for row in self.tabla.get_children(): 
            self.tabla.delete(row)
            
        seleccion = self.cb_enfermedad.get()
        if not seleccion: return
        
        id_enfermedad = self.dict_enf[seleccion]
        relaciones = obtener_sintomas_por_enfermedad(id_enfermedad)
        
        for rel in relaciones:
            # rel[1] es ID Síntoma, rel[2] es Nombre, rel[3] es Peso
            self.tabla.insert("", "end", values=(rel[1], rel[2], f"{rel[3]}%"))

    def salir(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PantallaAtras(root)
    root.mainloop()