import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from graph_reader import fetch_unread_emails
from gpt_classifier import classify_reply

# ───────────────────────────────────────────────────────────────
# ENV laden
# ───────────────────────────────────────────────────────────────
load_dotenv()

PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")
PUSHOVER_API_TOKEN = os.getenv("PUSHOVER_API_TOKEN")
LOG_PATH = "replies_log.xlsx"

# ───────────────────────────────────────────────────────────────
# Funktion: Nachricht via Pushover senden
# ───────────────────────────────────────────────────────────────
def send_pushover_message(title, message):
    payload = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "title": title,
        "message": message,
    }
    response = requests.post("https://api.pushover.net/1/messages.json", data=payload)
    if response.status_code == 200:
        print("✅ Pushover-Nachricht gesendet.")
    else:
        print(f"❌ Fehler beim Senden: {response.text}")

# ───────────────────────────────────────────────────────────────
# Funktion: Antwort in Excel loggen
# ───────────────────────────────────────────────────────────────
def save_to_excel(from_address, subject, preview, classification):
    if not os.path.isfile(LOG_PATH):
        pd.DataFrame(columns=["timestamp", "from", "subject", "preview", "classification"])\
          .to_excel(LOG_PATH, index=False)

    df = pd.read_excel(LOG_PATH)
    new_row = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "from": from_address,
        "subject": subject,
        "preview": preview[:200],
        "classification": classification
    }
    df.loc[len(df)] = new_row
    df.to_excel(LOG_PATH, index=False)

# ───────────────────────────────────────────────────────────────
# Hauptlogik: E-Mails analysieren, benachrichtigen & loggen
# ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    emails = fetch_unread_emails()
    for email in emails:
        body = email.get("bodyPreview", "")
        from_address = email["from"]["emailAddress"]["address"]
        subject = email["subject"]

        classification = classify_reply(body)
        print(f"📊 Klassifikation für '{from_address}': {classification}")

        save_to_excel(from_address, subject, body, classification)

        if classification in ["wahrscheinlich", "sehr wahrscheinlich"]:
            send_pushover_message(
                f"🤝 Potenzieller Partner: {from_address}",
                f"Betreff: {subject}\nKlassifikation: {classification}\n\nVorschau:\n{body[:200]}"
            )

