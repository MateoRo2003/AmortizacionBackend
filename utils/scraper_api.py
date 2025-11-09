# utils/scraper_api.py
import requests

API_KEY = "166ee4016ceee1f0894edecf82383fc0"
SCRAPER_URL = "https://api.scraperapi.com/"

def get_html_with_scraperapi(url, render=False):
    """
    Devuelve el HTML de una página usando ScraperAPI.
    Si render=True, ejecuta JavaScript antes de devolverlo.
    """
    try:
        payload = {
            "api_key": API_KEY,
            "url": url,
            "render": "true" if render else "false"
        }
        r = requests.get(SCRAPER_URL, params=payload, timeout=30)
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        print(f"[ScraperAPI ERROR] No se pudo obtener {url}: {e}")
        return None
