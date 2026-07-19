#!/usr/bin/env python3
"""
Luxury Hospitality Italia — Daily Report Sync
Legge il report giornaliero da Gmail, analizza duplicati, aggiorna registry, sincronizza routine.
Eseguito via GitHub Actions ogni giorno alle 03:30 IT.
"""

import os
import json
import sys
from datetime import datetime, timedelta
import base64
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.api_core.exceptions import GoogleAPICallError
from googleapiclient.discovery import build
from anthropic import Anthropic


GMAIL_SUBJECT = "Report Luxury Hospitality Italia - giornaliero 03:00 IT — routine completed"
REGISTRY_FILE = "Lavoro/Sales-Marketing/luxury-hospitality-report-registry.md"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_gmail_service(credentials_json_str):
    """Crea il servizio Gmail usando le credenziali OAuth da string JSON."""
    creds_dict = json.loads(credentials_json_str)
    creds = Credentials.from_authorized_user_info(creds_dict, SCOPES)
    return build("gmail", "v1", credentials=creds)


def search_emails(service, subject, days=1):
    """Cerca email con un subject specifico negli ultimi N giorni."""
    after_date = (datetime.now() - timedelta(days=days)).strftime("%Y/%m/%d")
    query = f'subject:"{subject}" after:{after_date}'

    try:
        results = service.users().messages().list(userId="me", q=query, maxResults=1).execute()
        messages = results.get("messages", [])
        return [msg["id"] for msg in messages]
    except GoogleAPICallError as e:
        print(f"Errore ricerca Gmail: {e}")
        return []


def get_message_content(service, message_id):
    """Ottiene il contenuto testuale di un messaggio Gmail."""
    try:
        msg = service.users().messages().get(userId="me", id=message_id, format="full").execute()
        headers = msg["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")

        body = ""
        if "parts" in msg["payload"]:
            for part in msg["payload"]["parts"]:
                if part["mimeType"] == "text/plain":
                    data = part["body"].get("data", "")
                    if data:
                        body += base64.urlsafe_b64decode(data).decode("utf-8")
        else:
            data = msg["payload"]["body"].get("data", "")
            if data:
                body = base64.urlsafe_b64decode(data).decode("utf-8")

        return body, subject
    except GoogleAPICallError as e:
        print(f"Errore lettura messaggio: {e}")
        return "", ""


def read_registry(registry_path):
    """Legge il file registry."""
    if not os.path.exists(registry_path):
        return ""
    with open(registry_path, "r", encoding="utf-8") as f:
        return f.read()


def update_registry_file(registry_path, new_content):
    """Aggiorna il file registry."""
    os.makedirs(os.path.dirname(registry_path), exist_ok=True)
    with open(registry_path, "w", encoding="utf-8") as f:
        f.write(new_content)


def analyze_report_and_update_registry(report_markdown, current_registry):
    """Usa Claude per analizzare il report, identificare duplicati, aggiornare registry."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERRORE: ANTHROPIC_API_KEY non configurata")
        sys.exit(1)

    client = Anthropic(api_key=api_key)

    prompt = f"""Tu sei Claude, assistente di Giampaolo Padula per il Luxury Hospitality Italia report.

REPORT OGGI:
{report_markdown}

REGISTRY ATTUALE (elementi gia' segnalati):
{current_registry}

COMPITO CRITICO:
1. LEGGI il registry attuale e identifica TUTTI gli elementi gia' segnalati (nomi hotel, contatti, progetti, leadership movements)
2. CONFRONTA il report di oggi con il registry
3. ESCLUDI COMPLETAMENTE dal report tutti gli elementi che sono gia' nel registry (duplicati)
4. TIENI SOLO i nuovi elementi che NON sono nel registry
5. AGGIORNA il registry: aggiungi il timestamp di oggi e i nuovi elementi SOLTANTO

REGOLA FONDAMENTALE:
- Se "Danilo Guerrini" e' gia' nel registry come "GM Belmond Romazzino", NON va incluso di nuovo
- Se "Hotel Eden Roma" e' gia' nel registry, NON va incluso di nuovo
- Solo gli elementi COMPLETAMENTE NUOVI vanno aggiunti

RISPONDI CON JSON:
{{
  "duplicates_count": <numero elementi esclusi perche' gia' nel registry>,
  "new_items": [<lista SOLO elementi nuovi non nel registry>],
  "updated_registry": "<contenuto completo del registry con SOLO i nuovi elementi aggiunti>",
  "notes": "<breve note>"
}}"""

    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text

    try:
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return None
    except json.JSONDecodeError:
        print("Errore parsing JSON")
        return None


def main():
    print("=" * 80)
    print("Luxury Hospitality Italia — Daily Report Sync")
    print(f"Data/ora: {datetime.now().isoformat()}")
    print("=" * 80)

    google_credentials = os.getenv("GOOGLE_CREDENTIALS")
    if not google_credentials:
        print("ERRORE: GOOGLE_CREDENTIALS non configurata in GitHub Secrets")
        sys.exit(1)

    print("\n[1/5] Connessione a Gmail...")
    try:
        service = get_gmail_service(google_credentials)
        print("✓ Connesso")
    except Exception as e:
        print(f"✗ Errore: {e}")
        sys.exit(1)

    print("[2/5] Ricerca report email...")
    message_ids = search_emails(service, GMAIL_SUBJECT, days=1)
    if not message_ids:
        print("✗ Nessun report trovato")
        sys.exit(1)
    print("✓ Trovato")

    print("[3/5] Lettura contenuto...")
    report_content, subject = get_message_content(service, message_ids[0])
    if not report_content:
        print("✗ Errore lettura")
        sys.exit(1)
    print(f"✓ Report letto ({len(report_content)} bytes)")

    print("[4/5] Lettura registry...")
    registry_content = read_registry(REGISTRY_FILE)
    print("✓ Registry letto")

    print("[5/5] Analisi duplicati (Claude)...")
    result = analyze_report_and_update_registry(report_content, registry_content)

    if not result:
        print("✗ Errore analisi")
        sys.exit(1)

    print("\n[UPDATE] Aggiornamento registry...")
    updated_registry = result.get("updated_registry", "")
    if updated_registry:
        update_registry_file(REGISTRY_FILE, updated_registry)
        print("✓ Registry aggiornato")
    else:
        print("⚠ Nessun cambio")

    print("\n" + "=" * 80)
    print("RISULTATI")
    print("=" * 80)
    print(f"Duplicati: {result.get('duplicates_count', 0)}")
    print(f"Nuovi: {len(result.get('new_items', []))}")
    if result.get('new_items'):
        for item in result.get('new_items', []):
            print(f"  - {item}")
    print(f"Note: {result.get('notes', 'N/A')}")
    print("=" * 80)
    print("\n✓ Sync completato")


if __name__ == "__main__":
    main()
