# scrapers/santander.py
from .base_scraper import BaseScraper
import re

class SantanderScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            nombre_banco="Santander",
            url="https://www.santander.com.ar/personas/prestamos/personales",
            render=True   # Pedimos a ScraperAPI que renderice
        )

    def parse_tasa(self, html):
        """
        Extrae TNA, TEA y CFTEA desde el HTML devuelto por ScraperAPI.
        """
        # Normalizamos saltos de línea
        text = html.replace("\n", " ").replace("\t", " ")

        # REGEX de captura
        pat_tna = re.search(r"Tasa Fija Nominal Anual[:\s]*([0-9]+,[0-9]+)", text, re.IGNORECASE)
        pat_tea = re.search(r"Tasa Efectiva Anual[:\s]*([0-9]+,[0-9]+)", text, re.IGNORECASE)
        pat_cftea = re.search(r"CFTEA[:\s]*([0-9]+,[0-9]+)", text, re.IGNORECASE)

        return {
            "Banco": self.nombre_banco,
            "TNA": float(pat_tna.group(1).replace(",", ".")) if pat_tna else None,
            "TEA": float(pat_tea.group(1).replace(",", ".")) if pat_tea else None,
            "CFTEA": float(pat_cftea.group(1).replace(",", ".")) if pat_cftea else None
        }


if __name__ == "__main__":
    import time
    scraper = SantanderScraper()
    print("🔍 Obteniendo datos desde Santander...")
    start = time.time()
    tasas = scraper.obtener_tasas()
    print("✅ Tasas extraídas:", tasas)
    print("⏱ Tiempo total:", time.time() - start)
