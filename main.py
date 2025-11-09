from flask import Flask, request, jsonify, send_from_directory
import json
import os
from datetime import datetime, timedelta

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

# Sirve todo desde la raíz
app = Flask(__name__, static_folder=".", template_folder=".")

@app.route('/<path:filename>')
def serve_root_files(filename):
    return send_from_directory('.', filename)

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

def cargar_tasas():
    file_path = "tasas.json"
    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                return data
    except:
        pass

    return None


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

@app.route("/")
def home():
    return send_from_directory('.', 'index.html')

@app.route("/api/calcular", methods=["POST"])
def api_calcular():
    data = request.json
    monto = float(data.get("monto", 0))
    n_cuotas = int(data.get("cuotas", 1))
    banco = data.get("banco")

    if banco not in scrapers_dict:
        return jsonify({"error": "Banco no válido"}), 400

    tasas_guardadas = cargar_tasas()
    tna = tea = cftea = None

    # Buscar en tasas.json
    if tasas_guardadas:
        for t in tasas_guardadas:
            if t["Banco"] == banco:
                tna = t.get("TNA")
                tea = t.get("TEA")
                cftea = t.get("CFTEA")
                break

    # Solo scrapea si falta TNA
    if tna is None:
        scraper = scrapers_dict[banco]
        tasas = scraper.obtener_tasas()
        tna = tasas.get("TNA")
        tea = tasas.get("TEA")
        cftea = tasas.get("CFTEA")

        if tna:
            guardar_tasa_individual(banco, tna, tea, cftea)

    if tna is None:
        return jsonify({"error": "No se pudo obtener TNA del banco"}), 500

    tabla = generar_tabla_amortizacion(monto, n_cuotas, tna)

    return jsonify({
        "Banco": banco,
        "TNA": tna,
        "TEA": tea,
        "CFTEA": cftea,
        "Tabla": tabla
    })

    data = request.json
    monto = float(data.get("monto", 0))
    n_cuotas = int(data.get("cuotas", 1))
    banco = data.get("banco")

    if banco not in scrapers_dict:
        return jsonify({"error": "Banco no válido"}), 400

    tasas_guardadas = cargar_tasas()
    tna = tea = cftea = None

    # Buscar en tasas.json
    if tasas_guardadas:
        for t in tasas_guardadas:
            if t["Banco"] == banco:
                tna = t.get("TNA")
                tea = t.get("TEA")
                cftea = t.get("CFTEA")
                break

    # Solo scrapea si no hay TNA
    if tna is None:
        scraper = scrapers_dict[banco]
        tasas = scraper.obtener_tasas()
        tna = tasas.get("TNA")
        tea = tasas.get("TEA")
        cftea = tasas.get("CFTEA")

        if tna:
            guardar_tasa_individual(banco, tna, tea, cftea)

    if tna is None:
        return jsonify({"error": "No se pudo obtener TNA del banco"}), 500

    tabla = generar_tabla_amortizacion(monto, n_cuotas, tna)

    return jsonify({
        "Banco": banco,
        "TNA": tna,
        "TEA": tea,      # puede ser None
        "CFTEA": cftea,  # puede ser None
        "Tabla": tabla
    })
    data = request.json
    monto = float(data.get("monto", 0))
    n_cuotas = int(data.get("cuotas", 1))
    banco = data.get("banco")

    if banco not in scrapers_dict:
        return jsonify({"error": "Banco no válido"}), 400

    tasas_guardadas = cargar_tasas()
    tna = tea = cftea = None

    # Buscar en tasas.json
    if tasas_guardadas:
        for t in tasas_guardadas:
            if t["Banco"] == banco:
                tna = t.get("TNA")
                tea = t.get("TEA")
                cftea = t.get("CFTEA")
                break

    # Si faltan datos, scrapeamos
    if tna is None or tea is None or cftea is None:
        scraper = scrapers_dict[banco]
        tasas = scraper.obtener_tasas()

        tna = tasas.get("TNA")
        tea = tasas.get("TEA")
        cftea = tasas.get("CFTEA")

        # Guardar para la próxima
        if tna:
            guardar_tasa_individual(banco, tna, tea, cftea)

    if tna is None:
        return jsonify({"error": "No se pudo obtener TNA del banco"}), 500

    tabla = generar_tabla_amortizacion(monto, n_cuotas, tna)

    return jsonify({
        "Banco": banco,
        "TNA": tna,
        "TEA": tea,
        "CFTEA": cftea,
        "Tabla": tabla
    })

def guardar_tasa_individual(banco, tna, tea, cftea):
    file_path = "tasas.json"
    tasas = cargar_tasas() or []

    tasas = [t for t in tasas if t["Banco"] != banco]

    tasas.append({
        "Banco": banco,
        "TNA": tna,
        "TEA": tea,
        "CFTEA": cftea
    })

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(tasas, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
     port = int(os.environ.get("PORT", 5000))
     app.run(host="0.0.0.0", port=port)
