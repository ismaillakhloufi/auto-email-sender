import ssl
import time
import smtplib
import pandas as pd
from pathlib import Path
from email.message import EmailMessage
from typing import List
from config import (
    EMAIL_SENDER, APP_PASSWORD, SMTP_SERVER, SMTP_PORT,
    SUBJECT, BODY, CV_FILE, SEND_MODE, BCC_CHUNK_SIZE,
    SLEEP_BETWEEN_EMAILS_SEC, CSV_FILE
)

def chunk(lst: List[str], size: int) -> List[List[str]]:
    return [lst[i:i+size] for i in range(0, len(lst), size)]

def build_message(sender: str, to_: List[str], bcc_: List[str], subject: str, body: str, attachment_path: Path) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = ", ".join(to_) if to_ else sender
    if bcc_:
        msg["Bcc"] = ", ".join(bcc_)
    msg["Subject"] = subject
    msg.set_content(body)

    with attachment_path.open("rb") as f:
        data = f.read()
    msg.add_attachment(
        data, maintype="application", subtype="pdf", filename=attachment_path.name
    )
    return msg

def send_messages(messages: List[EmailMessage]):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(EMAIL_SENDER, APP_PASSWORD)
        for i, m in enumerate(messages, 1):
            server.send_message(m)
            print(f"[{i}/{len(messages)}] Sent.")
            time.sleep(SLEEP_BETWEEN_EMAILS_SEC)

def prepare_and_send(emails):
    if not EMAIL_SENDER or not APP_PASSWORD:
        raise SystemExit("⚠️ Set GMAIL_ADDRESS and GMAIL_APP_PASSWORD in environment variables.")
    if not CSV_FILE.exists():
        raise SystemExit(f"⚠️ CSV file not found: {CSV_FILE}")
    if not CV_FILE.exists():
        raise SystemExit(f"⚠️ CV file not found: {CV_FILE}")

    if not emails:
        raise SystemExit("⚠️ No emails found in CSV.")

    outgoing: List[EmailMessage] = []
    if SEND_MODE == "bcc":
        for batch in chunk(emails, BCC_CHUNK_SIZE):
            outgoing.append(build_message(
                sender=EMAIL_SENDER,
                to_=[EMAIL_SENDER],
                bcc_=batch,
                subject=SUBJECT,
                body=BODY,
                attachment_path=CV_FILE
            ))
    elif SEND_MODE == "individual":
        for recipient in emails:
            outgoing.append(build_message(
                sender=EMAIL_SENDER,
                to_=[recipient],
                bcc_=[],
                subject=SUBJECT,
                body=BODY,
                attachment_path=CV_FILE
            ))
    else:
        raise SystemExit('⚠️ SEND_MODE must be "bcc" or "individual".')

    send_messages(outgoing)
    print("🎉 Done.")
