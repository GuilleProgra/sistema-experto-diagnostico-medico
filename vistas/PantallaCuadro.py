import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from db.consultas_cuadro import obtener_sintomas_por_enfermedad, insertar_relacion, eliminar_relacion
from db.consultas_enfermedades import obtener_todos_registros as get_enf
from db.consultas_sintomas import obtener_todos_registros as get_sin

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception: pass

class PantallaCuadro:
    def __init__(self, root, al_cerrar_callback=None):
        self.root = root
        self.al_cerrar_callback = al_cerrar_callback
        self.root.title("Cuadro Patológico")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.salir())
        
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.assets_dir = os.path.join(base_dir, "assets")
        
        self.canvas = tk.Canvas(self.root, width=self.w, height=self.h, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.dibujar_fondo()
        self.img_vacia = tk.PhotoImage()

        self.dict_enf = {} 
        self.dict_sin = {}
        self.relaciones_temporales = [] 

        self.cargar_iconos()
        self.crear_interfaz()
        self.cargar_datos_combos()

    def cargar_iconos(self):
        self.iconos = {}
        nombres = ["grabar", "cancelar", "salir"]
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
        except:
            self.canvas.config(bg="#e2e8f0")
        self.canvas.create_text(self.w // 2, self.h * 0.08, text="** CUADRO PATOLÓGICO **", font=("Helvetica", 40, "bold"), fill="#1a365d")

    def crear_interfaz(self):
        frame_principal = tk.Frame(self.canvas, bg="#f8fafc", highlightbackground="#1a365d", highlightthickness=3)
        self.canvas.create_window(self.w//2, self.h//2 + 30, window=frame_principal, width=self.w * 0.85, height=self.h * 0.78)

        lbl_style = {"bg": "#f8fafc", "fg": "#1a365d", "font": ("Segoe UI", 12, "bold")}
        combo_style = {"font": ("Segoe UI", 12), "state": "readonly"}

        # ================= SECCIÓN SUPERIOR =================
        frame_sup = tk.Frame(frame_principal, bg="#f8fafc")
        frame_sup.pack(fill="x", pady=15, padx=20)

        # IZQUIERDA: Enfermedades
        frame_izq = tk.Frame(frame_sup, bg="#f8fafc")
        frame_izq.pack(side="left", expand=True, fill="both")
        
        tk.Label(frame_izq, text="Enfermedades:", **lbl_style).pack(anchor="w")
        self.cb_enfermedad = ttk.Combobox(frame_izq, width=40, **combo_style)
        self.cb_enfermedad.pack(anchor="w", pady=5)
        self.cb_enfermedad.bind("<<ComboboxSelected>>", self.on_enfermedad_select)

        self.lbl_img_enf = tk.Label(frame_izq, text="Sin Imagen", font=("Segoe UI", 11, "bold"), fg="#475569",
                                    bg="#e2e8f0", relief="solid", borderwidth=1, 
                                    image=self.img_vacia, compound="center", width=300, height=200)
        self.lbl_img_enf.pack(anchor="w", pady=10)

        # DERECHA: Síntomas
        frame_der = tk.Frame(frame_sup, bg="#f8fafc")
        frame_der.pack(side="right", expand=True, fill="both")
        
        tk.Label(frame_der, text="Características (Síntomas):", **lbl_style).pack(anchor="w")
        self.cb_sintoma = ttk.Combobox(frame_der, width=50, **combo_style)
        self.cb_sintoma.pack(anchor="w", pady=5)
        self.cb_sintoma.bind("<<ComboboxSelected>>", self.on_sintoma_select)

        self.lbl_img_sin = tk.Label(frame_der, text="Sin Imagen", font=("Segoe UI", 11, "bold"), fg="#475569",
                                    bg="#e2e8f0", relief="solid", borderwidth=1, 
                                    image=self.img_vacia, compound="center", width=300, height=200)
        self.lbl_img_sin.pack(anchor="w", pady=10)

        # ================= SECCIÓN MEDIA (Peso) =================
        frame_medio = tk.Frame(frame_principal, bg="#f8fafc")
        frame_medio.pack(fill="x", padx=20, pady=5)

        frame_peso = tk.Frame(frame_medio, bg="#f8fafc")
        frame_peso.pack(side="top")

        tk.Label(frame_peso, text="Peso (%):", **lbl_style).pack(side="left", padx=5)
        self.entry_peso = tk.Entry(frame_peso, font=("Segoe UI", 12, "bold"), width=5, justify="center")
        self.entry_peso.pack(side="left", padx=5)

        # ================= SECCIÓN INFERIOR (Tabla y Botones Laterales) =================
        frame_inf = tk.Frame(frame_principal, bg="#f8fafc")
        frame_inf.pack(fill="both", expand=True, padx=20, pady=(0,10))

        tk.Label(frame_inf, text="Características seleccionadas:", **lbl_style).pack(anchor="w")
        
        frame_tabla_botones = tk.Frame(frame_inf, bg="#f8fafc")
        frame_tabla_botones.pack(fill="both", expand=True, pady=5)

        # TABLA
        self.tabla = ttk.Treeview(frame_tabla_botones, columns=("ID_Sin", "Síntoma", "Peso", "Estado"), show="headings", height=6)
        self.tabla.heading("ID_Sin", text="ID_Sin")
        self.tabla.heading("Síntoma", text="Síntoma")
        self.tabla.heading("Peso", text="Peso (%)")
        self.tabla.heading("Estado", text="Estado")
        
        self.tabla.column("ID_Sin", width=0, stretch=False)
        self.tabla.column("Síntoma", width=550)
        self.tabla.column("Peso", width=80, anchor="center")
        self.tabla.column("Estado", width=120, anchor="center")
        self.tabla.pack(side="left", fill="both", expand=True)

        # BOTONES LATERALES AÑADIR/ELIMINAR
        frame_botones_add_del = tk.Frame(frame_tabla_botones, bg="#f8fafc")
        frame_botones_add_del.pack(side="left", padx=15, pady=20)

        btn_add = tk.Button(frame_botones_add_del, text="Añadir", font=("Segoe UI", 10, "bold"), bg="#e2e8f0", fg="#1a365d", cursor="hand2", command=self.añadir_temporal)
        btn_add.pack(pady=10, fill="x", ipady=5)

        btn_del = tk.Button(frame_botones_add_del, text="Eliminar", font=("Segoe UI", 10, "bold"), bg="#e2e8f0", fg="#1a365d", cursor="hand2", command=self.eliminar_seleccionado)
        btn_del.pack(pady=10, fill="x", ipady=5)

        # ================= BOTONES INFERIORES GLOBALES =================
        frame_botones_globales = tk.Frame(frame_principal, bg="#f8fafc")
        frame_botones_globales.pack(fill="x", pady=10, padx=20)
        
        btn_style = {"font": ("Segoe UI", 11, "bold"), "bg": "#ffffff", "fg": "#1a365d", "cursor": "hand2", "relief": "solid", "borderwidth": 2, "width": 150, "height": 45}

        self.btn_guardar = tk.Button(frame_botones_globales, text=" GUARDAR", command=self.guardar_bd, **btn_style)
        if self.iconos["grabar"]: self.btn_guardar.config(image=self.iconos["grabar"], compound="left", padx=5)
        self.btn_guardar.pack(side="left", padx=10)

        btn_cancelar = tk.Button(frame_botones_globales, text=" CANCELAR", command=self.cancelar, **btn_style)
        if self.iconos["cancelar"]: btn_cancelar.config(image=self.iconos["cancelar"], compound="left", padx=5)
        btn_cancelar.pack(side="left", padx=10)

        btn_salir = tk.Button(frame_botones_globales, text=" SALIR", command=self.salir, **btn_style)
        if self.iconos["salir"]: btn_salir.config(image=self.iconos["salir"], compound="left", padx=5)
        btn_salir.pack(side="right", padx=10)
        
        self.btn_guardar.config(state="disabled")

    def cargar_datos_combos(self):
        enf_data = get_enf()
        nombres_enf = []
        for reg in enf_data:
            self.dict_enf[reg[1]] = (reg[0], reg[3])
            nombres_enf.append(reg[1])
        self.cb_enfermedad['values'] = nombres_enf

        sin_data = get_sin()
        nombres_sin = []
        for reg in sin_data:
            self.dict_sin[reg[1]] = (reg[0], reg[2])
            nombres_sin.append(reg[1])
        self.cb_sintoma['values'] = nombres_sin

        if nombres_enf:
            self.cb_enfermedad.current(0)
            self.on_enfermedad_select(None)
        if nombres_sin:
            self.cb_sintoma.current(0)
            self.on_sintoma_select(None)

    def mostrar_imagen(self, nombre_imagen, label_destino):
        if not nombre_imagen: nombre_imagen = "default.png"
        ruta = os.path.join(self.assets_dir, nombre_imagen)
        if os.path.exists(ruta):
            img = Image.open(ruta).resize((300, 200), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label_destino.config(image=photo, text="")
            label_destino.image = photo 
        else:
            label_destino.config(image=self.img_vacia, text="Sin Imagen", compound="center")

    def on_enfermedad_select(self, event):
        seleccion = self.cb_enfermedad.get()
        if seleccion in self.dict_enf:
            self.mostrar_imagen(self.dict_enf[seleccion][1], self.lbl_img_enf)
            self.cargar_tabla_desde_bd()

    def on_sintoma_select(self, event):
        seleccion = self.cb_sintoma.get()
        if seleccion in self.dict_sin:
            self.mostrar_imagen(self.dict_sin[seleccion][1], self.lbl_img_sin)

    def actualizar_estado_guardar(self):
        """Habilita el botón GUARDAR únicamente si hay síntomas nuevos pendientes por grabar."""
        cambios_pendientes = any(self.tabla.item(row, "values")[3] != "Guardado" for row in self.tabla.get_children())
        self.btn_guardar.config(state="normal" if cambios_pendientes else "disabled")

    def cargar_tabla_desde_bd(self):
        for row in self.tabla.get_children(): self.tabla.delete(row)
        self.relaciones_temporales.clear()
        
        if not self.cb_enfermedad.get(): return
        id_enfermedad = self.dict_enf[self.cb_enfermedad.get()][0]
        relaciones = obtener_sintomas_por_enfermedad(id_enfermedad)
        
        for rel in relaciones:
            self.tabla.insert("", "end", values=(rel[1], rel[2], f"{rel[3]}%", "Guardado"))
            self.relaciones_temporales.append({"id_rel_bd": rel[0], "id_sin": rel[1], "estado": "Guardado"})
            
        self.actualizar_estado_guardar()

    def añadir_temporal(self):
        nom_enf = self.cb_enfermedad.get()
        nom_sin = self.cb_sintoma.get()
        peso_txt = self.entry_peso.get().strip()

        if not nom_enf or not nom_sin or not peso_txt:
            return messagebox.showwarning("Faltan datos", "Seleccione enfermedad, síntoma e ingrese el peso.", parent=self.root)
            
        try:
            peso = int(peso_txt)
            if peso <= 0 or peso > 100: raise ValueError
        except ValueError:
            return messagebox.showerror("Error", "El peso de cada síntoma debe ser un número entre 1 y 100.", parent=self.root)

        id_sin = self.dict_sin[nom_sin][0]

        for row in self.tabla.get_children():
            if int(self.tabla.item(row, "values")[0]) == id_sin:
                return messagebox.showwarning("Repetido", "Ese síntoma ya está en la lista de esta enfermedad.", parent=self.root)

        self.tabla.insert("", "end", values=(id_sin, nom_sin, f"{peso}%", "* Pendiente de Guardar"))
        self.relaciones_temporales.append({"id_rel_bd": None, "id_sin": id_sin, "peso": peso, "estado": "Nuevo"})
        
        self.entry_peso.delete(0, tk.END)
        self.actualizar_estado_guardar()

    def eliminar_seleccionado(self):
        item = self.tabla.focus()
        if not item:
            return messagebox.showwarning("Atención", "Seleccione un síntoma de la lista para eliminar.", parent=self.root)
            
        valores = self.tabla.item(item, "values")
        id_sin = int(valores[0])
        estado = valores[3]

        if estado == "Guardado":
            if messagebox.askyesno("Confirmar", "¿Eliminar permanentemente este síntoma de la enfermedad?", parent=self.root):
                id_enf = self.dict_enf[self.cb_enfermedad.get()][0]
                id_rel_bd = next((r["id_rel_bd"] for r in self.relaciones_temporales if r["id_sin"] == id_sin), None)
                
                if id_rel_bd and eliminar_relacion(id_rel_bd, id_enf):
                    self.cargar_tabla_desde_bd()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar de la BD.", parent=self.root)
        else:
            self.tabla.delete(item)
            self.relaciones_temporales = [r for r in self.relaciones_temporales if r["id_sin"] != id_sin]
            self.actualizar_estado_guardar()

    def guardar_bd(self):
        id_enf = self.dict_enf[self.cb_enfermedad.get()][0]
        errores = 0
        
        for rel in self.relaciones_temporales:
            if rel["estado"] == "Nuevo":
                exito, msj = insertar_relacion(id_enf, rel["id_sin"], rel["peso"])
                if not exito: errores += 1
                
        if errores == 0:
            messagebox.showinfo("Éxito", "Toda la información se guardó correctamente.", parent=self.root)
        else:
            messagebox.showwarning("Atención", f"Se guardó la información, pero hubo {errores} error(es).", parent=self.root)
            
        self.cargar_tabla_desde_bd()

    def cancelar(self):
        if not self.cb_enfermedad.get(): return
        self.entry_peso.delete(0, tk.END)
        self.cargar_tabla_desde_bd()

    def salir(self):
        self.al_cerrar_callback() if self.al_cerrar_callback else self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PantallaCuadro(root)
    root.mainloop()