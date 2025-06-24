from datetime import datetime, timedelta
import requests
import os
from graph_reader import get_graph_token

def create_outlook_event(subject: str, body: str, to_email: str):
    token = get_graph_token()
    if not token:
        return "Fehler beim Tokenabruf"

    start_time = (datetime.utcnow() + timedelta(days=2, hours=10)).isoformat()
    end_time = (datetime.utcnow() + timedelta(days=2, hours=10, minutes=30)).isoformat()

    url = f"https://graph.microsoft.com/v1.0/users/{os.getenv('MS_USER_EMAIL')}/events"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "subject": subject,
        "body": {"contentType": "Text", "content": body},
        "start": {"dateTime": start_time, "timeZone": "UTC"},
        "end": {"dateTime": end_time, "timeZone": "UTC"},
        "attendees": [{"emailAddress": {"address": to_email}, "type": "required"}]
    }
    response = requests.post(url, headers=headers, json=payload)
    return f"Terminstatus: {response.status_code}"


