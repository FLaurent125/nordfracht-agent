from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_sales_email(context: str | None, company_url: str) -> str:
    if context:
        prompt = f"""
Du bist ein Netzwerk-Agent von Nordfracht. Basierend auf folgenden Infos zur Spedition {company_url}, schreibe eine individuelle E-Mail, warum Nordfracht sie als Partner gewinnen möchte.

Unsere Kunden aus Industrie und E-Commerce erwarten heute vor allem eines: Transparenz in der Lieferkette. Deshalb arbeiten wir mit der Impargo-App, um Echtzeit-Tracking in unsere Prozesse zu integrieren.

Die App ist leicht zu installieren und unkompliziert in der Nutzung – ohne zusätzliche Hardware.

Website-Kontext:
{context}

Antworte mit einer freundlichen, individuellen E-Mail im Namen von Felix Laurent.
"""
    else:
        prompt = f"""
Du bist ein Netzwerk-Agent von Nordfracht. Schreibe eine freundliche, professionelle E-Mail an eine Spedition, die potenziell als Partner für Nordfracht infrage kommt.

Unsere Kunden – vor allem aus Industrie und E-Commerce – erwarten Echtzeit-Tracking. Wir nutzen dafür die Impargo-App, die für Fahrer leicht zu bedienen ist und keine zusätzliche Hardware benötigt.

Ziel der Mail: Wir möchten die Spedition als Dienstleister gewinnen und in ein erstes Gespräch kommen.

Am Ende soll deutlich werden, dass wir **sie als Spediteur beauftragen möchten** und aktuell nach neuen Partnern suchen.

Die E-Mail kommt von Felix Laurent.

Verwende einen verbindlichen, aber höflichen Ton.
"""

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content


