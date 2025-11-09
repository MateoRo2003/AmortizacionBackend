# scrapers/macro_chrome_optimized.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re

class MacroScraper:
    def __init__(self):
        self.nombre_banco = "Macro"
        self.url = "https://sacatuprestamo.macro.com.ar/"

    def obtener_tasas(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--log-level=3")
        # Desactivar recursos que no necesitamos
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-fonts")

        service = Service(ChromeDriverManager().install())

        with webdriver.Chrome(service=service, options=chrome_options) as driver:
            driver.get(self.url)

            try:
                # Espera máxima 5s (antes 10s) solo al contenedor de tasas
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[contains(text(),'TNA') or contains(text(),'TEA')]")
                    )
                )
                # Extraemos solo el texto del contenedor encontrado
                text = element.text
                if not text:
                    # fallback al body
                    text = driver.find_element(By.TAG_NAME, "body").text
            except:
                text = driver.find_element(By.TAG_NAME, "body").text

            # Regex para extraer tasas
            pat_tna = re.search(r"TNA.*?([0-9]+,[0-9]+)%", text)
            pat_tea = re.search(r"TEA.*?([0-9]+,[0-9]+)%", text)
            pat_cftea = re.search(r"CFTEA.*?([0-9]+,[0-9]+)%", text)

            return {
                "Banco": self.nombre_banco,
                "TNA": float(pat_tna.group(1).replace(",", ".")) if pat_tna else None,
                "TEA": float(pat_tea.group(1).replace(",", ".")) if pat_tea else None,
                "CFTEA": float(pat_cftea.group(1).replace(",", ".")) if pat_cftea else None
            }

if __name__ == "__main__":
    import time
    scraper = MacroScraper()
    start_time = time.time()
    tasas = scraper.obtener_tasas()
    end_time = time.time()
    print("✅ Tasas extraídas:", tasas)
    print(f"⏱ Tiempo total: {end_time - start_time:.2f} segundos")
