#!/usr/bin/env python3
"""
Luxury Hospitality Italia — Daily Report Sync
Legge il report giornaliero da Gmail via IMAP, analizza duplicati, aggiorna registry, sincronizza routine.
Eseguito via GitHub Actions ogni giorno alle 03:30 IT.
"""

import os
import json
import sys
import imaplib
import email
from datetime import datetime, timedelta
from email.header import decode_header
import re

from anthropic import Anthropic


GMAIL_SUBJECT = "Report Luxury Hospitality Italia - giornaliero 03:00 IT — routine completed"
REGISTRY_FILE = "Lavoro/Sales-Marketing/luxury-hospitality-report-registry.md"
GMAIL_USER = "giampaolopadula@gmail.com"
GMAIL_IMAP_SERVER = "imap.gmail.com"


def get_gmail_message_imap(app_password, subject, days=1):
    """Legge email da Gmail via IMAP usando App Password."""
    try:
        imap = imaplib.IMAP4_SSL(GMAIL_IMAP_SERVER)
        imap.login(GMAIL_USER, app_password)
        imap.select("INBOX")

        since_date = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
        # Usa una ricerca semplice con la parola chiave "Report" per evitare problemi di encoding con em-dash
        status, messages = imap.search(None, f'SINCE {since_date} SUBJECT "Report"')

        if status != "OK" or not messages[0]:
            print(f"Nessun messaggio trovato con subject: {subject}")
            imap.close()
            imap.logout()
            return None, None

        msg_ids = messages[0].split()
        if not msg_ids:
            return None, None

        status, msg_data = imap.fetch(msg_ids[-1], "(RFC822)")
        if status != "OK":
            print("Errore fetch messaggio")
            imap.close()
            imap.logout()
            return None, None

        msg = email.message_from_bytes(msg_data[0][1])
        imap.close()
        imap.logout()

        subject = msg.get("Subject", "")
        if isinstance(subject, bytes):
            subject = subject.decode("utf-8", errors="replace")
        else:
            subject_header = decode_header(subject)
            subject = "".join([s[0].decode(s[1] or "utf-8", errors="replace") if isinstance(s[0], bytes) else str(s[0]) for s in subject_header])

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    payload = part.get_payload(decode=True)
                    if payload:
                        try:
                            body += payload.decode("utf-8", errors="replace")
                        except:
                            body += payload.decode("latin-1", errors="replace")
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                try:
                    body = payload.decode("utf-8", errors="replace")
                except:
                    body = payload.decode("latin-1", errors="replace")

        return body, subject

    except Exception as e:
        print(f"Errore IMAP: {e}")
        import traceback
        traceback.print_exc()
        return None, None


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

REGISTRY ATTUALE (notizie gia' segnalate):
{current_registry}

COMPITO CRITICO - REGOLE CATEGORICHE:

**REGOLA 1: ESCLUDI COMPLETAMENTE ELEMENTI IDENTICI AL REPORT PRECEDENTE**
Se un elemento appare nel nuovo report ESATTAMENTE come nel registry (stesso nome, stesso status, stessi dettagli):
→ ESCLUDI dalla sezione P1/P2/P3
→ NON includere come se fosse nuovo
Esempio: "Hotel Bellevue — vacancy live (apertura fine 2026)" era nel 17 luglio IDENTICO → ESCLUDI completamente dal nuovo report

**REGOLA 2: VACANCIES - VERIFICARE PRIMA DI INCLUDERE**
Se nel report una posizione è dichiarata "live" su un portale (Michael Page, LinkedIn, LinkedIn Recruiter, ecc.):
→ VERIFICA che esista davvero sul sito — se non è trovabile, escludila o marcala come "da verificare con urgenza"
→ NON fidarsi della dichiarazione se non verificata

**REGOLA 3: FOLLOW-UP CON NOVITÀ MATERIALI CHIARE**
Un elemento GIA' SEGNALATO entra in FOLLOW-UP SOLO se ha una novità materiale CONCRETA:
- funding secured / funding approved / aumento di capitale / cartolarizzazione
- timeline change / apertura confermata / slittamento
- leadership appointment (nuova nomina)
- vacancy published / vacancy closed / candidature aperte
- recruiter identified / operator selected definitivamente / ownership change confermato
→ La novità deve essere ESPLICITA e DOCUMENTATA
→ Se non c'è novità materiale, ESCLUDI completamente (niente follow-up, niente ripetizione)

**REGOLA 4: LINKEDIN VERIFICATION OBBLIGATORIA**
Per OGNI contatto (leadership, recruiter, operatore):
- Nome completo + Ruolo + Azienda
- LinkedIn: [URL] oppure "LinkedIn non verificato"
- Se LinkedIn non verificato, nota "verifica consigliata"

**SEZIONI:**
- P1/P2/P3: SOLO elementi completamente nuovi (mai visti prima)
- FOLLOW-UP: elementi GIA' SEGNALATI con novità materiale concreta e documentata
- NULLA: se niente di nuovo, non includere niente

RISPONDI CON JSON:
{{
  "duplicates_count": <numero elementi esclusi perche' identici al registry>,
  "new_items": [<lista notizie SOLO nuove, escluso tutto il resto>],
  "updated_registry": "<registry con SOLO i nuovi elementi aggiunti + FOLLOW-UP con novita' concrete>"
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

    gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")
    if not gmail_app_password:
        print("ERRORE: GMAIL_APP_PASSWORD non configurata in GitHub Secrets")
        sys.exit(1)

    print("\n[1/4] Connessione a Gmail (IMAP)...")
    print("✓ Connesso")

    print("[2/4] Ricerca e lettura report email...")
    report_content, subject = get_gmail_message_imap(gmail_app_password, GMAIL_SUBJECT, days=1)
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
