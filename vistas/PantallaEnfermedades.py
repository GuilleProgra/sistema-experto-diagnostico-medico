import tkinter as tk
from tkinter import messagebox, filedialog 
from PIL import Image, ImageTk
import os
import sys
import shutil 

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from db.consultas_enfermedades import (
    obtener_primer_registro, obtener_ultimo_registro, 
    obtener_siguiente_registro, obtener_anterior_registro,
    insertar_registro, actualizar_registro, eliminar_registro
)
from vistas.componentes_ui import (
    cargar_iconos, dibujar_fondo_y_titulo, crear_formulario, 
    crear_botones_navegacion, crear_botones_accion
)
from vistas.ventana_consulta import abrir_ventana_consulta

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception: pass

class PantallaEnfermedades:
    def __init__(self, root, al_cerrar_callback=None):
        self.root = root
        self.al_cerrar_callback = al_cerrar_callback
        self.root.title("Gestión de Enfermedades")
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

        dibujar_fondo_y_titulo(self.canvas, self.w, self.h, self.assets_dir, "DATOS DE ENFERMEDADES")
        self.iconos = cargar_iconos(self.assets_dir)
        self.img_vacia = tk.PhotoImage()

        self.entry_id, self.entry_nombre, self.text_desc, self.lbl_imagen = crear_formulario(
            self.canvas, self.w, self.h, self.img_vacia
        )
        
        # Para que el Nombre se siga leyendo claro en negro aunque esté bloqueado
        self.entry_nombre.config(disabledbackground="#f8fafc", disabledforeground="#000000")
        self.entry_id.config(disabledbackground="#f8fafc", disabledforeground="#1a365d")
        
        self.lbl_imagen.bind("<Button-1>", self.seleccionar_imagen)

        self.botones_nav = crear_botones_navegacion(self.root, self.canvas, self.w, self.h, self.iconos, 
            [self.ir_inicio, self.ir_anterior, self.ir_siguiente, self.ir_final])

        self.botones_accion = crear_botones_accion(self.root, self.canvas, self.w, self.h, self.iconos, 
            [self.preparar_nuevo, self.grabar_accion, self.cancelar_accion, 
             self.preparar_modificar, self.borrar_accion, self.abrir_consulta, self.salir])
        
        self.configurar_estado_botones(editando=False)
        self.ir_inicio() 

    # ==========================================
    # CONTROL DE ESTADO DE LA INTERFAZ
    # ==========================================
    def configurar_estado_botones(self, editando):
        """Activa o desactiva botones y cajas de texto según el modo actual."""
        estado_nav = "disabled" if editando else "normal"
        estado_edicion = "normal" if editando else "disabled"

        # 1. Bloquear o desbloquear flechas de navegación
        for btn in self.botones_nav.values():
            btn.config(state=estado_nav)

        # 2. Bloquear o desbloquear botones de acción generales
        self.botones_accion["NUEVO"].config(state=estado_nav)
        self.botones_accion["MODIFICAR"].config(state=estado_nav)
        self.botones_accion["BORRAR"].config(state=estado_nav)
        self.botones_accion["CONSULTA"].config(state=estado_nav)

        # 3. Activar o desactivar GRABAR y CANCELAR
        self.botones_accion["GRABAR"].config(state=estado_edicion)
        self.botones_accion["CANCELAR"].config(state=estado_edicion)

        # 4. Habilitar o bloquear las cajas de Nombre y Descripción
        self.entry_nombre.config(state=estado_edicion)
        self.text_desc.config(state=estado_edicion, bg="#ffffff" if editando else "#f8fafc")

    # ==========================================
    # LÓGICA DE INTERFAZ Y NAVEGACIÓN
    # ==========================================
    def mostrar_registro(self, registro):
        # Desbloqueamos temporalmente las cajas para que Python pueda escribir en ellas
        self.entry_id.config(state="normal")
        self.entry_nombre.config(state="normal")
        self.text_desc.config(state="normal")

        if not registro: 
            self.id_actual = None
            self.registro_actual = None
            self.entry_id.delete(0, tk.END)
            self.entry_nombre.delete(0, tk.END)
            self.text_desc.delete("1.0", tk.END)
            self.lbl_imagen.config(image=self.img_vacia, text="Sin registros", compound="center", cursor="")
            
            # Volvemos a poner el candado
            self.entry_id.config(state="disabled")
            self.entry_nombre.config(state="disabled")
            self.text_desc.config(state="disabled", bg="#f8fafc")
            return 
            
        self.registro_actual = registro 
        self.id_actual = registro[0]
        
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, str(registro[0]))
        
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, registro[1])
        
        self.text_desc.delete("1.0", tk.END)
        self.text_desc.insert("1.0", registro[2] if registro[2] else "")
        
        # Volvemos a poner el candado de solo lectura
        self.entry_id.config(state="disabled")
        self.entry_nombre.config(state="disabled")
        self.text_desc.config(state="disabled", bg="#f8fafc")
        
        if registro[3] and os.path.exists(os.path.join(self.assets_dir, registro[3])):
            img = Image.open(os.path.join(self.assets_dir, registro[3])).resize((400, 300), Image.Resampling.LANCZOS)
            self.img_preview = ImageTk.PhotoImage(img)
            self.lbl_imagen.config(image=self.img_preview, text="", cursor="")
        else:
            txt_error = "Imagen no encontrada\nen assets/" if registro[3] else "Sin Imagen"
            self.lbl_imagen.config(image=self.img_vacia, text=txt_error, compound="center", cursor="")

    # ==========================================
    # LÓGICA CRUD (NUEVO, MODIFICAR, BORRAR, GRABAR)
    # ==========================================
    def preparar_nuevo(self):
        self.accion_actual = 'NUEVO'
        self.ruta_img_seleccionada = None
        
        # Esto apaga navegación y desbloquea Nombre y Descripción
        self.configurar_estado_botones(editando=True)

        self.entry_id.config(state="normal")
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, "AUTO")
        self.entry_id.config(state="disabled")

        self.entry_nombre.delete(0, tk.END)
        self.text_desc.delete("1.0", tk.END)
        
        self.lbl_imagen.config(image=self.img_vacia, text="Clic aquí para\ncargar una imagen", 
                               compound="center", cursor="hand2", fg="#2563eb")
        self.entry_nombre.focus_set()

    def preparar_modificar(self):
        if not self.id_actual:
            messagebox.showwarning("Atención", "No hay ningún registro seleccionado para modificar.", parent=self.root)
            return

        self.accion_actual = 'MODIFICAR'
        self.ruta_img_seleccionada = None

        # Esto apaga navegación y desbloquea Nombre y Descripción conservando su texto
        self.configurar_estado_botones(editando=True)
        self.lbl_imagen.config(cursor="hand2")
        self.entry_nombre.focus_set()

    def borrar_accion(self):
        if not self.id_actual:
            messagebox.showwarning("Atención", "No hay ningún registro seleccionado para borrar.", parent=self.root)
            return

        respuesta = messagebox.askyesno("Confirmar Eliminación", 
                                        f"¿Estás seguro de que deseas eliminar permanentemente:\n\n'{self.entry_nombre.get()}'?",
                                        parent=self.root)
        if respuesta:
            nombre_imagen = self.registro_actual[3] if self.registro_actual else None
            exito = eliminar_registro(self.id_actual)
            
            if exito:
                if nombre_imagen:
                    ruta_img_completa = os.path.join(self.assets_dir, nombre_imagen)
                    if os.path.exists(ruta_img_completa):
                        try:
                            os.remove(ruta_img_completa)
                        except Exception as e:
                            print(f"Nota: El registro se borró de BD, pero la imagen no: {e}")
                
                messagebox.showinfo("Éxito", "El registro y su imagen han sido eliminados.", parent=self.root)
                self.ir_inicio() 
            else:
                messagebox.showerror("Error BD", "Hubo un problema al intentar eliminar el registro.", parent=self.root)

    def seleccionar_imagen(self, event):
        if not self.accion_actual: return 
            
        ruta = filedialog.askopenfilename(
            parent=self.root,
            title="Seleccionar imagen de la enfermedad",
            filetypes=[("Archivos de Imagen", "*.jpg *.jpeg *.png")]
        )
        
        if ruta:
            self.ruta_img_seleccionada = ruta
            img = Image.open(ruta).resize((400, 300), Image.Resampling.LANCZOS)
            self.img_preview = ImageTk.PhotoImage(img)
            self.lbl_imagen.config(image=self.img_preview, text="")

    def grabar_accion(self):
        nombre = self.entry_nombre.get().strip()
        desc = self.text_desc.get("1.0", tk.END).strip()
        
        if not nombre:
            messagebox.showwarning("Atención", "El nombre de la enfermedad es obligatorio.", parent=self.root)
            return

        nombre_imagen = None
        
        if self.ruta_img_seleccionada:
            nombre_imagen = os.path.basename(self.ruta_img_seleccionada) 
            ruta_destino = os.path.join(self.assets_dir, nombre_imagen)
            
            try:
                if self.ruta_img_seleccionada != ruta_destino:
                    shutil.copy(self.ruta_img_seleccionada, ruta_destino)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo copiar la imagen a assets: {e}", parent=self.root)
                return

        accion_realizada = self.accion_actual

        if accion_realizada == 'NUEVO':
            exito = insertar_registro(nombre, desc, nombre_imagen)
            mensaje = "¡El registro se ha guardado correctamente!"
        elif accion_realizada == 'MODIFICAR':
            exito = actualizar_registro(self.id_actual, nombre, desc, nombre_imagen)
            mensaje = "¡El registro se ha actualizado correctamente!"
        
        if exito:
            messagebox.showinfo("Éxito", mensaje, parent=self.root)
            
            self.accion_actual = None
            self.configurar_estado_botones(editando=False)
            
            if accion_realizada == 'NUEVO':
                self.ir_final()
            else:
                img_final = nombre_imagen if nombre_imagen else (self.registro_actual[3] if self.registro_actual else None)
                self.mostrar_registro((self.id_actual, nombre, desc, img_final))
        else:
            messagebox.showerror("Error BD", "Hubo un problema al comunicarse con la base de datos.", parent=self.root)

    def cancelar_accion(self):
        self.accion_actual = None
        self.ruta_img_seleccionada = None
        
        self.configurar_estado_botones(editando=False)
        self.mostrar_registro(self.registro_actual)

    def abrir_consulta(self):
        """Delega la creación de la ventana al nuevo módulo y le pasa la función mostrar_registro."""
        abrir_ventana_consulta(self.root, self.w, self.h, self.mostrar_registro)

    def ir_inicio(self): self.mostrar_registro(obtener_primer_registro())
    def ir_final(self): self.mostrar_registro(obtener_ultimo_registro())
    def ir_siguiente(self): self.mostrar_registro(obtener_siguiente_registro(self.id_actual)) if self.id_actual else None
    def ir_anterior(self): self.mostrar_registro(obtener_anterior_registro(self.id_actual)) if self.id_actual else None
    
    def no_hacer_nada(self): pass
    
    def salir(self):
        self.al_cerrar_callback() if self.al_cerrar_callback else self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PantallaEnfermedades(root)
    root.mainloop()