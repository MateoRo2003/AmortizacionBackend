# scrapers/bcra_selenium.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import re
import time

class BCRAScraper:
    def __init__(self):
        self.url = "https://www.bcra.gob.ar/PublicacionesEstadisticas/Principales_variables.asp"
        self.nombre_banco = "BCRA"

    def obtener_tasas(self):
        # Configuración Chrome headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=chrome_options
        )
        driver.get(self.url)
        time.sleep(3)  # espera que cargue la página

        # Buscamos la fila de "Tasa de interés de préstamos personales"
        filas = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        tna = None
        for fila in filas:
            celdas = fila.find_elements(By.TAG_NAME, "td")
            if len(celdas) >= 3 and "Tasa de interés de préstamos personales" in celdas[0].text:
                tna_text = celdas[2].text  # normalmente la 3ra columna es el valor
                tna = float(tna_text.replace(",", "."))
                break

        driver.quit()

        # De BCRA solo tenemos TNA, podemos dejar TEA y CFTEA como None
        return {
            "Banco": self.nombre_banco,
            "TNA": tna,
            "TEA": None,
            "CFTEA": None
        }

if __name__ == "__main__":
    scraper = BCRAScraper()
    tasas = scraper.obtener_tasas()
    print(tasas)
