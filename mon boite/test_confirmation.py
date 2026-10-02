import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USER or "no-reply@maison-impeccable.fr")

nom = "Jane Test"
email = "jane.test@gmail.com"
service = "Bureau / commerce"
telephone = "0611223344"

msg = EmailMessage()
msg["Subject"] = "Confirmation de votre demande de devis - Maison Impeccable"
msg["From"] = EMAIL_FROM
msg["To"] = email

body = f"""Bonjour {nom},

Merci de votre demande de devis pour Maison Impeccable.

Nous avons bien reçu votre message et nous vous recontacterons dans les 24 heures pour discuter de votre projet et vous proposer un devis personnalisé.

Service demandé: {service}
Numéro de téléphone: {telephone}

Si vous avez des questions en attendant, n'hésitez pas à nous contacter:
☎ 07 80 54 86 63
✉ mahsumim588@gmail.com

Cordialement,
L'équipe Maison Impeccable
"""

msg.set_content(body)

try:
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(msg)
        print("✓ Confirmation email sent successfully to jane.test@gmail.com")
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
