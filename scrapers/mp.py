# scrapers/mercado_pago.py
class MercadoPagoScraper:
    def __init__(self):
        self.nombre_banco = "Mercado Pago"

    def obtener_tasas(self):
        # Datos constantes
        return {
            "Banco": self.nombre_banco,
            "TNA": 99.0,
            "TEA": 158.90,
            "CFTEA": 213.24
        }

if __name__ == "__main__":
    scraper = MercadoPagoScraper()
    tasas = scraper.obtener_tasas()
    print(tasas)
