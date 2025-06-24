import os
import requests
import msal
from datetime import datetime, timedelta

def get_graph_token():
    app = msal.ConfidentialClientApplication(
        os.getenv("MS_CLIENT_ID"),
        authority=f"https://login.microsoftonline.com/{os.getenv('MS_TENANT_ID')}",
        client_credential=os.getenv("MS_CLIENT_SECRET")
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return result.get("access_token")

def create_outlook_event(subject: str, body: str, to_email: str):
    token = get_graph_token()
    if not token:
        return "Fehler beim Tokenabruf"
    url = f"https://graph.microsoft.com/v1.0/users/{os.getenv('MS_USER_EMAIL')}/events"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    start_time = datetime.utcnow() + timedelta(days=2, hours=10)
    end_time = start_time + timedelta(minutes=30)
    payload = {
        "subject": subject,
        "body": {"contentType": "Text", "content": body},
        "start": {"dateTime": start_time.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": end_time.isoformat(), "timeZone": "UTC"},
        "attendees": [{"emailAddress": {"address": to_email}, "type": "required"}]
    }
    response = requests.post(url, headers=headers, json=payload)
    return f"Termin erstellt: {response.status_code}"
