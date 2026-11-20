import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    """
    Establece y retorna la conexión a la base de datos del sistema experto.
    Si hay un error, imprime el mensaje y retorna None.
    """
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="memo_admin",
            password="memo123", # ¡No olvides poner la contraseña que creaste!
            database="sistema_experto"
        )
        
        if conexion.is_connected():
            return conexion
            
    except Error as e:
        print(f"Error al conectar a la base de datos MySQL: {e}")
        return None