import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os
# Importamos la ruta centralizada de la DB
# We import the centralized DB path
from database.db_manager import DB_PATH

# Configuración de rutas absolutas para la gráfica PNG
# Absolute path configuration for the PNG chart
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GRAFICA_PATH = os.path.join(BASE_DIR, 'data', 'grafica_precios_amazon.png')


def crear_grafica_profesional():
    """
    ESPAÑOL: Genera un gráfico de barras horizontales con el Top 10 de productos ordenados de menor a mayor precio.
    ENGLISH: Generates a horizontal bar chart featuring the Top 10 products sorted from lowest to highest price.
    """
    try:
        # 1. Carga y Validación / Loading and Validation
        if not os.path.exists(DB_PATH):
            print(f"❌ [VISUALIZER] No se encontró la DB en / Database not found at: {DB_PATH}")
            return

        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT nombre_producto, precio FROM productos", conn)
        conn.close()

        if df.empty:
            print("❌ [VISUALIZER] Base de datos vacía / Empty database.")
            return

        # 2. Pipeline de Limpieza Universal / Universal Cleaning Pipeline
        # Eliminamos duplicados exactos para no ensuciar el Top
        # Remove exact duplicates to keep the Top selection clean
        df = df.drop_duplicates(subset=['nombre_producto'])

        # Ordenamos ascendentemente y extraemos los 10 registros más representativos
        # Sort ascending and extract the top 10 most relevant records
        df = df.sort_values(by='precio', ascending=True).tail(10)

        # Formateo estético del string para que encaje en el eje vertical
        # Aesthetic string formatting to fit the vertical axis labels properly
        df['nombre_corto'] = df['nombre_producto'].str.slice(0, 35) + "..."

        # 3. Renderizado del Gráfico (Estilo Ejecutivo) / Chart Rendering (Executive Style)
        plt.figure(figsize=(12, 8))
        barras = plt.barh(df['nombre_corto'], df['precio'], color='#1F4E78', edgecolor='black')

        # Configuración de etiquetas y títulos / Labels and titles configuration
        plt.xlabel('Precio en USD ($) / Price in USD ($)', fontsize=12, fontweight='bold')
        plt.title('Comparativa de Precios - Amazon / Price Comparison - Amazon', fontsize=16, pad=25, fontweight='bold')
        plt.grid(axis='x', linestyle='--', alpha=0.6)

        # Inserción dinámica de etiquetas de precio sobre cada barra
        # Dynamic price label insertion on top of each bar
        for barra in barras:
            width = barra.get_width()
            plt.text(width + (width * 0.02), barra.get_y() + barra.get_height() / 2,
                     f'${width:,.2f}', va='center', fontweight='bold', fontsize=10)

        # 4. Guardado en Alta Resolución / High Resolution Export
        plt.tight_layout()
        plt.savefig(GRAFICA_PATH, dpi=300)
        plt.close() # Liberamos memoria de matplotlib / Free matplotlib memory

        print(f"✅ [VISUALIZER] Gráfica generada exitosamente en / Chart successfully generated at: {GRAFICA_PATH}")

    except Exception as e:
        print(f"❌ [VISUALIZER] Error al crear gráfica / Error creating chart: {e}")