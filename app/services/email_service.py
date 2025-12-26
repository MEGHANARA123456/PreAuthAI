import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import (
    EMAIL_HOST, EMAIL_PORT, EMAIL_USERNAME,
    EMAIL_PASSWORD, EMAIL_FROM
)

def send_reset_email(to_email: str, reset_link: str):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = to_email
    msg["Subject"] = "Password Reset Request"

    body = f"""
Hello,

You requested a password reset.

Click the link below to reset your password:
{reset_link}

This link expires in 15 minutes.

If you didn’t request this, ignore this email.
"""
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)
    print(f"Password reset email sent to {to_email}")