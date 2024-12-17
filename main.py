import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import gspread
import csv
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")

def get_client_email():
    with open(SERVICE_ACCOUNT_FILE, 'r') as file:
        data = json.load(file)
    return data.get('client_email')

def validate_sheet_access(sheet_url):
    SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
    gc = gspread.authorize(credentials)
    try:
        gc.open_by_url(sheet_url)
    except gspread.exceptions.APIError as e:
        if "403" in str(e):
            raise PermissionError("Access denied. Share the spreadsheet with the service account.")
    except gspread.exceptions.SpreadsheetNotFound:
        raise ValueError("Spreadsheet not found. Check the URL.")

def fetch_sheet_data(sheet_url):
    SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
    gc = gspread.authorize(credentials)
    spreadsheet = gc.open_by_url(sheet_url)
    name = spreadsheet.title
    sheet = spreadsheet.sheet1
    return sheet.get_all_records()

def generate_csv(data, output_path):
    print("genrating csv")
    with open(output_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    return output_path

def generate_pdf(data, output_path):
    header = list(data[0].keys())
    print("Genrating pdf")
    rows = [list(record.values()) for record in data]
    table_data = [header] + rows
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    elements = []
    table = Table(table_data)
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(table_style)
    elements.append(table)
    doc.build(elements)
    return output_path

def send_email(receiver_email, attachments):
    print("sending email")
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email
    message["Subject"] = f"Scheduled Google form files "

    body = "Here are the requested from files"
    message.attach(MIMEText(body, "plain"))

    for file_path in attachments:
        with open(file_path, "rb") as file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition", f"attachment; filename={os.path.basename(file_path)}"
            )
            message.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(message)
    print("sent email")