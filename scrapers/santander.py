# scrapers/santander.py
from .base_scraper import BaseScraper
import requests
import re

class SantanderScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            nombre_banco="Santander",
            url="https://www.santander.com.ar/personas/prestamos/personales",
            render=False
        )

    def parse_tasa(self, html):
        # no usamos BeautifulSoup, solo regex sobre el HTML crudo
        text = html

        tna = re.search(r"Tasa Fija Nominal Anual[:\s]*([0-9]+,[0-9]+)", text)
        tea = re.search(r"Tasa Efectiva Anual[:\s]*([0-9]+,[0-9]+)", text)
        cftea = re.search(r"CFTEA[:\s]*([0-9]+,[0-9]+)", text)

        return {
            "Banco": self.nombre_banco,
            "TNA": float(tna.group(1).replace(",", ".")) if tna else None,
            "TEA": float(tea.group(1).replace(",", ".")) if tea else None,
            "CFTEA": float(cftea.group(1).replace(",", ".")) if cftea else None
        }

    def obtener_tasas(self):
        response = requests.get(self.url, timeout=5)
        response.raise_for_status()
        return self.parse_tasa(response.text)

if __name__ == "__main__":
    import time
    scraper = SantanderScraper()
    print("🔍 Obteniendo datos desde Santander...")
    start_time = time.time()
    try:
        tasas = scraper.obtener_tasas()
        print("✅ Tasas extraídas:")
        print(tasas)
    except Exception as e:
        print("❌ Error:", e)
    end_time = time.time()
    print(f"⏱ Tiempo total para obtener tasas: {end_time - start_time:.2f} segundos")
