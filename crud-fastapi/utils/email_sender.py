# services/email_sender.py
import smtplib
import os
from email.message import EmailMessage
from logger import logger
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

class EmailSender:

    @staticmethod
    def send_email(to_email: str, subject: str, body: str, attachment_path: str | None = None):
        try:
            msg = EmailMessage()
            msg["From"] = SENDER_EMAIL
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.set_content(body)

            # Add attachment if file exists
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, "rb") as f:
                    file_data = f.read()
                    file_name = os.path.basename(attachment_path)
                msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
                logger.info(f"Added attachment to email: {file_name}")

            # Send email via SMTP
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SENDER_EMAIL, EMAIL_PASSWORD)
                server.send_message(msg)
                logger.info(f"Email sent to {to_email}")

            return True

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
