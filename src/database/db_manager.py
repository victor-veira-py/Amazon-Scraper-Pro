import sqlite3
import os

# Localización dinámica de la raíz del proyecto para centralizar el almacenamiento
# Dynamic location of the project root to centralize storage
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'data', 'amazon_monitor.db')


def inicializar_db():
    """
    Crea el directorio 'data' si no existe e inicializa la tabla de productos con la estructura limpia.
    Creates the 'data' directory if it does not exist and initializes the products table with a clean structure.
    """
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH))

    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    # Estructura de columnas adaptada para el almacenamiento de productos de Amazon
    # Column structure tailored for storing Amazon product data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_busqueda DATETIME DEFAULT CURRENT_TIMESTAMP,
            producto_buscado TEXT,
            tienda TEXT,
            nombre_producto TEXT,
            precio REAL,
            moneda TEXT,
            enlace_producto TEXT
        )
    ''')
    conexion.commit()
    conexion.close()
    print(f"✅ [DATABASE] Estructura lista en / Schema ready at: {DB_PATH}")


def vaciar_db_fisicamente():
    """
    ELIMINACIÓN TOTAL. Borra el archivo de la base de datos y vacía por completo la carpeta 'data'.
    TOTAL PURGE. Deletes the database file and completely empties the 'data' folder.
    """
    data_dir = os.path.dirname(DB_PATH)

    print("--- 🧹 Limpiando registros y archivos anteriores / Purging records and previous files ---")

    # 1. Borrar archivos físicos en la carpeta data / Delete physical files inside data folder
    if os.path.exists(data_dir):
        for archivo in os.listdir(data_dir):
            ruta_archivo = os.path.join(data_dir, archivo)
            if archivo != '.gitkeep' and os.path.isfile(ruta_archivo):
                try:
                    os.remove(ruta_archivo)
                    print(f"🗑️ Archivo eliminado / Deleted file: {archivo}")
                except Exception as e:
                    print(f"⚠️ No se pudo eliminar / Could not delete {archivo}: {e}")

    # 2. Reinicializar la base de datos desde cero / Reinitialize database from scratch
    inicializar_db()
    print("✅ [DATABASE] Sistema de datos reseteado con éxito / Data system successfully reset.")


def guardar_producto(nombre, precio, enlace, producto_buscado, tienda="Amazon", moneda="USD"):
    """
    Inserta un nuevo producto extraído en la base de datos relacional.
    Inserts a newly extracted product into the relational database.
    """
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO productos (producto_buscado, tienda, nombre_producto, precio, moneda, enlace_producto) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (producto_buscado, tienda, nombre, precio, moneda, enlace))

        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print(f"❌ [DATABASE] Error de inserción / Insertion error at {DB_PATH}: {e}")
        return False