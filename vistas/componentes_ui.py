import tkinter as tk
from PIL import Image, ImageTk
import os

def cargar_iconos(assets_dir):
    iconos = {}
    nombres = ["inicio", "anterior", "siguiente", "final", 
               "nuevo", "grabar", "cancelar", "editar", "borrar", "consulta", "salir"]
    for clave in nombres:
        ruta = os.path.join(assets_dir, f"{clave}.png")
        if os.path.exists(ruta):
            img = Image.open(ruta).resize((30, 30), Image.Resampling.LANCZOS)
            iconos[clave] = ImageTk.PhotoImage(img)
        else:
            iconos[clave] = None
    return iconos

def dibujar_fondo_y_titulo(canvas, w, h, assets_dir, titulo):
    try:
        img_fondo = Image.open(os.path.join(assets_dir, "fondo.jpg")).resize((w, h), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(img_fondo)
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
        canvas.bg_image = bg_image  
    except:
        canvas.config(bg="#e2e8f0")
        
    canvas.create_text(w // 2, h * 0.08, text=titulo, font=("Helvetica", 45, "bold"), fill="#1a365d")

def crear_formulario(canvas, w, h, img_vacia):
    ancho_form, alto_form = w * 0.8, h * 0.45
    x_ini, y_ini = (w - ancho_form) // 2, h * 0.15
    
    canvas.create_rectangle(x_ini, y_ini, x_ini + ancho_form, y_ini + alto_form, 
                            outline="#1a365d", width=3, fill="#f8fafc")

    lbl_style = {"bg": "#f8fafc", "fg": "#1a365d", "font": ("Segoe UI", 14, "bold")}
    entry_style = {"font": ("Segoe UI", 14), "relief": "solid", "borderwidth": 1}

    frame_inputs = tk.Frame(canvas, bg="#f8fafc")
    canvas.create_window(x_ini + 40, y_ini + 30, window=frame_inputs, anchor="nw")

    tk.Label(frame_inputs, text="ID Enfermedad:", **lbl_style).grid(row=0, column=0, sticky="w", pady=10)
    entry_id = tk.Entry(frame_inputs, **entry_style, width=10, state="normal")
    entry_id.grid(row=0, column=1, sticky="w", pady=10, padx=10)

    tk.Label(frame_inputs, text="Nombre:", **lbl_style).grid(row=1, column=0, sticky="w", pady=10)
    entry_nombre = tk.Entry(frame_inputs, **entry_style, width=40)
    entry_nombre.grid(row=1, column=1, sticky="w", pady=10, padx=10)

    tk.Label(frame_inputs, text="Descripción:", **lbl_style).grid(row=2, column=0, sticky="nw", pady=10)
    text_desc = tk.Text(frame_inputs, font=("Segoe UI", 12), relief="solid", borderwidth=1, width=47, height=8)
    text_desc.grid(row=2, column=1, sticky="w", pady=10, padx=10)

    frame_img = tk.Frame(canvas, bg="#f8fafc")
    canvas.create_window(x_ini + ancho_form - 50, y_ini + 40, window=frame_img, anchor="ne")

    lbl_imagen = tk.Label(frame_img, text="Sin Imagen", font=("Segoe UI", 12, "bold"), 
                          fg="#475569", bg="#e2e8f0", relief="solid", borderwidth=1,
                          image=img_vacia, compound="center", width=400, height=300)
    lbl_imagen.pack()
    
    return entry_id, entry_nombre, text_desc, lbl_imagen

def crear_botones_navegacion(root, canvas, w, h, iconos, comandos):
    btn_style = {"font": ("Segoe UI", 12, "bold"), "bg": "#ffffff", "fg": "#1a365d", 
                 "cursor": "hand2", "relief": "solid", "borderwidth": 2}
    nombres = ["INICIO", "ANTERIOR", "SIGUIENTE", "FINAL"]
    claves = ["inicio", "anterior", "siguiente", "final"]
    btn_w, separacion, y_pos = 200, 20, h * 0.65
    x_start = (w - ((4 * btn_w) + (3 * separacion))) // 2 + (btn_w // 2)

    # NUEVO: Diccionario para guardar los botones de navegación
    botones_nav = {} 
    
    for i in range(4):
        btn = tk.Button(root, text=f" {nombres[i]}", command=comandos[i], **btn_style)
        if iconos[claves[i]]:
            btn.config(image=iconos[claves[i]], compound="left", padx=5)
        canvas.create_window(x_start + i * (btn_w + separacion), y_pos, window=btn, width=btn_w, height=50)
        
        # NUEVO: Guardamos el botón en el diccionario
        botones_nav[nombres[i]] = btn 
        
    return botones_nav # NUEVO: Devolvemos el diccionario

def crear_botones_accion(root, canvas, w, h, iconos, comandos):
    btn_style = {"font": ("Segoe UI", 11, "bold"), "bg": "#ffffff", "fg": "#1a365d", 
                 "cursor": "hand2", "relief": "solid", "borderwidth": 2}
                 
    nombres = ["NUEVO", "GRABAR", "CANCELAR", "MODIFICAR", "BORRAR", "CONSULTA", "SALIR"]
    claves = ["nuevo", "grabar", "cancelar", "editar", "borrar", "consulta", "salir"]
    
    btn_w, separacion, y_pos = 165, 10, h * 0.78
    
    x_start = (w - ((7 * btn_w) + (6 * separacion))) // 2 + (btn_w // 2)

    botones = {} 

    for i in range(7):
        btn = tk.Button(root, text=f" {nombres[i]}", command=comandos[i], **btn_style)
        if nombres[i] == "CONSULTA":
            btn.config(bg="#f59e0b", fg="white")
        if iconos[claves[i]]:
            btn.config(image=iconos[claves[i]], compound="left", padx=5)
        canvas.create_window(x_start + i * (btn_w + separacion), y_pos, window=btn, width=btn_w, height=50)
        
        botones[nombres[i]] = btn 
        
    return botones