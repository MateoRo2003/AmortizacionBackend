import os
import json



# Forzar working directory al del script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from scrapers.bbva import BBVAScraper
from scrapers.bcra import BCRAScraper
from scrapers.bna import BNAScraperOptimized
from scrapers.galicia import GaliciaScraper
from scrapers.macro_chrome import MacroScraper
from scrapers.mp import MercadoPagoScraper
from scrapers.naranjax import NaranjaXScraper
from scrapers.santander import SantanderScraper
from scrapers.patagonia import PatagoniaScraperOptimized

scrapers_dict = {
    "Santander": SantanderScraper(),
    "BNA": BNAScraperOptimized(),
    "Macro": MacroScraper(),
    "BCRA": BCRAScraper(),
    "NaranjaX": NaranjaXScraper(),
    "BBVA": BBVAScraper(),
    "Galicia": GaliciaScraper(),
    "MercadoPago": MercadoPagoScraper(),
    "Patagonia": PatagoniaScraperOptimized()
}

def actualizar_tasas():
    tasas_actualizadas = []

    for banco, scraper in scrapers_dict.items():
        try:
            tasas = scraper.obtener_tasas()
            print(f"[DEBUG] {banco} devolvió: {tasas}")

            tna = tasas.get("TNA")
            tea = tasas.get("TEA")
            cftea = tasas.get("CFTEA")

            if not tna:
                print(f"[ERROR] No se pudo obtener TNA de {banco}")
                continue

            tasas_actualizadas.append({
                "Banco": banco,
                "TNA": tna,
                "TEA": tea,
                "CFTEA": cftea
            })

            print(f"[OK] {banco}: TNA={tna}, TEA={tea}, CFTEA={cftea}")

        except Exception as e:
            print(f"[ERROR] Falló {banco}: {e}")

    with open("tasas.json", "w", encoding="utf-8") as f:
        json.dump(tasas_actualizadas, f, indent=4, ensure_ascii=False)

    print("\nArchivo tasas.json actualizado correctamente.")

if __name__ == "__main__":
    actualizar_tasas()
