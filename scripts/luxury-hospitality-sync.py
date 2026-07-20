#!/usr/bin/env python3
"""
Luxury Hospitality Italia — Daily Report Sync
Legge il report giornaliero da file Word, analizza duplicati, aggiorna registry.
"""

import os
import json
import sys
import re
from datetime import datetime
from pathlib import Path

from docx import Document
import google.generativeai as genai


REGISTRY_FILE = "Lavoro/Sales-Marketing/luxury-hospitality-report-registry.md"
REPORTS_DIR = "Email/Allegati-da-analizzare"


def find_latest_report():
    """Trova il file Word più recente nella cartella Allegati-da-analizzare (ricerca ricorsiva)."""
    report_dir = Path(REPORTS_DIR)
    if not report_dir.exists():
        return None

    # Ricerca ricorsiva per tutti i .docx nella cartella
    word_files = list(report_dir.rglob("*.docx"))
    if not word_files:
        return None

    # Ordina per data di modifica, più recente first
    word_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return word_files[0]


def read_word_file(file_path):
    """Legge il contenuto di un file Word."""
    try:
        doc = Document(file_path)
        text = ""
        for para in doc.paragraphs:
            if para.text.strip():
                text += para.text + "\n"
        return text
    except Exception as e:
        print(f"Errore lettura file Word: {e}")
        return None


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
    """Usa Google Gemini per analizzare il report, identificare duplicati, aggiornare registry."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("ERRORE: GOOGLE_API_KEY non configurata")
        sys.exit(1)

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""Tu sei un assistente per Giampaolo Padula per l'analisi del Luxury Hospitality Italia report.

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
Se nel report una posizione è dichiarata "live" su un portale (Michael Page, LinkedIn, Recruiter, ecc.):
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

    message = model.generate_content(prompt)
    response_text = message.text

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

    print("\n[1/4] Ricerca report Word...")
    report_file = find_latest_report()
    if not report_file:
        print("✗ Nessun report Word trovato")
        sys.exit(1)
    print(f"✓ Trovato: {report_file.name}")

    print("[2/4] Lettura contenuto...")
    report_content = read_word_file(report_file)
    if not report_content:
        print("✗ Errore lettura")
        sys.exit(1)
    print(f"✓ Report letto ({len(report_content)} bytes)")

    print("[3/4] Lettura registry...")
    registry_content = read_registry(REGISTRY_FILE)
    print("✓ Registry letto")

    print("[4/4] Analisi duplicati (Claude)...")
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
