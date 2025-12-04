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
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        driver.get(self.url)
        time.sleep(5)

        # Extraigo TODO el texto visible
        text = driver.find_element("tag name", "body").text
        driver.quit()

        # Busco SOLO el bloque de "SERVICIO PLUS GOLD y PLUS"
        bloque = re.search(
            r"Para clientes que tengan contratado el\s+SERVICIO\s+PLUS\s+GOLD\s+y\s+PLUS\s*:(.*?)(?:Para clientes que tengan|$)",
            text,
            re.IGNORECASE | re.DOTALL
        )

        if not bloque:
            print("❌ No se encontró el bloque 'SERVICIO PLUS GOLD y PLUS'")
            return None

        bloque_texto = bloque.group(1)

        # número flexible (98% / 156,56%)
        num = r"([0-9]+(?:,[0-9]+)?)%"

        # Extraer SOLO estos 3 datos
        pat_tna = re.search(r"TNA[:\s]*" + num, bloque_texto, re.IGNORECASE)
        pat_tea = re.search(r"TEA[:\s]*" + num, bloque_texto, re.IGNORECASE)
        pat_cftea = re.search(r"CFTEA[:\s]*" + num, bloque_texto, re.IGNORECASE)

        # Convertir a float
        def to_float(val):
            return float(val.replace(",", ".")) if val else None

        tna = to_float(pat_tna.group(1)) if pat_tna else None
        tea = to_float(pat_tea.group(1)) if pat_tea else None
        cftea = to_float(pat_cftea.group(1)) if pat_cftea else None

        return {
            "Banco": self.nombre_banco,
            "TNA": tna,
            "TEA": tea,
            "CFTEA": cftea
        }


if __name__ == "__main__":
    start = time.time()
    scraper = GaliciaScraper()
    tasas = scraper.obtener_tasas()
    end = time.time()

    print("✅ Tasas extraídas desde Banco Galicia:", tasas)
    print(f"⏱ Tiempo total: {end - start:.2f} segundos")
