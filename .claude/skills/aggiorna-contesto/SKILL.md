---
name: aggiorna-contesto
description: Raccoglie tramite domande le informazioni necessarie per aggiornare il contesto del workspace (CLAUDE.md e i file in context/), propone un piano di modifica completo e lo applica solo dopo l'approvazione esplicita di Giampaolo. Se non approvato, non modifica nulla. Usare quando si vuole registrare una nuova regola, preferenza, informazione stabile o cambiamento di contesto.
argument-hint: [descrizione libera di cosa aggiornare, opzionale]
---

# Aggiorna contesto

Skill per mantenere aggiornati `CLAUDE.md` e i file dentro `context/` (e i loro equivalenti locali) in modo strutturato e sicuro: raccoglie l'informazione tramite domande, decide dove e come inserirla, mostra il piano completo e lo applica solo dopo l'approvazione esplicita. Se Giampaolo non approva, non modifica nulla.

## 1. Punto di partenza

Se Giampaolo ha già indicato l'informazione o la richiesta nel comando (es. "/aggiorna-contesto d'ora in poi rispondi sempre in tono più diretto"), partire da quella. Se invece la skill è invocata senza indicazioni, chiedere: "Cosa vuoi che aggiorni o ricordi?" e attendere la risposta prima di procedere.

## 2. Raccolta delle informazioni (una domanda alla volta)

Fare solo le domande necessarie, una alla volta, solo quelle il cui esito cambia realmente dove o come scrivere l'informazione — non un questionario fisso. Le domande servono a stabilire:

- **Natura**: è una regola o preferenza stabile da ricordare sempre, o serve solo per la richiesta corrente? Se serve solo ora, fermarsi e dirlo: non c'è nulla da aggiornare nel contesto.
- **Ambito**: è generale (vale ovunque), specifica di un'area (Lavoro, Email, social, ecc.), di un progetto locale, oppure temporanea o riservata?
- **Tipo**: è una correzione di comportamento, un fatto o una decisione di progetto, un riferimento a un sistema esterno, o un dato identitario/di preferenza stabile?

Non fare domande il cui esito è già deducibile leggendo i file esistenti: prima di chiedere, verificare da sé cosa è già scritto e se l'informazione integra, aggiorna, sostituisce o confligge con qualcosa di presente.

## 3. Individuazione della destinazione

In base alle risposte, determinare quale file aggiornare, seguendo la struttura già stabilita in `CLAUDE.md`:

- Contesto universale (`@context/...` in CLAUDE.md): identità, metodo di lavoro, tono di voce, comunicazione staff/fornitori, modalità di interazione, preferenze tecniche, documenti/allegati.
- Contesti specialistici non auto-caricati: opportunità professionali, networking/social, minute HOD, budget e controllo di gestione, registro interlocutori.
- `Lavoro/CLAUDE.md` o il relativo `context.md` locale, se riguarda un'area operativa specifica del resort.
- Il `context.md` di un progetto locale (es. `Email/`), se riguarda solo quel progetto.
- Il dossier riservato, solo se il dato è economico, contrattuale o familiare e serve concretamente a valutare un'opportunità professionale.
- `CLAUDE.md` principale, solo per cambiamenti strutturali del workspace stesso (nuove cartelle, nuove convenzioni, nuovi rimandi a skill) — mai per contenuti che appartengono più correttamente a un file di `context/`.

Se non è chiaro quale sia il file giusto, o l'informazione potrebbe stare in più posti, chiedere a Giampaolo invece di scegliere da sola.

## 4. Piano di modifica (obbligatorio, prima di scrivere qualunque cosa)

Prima di modificare qualunque file, mostrare a schermo un piano completo con:

- il file (o i file) che verranno modificati;
- il contenuto esatto che verrà aggiunto, cambiato o rimosso (mostrare il testo, non solo descriverlo);
- il motivo della scelta di quella destinazione;
- eventuali duplicazioni, sovrapposizioni o conflitti individuati con contenuti già presenti, e come vengono risolti;
- se la modifica riscrive integralmente un file esistente, segnalare esplicitamente ogni riga o sezione che verrebbe rimossa.

## 5. Approvazione obbligatoria

Non modificare alcun file finché Giampaolo non approva esplicitamente il piano. Se chiede modifiche, aggiornare la proposta e richiedere di nuovo l'approvazione, senza scrivere nulla nel frattempo. Se rifiuta il piano, non cambiare niente e chiudere senza ulteriori azioni.

## 6. Applicazione

Solo dopo l'approvazione, applicare esattamente le modifiche mostrate nel piano — non introdurre variazioni rispetto a quanto approvato. Al termine, confermare cosa è stato modificato e dove si trova, così Giampaolo sa dove ritrovarlo o aggiornarlo in futuro.

## Cosa non fare

- Non modificare mai `CLAUDE.md` o i file di `context/` (o i loro equivalenti locali) senza il piano approvato al punto 4.
- Non creare file di test, bozze o copie di verifica: solo le modifiche reali ai file di destinazione, una volta approvate.
- Non duplicare un'informazione già presente altrove senza una ragione concreta e approvata — se esiste già, proporre di aggiornarla lì invece di crearne una nuova.
- Non toccare il dossier riservato per informazioni che non riguardano concretamente la valutazione di un'opportunità professionale specifica.
