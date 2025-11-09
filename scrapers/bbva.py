# scrapers/bbva.py
from .base_scraper import BaseScraper
import requests
import re

class BBVAScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            nombre_banco="BBVA Argentina",
            url="https://www.bbva.com.ar/prestamos-en-el-acto.html",
            render=False
        )

    def parse_tasa(self, html):
        # no usamos BeautifulSoup, solo regex sobre el HTML crudo
        text = html

        # Buscamos TNA, TEA y CFTEA
        pat_tna = re.search(r"Tasa\s*Nominal\s*Anual[:\s]*([0-9]+(?:,[0-9]+)?)%", text, re.IGNORECASE)
        pat_tea = re.search(r"Tasa\s*Efectiva\s*Anual[:\s]*([0-9]+(?:,[0-9]+)?)%", text, re.IGNORECASE)
        pat_cftea = re.search(r"CFTEA[:\s]*([0-9]+(?:,[0-9]+)?)%", text, re.IGNORECASE)

        return {
            "Banco": self.nombre_banco,
            "TNA": float(pat_tna.group(1).replace(",", ".")) if pat_tna else None,
            "TEA": float(pat_tea.group(1).replace(",", ".")) if pat_tea else None,
            "CFTEA": float(pat_cftea.group(1).replace(",", ".")) if pat_cftea else None
        }

    def obtener_tasas(self):
        # petición HTTP directa
        response = requests.get(self.url, timeout=5)
        response.raise_for_status()
        return self.parse_tasa(response.text)


if __name__ == "__main__":
    import time
    scraper = BBVAScraper()
    print("🔍 Obteniendo datos desde BBVA Argentina…")
    start_time = time.time()
    tasas = scraper.obtener_tasas()
    end_time = time.time()
    print("✅ Tasas extraídas:")
    print(tasas)
    print(f"⏱ Tiempo total para obtener tasas: {end_time - start_time:.2f} segundos")
