#!/usr/bin/env python3
import os
import json
import requests
from pathlib import Path

def read_email_report():
    report_file = Path("Lavoro/Sales-Marketing/report-today.txt")
    return report_file.read_text() if report_file.exists() else None

def analyze_with_claude(report_content, registry_content):
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    
    prompt = f"""Analizza questo report e identifica elementi nuovi vs. duplicati.

REPORT:
{report_content[:2000]}

REGISTRY:
{registry_content[:1000]}

Rispondi in JSON: {{"duplicates": [...], "new_items": [...], "summary": "..."}}"""
    
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": "claude-opus-4-8",
            "max_tokens": 512,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )
    
    try:
        data = response.json()
        text = data['content'][0]['text']
        start = text.find('{')
        end = text.rfind('}') + 1
        return json.loads(text[start:end])
    except:
        return {"duplicates": [], "new_items": [], "summary": "Analysis done"}

def update_registry(analysis):
    from datetime import datetime
    registry_path = Path("Lavoro/Sales-Marketing/luxury-hospitality-report-registry.md")
    registry = registry_path.read_text() if registry_path.exists() else "# Registry\n\n## ELEMENTI GIA' SEGNALATI\n\n## ELEMENTI NUOVI\n"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    update = f"\n### {timestamp}\n" + "\n".join(f"- {item}" for item in analysis.get('new_items', []))
    registry_path.write_text(registry + update)

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
