import os
import base64
import csv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from message import give_text_html
from dotenv import load_dotenv

load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]

CSV_FILE = "recipients.csv"
PDF_FILE = "resume.pdf"

def get_credentials():
    """Authenticate and get Google API credentials."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    return creds




def create_email(sender, to, reciepient_name, reciepient_company, pdf_path):
    """Create an email message with a PDF attachment."""
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = f"Application for SDE Role at {reciepient_company}"
    text, html = give_text_html(reciepient_name, reciepient_company)
    msg.attach(MIMEText(text, "plain"))
    # msg.attach(MIMEText(html, "html"))
    if os.path.exists(PDF_FILE):
        with open(PDF_FILE, "rb") as pdf_file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(pdf_file.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(PDF_FILE)}"')
            msg.attach(part)

    return {"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode()}

def send_email(service, sender, to, reciepient_name, reciepient_company, pdf_path):
    """Send an email using the Gmail API."""
    message = create_email(sender, to, reciepient_name, reciepient_company, pdf_path)
    try:
        service.users().messages().send(userId="me", body=message).execute()
        print(f"Email sent to {to}")
    except HttpError as error:
        print(f"An error occurred: {error}")

def main():
    """Read CSV, authenticate, and send emails with attachments."""
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)
    sender_email = SENDER_EMAIL  # Replace with your email

    # Read recipient data from CSV
    with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            reciepient_name = row["Name"]
            reciepient_company = row["Company"]
            recipient = row["Email"]
            send_email(service, sender_email, recipient, reciepient_name, reciepient_company, PDF_FILE)

if __name__ == "__main__":
    main()
