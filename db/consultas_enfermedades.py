# Archivo: db/consultas_enfermedades.py
from db.conexion import obtener_conexion

def obtener_primer_registro():
    conexion = obtener_conexion()
    if not conexion: return None
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM enfermedad ORDER BY id_enfermedad ASC LIMIT 1")
        return cursor.fetchone()
    finally:
        if conexion: conexion.close()

def obtener_ultimo_registro():
    conexion = obtener_conexion()
    if not conexion: return None
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM enfermedad ORDER BY id_enfermedad DESC LIMIT 1")
        return cursor.fetchone()
    finally:
        if conexion: conexion.close()

def obtener_siguiente_registro(id_actual):
    conexion = obtener_conexion()
    if not conexion: return None
    try:
        cursor = conexion.cursor()
        cursor.execute(f"SELECT * FROM enfermedad WHERE id_enfermedad > {id_actual} ORDER BY id_enfermedad ASC LIMIT 1")
        return cursor.fetchone()
    finally:
        if conexion: conexion.close()

def obtener_anterior_registro(id_actual):
    conexion = obtener_conexion()
    if not conexion: return None
    try:
        cursor = conexion.cursor()
        cursor.execute(f"SELECT * FROM enfermedad WHERE id_enfermedad < {id_actual} ORDER BY id_enfermedad DESC LIMIT 1")
        return cursor.fetchone()
    finally:
        if conexion: conexion.close()

def insertar_registro(nombre, descripcion, imagen_nombre):
    """Inserta una nueva enfermedad en la base de datos."""
    conexion = obtener_conexion()
    if not conexion: return False
    
    try:
        cursor = conexion.cursor()
        # El ID es autoincrementable, por lo que no lo mandamos en el INSERT
        sql = "INSERT INTO enfermedad (nombre, descripcion, imagen) VALUES (%s, %s, %s)"
        valores = (nombre, descripcion, imagen_nombre)
        
        cursor.execute(sql, valores)
        conexion.commit() # ¡Muy importante para que los cambios se guarden!
        return True
    except Exception as e:
        print(f"Error al insertar registro: {e}")
        return False
    finally:
        if conexion: conexion.close()

def actualizar_registro(id_enfermedad, nombre, descripcion, imagen_nombre):
    """Actualiza los datos de una enfermedad existente."""
    conexion = obtener_conexion()
    if not conexion: return False
    
    try:
        cursor = conexion.cursor()
        
        # Si mandamos una imagen nueva, actualizamos todo
        if imagen_nombre:
            sql = "UPDATE enfermedad SET nombre = %s, descripcion = %s, imagen = %s WHERE id_enfermedad = %s"
            valores = (nombre, descripcion, imagen_nombre, id_enfermedad)
        # Si imagen_nombre viene vacío, actualizamos solo el texto y conservamos la foto anterior
        else:
            sql = "UPDATE enfermedad SET nombre = %s, descripcion = %s WHERE id_enfermedad = %s"
            valores = (nombre, descripcion, id_enfermedad)
            
        cursor.execute(sql, valores)
        conexion.commit() 
        return True
    except Exception as e:
        print(f"Error al actualizar registro: {e}")
        return False
    finally:
        if conexion: conexion.close()

def eliminar_registro(id_enfermedad):
    """Elimina un registro de la base de datos por su ID."""
    conexion = obtener_conexion()
    if not conexion: return False
    
    try:
        cursor = conexion.cursor()
        sql = "DELETE FROM enfermedad WHERE id_enfermedad = %s"
        cursor.execute(sql, (id_enfermedad,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar registro: {e}")
        return False
    finally:
        if conexion: conexion.close()

def obtener_todos_registros(busqueda=""):
    """Obtiene todos los registros o los filtra por ID o Nombre."""
    conexion = obtener_conexion()
    if not conexion: return []
    try:
        cursor = conexion.cursor()
        if busqueda:
            # Buscamos coincidencias en ID o Nombre
            sql = "SELECT * FROM enfermedad WHERE id_enfermedad LIKE %s OR nombre LIKE %s"
            param = f"%{busqueda}%"
            cursor.execute(sql, (param, param))
        else:
            cursor.execute("SELECT * FROM enfermedad")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error en consulta: {e}")
        return []
    finally:
        if conexion: conexion.close()