import os
import pandas as pd
from dotenv import load_dotenv
from mail_utils import send_email

load_dotenv()

EXCEL_FILE = "partnerliste.xlsx"

EMAIL_SUBJECT = {
    "de": "Partnerschaft mit Nordfracht",
    "en": "Partnership with Nordfracht"
}

EMAIL_BODY = {
    "de": '''Sehr geehrte Damen und Herren,

mein Name ist Felix Laurent und ich bin bei Nordfracht für den Aufbau zuverlässiger Speditionspartnerschaften zuständig.

Unsere Kunden – vor allem aus Industrie und E-Commerce – erwarten heute vor allem eines: Transparenz in der Lieferkette. Deshalb arbeiten wir mit der Impargo-App, um Echtzeit-Tracking in unsere Prozesse zu integrieren – für den Kunden, aber auch zur Optimierung auf Ihrer Seite.

Wir suchen aktuell nach verlässlichen Partnern mit eigenem Fuhrpark, die sich einfach in unser System einbinden lassen. Die App ist leicht zu installieren und unkompliziert in der Nutzung – ohne zusätzliche Hardware.

Haben Sie Interesse an einer Zusammenarbeit oder einem kurzen Austausch in den nächsten Tagen? Ich würde mich freuen, von Ihnen zu hören.

Mit freundlichen Grüßen
Felix Laurent
Nordfracht GBR''',

    "en": '''Dear Sir or Madam,

My name is Felix Laurent and I am responsible for establishing reliable carrier partnerships at Nordfracht.

Our customers – particularly from industry and e-commerce – expect one thing above all: transparency in the supply chain. That’s why we work with the Impargo app to integrate real-time tracking into our processes – both for the customer and to optimize your operations.

We are currently looking for reliable partners with their own fleet who can easily be integrated into our system. The app is simple to install and easy to use – no additional hardware required.

Are you interested in a collaboration or a short conversation in the coming days? I’d be happy to hear from you.

Best regards,
Felix Laurent
Nordfracht GBR'''
}

# Einlesen der Partnerliste
try:
    df = pd.read_excel(EXCEL_FILE)
except Exception as e:
    print(f"❌ Fehler beim Laden der Excel-Datei: {e}")
    exit()

# Nur Partner ohne Versanddatum kontaktieren
df_to_send = df[df["Letzter_Kontakt"].isna()]

# E-Mails verschicken
for index, row in df_to_send.iterrows():
    email = row["Email"]
    sprache = str(row["Sprache"]).strip().lower()[:2]  # z. B. "de" oder "en"

    if sprache not in EMAIL_BODY:
        print(f"⚠️ Sprache nicht erkannt oder unterstützt für {email}, überspringe.")
        continue

    subject = EMAIL_SUBJECT[sprache]
    body = EMAIL_BODY[sprache]

    print(f"📤 Sende an {email} in Sprache {sprache}...")
    status = send_email(email, subject, body)

    if status:
        df.at[index, "Letzter_Kontakt"] = pd.Timestamp.today().strftime("%Y-%m-%d")
        print("✅ Gesendet.")
    else:
        print("❌ Fehler beim Senden.")

# Datei speichern
try:
    df.to_excel("partnerliste_aktualisiert.xlsx", index=False)
except Exception as e:
    print(f"❌ Konnte aktualisierte Datei nicht speichern: {e}")

