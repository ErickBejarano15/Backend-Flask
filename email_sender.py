# backend/email_sender.py

import os
import base64
import pickle
from email.mime.text import MIMEText
from dotenv import load_dotenv, find_dotenv

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# ——— Diagnóstico: carga el mismo .env que app.py ——————————
env_path = find_dotenv()
print(f"[email_sender] find_dotenv → {env_path!r}")
load_dotenv(env_path)
print(f"[email_sender] MAIL_SENDER   = {os.getenv('MAIL_SENDER')!r}")
print(f"[email_sender] MAIL_RECEIVER = {os.getenv('MAIL_RECEIVER')!r}")
# ————————————————————————————————————————————————————————————

SCOPES     = ['https://www.googleapis.com/auth/gmail.send']
CREDS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'

def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def send_email(nombre, reply_to, asunto, mensaje):
    remitente = os.getenv('MAIL_SENDER')
    destino   = os.getenv('MAIL_RECEIVER')
    service   = get_gmail_service()

    cuerpo   = f"Nombre: {nombre}\nCorreo de vuelta: {reply_to}\n\n{mensaje}"
    mime_msg = MIMEText(cuerpo, 'plain')
    mime_msg['to']      = destino
    mime_msg['from']    = remitente
    mime_msg['subject'] = asunto

    raw = base64.urlsafe_b64encode(mime_msg.as_bytes()).decode()
    service.users().messages().send(userId='me', body={'raw': raw}).execute()
