# scrapers/bna_optimized.py
from .base_scraper import BaseScraper
import re
import requests
import time

class BNAScraperOptimized(BaseScraper):
    def __init__(self):
        super().__init__(
            nombre_banco="Banco Nación",
            url="https://www.bna.com.ar/home/informacionalusuariofinanciero",
            render=False
        )

    def parse_tasa(self, html):
        # Buscamos directamente con regex, sin usar BeautifulSoup
        tna_match = re.search(r"T\.N\.A\.\s*\(30 días\)\s*=\s*([0-9]+,[0-9]+)%", html, re.IGNORECASE)
        tea_match = re.search(r"T\.E\.A\.\s*=\s*([0-9]+,[0-9]+)%", html, re.IGNORECASE)

        return {
            "Banco": self.nombre_banco,
            "TNA": float(tna_match.group(1).replace(",", ".")) if tna_match else None,
            "TEA": float(tea_match.group(1).replace(",", ".")) if tea_match else None,
            "CFTEA": None
        }

    def obtener_tasas(self):
        # Request directo, sin render de JS
        response = requests.get(self.url, timeout=5)
        response.raise_for_status()
        html = response.text
        return self.parse_tasa(html)

if __name__ == "__main__":
    scraper = BNAScraperOptimized()
    print("🔍 Obteniendo datos desde Banco Nación...")
    start_time = time.time()
    tasas = scraper.obtener_tasas()
    end_time = time.time()
    print("✅ Tasas extraídas:")
    print(tasas)
    print(f"⏱ Tiempo total para obtener tasas: {end_time - start_time:.2f} segundos")
