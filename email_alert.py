import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("credentials.env")

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER = os.getenv("RECEIVER_EMAIL")

print("EMAIL:", EMAIL)
print("PASSWORD:", PASSWORD)
print("RECEIVER:", RECEIVER)


class EmailAlert:

    def __init__(self):
        self.alert_sent = False

    def send_email(self, count):

        if self.alert_sent:
            return

        if EMAIL is None or PASSWORD is None or RECEIVER is None:
            print("Email configuration missing.")
            return

        subject = "Occupancy Alert"

        body = f"""
Occupancy Threshold Exceeded

Detected Persons : {count}

Time : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}
"""

        msg = MIMEText(body)

        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = RECEIVER

        try:
            server = smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()

            server.login(EMAIL,PASSWORD)

            server.sendmail(
                EMAIL,
                RECEIVER,
                msg.as_string()
            )

            server.quit()

            print("✅ Email Sent Successfully")

            self.alert_sent=True

        except Exception as e:
            print("❌ Email Error:",e)

    def reset(self):
        self.alert_sent=False


email_alert=EmailAlert()