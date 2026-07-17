#!/usr/bin/env python3
"""
Luxury Hospitality Italia — Daily Report Sync
Legge il report da Gmail, analizza duplicati con Claude, aggiorna il registry.
"""

import os
import json
import base64
from datetime import datetime
from pathlib import Path

try:
    from google.oauth2.service_account import Credentials
    from google.oauth2.credentials import Credentials as UserCredentials
    import googleapiclient.discovery
except ImportError:
    pass

from anthropic import Anthropic

def authenticate_gmail():
    """Autentica con Gmail usando le credenziali."""
    creds_json = os.environ.get('GOOGLE_CREDENTIALS')
    if not creds_json:
        raise ValueError("GOOGLE_CREDENTIALS env var not set")
    
    creds_dict = json.loads(creds_json)
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
    
    try:
        credentials = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    except:
        credentials = UserCredentials.from_authorized_user_info(creds_dict, SCOPES)
    
    return googleapiclient.discovery.build('gmail', 'v1', credentials=credentials)

def read_email_report():
    """Legge il report da Gmail."""
    service = authenticate_gmail()
    query = 'subject:"Report Luxury Hospitality Italia - giornaliero 03:00 IT — routine completed" newer_than:1d'
    results = service.users().messages().list(userId='me', q=query, maxResults=1).execute()
    
    if not results.get('messages'):
        return None
    
    msg = service.users().messages().get(userId='me', id=results['messages'][0]['id'], format='full').execute()
    
    for part in msg['payload'].get('parts', []):
        if part['mimeType'] == 'text/plain':
            data = part['body'].get('data', '')
            if data:
                return base64.urlsafe_b64decode(data).decode('utf-8')
    
    data = msg['payload']['body'].get('data', '')
    return base64.urlsafe_b64decode(data).decode('utf-8') if data else None

def analyze_with_claude(report_content, registry_content):
    """Analizza con Claude per identificare duplicati."""
    client = Anthropic()
    
    prompt = f"""Analizza questo report e identifica elementi nuovi vs. duplicati.

REPORT:
{report_content[:2000]}

REGISTRY ATTUALE:
{registry_content[:1000]}

Rispondi in JSON: {{"duplicates": [...], "new_items": [...], "summary": "..."}}"""
    
    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )
    
    try:
        text = message.content[0].text
        start = text.find('{')
        end = text.rfind('}') + 1
        return json.loads(text[start:end])
    except:
        return {"duplicates": [], "new_items": [], "summary": "Analysis done"}

def update_registry(analysis):
    """Aggiorna il registry."""
    registry_path = Path("Lavoro/Sales-Marketing/luxury-hospitality-report-registry.md")
    registry_content = registry_path.read_text() if registry_path.exists() else "# Registry\n\n## ELEMENTI GIA' SEGNALATI\n\n## ELEMENTI NUOVI\n"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    update = f"\n### {timestamp}\n" + "\n".join(f"- {item}" for item in analysis.get('new_items', []))
    
    registry_path.write_text(registry_content + update)

def main():
    print("Sync started...")
    report = read_email_report()
    if not report:
        print("No report found")
        return
    
    registry_path = Path("Lavoro/Sales-Marketing/luxury-hospitality-report-registry.md")
    registry = registry_path.read_text() if registry_path.exists() else ""
    
    analysis = analyze_with_claude(report, registry)
    update_registry(analysis)
    print(f"Done: {len(analysis.get('new_items', []))} new items")

if __name__ == "__main__":
    main()
