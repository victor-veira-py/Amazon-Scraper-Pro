import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from database.db_manager import guardar_producto


def ejecutar_scraper_amazon(busqueda):
    """
    ESPAÑOL: Orquesta Selenium para buscar cualquier producto en Amazon y extraer los datos dinámicamente.
    ENGLISH: Orchestrates Selenium to search for any product on Amazon and extract data dynamically.
    """
    opts = Options()
    # User-Agent para emular navegación humana y reducir bloqueos
    # User-Agent to emulate human browsing and reduce blocks
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=opts)

    try:
        url = f"https://www.amazon.com/s?k={busqueda.replace(' ', '+')}"
        driver.get(url)

        print(f"\n🔍 [SCRAPER] Buscando / Searching for: '{busqueda}'...")

        # Pausa estratégica para control manual de geolocalización en el navegador
        # Strategic pause for manual geolocation control in the browser
        input("👉 Cambia la ubicación en Amazon (si es necesario) y presiona ENTER en esta consola para continuar...")

        time.sleep(3)  # Espera técnica de renderizado / Rendering technical wait

        items = driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')
        print(f"📦 [INFO] Se encontraron {len(items)} productos en la página / Found {len(items)} products on the page.")

        conteo = 0

        for item in items:
            if conteo >= 20:  # Límite de extracción / Extraction limit
                break

            try:
                # Extracción del título del producto / Product title extraction
                try:
                    nombre = item.find_element(By.CSS_SELECTOR, 'h2 span').text.strip()
                except:
                    nombre = item.find_element(By.CLASS_NAME, 'a-truncate-cut').text.strip()

                if not nombre:
                    continue

                # Extracción y limpieza del precio numérico / Price extraction and cleaning
                try:
                    precio_raw = item.find_element(By.CLASS_NAME, 'a-price-whole').text
                except:
                    try:
                        precio_raw = item.find_element(By.CLASS_NAME, 'a-offscreen').get_attribute('innerHTML')
                    except:
                        continue  # Omite si no tiene precio ejecutable / Skip if no executable price

                precio_limpio = precio_raw.replace('US$', '').replace('$', '').replace(',', '').replace('\n',
                                                                                                        '').strip()
                precio_final = float(precio_limpio)

                # Extracción del enlace directo / Direct link extraction
                try:
                    link = item.find_element(By.CSS_SELECTOR, 'h2 a').get_attribute('href')
                except:
                    link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')

                # GUARDADO CONEXO: Pasamos los argumentos exactos al db_manager
                # CONNECTED SAVE: Pass exact arguments to db_manager
                guardar_producto(nombre, precio_final, link, producto_buscado=busqueda)

                print(f"✅ [{conteo + 1}] Guardado: {nombre[:45]}... | ${precio_final}")
                conteo += 1

            except Exception:
                continue

    finally:
        driver.quit()
        print(f"🚀 [SCRAPER] Proceso terminado. Total guardados / Process finished. Total saved: {conteo}")