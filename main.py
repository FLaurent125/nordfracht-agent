import streamlit as st
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()  # Lädt .env-Datei

from mail_utils import send_email

st.title("🚛 Nordfracht Partner-Agent")

# Texte auf Deutsch und Englisch
DEUTSCHER_TEXT = """
Sehr geehrte Damen und Herren,

mein Name ist Felix Laurent und ich bin bei Nordfracht für den Aufbau zuverlässiger Speditionspartnerschaften zuständig.

Unsere Kunden – vor allem aus Industrie und E-Commerce – erwarten heute vor allem eines: Transparenz in der Lieferkette. Deshalb arbeiten wir mit der Impargo-App, um Echtzeit-Tracking in unsere Prozesse zu integrieren – für den Kunden, aber auch zur Optimierung auf Ihrer Seite.

Wir suchen aktuell nach verlässlichen Partnern mit eigenem Fuhrpark, die sich einfach in unser System einbinden lassen. Die App ist leicht zu installieren und unkompliziert in der Nutzung – ohne zusätzliche Hardware.

Haben Sie Interesse an einer Zusammenarbeit oder einem kurzen Austausch in den nächsten Tagen? Ich würde mich freuen, von Ihnen zu hören.

Mit freundlichen Grüßen
Felix Laurent
Nordfracht GBR
"""

ENGLISCHER_TEXT = """
Dear Sir or Madam,

my name is Felix Laurent and I am responsible at Nordfracht for building reliable carrier partnerships.

Our customers – especially in industry and e-commerce – expect one thing above all: transparency in the supply chain. That's why we use the Impargo app to integrate real-time tracking into our operations – both for the customer and to optimize your side.

We are currently looking for reliable partners with their own fleet who can be easily integrated into our system. The app is easy to install and use – without any additional hardware.

Would you be interested in a collaboration or a short exchange in the next few days? I would be delighted to hear from you.

Kind regards
Felix Laurent
Nordfracht GBR
"""

uploaded_file = st.file_uploader("📄 Lade deine partnerliste.xlsx hoch", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Gefundene Einträge:", df.shape[0])

    if st.button("📬 Kampagne starten"):
        for idx, row in df.iterrows():
            if pd.isna(row["Letzter_Kontakt"]):
                sprache = str(row["Sprache"]).strip().lower()
                email_body = DEUTSCHER_TEXT if sprache == "de" else ENGLISCHER_TEXT
                subject = "Partnerschaft mit Nordfracht"

                st.markdown(f"✉️ **Sende an:** {row['Email']} ({sprache})")
                status = send_email(row["Email"], subject, email_body)
                st.success(f"✅ E-Mail an {row['Email']} versendet – {status}")
                df.at[idx, "Letzter_Kontakt"] = datetime.today().strftime('%Y-%m-%d')

        df.to_excel("partnerliste_aktualisiert.xlsx", index=False)
        st.success("📁 partnerliste_aktualisiert.xlsx gespeichert")
