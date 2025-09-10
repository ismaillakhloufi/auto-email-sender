import re
import pandas as pd
from pathlib import Path
from typing import List, Set
import fitz  # PyMuPDF for PDF parsing

# Regex email simple et robuste
EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")

def extract_emails(text: str) -> List[str]:
    """Extract emails from text using regex."""
    return EMAIL_REGEX.findall(text)

def clean_emails(emails: List[str]) -> List[str]:
    """Lowercase + deduplicate while preserving order."""
    seen: Set[str] = set()
    cleaned: List[str] = []
    for e in (x.strip().lower() for x in emails):
        if e and e not in seen:
            seen.add(e)
            cleaned.append(e)
    return cleaned

def load_emails_from_pdf(pdf_path: Path) -> List[str]:
    """Read PDF text and extract emails."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    doc.close()
    found = extract_emails(text)
    return clean_emails(found)

def save_emails_to_csv(emails: List[str], csv_path: Path):
    """Save email list to CSV file (one per row)."""
    df = pd.DataFrame(emails, columns=["email"])
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"✅ {len(emails)} emails saved to {csv_path}")
