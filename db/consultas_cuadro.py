from db.conexion import obtener_conexion

def obtener_todas_enfermedades():
    """Para llenar el ComboBox de Enfermedades (ID y Nombre)"""
    conexion = obtener_conexion()
    if not conexion: return []
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_enfermedad, nombre FROM enfermedad ORDER BY id_enfermedad ASC")
        return cursor.fetchall()
    finally:
        if conexion: conexion.close()

def obtener_todos_sintomas():
    """Para llenar el ComboBox de Síntomas (ID y Nombre)"""
    conexion = obtener_conexion()
    if not conexion: return []
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_sintoma, nombre FROM sintoma ORDER BY id_sintoma ASC")
        return cursor.fetchall()
    finally:
        if conexion: conexion.close()

def obtener_sintomas_por_enfermedad(id_enfermedad):
    """Obtiene los síntomas ya agregados a una enfermedad y sus pesos"""
    conexion = obtener_conexion()
    if not conexion: return []
    try:
        cursor = conexion.cursor()
        sql = """
            SELECT c.id_relacion, s.id_sintoma, s.nombre, c.peso 
            FROM cuadro_patologico c
            JOIN sintoma s ON c.id_sintoma = s.id_sintoma
            WHERE c.id_enfermedad = %s
        """
        cursor.execute(sql, (id_enfermedad,))
        return cursor.fetchall()
    finally:
        if conexion: conexion.close()

def calcular_suma_total(id_enfermedad):
    """Calcula la SUMA_TOTAL actual de los pesos de una enfermedad"""
    conexion = obtener_conexion()
    if not conexion: return 0
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT SUM(peso) FROM cuadro_patologico WHERE id_enfermedad = %s", (id_enfermedad,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado[0] else 0
    finally:
        if conexion: conexion.close()

def insertar_relacion(id_enfermedad, id_sintoma, peso):
    """Inserta un nuevo síntoma a una enfermedad, calculando la SUMA_TOTAL"""
    conexion = obtener_conexion()
    if not conexion: return False, "Error de conexión."
    
    try:
        # 1. Verificar que el síntoma no esté repetido en esta enfermedad
        cursor = conexion.cursor()
        cursor.execute("SELECT id_relacion FROM cuadro_patologico WHERE id_enfermedad = %s AND id_sintoma = %s", 
                       (id_enfermedad, id_sintoma))
        if cursor.fetchone():
            return False, "Este síntoma ya está agregado a la enfermedad."

        # 2. Insertar el nuevo registro (SUMA_TOTAL se recalcula después para todos)
        sql_insert = "INSERT INTO cuadro_patologico (id_enfermedad, id_sintoma, peso, SUMA_TOTAL) VALUES (%s, %s, %s, 0)"
        cursor.execute(sql_insert, (id_enfermedad, id_sintoma, peso))
        conexion.commit()

        # 3. Recalcular y actualizar SUMA_TOTAL para todos los registros de esta enfermedad
        actualizar_suma_total(id_enfermedad)
        return True, "Síntoma agregado correctamente."
    except Exception as e:
        print(f"Error al insertar relación: {e}")
        return False, "Hubo un error en la base de datos."
    finally:
        if conexion: conexion.close()

def eliminar_relacion(id_relacion, id_enfermedad):
    """Elimina una relación y actualiza la SUMA_TOTAL de los restantes"""
    conexion = obtener_conexion()
    if not conexion: return False
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM cuadro_patologico WHERE id_relacion = %s", (id_relacion,))
        conexion.commit()
        
        # Recalcular SUMA_TOTAL
        actualizar_suma_total(id_enfermedad)
        return True
    except Exception as e:
        print(f"Error al eliminar relación: {e}")
        return False
    finally:
        if conexion: conexion.close()

def actualizar_suma_total(id_enfermedad):
    """Función interna: Suma todos los pesos de la enfermedad y los actualiza en la BD"""
    conexion = obtener_conexion()
    if not conexion: return
    try:
        cursor = conexion.cursor()
        suma_actual = calcular_suma_total(id_enfermedad)
        
        sql_update = "UPDATE cuadro_patologico SET SUMA_TOTAL = %s WHERE id_enfermedad = %s"
        cursor.execute(sql_update, (suma_actual, id_enfermedad))
        conexion.commit()
    finally:
        if conexion: conexion.close()
        
def obtener_todas_relaciones_tabla(busqueda=""):
    """Para la ventana de consulta general de todo el Cuadro Patológico"""
    conexion = obtener_conexion()
    if not conexion: return []
    try:
        cursor = conexion.cursor()
        sql = """
            SELECT c.id_relacion, e.nombre AS enfermedad, s.nombre AS sintoma, c.peso, c.SUMA_TOTAL
            FROM cuadro_patologico c
            JOIN enfermedad e ON c.id_enfermedad = e.id_enfermedad
            JOIN sintoma s ON c.id_sintoma = s.id_sintoma
        """
        if busqueda:
            sql += " WHERE e.nombre LIKE %s OR s.nombre LIKE %s ORDER BY e.id_enfermedad"
            param = f"%{busqueda}%"
            cursor.execute(sql, (param, param))
        else:
            sql += " ORDER BY e.id_enfermedad"
            cursor.execute(sql)
            
        return cursor.fetchall()
    finally:
        if conexion: conexion.close()

def ejecutar_inferencia_directa(ids_sintomas):
    """
    1. Actualiza la columna 'bandera' (1 para síntomas seleccionados, 0 para el resto).
    2. Suma los pesos por enfermedad y aplica la regla de tres contra SUMA_TOTAL.
    3. Devuelve al menos 5 enfermedades ordenadas de mayor a menor porcentaje.
    """
    conexion = obtener_conexion()
    if not conexion:
        return []
    
    try:
        cursor = conexion.cursor()
        
        # Asegurar que exista la columna 'bandera' como en las diapositivas de la profesora
        try:
            cursor.execute("ALTER TABLE cuadro_patologico ADD COLUMN bandera INT DEFAULT 0")
            conexion.commit()
        except Exception:
            pass # Si ya existe la columna, continuamos normalmente

        # 1. Reiniciar todas las banderas a 0
        cursor.execute("UPDATE cuadro_patologico SET bandera = 0")
        
        # 2. Activar bandera = 1 en los síntomas seleccionados por el usuario (Base de Hechos)
        if ids_sintomas:
            formato_ids = ",".join(["%s"] * len(ids_sintomas))
            cursor.execute(f"UPDATE cuadro_patologico SET bandera = 1 WHERE id_sintoma IN ({formato_ids})", tuple(ids_sintomas))
        
        conexion.commit()

        # 3. Sumar síntomas por enfermedad y calcular porcentaje con regla de 3
        query = """
            SELECT 
                e.id_enfermedad,
                e.nombre,
                COALESCE(SUM(CASE WHEN c.bandera = 1 THEN c.peso ELSE 0 END), 0) AS total_obtenido,
                MAX(c.SUMA_TOTAL) AS suma_total_enfermedad,
                e.imagen
            FROM enfermedad e
            LEFT JOIN cuadro_patologico c ON e.id_enfermedad = c.id_enfermedad
            GROUP BY e.id_enfermedad, e.nombre, e.imagen
        """
        cursor.execute(query)
        registros = cursor.fetchall()
        
        resultados = []
        for reg in registros:
            id_enf, nombre, total, suma_total, imagen = reg
            total = int(total) if total else 0
            suma_total = int(suma_total) if suma_total and suma_total > 0 else 100
            
            # Regla de tres: (Total * 100) / SUMA_TOTAL redondeado a entero como en la diapositiva
            porcentaje = round((total * 100) / suma_total)
            resultados.append({
                "id": id_enf,
                "nombre": nombre,
                "total": total,
                "suma_total": suma_total,
                "porcentaje": porcentaje,
                "imagen": imagen
            })
            
        # 4. Ordenar de manera descendente por porcentaje (y por puntos obtenidos en caso de empate)
        resultados.sort(key=lambda x: (x["porcentaje"], x["total"]), reverse=True)
        
        # Filtramos SOLO las enfermedades que tuvieron al menos 1 síntoma en común (> 0%)
        positivos = [r for r in resultados if r["porcentaje"] > 0]
        
        # Devolvemos solo los positivos (si hay más de 6, cortamos la lista para no saturar la pantalla)
        return positivos[:6]
            
    except Exception as e:
        print(f"Error en inferencia directa: {e}")
        return []
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()