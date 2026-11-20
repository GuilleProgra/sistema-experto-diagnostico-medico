# Sistema Experto de Diagnóstico Médico

Aplicación de escritorio desarrollada en **Python** y **Tkinter** con base de datos **MySQL** (`sistema_experto`) para la gestión de enfermedades, síntomas y cuadros patológicos con pesos e inferencia de diagnóstico.

## Características principales
- **Motor de inferencia y cuadros patológicos:** Asociación de síntomas a enfermedades con pesos y cálculo de puntuación acumulada (`cuadro_patologico`).
- **Gestión CRUD:** Administración de enfermedades, síntomas y relaciones desde la interfaz gráfica.
- **Búsqueda y navegación:** Filtrado en tiempo real, pantallas dedicadas para consulta, explicación y diagnóstico.
- **Persistencia en MySQL:** Script de base de datos incluido en `db/sistema_experto.sql`.

## Tecnologías utilizadas
- **Lenguaje:** Python
- **Interfaz gráfica:** Tkinter
- **Base de datos:** MySQL (`sistema_experto`)

## Estructura del proyecto
- `db/`: conexión (`conexion.py`), consultas (`consultas_cuadro.py`, `consultas_enfermedades.py`, `consultas_sintomas.py`) y script de base de datos (`sistema_experto.sql`).
- `vistas/`: pantallas e interfaz de usuario en Tkinter.
- `assets/`: imágenes e íconos utilizados por la aplicación.

## Configuración rápida
1. Crea y carga la base de datos ejecutando `db/sistema_experto.sql` en tu servidor MySQL.
2. Configura los parámetros de conexión en `db/conexion.py`.
3. Ejecuta la aplicación desde la raíz del proyecto con Python.
