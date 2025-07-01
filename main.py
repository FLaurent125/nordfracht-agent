import streamlit as st
import pandas as pd
from datetime import datetime
from mail_utils import send_email

st.title("🚛 Nordfracht Partner-Agent")

# E-Mail-Texte auf Deutsch und Englisch
DEUTSCHER_TEXT = """
Sehr geehrte Damen und Herren,

mein Name ist Felix Laurent und ich bin bei Nordfracht für den Aufbau zuverlässiger Speditionspartnerschaften zuständig.

Unsere Kunden – insbesondere aus Industrie und E-Commerce – erwarten heute vor allem eines: Transparenz in der Lieferkette. Um dem gerecht zu werden, setzen wir auf eine intelligente Lösung: Mit der Impargo-App ermöglichen wir Echtzeit-Tracking, automatisierte Avisierungen und proaktive Kommunikation – für den Kunden, aber auch zur Entlastung Ihrer Fahrer und Disponenten.

Wir sind aktuell auf der Suche nach verlässlichen Partnern mit eigenem Fuhrpark, die Transporte für uns übernehmen und von folgenden Vorteilen profitieren möchten:

- Direkte Aufträge von Nordfracht – ohne eigene Akquise

- Einfache App-Nutzung – kein Hardware-Einbau, keine technische Hürden

- Weniger Rückfragen – unser Chatbot informiert Kunden automatisch über ETA, Adresse & Status

- Effizientere Be- und Entladung – durch automatische Avisierung beim Kunden & Lager

- Datenschutz garantiert – es wird keine GPS-Position übermittelt, nur die berechnete Ankunftszeit (ETA)

- Keine Kosten für Sie – die App ist für Partner kostenlos

Die App lässt sich in weniger als einer Minute starten, läuft stabil und wurde bereits erfolgreich mit zahlreichen Partnern getestet.

Haben Sie Interesse an einer Zusammenarbeit oder einem kurzen Austausch in den nächsten Tagen?
Ich würde mich freuen, von Ihnen zu hören.

Mit freundlichen Grüßen
Felix Laurent
Nordfracht GbR
"""

ENGLISCHER_TEXT = """
Dear Sir or Madam,

My name is Felix Laurent and I am responsible for building reliable carrier partnerships at Nordfracht.

Our customers – especially from industry and e-commerce – increasingly expect transparency in the supply chain. To meet this demand, we work with the Impargo app to provide real-time tracking, automated notifications, and proactive communication – not only for the customer, but also to simplify your processes as a carrier.

We are currently looking for reliable partners with their own fleet who can handle transports for us and benefit from the following advantages:

- Direct transport orders from Nordfracht – no need for your own sales effort

- Simple app usage – no hardware installation or technical setup required

- Fewer customer inquiries – our chatbot automatically informs recipients about ETA, delivery address, and status

- Faster loading and unloading – through automatic notifications to the warehouse and customer

- Data protection guaranteed – the driver’s GPS location is never shared – only the estimated time of arrival (ETA) is calculated

- Completely free of charge – the app is free to use for our partners

The app is easy to install, takes less than a minute to activate, and has already been successfully used with many of our partners.

Would you be interested in a potential collaboration or a brief call in the coming days?
I would be happy to hear from you.

Kind regards,
Felix Laurent
Nordfracht GbR
"""

uploaded_file = st.file_uploader("📄 Lade deine partnerliste.xlsx hoch", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Sicherheit: Spalte explizit auf string setzen, um FutureWarning zu vermeiden
    if "Letzter_Kontakt" in df.columns:
        df["Letzter_Kontakt"] = df["Letzter_Kontakt"].astype("object")
    else:
        df["Letzter_Kontakt"] = None

    st.write("Gefundene Einträge:", df.shape[0])

    if st.button("📬 Kampagne starten"):
        for idx, row in df.iterrows():
            if pd.isna(row["Letzter_Kontakt"]):
                sprache = str(row.get("Sprache", "")).strip().lower()
                email_body = DEUTSCHER_TEXT if sprache == "de" else ENGLISCHER_TEXT
                subject = "Partnerschaft mit Nordfracht"

                email = row.get("Email", "")
                if email:
                    st.markdown(f"✉️ **Sende an:** {email} ({sprache})")
                    status = send_email(email, subject, email_body)
                    st.success(f"✅ E-Mail an {email} versendet – {status}")
                    df.at[idx, "Letzter_Kontakt"] = datetime.today().strftime('%Y-%m-%d')
                else:
                    st.warning(f"⚠️ Keine gültige E-Mail-Adresse in Zeile {idx + 2}")

        try:
            df.to_excel("partnerliste_aktualisiert.xlsx", index=False)
            st.success("📁 partnerliste_aktualisiert.xlsx gespeichert")
        except Exception as e:
            st.error(f"❌ Fehler beim Speichern der Excel-Datei: {e}")
