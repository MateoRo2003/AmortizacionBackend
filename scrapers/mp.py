# scrapers/mercado_pago.py
class MercadoPagoScraper:
    def __init__(self):
        self.nombre_banco = "Mercado Pago"

    def obtener_tasas(self):
        # Datos constantes
        return {
            "Banco": self.nombre_banco,
            "TNA": 249.0,
            "TEA": 860.0,
            "CFTEA": 1370.28
        }

if __name__ == "__main__":
    scraper = MercadoPagoScraper()
    tasas = scraper.obtener_tasas()
    print(tasas)
