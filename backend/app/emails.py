import smtplib
from email.message import EmailMessage
from typing import Optional

from app.core.config import settings


def send_email(subject: str, recipient: str, body: str, html: Optional[str] = None) -> bool:
    """Send email via SMTP (if configured) or fallback to console for dev."""
    if not settings.SMTP_HOST or not settings.SMTP_FROM:
        # fallback to console (development)
        print("--- EMAIL (console) ---")
        print(f"To: {recipient}")
        print(f"Subject: {subject}")
        print(body)
        print("-----------------------")
        return True

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_FROM
    msg["To"] = recipient
    msg.set_content(body)
    if html:
        msg.add_alternative(html, subtype="html")

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT or 25) as smtp:
            smtp.ehlo()
            if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
                smtp.starttls()
                smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("Failed to send email:", e)
        return False
