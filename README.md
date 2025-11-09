# Amortización Backend

Este repositorio contiene el **backend en Flask** para el proyecto de simulación de préstamos y comparación de bancos en Argentina.  
El backend está diseñado para ser consumido por un frontend separado y está desplegado en **Render**.

## 🌐 URL de producción

[https://amortizacionbackend.onrender.com](https://amortizacionbackend.onrender.com)

> ⚡ Este backend no está pensado para ejecutarse localmente. Está optimizado para producción y conectado con un frontend desplegado en Vercel.

## 🛠 Tecnologías

- Python 3.x  
- Flask  
- Flask-CORS (para permitir requests desde el frontend)  
- Gunicorn (para despliegue en Render)  
- Scrapers personalizados para distintos bancos de Argentina  

## ⚡ API Endpoints

### POST `/api/calcular`

Calcula la tabla de amortización de un préstamo según banco, monto y cuotas.

**Request Body:**

```json
{
    "monto": 100000,
    "cuotas": 12,
    "banco": "Santander"
}
Response:

json
Copiar código
{
    "Banco": "Santander",
    "TNA": 95.0,
    "TEA": 130.0,
    "CFTEA": 132.5,
    "Tabla": [
        {
            "Cuota": 1,
            "Cuota_total": 10000,
            "Interes": 800,
            "Amortizacion": 9200,
            "Saldo": 90800
        },
        ...
    ]
}
✅ Soporta preflight requests OPTIONS y está configurado para CORS, permitiendo únicamente el dominio del frontend en Vercel:

python
Copiar código
CORS(app, origins=["https://amortizacion-fronted.vercel.app"])
🗂 Estructura del proyecto
bash
Copiar código
/amortizacion-backend
│
├─ main.py                # Archivo principal de Flask
├─ tasas.json             # Cache de tasas de bancos
├─ scrapers/              # Scrapers personalizados por banco
├─ requirements.txt       # Dependencias

💡 Notas importantes
Se mantiene un cache local (tasas.json) para reducir scraping y mejorar rendimiento.

Todas las requests deben provenir del frontend autorizado.

El backend está listo para producción y no requiere ejecución local.

