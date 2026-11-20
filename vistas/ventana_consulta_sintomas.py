import tkinter as tk
from tkinter import ttk
from db.consultas_sintomas import obtener_todos_registros

def abrir_ventana_consulta_sintomas(root, w, h, callback_seleccion):
    ventana_consulta = tk.Toplevel(root)
    ventana_consulta.title("Consulta de Síntomas")
    
    ancho_ventana = 700
    alto_ventana = 450
    x_pos = int((w / 2) - (ancho_ventana / 2))
    y_pos = int((h / 2) - (alto_ventana / 2))
    
    ventana_consulta.geometry(f"{ancho_ventana}x{alto_ventana}+{x_pos}+{y_pos}")
    ventana_consulta.configure(bg="#f8fafc")
    ventana_consulta.transient(root)
    ventana_consulta.grab_set()

    frame_top = tk.Frame(ventana_consulta, bg="#f8fafc")
    frame_top.pack(pady=15, fill="x", padx=20)

    tk.Label(frame_top, text="Buscar (ID o Nombre):", bg="#f8fafc", font=("Segoe UI", 12, "bold"), fg="#1a365d").pack(side="left")
    entry_buscar = tk.Entry(frame_top, font=("Segoe UI", 12), relief="solid", borderwidth=1)
    entry_buscar.pack(side="left", padx=10, fill="x", expand=True)
    
    btn_buscar = tk.Button(frame_top, text=" Buscar ", font=("Segoe UI", 10, "bold"), bg="#f59e0b", fg="white", cursor="hand2")
    btn_buscar.pack(side="left")

    frame_tabla = tk.Frame(ventana_consulta)
    frame_tabla.pack(fill="both", expand=True, padx=20, pady=(0, 10))

    scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
    scroll_y.pack(side="right", fill="y")

    columnas = ("ID", "Nombre", "Imagen")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", yscrollcommand=scroll_y.set)
    
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Síntoma")
    tabla.heading("Imagen", text="Archivo")

    tabla.column("ID", width=50, anchor="center")
    tabla.column("Nombre", width=450)
    tabla.column("Imagen", width=150, anchor="center")

    tabla.pack(side="left", fill="both", expand=True)
    scroll_y.config(command=tabla.yview)

    def cargar_datos(filtro=""):
        for row in tabla.get_children():
            tabla.delete(row)
        registros = obtener_todos_registros(filtro)
        for reg in registros:
            img_val = reg[2] if reg[2] else "default.png"
            tabla.insert("", "end", values=(reg[0], reg[1], img_val))

    def seleccionar_registro(event):
        item = tabla.focus()
        if not item: return
        valores = tabla.item(item, "values")
        id_seleccionado = int(valores[0])
        regs = obtener_todos_registros(str(id_seleccionado))
        for r in regs:
            if r[0] == id_seleccionado:
                callback_seleccion(r)
                ventana_consulta.destroy() 
                break

    btn_buscar.config(command=lambda: cargar_datos(entry_buscar.get().strip()))
    tabla.bind("<Double-1>", seleccionar_registro) 
    cargar_datos()

    tk.Label(ventana_consulta, text="* Haz doble clic en una fila para ver el registro completo.", 
             bg="#f8fafc", fg="#475569", font=("Segoe UI", 10, "italic")).pack(pady=(0,15))