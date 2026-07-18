---
name: gm-mail
description: Carica esplicitamente il contesto locale di un'area del workspace (Lavoro, Email) in qualsiasi momento della conversazione, anche quando il caricamento automatico non è ancora scattato. Usare quando l'argomento richiede contesto locale (es. rispondere a una mail che riguarda temi alberghieri) senza necessariamente leggere un file di quella cartella.
argument-hint: [lavoro|email|lavoro email]
---

# Carica contesto

Carica esplicitamente il contesto locale di una o più aree del workspace, a prescindere dal caricamento automatico.

## Variabili

area: $ARGUMENTS (una o più tra: lavoro, email — separate da spazio)

## Istruzioni

### Caso 1: nessun argomento

Carica entrambe le aree di default (Lavoro ed Email), senza chiedere quale.

### Caso 2: area specificata

Per ciascuna area indicata, leggi il relativo CLAUDE.md locale:
- `lavoro` → leggi `Lavoro/CLAUDE.md` (importa stile manageriale e contesto alberghiero)
- `email` → leggi `Email/CLAUDE.md` (importa le regole operative e-mail)

Se un'area non è riconosciuta, segnalalo ed elenca quelle disponibili.

### Conferma

Dopo il caricamento, conferma brevemente cosa è stato caricato (una riga per area), senza mostrare il contenuto integrale dei file.
