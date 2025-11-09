# scrapers/patagonia_optimized.py
from .base_scraper import BaseScraper
import re
import requests
import time

class PatagoniaScraperOptimized(BaseScraper):
    def __init__(self):
        super().__init__(
            nombre_banco="Banco Patagonia",
            url="https://www.bancopatagonia.com.ar/personas/prestamos/patagonia-simple.php",
            render=False
        )

    def parse_tasa(self, html):
        # TNA formato: "TASA NOMINAL ANUAL:120%"
        tna_match = re.search(
            r"TASA\s+NOMINAL\s+ANUAL\s*[:\-]?\s*([0-9]+(?:,[0-9]+)?)%",
            html,
            re.IGNORECASE
        )

        # TEA formato: "TASA EFECTIVA ANUAL: 214,07%"
        tea_match = re.search(
            r"TASA\s+EFECTIVA\s+ANUAL\s*[:\-]?\s*([0-9]+(?:,[0-9]+)?)%",
            html,
            re.IGNORECASE
        )

        # CFTEA con IVA formato: "292,22% (con IVA)"
        cftea_match = re.search(
            r"([0-9]+(?:,[0-9]+)?)%\s*\(con\s*IVA\)",
            html,
            re.IGNORECASE
        )

        return {
            "Banco": self.nombre_banco,
            "TNA": float(tna_match.group(1).replace(",", ".")) if tna_match else None,
            "TEA": float(tea_match.group(1).replace(",", ".")) if tea_match else None,
            "CFTEA": float(cftea_match.group(1).replace(",", ".")) if cftea_match else None
        }

    def obtener_tasas(self):
        response = requests.get(self.url, timeout=10)
        response.raise_for_status()
        html = response.text
        return self.parse_tasa(html)


if __name__ == "__main__":
    scraper = PatagoniaScraperOptimized()
    print("🔍 Obteniendo datos desde Banco Patagonia...")
    start_time = time.time()
    tasas = scraper.obtener_tasas()
    end_time = time.time()
    print("✅ Tasas extraídas:")
    print(tasas)
    print(f"⏱ Tiempo total: {end_time - start_time:.2f} segundos")
