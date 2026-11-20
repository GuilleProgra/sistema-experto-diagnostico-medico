import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
sys.path.append(os.path.join(base_dir, "vistas"))

from db.consultas_sintomas import obtener_todos_registros as get_sin
from db.consultas_cuadro import ejecutar_inferencia_directa
from PantallaIdentificacion import PantallaIdentificacion

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# Variable global para compartir la última inferencia con el Módulo de Explicación
ULTIMA_EXPLICACION = None

class PantallaAdelante:
    def __init__(self, root):
        self.root = root
        self.root.title("Búsqueda Hacia Adelante")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.salir())
        
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.assets_dir = os.path.join(base_dir, "assets")
        
        self.canvas = tk.Canvas(self.root, width=self.w, height=self.h, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.dibujar_fondo()
        self.dict_sin = {}
        self.lista_completa_sintomas = [] 
        self.sintomas_seleccionados = [] 

        self.cargar_iconos()
        self.crear_interfaz()
        self.cargar_datos_combos()

    def cargar_iconos(self):
        self.iconos = {}
        nombres = ["agregar", "borrar", "inferir", "salir"]
        for clave in nombres:
            ruta = os.path.join(self.assets_dir, f"{clave}.png")
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
        except Exception:
            self.canvas.config(bg="#e2e8f0")
            
        self.canvas.create_text(self.w // 2, self.h * 0.08, text="BÚSQUEDA HACIA ADELANTE", font=("Helvetica", 40, "bold"), fill="#dc2626")

    def crear_interfaz(self):
        frame_principal = tk.Frame(self.canvas, bg="#f8fafc", highlightbackground="#1a365d", highlightthickness=3)
        self.canvas.create_window(self.w//2, self.h//2 + 30, window=frame_principal, width=self.w * 0.85, height=self.h * 0.78)

        combo_style = {"font": ("Segoe UI", 12), "state": "readonly"}

        # ================= SECCIÓN SUPERIOR (Buscador y Combobox) =================
        frame_sup = tk.Frame(frame_principal, bg="#f8fafc")
        frame_sup.pack(fill="x", pady=20, padx=40)

        tk.Label(frame_sup, text="Buscar y seleccionar características (Síntomas):", font=("Segoe UI", 12, "bold"), bg="#f8fafc", fg="#1a365d").pack(anchor="w", pady=(0, 5))
        
        frame_herramientas = tk.Frame(frame_sup, bg="#f8fafc")
        frame_herramientas.pack(fill="x")

        tk.Label(frame_herramientas, text="🔍 Buscar:", font=("Segoe UI", 11, "bold"), bg="#f8fafc", fg="#475569").pack(side="left")
        self.entry_buscar = tk.Entry(frame_herramientas, font=("Segoe UI", 12), width=25)
        self.entry_buscar.pack(side="left", padx=(5, 20), ipady=4)
        self.entry_buscar.bind("<KeyRelease>", self.filtrar_sintomas)

        tk.Label(frame_herramientas, text="Selección:", font=("Segoe UI", 11, "bold"), bg="#f8fafc", fg="#475569").pack(side="left")
        self.cb_sintoma = ttk.Combobox(frame_herramientas, width=50, **combo_style)
        self.cb_sintoma.pack(side="left", padx=(5, 20), ipady=4)

        btn_add = tk.Button(frame_herramientas, text=" Añadir", font=("Segoe UI", 11, "bold"), bg="#e2e8f0", fg="#1a365d", cursor="hand2", command=self.añadir_sintoma)
        if self.iconos["agregar"]: btn_add.config(image=self.iconos["agregar"], compound="left", padx=5)
        btn_add.pack(side="left", ipady=4, ipadx=15)

        # ================= SECCIÓN CENTRAL (Tabla y Botón Eliminar) =================
        frame_central = tk.Frame(frame_principal, bg="#f8fafc")
        frame_central.pack(fill="both", expand=True, padx=40, pady=10)

        tk.Label(frame_central, text="Características seleccionadas:", font=("Segoe UI", 12, "bold"), bg="#f8fafc", fg="#1a365d").pack(anchor="w")

        frame_tabla_botones = tk.Frame(frame_central, bg="#f8fafc")
        frame_tabla_botones.pack(fill="both", expand=True, pady=5)

        self.tabla = ttk.Treeview(frame_tabla_botones, columns=("ID_Sin", "Síntoma"), show="headings")
        
        # Ocultamos visualmente la columna ID_Sin, pero la dejamos en memoria
        self.tabla.heading("ID_Sin", text="")
        self.tabla.column("ID_Sin", width=0, stretch=False)
        
        self.tabla.heading("Síntoma", text="Síntoma")
        self.tabla.column("Síntoma", width=750, anchor="w")
        
        self.tabla.pack(side="left", fill="both", expand=True)

        btn_del = tk.Button(frame_tabla_botones, text=" Eliminar", font=("Segoe UI", 11, "bold"), bg="#e2e8f0", fg="#1a365d", cursor="hand2", command=self.eliminar_sintoma)
        if self.iconos["borrar"]: btn_del.config(image=self.iconos["borrar"], compound="left", padx=5)
        btn_del.pack(side="left", padx=20, anchor="n", ipady=4, ipadx=10)

        # ================= SECCIÓN INFERIOR =================
        frame_inf = tk.Frame(frame_principal, bg="#f8fafc")
        frame_inf.pack(fill="x", pady=25, padx=40)

        self.btn_inferir = tk.Button(
            frame_inf, text=" INFERIR", command=self.realizar_inferencia, 
            font=("Segoe UI", 16, "bold"), bg="#1a365d", fg="#ffffff", 
            cursor="hand2", relief="solid", borderwidth=2
        )
        if self.iconos["inferir"]: 
            self.btn_inferir.config(image=self.iconos["inferir"], compound="left", padx=10)
        self.btn_inferir.pack(side="left", expand=True, ipadx=40, ipady=12)

        btn_salir = tk.Button(
            frame_inf, text=" SALIR", command=self.salir, 
            font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1a365d", 
            cursor="hand2", relief="solid", borderwidth=2
        )
        if self.iconos["salir"]: 
            btn_salir.config(image=self.iconos["salir"], compound="left", padx=5)
        btn_salir.pack(side="right", ipadx=15, ipady=8)

    def cargar_datos_combos(self):
        sin_data = get_sin()
        self.lista_completa_sintomas = []
        for reg in sin_data:
            self.dict_sin[reg[1]] = reg[0] 
            self.lista_completa_sintomas.append(reg[1])
            
        self.cb_sintoma['values'] = self.lista_completa_sintomas
        if self.lista_completa_sintomas:
            self.cb_sintoma.current(0)

    def filtrar_sintomas(self, event):
        texto_buscado = self.entry_buscar.get().strip().lower()
        
        if texto_buscado == "":
            self.cb_sintoma['values'] = self.lista_completa_sintomas
        else:
            filtrados = [sin for sin in self.lista_completa_sintomas if texto_buscado in sin.lower()]
            self.cb_sintoma['values'] = filtrados
            
        if self.cb_sintoma['values']:
            self.cb_sintoma.current(0)
        else:
            self.cb_sintoma.set('')

    def añadir_sintoma(self):
        nom_sin = self.cb_sintoma.get()
        if not nom_sin or nom_sin not in self.dict_sin: 
            return messagebox.showwarning("Atención", "Seleccione un síntoma válido de la lista.", parent=self.root)
        
        id_sin = self.dict_sin[nom_sin]

        for row in self.tabla.get_children():
            if int(self.tabla.item(row, "values")[0]) == id_sin:
                return messagebox.showwarning("Atención", "Ese síntoma ya fue agregado a la tabla.", parent=self.root)

        self.tabla.insert("", "end", values=(id_sin, nom_sin))
        self.sintomas_seleccionados.append(id_sin)
        
        self.entry_buscar.delete(0, tk.END)
        self.filtrar_sintomas(None)
        self.entry_buscar.focus() 

    def eliminar_sintoma(self):
        item = self.tabla.focus()
        if not item:
            return messagebox.showwarning("Atención", "Seleccione un síntoma de la tabla para eliminar.", parent=self.root)
            
        valores = self.tabla.item(item, "values")
        id_sin = int(valores[0])
        
        self.tabla.delete(item)
        if id_sin in self.sintomas_seleccionados:
            self.sintomas_seleccionados.remove(id_sin)

    def limpiar_para_nueva_inferencia(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        self.sintomas_seleccionados.clear()
        ejecutar_inferencia_directa([]) 

    def realizar_inferencia(self):
        if not self.sintomas_seleccionados:
            return messagebox.showwarning("Atención", "Agregue al menos un síntoma para realizar la inferencia.", parent=self.root)
            
        resultados = ejecutar_inferencia_directa(self.sintomas_seleccionados)
        if not resultados:
            return messagebox.showerror("Error", "No se pudo realizar la inferencia. Revise que la base de datos esté activa.", parent=self.root)

        global ULTIMA_EXPLICACION
        lineas = [
            "=======================================================================",
            "          MEMORIA DE CÁLCULO - INFERENCIA DIRECTA (REGLA DE 3)         ",
            "=======================================================================\n",
            f"IDs de Síntomas activados con bandera = 1: {self.sintomas_seleccionados}\n"
        ]
        for r in resultados[:6]:
            lineas.append(
                f"Enfermedad: {r['nombre']}\n"
                f"   {r['suma_total']} pts ----- 100%\n"
                f"   {r['total']} pts ----- X = {r['porcentaje']}% de certeza\n"
            )
        ULTIMA_EXPLICACION = "\n".join(lineas)

        ventana_res = tk.Toplevel(self.root)
        PantallaIdentificacion(
            ventana_res, 
            resultados=resultados,
            callback_continuar=self.limpiar_para_nueva_inferencia,
            callback_salir_menu=self.salir
        )

    def salir(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PantallaAdelante(root)
    root.mainloop()