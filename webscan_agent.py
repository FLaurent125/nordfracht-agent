import requests
from bs4 import BeautifulSoup

def extract_website_summary(url: str) -> str:
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = " ".join(p.get_text() for p in paragraphs[:10])
        return f"Analyse der Website {url}: {text.strip()[:2000]}"
    except Exception as e:
        return f"Konnte Website nicht analysieren ({e})"
