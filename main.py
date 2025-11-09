from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

# Importación de scrapers
from scrapers.bbva import BBVAScraper
from scrapers.bcra import BCRAScraper
from scrapers.bna import BNAScraperOptimized
from scrapers.galicia import GaliciaScraper
from scrapers.macro_chrome import MacroScraper
from scrapers.mp import MercadoPagoScraper
from scrapers.naranjax import NaranjaXScraper
from scrapers.santander import SantanderScraper
from scrapers.patagonia import PatagoniaScraperOptimized

app = Flask(__name__)
CORS(app, origins=["https://amortizacion-fronted.vercel.app"])

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

TASAS_FILE = "tasas.json"

def cargar_tasas():
    if not os.path.exists(TASAS_FILE):
        return []
    try:
        with open(TASAS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def guardar_tasa_individual(banco, tna, tea, cftea):
    tasas = cargar_tasas()
    tasas = [t for t in tasas if t["Banco"] != banco]
    tasas.append({
        "Banco": banco,
        "TNA": tna,
        "TEA": tea,
        "CFTEA": cftea
    })
    with open(TASAS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasas, f, indent=4, ensure_ascii=False)

def generar_tabla_amortizacion(monto, n_cuotas, tna):
    saldo = monto
    i = (tna / 100) / 12
    cuota_fija = monto * i / (1 - (1 + i) ** -n_cuotas)
    tabla = []
    for n in range(1, n_cuotas + 1):
        interes = saldo * i
        amortizacion = cuota_fija - interes
        saldo -= amortizacion
        tabla.append({
            "Cuota": n,
            "Cuota_total": round(cuota_fija, 2),
            "Interes": round(interes, 2),
            "Amortizacion": round(amortizacion, 2),
            "Saldo": round(max(saldo, 0), 2)
        })
    return tabla

@app.route("/api/calcular", methods=["POST"])
def api_calcular():
    data = request.json
    monto = float(data.get("monto", 0))
    n_cuotas = int(data.get("cuotas", 1))
    banco = data.get("banco")

    if banco not in scrapers_dict:
        return jsonify({"error": "Banco no válido"}), 400

    tasas_guardadas = cargar_tasas()
    tasa = next((t for t in tasas_guardadas if t["Banco"] == banco), None)

    if tasa:
        tna = tasa.get("TNA")
        tea = tasa.get("TEA")
        cftea = tasa.get("CFTEA")
    else:
        # Solo scrapea si no existe
        scraper = scrapers_dict[banco]
        tasas = scraper.obtener_tasas()
        tna = tasas.get("TNA")
        tea = tasas.get("TEA")
        cftea = tasas.get("CFTEA")
        if tna:
            guardar_tasa_individual(banco, tna, tea, cftea)

    if not tna:
        return jsonify({"error": "No se pudo obtener TNA del banco"}), 500

    tabla = generar_tabla_amortizacion(monto, n_cuotas, tna)

    return jsonify({
        "Banco": banco,
        "TNA": tna,
        "TEA": tea,
        "CFTEA": cftea,
        "Tabla": tabla
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
