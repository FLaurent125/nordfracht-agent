import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(to_email: str, subject: str, body: str) -> str:
    message = Mail(
        from_email=st.secrets["MS_USER_EMAIL"],
        to_emails=to_email,
        subject=subject,
        plain_text_content=body
    )
    sg = SendGridAPIClient(st.secrets["SENDGRID_API_KEY"])
    response = sg.send(message)
    return f"Status: {response.status_code}"
