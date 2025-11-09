# scrapers/naranjax.py
from .base_scraper import BaseScraper
import requests
import re

class NaranjaXScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            nombre_banco="Naranja X",
            url="https://www.naranjax.com/prestamos",
            render=False
        )

    def parse_tasa(self, html):
        # no usamos BeautifulSoup, solo regex sobre el HTML crudo
        text = html

        # Buscamos las tasas máximas que aparecen en el texto
        tna = re.search(r"TNA.*?([0-9]+(?:,[0-9]+)?)%", text)
        tea = re.search(r"TEA.*?([0-9]+(?:,[0-9]+)?)%", text)
        cftea = re.search(r"CFTEA.*?([0-9]+(?:,[0-9]+)?)%", text)

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
    scraper = NaranjaXScraper()
    print("🔍 Obteniendo datos desde Naranja X...")
    start_time = time.time()
    try:
        tasas = scraper.obtener_tasas()
        print("✅ Tasas extraídas:")
        print(tasas)
    except Exception as e:
        print("❌ Error:", e)
    end_time = time.time()
    print(f"⏱ Tiempo total para obtener tasas: {end_time - start_time:.2f} segundos")
