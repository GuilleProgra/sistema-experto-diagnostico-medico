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

class PantallaMenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Principal - SE")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", self.salir_atajo)
        
        self.w = self.root.winfo_screenwidth()
        self.h = self.root.winfo_screenheight()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        rutas = {
            "fondo": os.path.join(base_dir, "assets", "fondo.jpg"),
            "experto": os.path.join(base_dir, "assets", "experto.png"),
            "usuario": os.path.join(base_dir, "assets", "usuario.png"),
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

        # Título
        self.canvas.create_text(self.w // 2, self.h * 0.12, text="MENÚ PRINCIPAL", 
                                font=("Helvetica", 55, "bold"), fill="#1a365d")

        # ==========================================
        # PANEL DERECHO: CUADRO DE DESCRIPCIÓN
        # ==========================================
        x_cuadro = self.w * 0.52
        y_cuadro_inicio = self.h * 0.30
        y_cuadro_fin = self.h * 0.80
        ancho_cuadro = self.w * 0.90
        
        # Dibujar un recuadro blanco semitransparente
        self.canvas.create_rectangle(x_cuadro, y_cuadro_inicio, ancho_cuadro, y_cuadro_fin, 
                                     outline="#1a365d", width=3, fill="#f8fafc")
        
        texto_defecto = "Pasa el ratón sobre una opción de la\nizquierda para ver su descripción aquí."
        
        # AJUSTE: Letra más pequeña (18) y "width=700" para que el texto abarque a lo ancho y no se amontone
        self.texto_descripcion = self.canvas.create_text(
            (x_cuadro + ancho_cuadro) / 2, (y_cuadro_inicio + y_cuadro_fin) / 2, 
            text=texto_defecto, font=("Segoe UI", 18, "italic"), fill="#475569", justify="center", width=700
        )

        # ==========================================
        # PANEL IZQUIERDO: BOTONES E ICONOS
        # ==========================================
        self.iconos = {}
        for clave in ["experto", "usuario", "salir"]:
            ruta = rutas[clave]
            if os.path.exists(ruta):
                img = Image.open(ruta).resize((40, 40), Image.Resampling.LANCZOS)
                self.iconos[clave] = ImageTk.PhotoImage(img)
            else:
                self.iconos[clave] = None

        btn_style = {
            "font": ("Segoe UI", 16, "bold"), "bg": "#ffffff", "fg": "#1a365d",
            "activebackground": "#f1f5f9", "activeforeground": "#1a365d",
            "cursor": "hand2", "relief": "solid", "borderwidth": 2
        }

        # Coordenada X para los botones
        x_botones = self.w * 0.25

        # 1. Botón Interfaz Experto
        self.btn_experto = tk.Button(self.root, command=self.abrir_experto, text=" INTERFAZ EXPERTO", **btn_style)
        if self.iconos["experto"]:
            self.btn_experto.config(image=self.iconos["experto"], compound="left")
        # AJUSTE: Forzamos el tamaño a 400x75 directo en el Canvas
        self.canvas.create_window(x_botones, self.h * 0.40, window=self.btn_experto, anchor="center", width=400, height=75)

        # 2. Botón Interfaz Usuario
        self.btn_usuario = tk.Button(self.root, command=self.abrir_usuario, text=" INTERFAZ USUARIO", **btn_style)
        if self.iconos["usuario"]:
            self.btn_usuario.config(image=self.iconos["usuario"], compound="left")
        # AJUSTE: Forzamos el tamaño a 400x75
        self.canvas.create_window(x_botones, self.h * 0.55, window=self.btn_usuario, anchor="center", width=400, height=75)

        # 3. Botón Salir (Regresar)
        self.btn_salir = tk.Button(self.root, command=self.salir, text=" REGRESAR", **btn_style)
        if self.iconos["salir"]:
            self.btn_salir.config(image=self.iconos["salir"], compound="left")
        # AJUSTE: Forzamos el tamaño a 400x75
        self.canvas.create_window(x_botones, self.h * 0.70, window=self.btn_salir, anchor="center", width=400, height=75)

        # ==========================================
        # LÓGICA DE HOVER (Ratón por encima)
        # ==========================================
        desc_experto = "MÓDULO DE EXPERTO\n\nPermite al ingeniero de conocimiento o médico gestionar la base de reglas, agregar nuevas enfermedades, modificar los síntomas y ajustar el motor de inferencia."
        desc_usuario = "MÓDULO DE USUARIO\n\nDiseñado para el paciente. Permite introducir síntomas, responder al cuestionario del sistema y recibir un diagnóstico probabilístico."
        desc_salir = "REGRESAR\n\nCierra el menú principal y regresa a la pantalla de bienvenida del sistema."

        self.btn_experto.bind("<Enter>", lambda e: self.actualizar_texto(desc_experto, normal=True))
        self.btn_experto.bind("<Leave>", lambda e: self.actualizar_texto(texto_defecto, normal=False))

        self.btn_usuario.bind("<Enter>", lambda e: self.actualizar_texto(desc_usuario, normal=True))
        self.btn_usuario.bind("<Leave>", lambda e: self.actualizar_texto(texto_defecto, normal=False))

        self.btn_salir.bind("<Enter>", lambda e: self.actualizar_texto(desc_salir, normal=True))
        self.btn_salir.bind("<Leave>", lambda e: self.actualizar_texto(texto_defecto, normal=False))

    # Métodos de interactividad
    def actualizar_texto(self, texto, normal):
        if normal:
            # AJUSTE: Letra más pequeña (16) para descripciones largas
            self.canvas.itemconfig(self.texto_descripcion, text=texto, font=("Segoe UI", 16, "bold"), fill="#1a365d")
        else:
            self.canvas.itemconfig(self.texto_descripcion, text=texto, font=("Segoe UI", 18, "italic"), fill="#475569")

    def abrir_experto(self):
        # Crear ventana secundaria (Toplevel)
        ventana_pass = tk.Toplevel(self.root)
        ventana_pass.title("Plantilla_CONTRASEÑA")
        
        # Tamaño de la ventana emergente
        ancho_ventana = 350
        alto_ventana = 200
        
        # Calcular posición para centrarla en la pantalla
        x = (self.w // 2) - (ancho_ventana // 2)
        y = (self.h // 2) - (alto_ventana // 2)
        ventana_pass.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        
        # Evitar que se cambie el tamaño y hacerla modal (bloquea la principal)
        ventana_pass.resizable(False, False)
        ventana_pass.transient(self.root)
        ventana_pass.grab_set()

        # Configurar colores para que combine con tu diseño
        ventana_pass.configure(bg="#f8fafc")
        
        # Etiqueta de instrucción
        lbl_instruccion = tk.Label(ventana_pass, text="Introduzca la contraseña...", 
                                   bg="#f8fafc", fg="#1a365d", font=("Segoe UI", 10))
        lbl_instruccion.pack(pady=(15, 10), anchor="w", padx=20)

        # Contenedor para el Entry y su etiqueta
        frame_input = tk.Frame(ventana_pass, bg="#f8fafc")
        frame_input.pack(pady=5)

        lbl_pass = tk.Label(frame_input, text="Contraseña:", bg="#f8fafc", 
                            fg="#1a365d", font=("Segoe UI", 10, "bold"))
        lbl_pass.pack(side="left", padx=5)

        # Entry con show="*" para ocultar el texto
        entry_pass = tk.Entry(frame_input, show="*", font=("Segoe UI", 10), width=20)
        entry_pass.pack(side="left", padx=5)
        entry_pass.focus() # Poner el cursor automáticamente aquí

        # Funciones de los botones Aceptar y Cancelar
        def verificar(event=None):
            password = entry_pass.get()
            if password == "experto123": 
                # 1. Cierra la ventanita de la contraseña
                ventana_pass.destroy()
                
                # 2. Importamos tu nueva pantalla (Asegúrate de que el archivo se llame PantallaExperto.py)
                from PantallaExperto import PantallaExperto
                
                # 3. Creamos una nueva ventana sobrepuesta y la abrimos
                ventana_experto = tk.Toplevel(self.root)
                app_experto = PantallaExperto(ventana_experto)
                
            else:
                messagebox.showerror("Error", "Contraseña incorrecta. Intente de nuevo.")
                entry_pass.delete(0, tk.END)

        def cancelar():
            ventana_pass.destroy()

        # Permitir que el usuario presione 'Enter' en su teclado para aceptar
        ventana_pass.bind("<Return>", verificar)

        # Permitir que el usuario presione 'Enter' en su teclado para aceptar
        ventana_pass.bind("<Return>", verificar)

        # Contenedor para los botones
        frame_botones = tk.Frame(ventana_pass, bg="#f8fafc")
        frame_botones.pack(pady=20) 

        btn_estilo = {"font": ("Segoe UI", 10, "bold"), "bg": "#e2e8f0", 
                      "fg": "#1a365d", "cursor": "hand2", "width": 10}

        btn_aceptar = tk.Button(frame_botones, text="Aceptar", command=verificar, **btn_estilo)
        btn_aceptar.pack(side="left", padx=15, ipady=6, ipadx=5)

        btn_cancelar = tk.Button(frame_botones, text="Cancelar", command=cancelar, **btn_estilo)
        btn_cancelar.pack(side="left", padx=15, ipady=6, ipadx=5)
        

    def abrir_usuario(self):
        from PantallaUsuario import PantallaUsuario
        ventana_usuario = tk.Toplevel(self.root)
        app_usuario = PantallaUsuario(ventana_usuario)

    def salir(self):
        self.root.destroy()
        
    def salir_atajo(self, event):
        self.salir()

if __name__ == "__main__":
    root = tk.Tk()
    app = PantallaMenuPrincipal(root)
    root.mainloop()