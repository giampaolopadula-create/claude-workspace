---
name: load-project
description: Carica il contesto di un progetto specifico nella sessione leggendo il suo context.md. Usare quando si vuole lavorare su un progetto specifico in projects/ e si ha bisogno di caricare il suo contesto, oppure quando si vuole creare un nuovo context.md per un progetto che ne è sprovvisto.
---

# Load Project

Carica il contesto di un progetto specifico nella sessione.

## Variabili

progetto: $ARGUMENTS (nome della cartella del progetto, es. `podcast`)

---

## Istruzioni

### Caso 1: Nessun argomento fornito

Se l'utente non ha specificato un nome di progetto:

1. Elenca tutte le cartelle presenti in `projects/`
2. Chiedi all'utente quale progetto vuole caricare

### Caso 2: Progetto specificato

Se l'utente ha specificato un nome di progetto:

1. **Verifica che la cartella esista:** Controlla se esiste `projects/{progetto}/`
   - Se la cartella non esiste, avvisa l'utente che il progetto non è stato trovato, elenca i progetti disponibili e chiedi quale intendeva

2. **Verifica che il context.md esista:** Controlla se esiste `projects/{progetto}/context.md`
   - Se esiste: vai allo step 3
   - Se non esiste: vai al Caso 3

3. **Carica il contesto:** Leggi il file `projects/{progetto}/context.md`

4. **Conferma:** Comunica all'utente che il contesto del progetto è stato caricato, mostrando un breve riepilogo del contenuto (titolo del progetto e sezioni principali)

### Caso 3: context.md mancante

Se la cartella del progetto esiste ma non ha un file `context.md`:

1. Avvisa l'utente che il progetto esiste ma non ha un file di contesto
2. Chiedi se vuole crearne uno
3. Se l'utente conferma:
   - Chiedi una breve descrizione del progetto (nome, formato, temi, obiettivi)
   - Crea il file `projects/{progetto}/context.md` con le informazioni raccolte, seguendo la struttura dei context.md esistenti (vedi `projects/podcast/context.md` come riferimento)
   - Conferma la creazione e il caricamento
4. Se l'utente rifiuta: fermati e comunica che il progetto è stato caricato senza contesto
