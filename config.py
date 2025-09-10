import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Gmail credentials
EMAIL_SENDER = os.environ.get("GMAIL_ADDRESS")
APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

# SMTP server
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# Files (from env)
PDF_FILE = Path(os.environ.get("PDF_FILE"))
CSV_FILE = Path(os.environ.get("CSV_FILE"))
CV_FILE = Path(os.environ.get("CV_FILE"))

# Email parameters
SUBJECT = "Candidature – Ingénieur Data/Cloud"
BODY = (
    "Bonjour,\n"
    "Je m’appelle LAKHLOUFI ISMAIL, ingénieure en Data Science et Cloud Computing.\n"
    "Je suis actuellement à la recherche de ma première expérience professionnelle dans le domaine de la data et du cloud.\n"
    "Je vous partage mon CV ci-joint et reste à votre disposition.\n\n"
    "Cordialement,\n"
    "LAKHLOUFI ISMAIL"
)

# Send mode: "bcc" or "individual"
SEND_MODE = "individual"
BCC_CHUNK_SIZE = 90
SLEEP_BETWEEN_EMAILS_SEC = 1.0
