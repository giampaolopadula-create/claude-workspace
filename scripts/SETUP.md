# Luxury Hospitality Italia — Automazione Daily Sync

Setup per l'automazione giornaliera del Luxury Hospitality Italia report (03:30 IT).

## Cosa fa

Ogni giorno alle 03:30 IT:
1. Legge l'email del report da Gmail (subject: "Report Luxury Hospitality Italia - giornaliero 03:00 IT — routine completed")
2. Analizza il report con Claude
3. Identifica i duplicati confrontando con il registry
4. Aggiorna il file `Lavoro/Sales-Marketing/luxury-hospitality-report-registry.md`
5. Fa commit automatico su GitHub

## Setup (5 minuti)

### 1. Google OAuth — Credenziali Gmail

1. Vai a https://console.cloud.google.com/
2. Crea un nuovo progetto (oppure usane uno esistente)
3. Abilita **Gmail API**:
   - Vai a "APIs & Services" → "Library"
   - Cerca "Gmail API" → "Enable"
4. Crea OAuth 2.0 credentials (tipo "Desktop application"):
   - "APIs & Services" → "Credentials"
   - "Create Credentials" → "OAuth 2.0 Client ID"
   - Tipo: "Desktop application"
   - Scarica il JSON file (file → "Download as JSON")

### 2. Autorizzazione Gmail (autenticazione 1 volta)

Esegui questo comando **una sola volta** dal tuo computer (non in GitHub Actions):

```bash
python scripts/authorize-gmail.py "<path-al-json-scaricato>"
```

Lo script:
- Apre il browser per autenticazione OAuth
- Salva le credenziali autorizzate in `scripts/google_credentials.json`

**Nota**: il file `google_credentials.json` contiene token sensibili — **non committarlo su GitHub**. È già in `.gitignore`.

### 3. GitHub Secrets — Credenziali

Aggiungi le credenziali come GitHub Secrets:

1. Vai al tuo repo GitHub → Settings → Secrets and variables → Actions
2. Crea due secrets:

   **a) `ANTHROPIC_API_KEY`**
   - Vai a https://console.anthropic.com/
   - Crea un nuovo API key
   - Copia il valore
   - In GitHub: "New repository secret" → name: `ANTHROPIC_API_KEY` → paste value

   **b) `GOOGLE_CREDENTIALS`**
   - Apri il file `scripts/google_credentials.json` (creato al step 2)
   - Copia l'intero contenuto JSON
   - In GitHub: "New repository secret" → name: `GOOGLE_CREDENTIALS` → paste JSON

### 4. Test

Esegui il workflow manualmente la prima volta:

1. GitHub → Actions → "Luxury Hospitality Italia — Daily Sync"
2. "Run workflow" → "Run workflow"
3. Aspetta che finisca (≈2-3 min)
4. Verifica che il registry sia stato aggiornato

Se tutto va bene, il workflow si attiva automaticamente ogni giorno alle 03:30 IT.

## Troubleshooting

### "GOOGLE_CREDENTIALS not configured"
→ Verifica che il secret `GOOGLE_CREDENTIALS` esista su GitHub (Settings → Secrets)

### "ANTHROPIC_API_KEY not configured"
→ Verifica che il secret `ANTHROPIC_API_KEY` esista su GitHub

### "No email found"
→ Verifica che:
- La routine stia inviando il report con il subject esatto: "Report Luxury Hospitality Italia - giornaliero 03:00 IT — routine completed"
- L'email sia stata ricevuta negli ultimi giorni

### "Gmail API error: 'gmail' service not available"
→ Autorizza di nuovo: `python scripts/authorize-gmail.py <json-path>`

## Manutenzione

- **Ogni 7 giorni ca.**: l'autorizzazione Google potrebbe scadere. Se il workflow fallisce, ri-esegui l'autorizzazione (step 2).
- **Disabilitare temporaneamente**: disabilita il workflow da GitHub Actions (no change needed nel repo).

## File coinvolti

```
scripts/
  ├── luxury-hospitality-sync.py       (script principale)
  ├── authorize-gmail.py               (autorizzazione OAuth — esegui 1 volta)
  ├── requirements.txt                 (dipendenze)
  ├── google_credentials.json          (credenziali autorizzate — NON committare)
  └── SETUP.md                         (questo file)

.github/workflows/
  └── luxury-hospitality-sync.yml      (GitHub Actions workflow)

Lavoro/Sales-Marketing/
  └── luxury-hospitality-report-registry.md  (file aggiornato automaticamente)
```

## Note

- Il workflow gira su GitHub (server GitHub, non sul tuo computer)
- Puoi tenere il computer spento — GitHub esegue il task comunque
- I commit sono fatti da "Luxury Hospitality Sync" (bot)
- Non ci sono costi extra (GitHub Actions è gratuito per repo pubblici)
