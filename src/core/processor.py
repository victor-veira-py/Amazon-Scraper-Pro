import pandas as pd
import sqlite3
import os
# Importamos la ruta desde el manager para que siempre sea la misma
# We import the path from the manager so it remains centralized
from database.db_manager import DB_PATH

# Configuración de rutas absolutas para el reporte Excel
# Absolute path configuration for the Excel report
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXCEL_PATH = os.path.join(BASE_DIR, 'data', 'Reporte_Amazon_Busqueda.xlsx')


def analizar_y_exportar_limpio():
    """
    Extrae los datos de SQLite, los limpia, renombra las cabeceras a formato formal y genera el Excel expandido.
    Extracts data from SQLite, cleans it, renames headers to formal format, and generates the expanded Excel.
    """
    try:
        # 1. Validación de Base de Datos / Database Validation
        if not os.path.exists(DB_PATH):
            print(f"❌ [PROCESSOR] No existe la base de datos en / Database not found at: {DB_PATH}")
            return

        conn = sqlite3.connect(DB_PATH)

        # Seleccionamos las columnas de interés excluyendo el ID autoincremental
        # Select data columns excluding the autoincrement ID
        query = """
            SELECT fecha_busqueda, producto_buscado, tienda, nombre_producto, precio, moneda, enlace_producto 
            FROM productos 
            ORDER BY precio ASC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            print("❌ [PROCESSOR] La base de datos está vacía / Database is empty.")
            return

        # 2. Normalización de Textos / Text Normalization
        # Limitamos el nombre a 100 caracteres para evitar desbordamiento visual en Excel
        # Limit product name to 100 characters to prevent visual overflow in Excel
        df['nombre_producto'] = df['nombre_producto'].str.slice(0, 100)

        # 3. Mapeo para Encabezados Formales (Comienzan en Mayúscula y sin guiones bajos)
        # Mapping for Formal Headers (Capitalized and without underscores)
        cabeceras_formales = {
            'fecha_busqueda': 'Fecha de Búsqueda',
            'producto_buscado': 'Producto',
            'tienda': 'Tienda',
            'nombre_producto': 'Nombre del Producto',
            'precio': 'Precio',
            'moneda': 'Moneda',
            'enlace_producto': 'Enlace del Producto'
        }

        # 4. Motor de Exportación Avanzado (XlsxWriter) / Advanced Export Engine (XlsxWriter)
        with pd.ExcelWriter(EXCEL_PATH, engine='xlsxwriter') as writer:
            # Exportamos el DataFrame aplicando el renombrado de columnas
            df.rename(columns=cabeceras_formales).to_excel(writer, sheet_name='Resultados', index=False)

            workbook = writer.book
            worksheet = writer.sheets['Resultados']

            # Estilos de celda corporativos / Corporate cell styles
            formato_encabezado = workbook.add_format({
                'bold': True, 'text_wrap': True, 'valign': 'vcenter',
                'align': 'center', 'fg_color': '#1F4E78',
                'font_color': 'white', 'border': 1
            })
            formato_centrado = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

            # Aplicar estilos a los nuevos encabezados / Apply styles to new headers
            for col_num, value in enumerate(cabeceras_formales.values()):
                worksheet.write(0, col_num, value, formato_encabezado)

            # Ajuste de anchos logísticos para una legibilidad óptima
            # Width adjustment for optimal readability
            worksheet.set_column('A:A', 22, formato_centrado)  # Fecha de Búsqueda (¡Expandido para evitar solapamiento!)
            worksheet.set_column('B:B', 18, formato_centrado)  # Producto
            worksheet.set_column('C:C', 12, formato_centrado)  # Tienda
            worksheet.set_column('D:D', 65)                    # Nombre del Producto
            worksheet.set_column('E:E', 15, formato_centrado)  # Precio
            worksheet.set_column('F:F', 10, formato_centrado)  # Moneda
            worksheet.set_column('G:G', 50)                    # Enlace del Producto

        print(f"✅ [PROCESSOR] Reporte generado exitosamente en / Report successfully generated at: {EXCEL_PATH}")

    except Exception as e:
        print(f"❌ [PROCESSOR] Error en el análisis / Error during analysis: {e}")