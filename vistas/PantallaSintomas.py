import tkinter as tk
from tkinter import messagebox, filedialog 
from PIL import Image, ImageTk
import os
import sys
import shutil 

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from db.consultas_sintomas import (
    obtener_primer_registro, obtener_ultimo_registro, 
    obtener_siguiente_registro, obtener_anterior_registro,
    insertar_registro, actualizar_registro, eliminar_registro
)
from vistas.componentes_ui import (
    cargar_iconos, dibujar_fondo_y_titulo, crear_formulario, 
    crear_botones_navegacion, crear_botones_accion
)
from vistas.ventana_consulta_sintomas import abrir_ventana_consulta_sintomas

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception: pass

class PantallaSintomas:
    def __init__(self, root, al_cerrar_callback=None):
        self.root = root
        self.al_cerrar_callback = al_cerrar_callback
        self.root.title("Gestión de Síntomas")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.salir())
        
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.assets_dir = os.path.join(base_dir, "assets")
        
        self.id_actual = None 
        self.registro_actual = None
        self.accion_actual = None 
        self.ruta_img_seleccionada = None 
        
        self.canvas = tk.Canvas(self.root, width=self.w, height=self.h, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        dibujar_fondo_y_titulo(self.canvas, self.w, self.h, self.assets_dir, "DATOS DE SÍNTOMAS")
        self.iconos = cargar_iconos(self.assets_dir)
        self.img_vacia = tk.PhotoImage()

        self.entry_id, self.entry_nombre, self.text_desc, self.lbl_imagen = crear_formulario(
            self.canvas, self.w, self.h, self.img_vacia
        )
        
        self.entry_nombre.config(disabledbackground="#f8fafc", disabledforeground="#000000")
        self.entry_id.config(disabledbackground="#f8fafc", disabledforeground="#1a365d")
        
        # Bloqueamos permanentemente la descripción porque los síntomas no la usan
        self.text_desc.insert("1.0", "(Los síntomas no requieren descripción larga)")
        self.text_desc.config(state="disabled", bg="#e2e8f0", fg="#64748b")
        
        self.lbl_imagen.bind("<Button-1>", self.seleccionar_imagen)

        self.botones_nav = crear_botones_navegacion(self.root, self.canvas, self.w, self.h, self.iconos, 
            [self.ir_inicio, self.ir_anterior, self.ir_siguiente, self.ir_final])

        self.botones_accion = crear_botones_accion(self.root, self.canvas, self.w, self.h, self.iconos, 
            [self.preparar_nuevo, self.grabar_accion, self.cancelar_accion, 
             self.preparar_modificar, self.borrar_accion, self.abrir_consulta, self.salir])
        
        self.configurar_estado_botones(editando=False)
        self.ir_inicio() 

    def configurar_estado_botones(self, editando):
        estado_nav = "disabled" if editando else "normal"
        estado_edicion = "normal" if editando else "disabled"

        for btn in self.botones_nav.values(): btn.config(state=estado_nav)
        for nom in ["NUEVO", "MODIFICAR", "BORRAR", "CONSULTA"]: self.botones_accion[nom].config(state=estado_nav)
        for nom in ["GRABAR", "CANCELAR"]: self.botones_accion[nom].config(state=estado_edicion)
        self.entry_nombre.config(state=estado_edicion)

    def mostrar_registro(self, registro):
        self.entry_id.config(state="normal")
        self.entry_nombre.config(state="normal")

        if not registro: 
            self.id_actual = None
            self.registro_actual = None
            self.entry_id.delete(0, tk.END)
            self.entry_nombre.delete(0, tk.END)
            self.lbl_imagen.config(image=self.img_vacia, text="Sin registros", compound="center")
            self.entry_id.config(state="disabled")
            self.entry_nombre.config(state="disabled")
            return 
            
        self.registro_actual = registro 
        self.id_actual = registro[0]
        
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, str(registro[0]))
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, registro[1])
        
        self.entry_id.config(state="disabled")
        self.entry_nombre.config(state="disabled")
        
        nombre_imagen = registro[2] if registro[2] else "default.png"
        ruta_img = os.path.join(self.assets_dir, nombre_imagen)
        
        if os.path.exists(ruta_img):
            img = Image.open(ruta_img).resize((400, 300), Image.Resampling.LANCZOS)
            self.img_preview = ImageTk.PhotoImage(img)
            self.lbl_imagen.config(image=self.img_preview, text="")
        else:
            self.lbl_imagen.config(image=self.img_vacia, text="Imagen no encontrada", compound="center")

    def preparar_nuevo(self):
        self.accion_actual = 'NUEVO'
        self.ruta_img_seleccionada = None
        self.configurar_estado_botones(editando=True)
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, "AUTO")
        self.entry_id.config(state="disabled")
        self.entry_nombre.delete(0, tk.END)
        self.lbl_imagen.config(image=self.img_vacia, text="Clic aquí para\ncargar una imagen", cursor="hand2")
        self.entry_nombre.focus_set()

    def preparar_modificar(self):
        if not self.id_actual: return messagebox.showwarning("Atención", "Seleccione un registro.", parent=self.root)
        self.accion_actual = 'MODIFICAR'
        self.ruta_img_seleccionada = None
        self.configurar_estado_botones(editando=True)
        self.lbl_imagen.config(cursor="hand2")
        self.entry_nombre.focus_set()

    def borrar_accion(self):
        if not self.id_actual: return
        if messagebox.askyesno("Confirmar", f"¿Eliminar permanentemente:\n\n'{self.entry_nombre.get()}'?", parent=self.root):
            nombre_img = self.registro_actual[2] if self.registro_actual else None
            if eliminar_registro(self.id_actual):
                if nombre_img and nombre_img != "default.png":
                    ruta = os.path.join(self.assets_dir, nombre_img)
                    if os.path.exists(ruta): os.remove(ruta)
                messagebox.showinfo("Éxito", "Síntoma eliminado.", parent=self.root)
                self.ir_inicio() 
            else: messagebox.showerror("Error", "Problema en BD.", parent=self.root)

    def seleccionar_imagen(self, event):
        if not self.accion_actual: return 
        ruta = filedialog.askopenfilename(parent=self.root, filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if ruta:
            self.ruta_img_seleccionada = ruta
            img = Image.open(ruta).resize((400, 300), Image.Resampling.LANCZOS)
            self.img_preview = ImageTk.PhotoImage(img)
            self.lbl_imagen.config(image=self.img_preview, text="")

    def grabar_accion(self):
        nombre = self.entry_nombre.get().strip()
        if not nombre: return messagebox.showwarning("Atención", "El nombre es obligatorio.", parent=self.root)

        nombre_imagen = None
        if self.ruta_img_seleccionada:
            nombre_imagen = os.path.basename(self.ruta_img_seleccionada) 
            ruta_destino = os.path.join(self.assets_dir, nombre_imagen)
            try:
                if self.ruta_img_seleccionada != ruta_destino: shutil.copy(self.ruta_img_seleccionada, ruta_destino)
            except Exception as e: return messagebox.showerror("Error", f"No se pudo copiar: {e}", parent=self.root)

        if self.accion_actual == 'NUEVO': exito = insertar_registro(nombre, nombre_imagen)
        else: exito = actualizar_registro(self.id_actual, nombre, nombre_imagen)
        
        if exito:
            messagebox.showinfo("Éxito", "Registro guardado.", parent=self.root)
            accion = self.accion_actual
            self.accion_actual = None
            self.configurar_estado_botones(editando=False)
            self.ir_final() if accion == 'NUEVO' else self.mostrar_registro((self.id_actual, nombre, nombre_imagen or self.registro_actual[2]))
        else: messagebox.showerror("Error", "Fallo en BD.", parent=self.root)

    def cancelar_accion(self):
        self.accion_actual, self.ruta_img_seleccionada = None, None
        self.configurar_estado_botones(editando=False)
        self.mostrar_registro(self.registro_actual)

    def abrir_consulta(self): abrir_ventana_consulta_sintomas(self.root, self.w, self.h, self.mostrar_registro)
    def ir_inicio(self): self.mostrar_registro(obtener_primer_registro())
    def ir_final(self): self.mostrar_registro(obtener_ultimo_registro())
    def ir_siguiente(self): self.mostrar_registro(obtener_siguiente_registro(self.id_actual)) if self.id_actual else None
    def ir_anterior(self): self.mostrar_registro(obtener_anterior_registro(self.id_actual)) if self.id_actual else None
    def salir(self): self.al_cerrar_callback() if self.al_cerrar_callback else self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PantallaSintomas(root)
    root.mainloop()