#!/usr/bin/env python3
"""
Download Luxury Hospitality report from Google Drive
Scarica il report quotidiano da Google Drive nella cartella report quotidiano hospitality
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from io import BytesIO

# Configurazione
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
REPORT_FOLDER_NAME = "Luxury Hospitality Reports"
DOWNLOAD_DIR = Path("Email/Allegati-da-analizzare/report quotidiano hospitality")
CREDENTIALS_FILE = Path(__file__).parent / "credentials-gdrive.json"
TOKEN_FILE = Path(__file__).parent / "token-gdrive.json"

def authenticate_gdrive():
    """Autentica con Google Drive"""
    creds = None

    # Se token esiste, caricalo
    if TOKEN_FILE.exists():
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    # Se token non valido, autentica di nuovo
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Usa il file credentials.json (scaricato da Google Cloud Console)
            if not CREDENTIALS_FILE.exists():
                print(f"ERRORE: {CREDENTIALS_FILE} non trovato.")
                print("Scarica il file credentials.json da Google Cloud Console.")
                print("1. Vai a https://console.cloud.google.com")
                print("2. Crea un OAuth 2.0 Client ID (Desktop application)")
                print("3. Scarica il JSON e salvalo come 'credentials-gdrive.json'")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Salva il token per future autenticazioni
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def find_report_folder(service):
    """Trova la cartella 'Luxury Hospitality Reports' in Google Drive"""
    query = f"name='{REPORT_FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])

    if not items:
        print(f"ERRORE: Cartella '{REPORT_FOLDER_NAME}' non trovata in Google Drive")
        return None

    return items[0]['id']

def find_latest_report(service, folder_id):
    """Trova il file report più recente nella cartella"""
    query = f"'{folder_id}' in parents and name contains 'Luxury Hospitality Italia' and mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document' and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='files(id, name, createdTime)', orderBy='createdTime desc').execute()
    items = results.get('files', [])

    if not items:
        print("ERRORE: Nessun report trovato in Google Drive")
        return None

    return items[0]

def download_file(service, file_id, file_name):
    """Scarica il file da Google Drive"""
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    request = service.files().get_media(fileId=file_id)
    file_path = DOWNLOAD_DIR / file_name

    with open(file_path, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%")

    return file_path

def main():
    print("=" * 80)
    print("Download Luxury Hospitality Report from Google Drive")
    print("=" * 80)

    # Autentica
    print("\n[1/4] Autenticazione Google Drive...")
    service = authenticate_gdrive()
    print("[OK] Autenticazione riuscita")

    # Trova cartella
    print("[2/4] Ricerca cartella 'Luxury Hospitality Reports'...")
    folder_id = find_report_folder(service)
    if not folder_id:
        sys.exit(1)
    print(f"[OK] Cartella trovata: {folder_id}")

    # Trova report più recente
    print("[3/4] Ricerca report più recente...")
    report = find_latest_report(service, folder_id)
    if not report:
        sys.exit(1)
    print(f"[OK] Report trovato: {report['name']}")
    print(f"     Data creazione: {report['createdTime']}")

    # Scarica file
    print("[4/4] Download del file...")
    file_path = download_file(service, report['id'], report['name'])
    print(f"[OK] File scaricato: {file_path}")

    print("\n" + "=" * 80)
    print("Download completato!")
    print("=" * 80)

if __name__ == "__main__":
    main()
