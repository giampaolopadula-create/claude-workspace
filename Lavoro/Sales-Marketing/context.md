# Luxury Hospitality Report — Contesto Operativo

## Flusso Quotidiano del Sistema (Semplificato)

Il sistema funziona con un ciclo quotidiano semplice e affidabile:

**Routine Claude (03:00 IT)**
- Genera report giornaliero sulle opportunità luxury hospitality
- Salva report su Google Drive nella cartella "Luxury Hospitality Reports"
- Nome standardizzato: `Luxury Hospitality Italia - YYYY-MM-DD.docx`
- Invia notifica email quando completo

**Giampaolo scarica e legge il report**
- Scarica il file da Google Drive (manualmente o con script semplice)
- Legge il report con calma durante la giornata
- Identifica: doppioni, errori, informazioni non verificate

**Claude legge report + file storico**
- Legge il report generato dalla routine
- Legge il file storico `luxury-hospitality-duplicates-and-errors.md`
- Identifica e comunica i DOPPIONI (elementi già visti prima)

**Giampaolo comunica le inesattezze**
- Comunica a Claude: "Questo è un doppione", "Questo è sbagliato", "Questo è non verificato"

**Claude aggiorna il file storico**
- Incorpora i doppioni identificati
- Incorpora le inesattezze comunicate da Giampaolo
- File storico è pronto per il ciclo successivo

**Ciclo si ripete il giorno dopo**
- Routine Claude legge il file storico aggiornato
- Genera nuovo report tenendo conto dei doppioni noti

## Il File Storico è il Cervello del Sistema

**File:** `Lavoro/Sales-Marketing/luxury-hospitality-duplicates-and-errors.md`

**Consultato da:**
- Routine Claude (prima di generare il report — legge i doppioni noti per evitare ridondanze)
- Claude (durante la validazione — per identificare cosa è nuovo vs. cosa è già noto)

**Aggiornato da:**
- Claude (automaticamente, con i doppioni identificati e le inesattezze comunicate da Giampaolo)

**Contenuto:**
- Sezione "Doppioni Identificati": elementi già segnalati che NON si ripropongono
- Sezione "Errori Verificati": informazioni non verificate o sbagliate

**Principio:** Il sistema si auto-corregge ad ogni ciclo perché:
1. Routine legge il file storico e evita ridondanze
2. Claude identifica i doppioni e li comunica
3. Giampaolo verifica e comunica errori
4. Il file storico si arricchisce e diventa sempre più accurato

## File e Componenti

- **Routine:** "Report Luxury Hospitality Italia - giornaliero 03:00 IT" (Claude Cloud)
- **Prompt routine:** `Lavoro/Sales-Marketing/routine-prompt-finale.md` (versione semplificata, senza Ollama)
- **File storico:** `Lavoro/Sales-Marketing/luxury-hospitality-duplicates-and-errors.md`
- **Registry pulito:** `Lavoro/Sales-Marketing/luxury-hospitality-report-registry.md`

## Responsabilità

| Chi | Quando | Cosa |
|-----|--------|------|
| Routine Claude | 03:00 IT | Legge file storico, genera report, salva su Drive, invia notifica |
| Giampaolo | Mattina/Giornata | Scarica report, legge, identifica inesattezze |
| Claude | Dopo lettura di Giampaolo | Legge report + file storico, identifica doppioni, riceve inesattezze da Giampaolo |
| Claude | Finale | Aggiorna file storico (doppioni + inesattezze) |

## Tempistiche

- **03:00 IT:** Routine genera e salva report (~5 minuti)
- **Mattina/Giornata:** Giampaolo legge report (~15-30 minuti)
- **Pomeriggio:** Claude valida + Giampaolo comunica inesattezze (~10 minuti totali)
- **Giornata:** Claude aggiorna file storico (~2 minuti)

**Totale: 30-45 minuti per un ciclo completo, altamente affidabile.**

## Perché questo flusso funziona

1. **Semplice:** Niente Ollama lento o instabile — solo generazione + lettura manuale
2. **Veloce:** Meno di un'ora per un ciclo completo
3. **Affidabile:** Umano verifica umano (Giampaolo) + Claude per il tracciamento
4. **Automatizzato:** La routine gira da sola, Giampaolo legge quando ha tempo
5. **Auto-correttivo:** Il file storico diventa sempre più accurato ad ogni ciclo
