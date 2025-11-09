# scrapers/base_scraper.py
from utils.scraper_api import get_html_with_scraperapi

class BaseScraper:
    def __init__(self, nombre_banco, url, render=False):
        self.nombre_banco = nombre_banco
        self.url = url
        self.render = render

    def fetch_html(self):
        html = get_html_with_scraperapi(self.url, self.render)
        if not html:
            print(f"[ERROR] {self.nombre_banco}: no se pudo obtener HTML.")
        return html

    def parse_tasa(self, html):
        """Método que debe sobrescribir cada banco."""
        raise NotImplementedError("Debes implementar parse_tasa en la subclase")

    def obtener_tasas(self):
        html = self.fetch_html()
        if not html:
            return {"Banco": self.nombre_banco, "TNA": None, "TEA": None, "CFTEA": None}
        try:
            return self.parse_tasa(html)
        except Exception as e:
            print(f"[ERROR] {self.nombre_banco}: error al parsear tasas ({e})")
            return {"Banco": self.nombre_banco, "TNA": None, "TEA": None, "CFTEA": None}
