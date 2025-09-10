from config import PDF_FILE, CSV_FILE
from email_loader import load_emails_from_pdf, save_emails_to_csv
from mailer import prepare_and_send

def main():
    # 1) Extract emails from PDF and save to CSV
    emails = load_emails_from_pdf(PDF_FILE)
    if not emails:
        raise SystemExit("⚠️ No valid emails found in PDF.")
    save_emails_to_csv(emails, CSV_FILE)
    
   
    # 2) Send emails with CV attached
    prepare_and_send(emails)

if __name__ == "__main__":
    main()
