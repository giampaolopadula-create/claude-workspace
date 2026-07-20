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
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""Analizza il report e aggiorna il registry.

REPORT:
{report_markdown}

REGISTRY:
{current_registry}

REGOLE:
1. Escludi elementi IDENTICI al registry (stesso nome, status, dettagli)
2. Per vacancy "live": verifica esistano realmente
3. Segna FOLLOW-UP solo con novità concrete (funding, timeline, leadership, vacancy status)
4. Senza novità materiale: escludi completamente

Rispondi JSON:
{{"duplicates_count": N, "new_items": [...], "updated_registry": "..."}}"""

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
