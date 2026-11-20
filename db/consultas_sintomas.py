from db.conexion import obtener_conexion

def obtener_primer_registro():
    conexion = obtener_conexion()
    if not conexion: return None
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM sintoma ORDER BY id_sintoma ASC LIMIT 1")
        return cursor.fetchone()
    finally:
        if conexion: conexion.close()

def obtener_ultimo_registro():
    conexion = obtener_conexion()
    if not conexion: return None
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM sintoma ORDER BY id_sintoma DESC LIMIT 1")
        return cursor.fetchone()
    finally:
        if conexion: conexion.close()

def obtener_siguiente_registro(id_actual):
    conexion = obtener_conexion()
    if not conexion: return None
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM sintoma WHERE id_sintoma > %s ORDER BY id_sintoma ASC LIMIT 1", (id_actual,))
        resultado = cursor.fetchone()
        return resultado if resultado else obtener_ultimo_registro()
    finally:
        if conexion: conexion.close()

def obtener_anterior_registro(id_actual):
    conexion = obtener_conexion()
    if not conexion: return None
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM sintoma WHERE id_sintoma < %s ORDER BY id_sintoma DESC LIMIT 1", (id_actual,))
        resultado = cursor.fetchone()
        return resultado if resultado else obtener_primer_registro()
    finally:
        if conexion: conexion.close()

def insertar_registro(nombre, imagen):
    conexion = obtener_conexion()
    if not conexion: return False
    try:
        cursor = conexion.cursor()
        # Si no hay imagen, asignamos la imagen por defecto como pide la práctica
        img_val = imagen if imagen else 'default.png'
        sql = "INSERT INTO sintoma (nombre, imagen) VALUES (%s, %s)"
        cursor.execute(sql, (nombre, img_val))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al insertar síntoma: {e}")
        return False
    finally:
        if conexion: conexion.close()

def actualizar_registro(id_sintoma, nombre, imagen):
    conexion = obtener_conexion()
    if not conexion: return False
    try:
        cursor = conexion.cursor()
        if imagen:
            sql = "UPDATE sintoma SET nombre = %s, imagen = %s WHERE id_sintoma = %s"
            cursor.execute(sql, (nombre, imagen, id_sintoma))
        else:
            # Si no cambian la imagen, conservamos la que ya tenía
            sql = "UPDATE sintoma SET nombre = %s WHERE id_sintoma = %s"
            cursor.execute(sql, (nombre, id_sintoma))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar síntoma: {e}")
        return False
    finally:
        if conexion: conexion.close()

def eliminar_registro(id_sintoma):
    conexion = obtener_conexion()
    if not conexion: return False
    try:
        cursor = conexion.cursor()
        sql = "DELETE FROM sintoma WHERE id_sintoma = %s"
        cursor.execute(sql, (id_sintoma,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar síntoma: {e}")
        return False
    finally:
        if conexion: conexion.close()

def obtener_todos_registros(busqueda=""):
    conexion = obtener_conexion()
    if not conexion: return []
    try:
        cursor = conexion.cursor()
        if busqueda:
            sql = "SELECT * FROM sintoma WHERE id_sintoma LIKE %s OR nombre LIKE %s"
            param = f"%{busqueda}%"
            cursor.execute(sql, (param, param))
        else:
            cursor.execute("SELECT * FROM sintoma")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error en consulta: {e}")
        return []
    finally:
        if conexion: conexion.close()