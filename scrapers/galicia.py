# scrapers/galicia_selenium.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
import time

class GaliciaScraper:
    def __init__(self):
        self.nombre_banco = "Banco Galicia"
        self.url = "https://www.galicia.ar/personas/prestamos/prestamo-personal"

    def obtener_tasas(self):
        # Configuración Chrome headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        # Iniciamos driver usando webdriver_manager
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        driver.get(self.url)
        time.sleep(5)  # esperar que cargue JS dinámico

        # Extraemos todo el texto visible
        text = driver.find_element("tag name", "body").text
        driver.quit()

        # Buscamos TNA, TEA y CFTEA en el texto
        pat_tna = re.search(r"Tasa\s*Nominal\s*Anual.*?([0-9]+(?:,[0-9]+)?)", text, re.IGNORECASE)
        pat_tea = re.search(r"Tasa\s*Efectiva\s*Anual.*?([0-9]+(?:,[0-9]+)?)", text, re.IGNORECASE)
        pat_cftea = re.search(r"CFTEA.*?([0-9]+(?:,[0-9]+)?)", text, re.IGNORECASE)

        return {
            "Banco": self.nombre_banco,
            "TNA": float(pat_tna.group(1).replace(",", ".")) if pat_tna else None,
            "TEA": float(pat_tea.group(1).replace(",", ".")) if pat_tea else None,
            "CFTEA": float(pat_cftea.group(1).replace(",", ".")) if pat_cftea else None
        }

if __name__ == "__main__":
    import time

    scraper = GaliciaScraper()
    start_time = time.time()  # guardamos tiempo de inicio
    tasas = scraper.obtener_tasas()
    end_time = time.time()    # guardamos tiempo de fin

    print("✅ Tasas extraídas desde Banco Galicia:", tasas)
    print(f"⏱ Tiempo total para obtener tasas: {end_time - start_time:.2f} segundos")
