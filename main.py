import sys
import os

# TRUCO DE RUTAS: Asegura que Python reconozca la carpeta raíz en cualquier entorno
# PATH TRICK: Ensures Python recognizes the root folder in any environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import inicializar_db, vaciar_db_fisicamente
from scrapers.amazon_scraper import ejecutar_scraper_amazon
from src.core.processor import analizar_y_exportar_limpio
from src.core.visualizer import crear_grafica_profesional
from notifications.sender import enviar_reporte_automatizado


def menu_consola():
    """
    ESPAÑOL: Interfaz de consola interactiva bilingüe para el control de operaciones del sistema.
    ENGLISH: Interactive bilingual console interface for system operations control.
    """
    # Inicializa la base de datos de forma segura al arrancar
    inicializar_db()

    while True:
        print("\n" + "=" * 65)
        print("          AMAZON SCRAPER PRO - CONTROL PANEL / PANEL DE CONTROL")
        print("=" * 65)
        print("1. 🔍 Run Clean Search (Auto-purge data) / Ejecutar Búsqueda Limpia")
        print("2. 🧹 Clear Data History (Total Reset) / Borrar Historial de Data")
        print("3. ❌ Exit Program / Salir del Programa")
        print("=" * 65)

        opcion = input("👉 Select an option / Seleccione una opción (1-3): ").strip()

        if opcion == "1":
            # Ejecuta la limpieza inicial automática antes de la búsqueda
            vaciar_db_fisicamente()

            print("\n" + "-" * 50)
            termino = input(
                "📦 What product do you want to search for on Amazon?\n   ¿Qué producto deseas buscar hoy en Amazon?: ").strip()
            print("-" * 50)

            if termino:
                ejecutar_scraper_amazon(termino)
                print("\n📊 Generating reports and data analysis / Generando reportes y análisis de datos...")
                analizar_y_exportar_limpio()
                crear_grafica_profesional()
                enviar_reporte_automatizado()
                print("\n🎉 PROCESS COMPLETED SUCCESSFULLY! / ¡PROCESO COMPLETADO EXITOSAMENTE!")
            else:
                print("⚠️ Invalid search term / No ingresaste un término de búsqueda válido.")

        elif opcion == "2":
            print("\n⚠️ WARNING / ADVERTENCIA:")
            confirmar = input(
                "   Are you sure you want to delete ALL data? (y/n)\n   ¿Está seguro de borrar TODA la data? (s/n): ").lower().strip()
            if confirmar in ['s', 'y']:
                vaciar_db_fisicamente()
            else:
                print("❌ Operation canceled / Operación cancelada.")

        elif opcion == "3":
            print("\n👋 Exiting system. Goodbye, programmer! / Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print("❌ Invalid option. Try again / Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    menu_consola()