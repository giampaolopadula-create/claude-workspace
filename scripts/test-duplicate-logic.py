#!/usr/bin/env python3
"""Test del nuovo prompt per escludere SOLO news duplicate, non contatti"""

import json
from anthropic import Anthropic

# Registry dal 17 luglio (quello che Claude ha)
registry_content = """# Registro — Luxury Hospitality Italia
**Ultimo aggiornamento**: 17 luglio 2026

## ELEMENTI GIA' SEGNALATI

### Leadership Movements (già segnalati)
- **Danilo Guerrini** → GM Romazzino, Belmond (Costa Smeralda) — annunciato 10 luglio
- **Veronica Milo** → GM Vivosa Apulia Resort — 8 giugno 2026

### Progetti (già segnalati)
- **Gran Baita Cervinia**: demolizione avviata 3 giugno 2026, apertura fine 2028
- **FH55 Grand Hotel Palatino (Roma)**: fase 2 lavori avviata
- **Hotel Bellevue Cortina d'Ampezzo**: GM vacancy live, fine 2026

### Contatti
- Claudio Catani (VP Operations, FH55)
- Claudio Ceccherelli (Le Graal)
"""

# Report di DOMANI (18 luglio) - con MIX di duplicati e nuove notizie
report_today = """REPORT 18 LUGLIO 2026

P1 - AZIONE IMMEDIATA
Hotel Bellevue Cortina d'Ampezzo: GM vacancy live, fine 2026 — candidature aperte su careers.accor.com
[NOTA: Bellevue era nel 17 luglio come "GM vacancy", ma OGGI il report dice "candidature aperte" = NUOVA INFO]

P2 - ALTA PRIORITÀ
Danilo Guerrini: da GM Romazzino passa a CEO Belmond Luxury Experiences (promozione a livello group)
[NOTA: Danilo era nel 17 luglio come "GM Romazzino", ma OGGI è "promozione a CEO" = NUOVA NEWS sullo stesso contatto]

Danilo Guerrini: nuovo GM Romazzino, Belmond Costa Smeralda
[NOTA: Questo è IDENTICO al 17 luglio = DUPLICATO VERO, escludere]

P3 - MONITORAGGIO
Gran Baita Cervinia: cantiere avviato da 3 giugno, fondamenta completate
[NOTA: Gran Baita era nel 17 luglio come "demolizione avviata", OGGI "fondamenta completate" = PROGRESSO NUOVO]

Gran Baita Cervinia: demolizione avviata 3 giugno 2026, apertura fine 2028
[NOTA: Questo è IDENTICO al 17 luglio = DUPLICATO VERO, escludere]

FOLLOW-UP NUOVO
Hotel Summit Dolomiti (nuovo progetto): 180 camere, 5 stelle lusso, apertura 2027, GM ricercato
[NOTA: Completamente NUOVO, mai visto prima = INCLUDERLO]

Claudio Ceccherelli (Le Graal): lanciato nuovo resort Cortina 150 camere
[NOTA: Claudio era mappato nel 17 luglio, ma QUESTO è una nuova opportunità = NUOVA NEWS]
"""

# Prompt NUOVO (con la logica corretta)
prompt = f"""Tu sei Claude, assistente di Giampaolo Padula per il Luxury Hospitality Italia report.

REPORT OGGI (18 LUGLIO):
{report_today}

REGISTRY ATTUALE (dal 17 luglio):
{registry_content}

COMPITO CRITICO - ESCLUDERE SOLO LE NEWS DUPLICATE, NON I CONTATTI:
1. LEGGI il registry e identifica le NOTIZIE GIA' SEGNALATE
2. CONFRONTA il report di oggi con il registry
3. ESCLUDI solo le notizie/eventi che sono IDENTICI a quelli nel registry
4. INCLUDI tutte le notizie NUOVE sullo stesso contatto/albergo
5. AGGIORNA il registry con SOLO le nuove notizie

REGOLA FONDAMENTALE (IMPORTANTE):
- "Danilo Guerrini → GM Romazzino" (17 luglio) = VECCHIA NEWS, non ripetere
- Ma "Danilo Guerrini → CEO Belmond" (18 luglio) = NUOVA NEWS sullo STESSO CONTATTO → VA INCLUSA!
- "Gran Baita Cervinia: demolizione avviata" (17 luglio) = VECCHIA NEWS
- Ma "Gran Baita Cervinia: fondamenta completate" (18 luglio) = NUOVO PROGRESSO → VA INCLUSO!

ESCLUDI DUPLICATI (notizia identica ripetuta):
- Stessa persona + stesso evento specifico + stesso timing = DUPLICATO
- Ma stesso contatto con NEWS DIVERSA = NUOVO

RISPONDI CON JSON:
{{
  "duplicates_count": <numero notizie escluse>,
  "new_items": [<SOLO notizie nuove, incluse quelle su contatti/alberghi già menzionati>],
  "updated_registry": "<registry completo con le nuove notizie>",
  "notes": "<quali notizie vecchie sono state escluse>"
}}"""

print("=" * 80)
print("TEST LOGIC: Escludere SOLO news duplicate, inclure notizie nuove su stessi contatti")
print("=" * 80)
print("\nRegistry (dal 17 luglio):")
print(registry_content)
print("\n" + "-" * 80)
print("\nReport OGGI (18 luglio) - con mix di duplicati e nuove notizie:")
print(report_today)
print("\n" + "-" * 80)
print("\nChiamando Claude con il NUOVO prompt...")
print("=" * 80 + "\n")

try:
    client = Anthropic()
    message = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text
    print("RISPOSTA DI CLAUDE:")
    print(response_text)

    # Estrai JSON
    import re
    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        result = json.loads(json_match.group())
        print("\n" + "=" * 80)
        print("VERIFICA RISULTATI:")
        print("=" * 80)
        print(f"✓ Duplicati identificati: {result.get('duplicates_count', '?')}")
        print(f"✓ Nuove notizie incluse: {len(result.get('new_items', []))}")

        print("\nNuove notizie incluse (dovrebbero essere le 4 NON-duplicate):")
        for item in result.get('new_items', []):
            print(f"  - {item}")

        print(f"\nNote di Claude: {result.get('notes', 'N/A')}")

        # Verifica manuale
        print("\n" + "=" * 80)
        print("VERIFICA MANUALE (quello che DOVREBBE succedere):")
        print("=" * 80)
        print("DUPLICATI DA ESCLUDERE (2):")
        print("  1. 'Danilo Guerrini: nuovo GM Romazzino' — identico al 17 luglio")
        print("  2. 'Gran Baita Cervinia: demolizione avviata 3 giugno' — identico al 17 luglio")
        print("\nNUOVE NOTIZIE DA INCLUDERE (4):")
        print("  1. 'Hotel Bellevue: candidature aperte' — NUOVA INFO su Bellevue")
        print("  2. 'Danilo Guerrini: promozione a CEO' — NUOVA NEWS su Danilo")
        print("  3. 'Gran Baita Cervinia: fondamenta completate' — PROGRESSO su Gran Baita")
        print("  4. 'Hotel Summit Dolomiti: nuovo progetto' — COMPLETAMENTE NUOVO")
        print("  5. 'Claudio Ceccherelli: nuovo resort Cortina' — NUOVA OPPORTUNITY")

except Exception as e:
    print(f"ERRORE: {e}")
    import traceback
    traceback.print_exc()
