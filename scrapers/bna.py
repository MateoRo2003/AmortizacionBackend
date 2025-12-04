import requests
import re

class BNADestinoLibreScraper:
    def __init__(self):
        self.nombre_banco = "Banco Nación"
        self.url = "https://www.bna.com.ar/Personas/naciondestinolibre"

    def parse_tasas(self, html):
        # 1) Encontramos el bloque SOLO de "no adhieran"
        bloque_regex = (
            r"Para usuarios que no adhieran.*?Tasa fija(.*?)Calculado para"
        )

        bloque = re.search(bloque_regex, html, re.DOTALL | re.IGNORECASE)

        if not bloque:
            return {
                "Banco": self.nombre_banco,
                "TNA": None,
                "TEA": None,
                "CFT_TNA": None,
                "CFT_TEA": None
            }

        bloque_texto = bloque.group(1)

        # 2) Sacamos SOLO los porcentajes dentro de ese bloque
        valores = re.findall(r"(\d{1,3},\d{1,2})%", bloque_texto)

        if len(valores) < 4:
            return {
                "Banco": self.nombre_banco,
                "TNA": None,
                "TEA": None,
                "CFT_TNA": None,
                "CFT_TEA": None
            }

        return {
            "Banco": self.nombre_banco,
            "TNA": float(valores[0].replace(",", ".")),
            "TEA": float(valores[1].replace(",", ".")),
            "CFT_TNA": float(valores[2].replace(",", ".")),
            "CFT_TEA": float(valores[3].replace(",", "."))
        }

    def obtener_tasas(self):
        response = requests.get(self.url, timeout=10)
        response.raise_for_status()
        html = response.text
        return self.parse_tasas(html)


if __name__ == "__main__":
    scraper = BNADestinoLibreScraper()
    print("🔍 Obteniendo datos Banco Nación - Destino Libre...")
    tasas = scraper.obtener_tasas()
    print("✅ Tasas extraídas:")
    print(tasas)
