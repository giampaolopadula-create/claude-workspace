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
import ollama


REGISTRY_FILE = "Lavoro/Sales-Marketing/luxury-hospitality-report-registry.md"
DUPLICATES_AND_ERRORS_FILE = "Lavoro/Sales-Marketing/luxury-hospitality-duplicates-and-errors.md"
REPORTS_DIR = "Email/Allegati-da-analizzare"


def find_latest_report():
    """Trova il file Word più recente nella cartella Allegati-da-analizzare (ricerca ricorsiva)."""
    report_dir = Path(REPORTS_DIR)
    if not report_dir.exists():
        return None

    # Ricerca ricorsiva per tutti i .docx nella cartella (escludi file temporanei)
    word_files = [f for f in report_dir.rglob("*.docx") if not f.name.startswith("~$")]
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


def read_duplicates_and_errors(duplicates_file):
    """Legge il file storico di doppioni e errori."""
    if not os.path.exists(duplicates_file):
        return ""
    with open(duplicates_file, "r", encoding="utf-8") as f:
        return f.read()


def update_registry_file(registry_path, new_content):
    """Aggiorna il file registry."""
    os.makedirs(os.path.dirname(registry_path), exist_ok=True)
    with open(registry_path, "w", encoding="utf-8") as f:
        f.write(new_content)


def update_duplicates_and_errors_file(duplicates_file, analysis_result, current_content):
    """Aggiorna il file storico di doppioni/errori basandosi sui risultati di Ollama."""
    today = datetime.now().strftime("%Y-%m-%d")

    # Estrai elementi da aggiungere
    new_duplicates = analysis_result.get("identified_duplicates", [])
    new_unverified = analysis_result.get("unverified_items", [])

    # Parsa il contenuto attuale per evitare duplicati
    existing_content = current_content
    updated_content = existing_content

    # Aggiungi nuovi doppioni (se non già presenti)
    if new_duplicates:
        dup_section_exists = "## Doppioni Identificati" in updated_content
        if not dup_section_exists:
            updated_content += "\n## Doppioni Identificati\n\n"

        for dup in new_duplicates:
            dup_clean = dup.strip("* ").strip()
            if dup_clean and dup_clean not in updated_content:
                updated_content += f"| {dup_clean} | ? | {today} | Identificato da Ollama. |\n"

    # Aggiungi elementi non verificati (se non già presenti)
    if new_unverified:
        verify_section_exists = "## Errori Verificati" in updated_content
        if not verify_section_exists:
            updated_content += "\n## Errori Verificati\n\n"

        for item in new_unverified:
            item_clean = item.strip("* ").strip()
            if item_clean and item_clean not in updated_content:
                updated_content += f"| {item_clean} | {today} | Non verificato | Richiede verifica manuale. |\n"

    # Aggiorna timestamp (rimuovi righe vecchie e aggiungi nuove)
    updated_content = re.sub(r"Ultimo aggiornamento: .*\n", "", updated_content)
    updated_content = re.sub(r"Ultimo ciclo Ollama: .*\n", "", updated_content)

    # Aggiungi le nuove righe di timestamp dopo "Data creazione:"
    updated_content = re.sub(
        r"(Data creazione: [^\n]+\n)",
        f"\\1Ultimo aggiornamento: {today}\nUltimo ciclo Ollama: {today}\n",
        updated_content
    )

    # Salva il file
    os.makedirs(os.path.dirname(duplicates_file), exist_ok=True)
    with open(duplicates_file, "w", encoding="utf-8") as f:
        f.write(updated_content)

    return updated_content


def analyze_report_and_update_registry(report_markdown, current_registry, duplicates_and_errors_content):
    """Usa Ollama locale per analizzare il report, identificare duplicati, aggiornare registry."""

    prompt = f"""Analizza il report. LEGGI ATTENTAMENTE il file storico di doppioni e errori.

REGOLE:
- Elementi nel file 'Doppioni Identificati' → conteggia come duplicato, NON come nuovo
- Elementi nel file 'Errori Verificati' → marca come "da verificare", NON aggiungere al registry
- Aggiungi al registry SOLO elementi nuovi e verificati
- Aggiorna il registry con follow-up già noti (non contare come nuovo)
- ELENCA i doppioni identificati (per validazione successiva)

REPORT:
{report_markdown}

REGISTRY:
{current_registry}

FILE STORICO (Doppioni e Errori):
{duplicates_and_errors_content}

Rispondi così:
DUPLICATI: [numero]
DUPLICATI IDENTIFICATI:
* elemento 1
* elemento 2

NUOVI VERIFICATI:
* elemento 1
* elemento 2

DA VERIFICARE:
* elemento 1

REGISTRY UPDATE: [contenuto aggiornato]"""

    try:
        response = ollama.chat(
            model="llama2",
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = response.get("message", {}).get("content", "")

        # Parsing del formato testo strutturato da Ollama
        duplicates = 0
        identified_duplicates = []
        new_items = []
        unverified_items = []
        updated_registry = response_text

        # Estrai numero duplicati
        dup_match = re.search(r'DUPICRITI?:\s*(\d+)', response_text)
        if dup_match:
            duplicates = int(dup_match.group(1))

        # Parsing per sezioni
        in_dup_identified = False
        in_new_section = False
        in_verify_section = False

        for line in response_text.split('\n'):
            if 'DUPLICATI IDENTIFICATI' in line.upper():
                in_dup_identified = True
                in_new_section = False
                in_verify_section = False
                continue
            if 'NUOVI VERIFICATI' in line.upper():
                in_dup_identified = False
                in_new_section = True
                in_verify_section = False
                continue
            if 'DA VERIFICARE:' in line.upper():
                in_dup_identified = False
                in_new_section = False
                in_verify_section = True
                continue
            if 'REGISTRY UPDATE' in line.upper():
                in_dup_identified = False
                in_new_section = False
                in_verify_section = False
                continue

            if in_dup_identified and line.strip().startswith('*'):
                identified_duplicates.append(line.strip())
            elif in_new_section and line.strip().startswith('*'):
                new_items.append(line.strip())
            elif in_verify_section and line.strip().startswith('*'):
                unverified_items.append(line.strip())

        return {
            "duplicates_count": duplicates,
            "identified_duplicates": identified_duplicates,
            "new_items": new_items[:3],  # Top 3
            "unverified_items": unverified_items,
            "updated_registry": updated_registry,
            "notes": f"Analyzed by Ollama llama2"
        }
    except Exception as e:
        print(f"[ERRORE] Ollama: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    print("=" * 80)
    print("Luxury Hospitality Italia — Daily Report Sync")
    print(f"Data/ora: {datetime.now().isoformat()}")
    print("=" * 80)

    print("\n[1/4] Ricerca report Word...")
    report_file = find_latest_report()
    if not report_file:
        print("[FAIL] Nessun report Word trovato")
        sys.exit(1)
    print(f"[OK] Trovato: {report_file.name}")

    print("[2/4] Lettura contenuto...")
    report_content = read_word_file(report_file)
    if not report_content:
        print("[FAIL] Errore lettura")
        sys.exit(1)
    print(f"[OK] Report letto ({len(report_content)} bytes)")

    print("[3/4] Lettura registry...")
    registry_content = read_registry(REGISTRY_FILE)
    print("[OK] Registry letto")

    print("[3.5/4] Lettura file storico (doppioni/errori)...")
    duplicates_and_errors = read_duplicates_and_errors(DUPLICATES_AND_ERRORS_FILE)
    print("[OK] File storico letto")

    print("[4/4] Analisi duplicati (Ollama)...")
    result = analyze_report_and_update_registry(report_content, registry_content, duplicates_and_errors)

    if not result:
        print("[FAIL] Errore analisi")
        sys.exit(1)

    print("\n[UPDATE] Aggiornamento file storico (doppioni/errori)...")
    updated_duplicates = update_duplicates_and_errors_file(DUPLICATES_AND_ERRORS_FILE, result, duplicates_and_errors)
    print("[OK] File storico aggiornato")

    print("[UPDATE] Aggiornamento registry...")
    updated_registry = result.get("updated_registry", "")
    if updated_registry:
        update_registry_file(REGISTRY_FILE, updated_registry)
        print("[OK] Registry aggiornato")
    else:
        print("[WARN] Nessun cambio")

    print("\n" + "=" * 80)
    print("RISULTATI OLLAMA")
    print("=" * 80)
    print(f"Duplicati identificati: {result.get('duplicates_count', 0)}")
    if result.get('identified_duplicates'):
        for dup in result.get('identified_duplicates', []):
            print(f"  [DUP] {dup}")
    print(f"\nNuovi verificati: {len(result.get('new_items', []))}")
    if result.get('new_items'):
        for item in result.get('new_items', []):
            print(f"  [NEW] {item}")
    if result.get('unverified_items'):
        print(f"\nDa verificare: {len(result.get('unverified_items', []))}")
        for item in result.get('unverified_items', []):
            print(f"  [CHECK] {item}")
    print(f"\nNote: {result.get('notes', 'N/A')}")
    print("=" * 80)

    print("\n" + "=" * 80)
    print("AGGIORNAMENTI FILE STORICO")
    print("=" * 80)
    print(f"Doppioni aggiunti: {len(result.get('identified_duplicates', []))}")
    print(f"Elementi da verificare aggiunti: {len(result.get('unverified_items', []))}")
    print("[OK] File storico aggiornato e pronto per la prossima routine")
    print("=" * 80)
    print("\n[OK] Sync completato")


if __name__ == "__main__":
    main()
