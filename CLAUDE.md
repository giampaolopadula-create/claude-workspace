# Claude Workspace — Giampaolo Padula

General Manager, Valtur Cervinia Cristallo Ski Resort, hotel 5 stelle di 211 camere. Il workspace è diviso principalmente in **Lavoro** e **Vita privata**.

## Contesto universale

I seguenti file contengono informazioni e istruzioni valide nella generalità delle attività e devono essere caricati automaticamente:

@context/identita-profilo-professionale.md
@context/metodo-di-lavoro.md
@context/tono-voce-scrittura.md
@context/comunicazione-staff-fornitori-esterni.md
@context/modalita-interazione.md
@context/preferenze-tecniche-claude-code.md
@context/documenti-allegati-fonti.md

## Contesto professionale locale

Quando si lavora direttamente su file presenti dentro `Lavoro/` o in una sua sottocartella, Claude Code carica automaticamente anche `Lavoro/CLAUDE.md`, che importa il contesto relativo allo stile manageriale e al luxury hospitality.

Quando invece una richiesta riguarda chiaramente la gestione alberghiera, lo staff, i reparti, le operazioni del resort o altre attività professionali, ma viene svolta dalla root senza accedere a file presenti dentro `Lavoro/`, leggere integralmente prima di produrre il risultato:

- [stile-manageriale.md](context/stile-manageriale.md)
- [contesto-alberghiero.md](context/contesto-alberghiero.md)

Il file `Lavoro/CLAUDE.md` resta il meccanismo automatico utilizzato quando si lavora direttamente dentro `Lavoro/` o nelle sue sottocartelle.

## Contesti specialistici

I seguenti file non sono importati automaticamente. Devono essere letti integralmente prima di produrre il risultato quando la richiesta rientra chiaramente nel relativo ambito:

- Per valutazioni di carriera, candidature, head hunter, incarichi di advisory o consulenze: [opportunita-professionali.md](context/opportunita-professionali.md)
- Per LinkedIn, Instagram, messaggi di networking e contenuti professionali sui social: [networking-social.md](context/networking-social.md)
- Per minute delle riunioni HOD e relativi follow-up: [minute-riunioni-hod.md](workflows/minute-riunioni-hod.md)
- Per report di budget e controllo di gestione: [report-budget-controllo-gestione.md](workflows/report-budget-controllo-gestione.md)
- Per attività di lettura, ricostruzione e preparazione di risposte alle e-mail avviate dalla root, leggere integralmente [Email/context.md](Email/context.md) prima di produrre il risultato. Quando si lavora direttamente dentro `Email/`, il file `Email/CLAUDE.md` importa automaticamente il relativo `context.md`. Per elaborare una nuova pratica e-mail, utilizzare sempre la skill `/email [oggetto o argomento]`. Non avviare il workflow e-mail con una richiesta generica quando è disponibile la skill.
- Prima di preparare una comunicazione destinata a una persona specifica, verificare se esistono indicazioni dedicate in [registro-interlocutori.md](context/registro-interlocutori.md).

## Dossier riservato

Il file:

`Vita privata/Lavoro privato/Ricerca opportunità/opportunita-professionali-riservate.md`

contiene dati economici, contrattuali e familiari utili alla valutazione di opportunità professionali.

Non è caricato automaticamente. Deve essere consultato soltanto quando il compito riguarda concretamente la valutazione, il confronto o la negoziazione di un'opportunità professionale specifica.

Prima di utilizzare informazioni contenute nel dossier, verificarne la data di aggiornamento e chiedere conferma a Giampaolo quando il dato potrebbe essere cambiato.

## Contesti locali di progetto

Alcune cartelle operative possono contenere:

- un `CLAUDE.md` locale;
- un file `context.md` specifico del progetto.

Il `CLAUDE.md` locale importa il relativo contesto tramite:

@context.md

Il file `context.md` deve contenere esclusivamente informazioni specifiche del progetto, come obiettivi, situazione attuale, interlocutori, decisioni, vincoli, scadenze, attività aperte e documenti di riferimento.

Non deve duplicare le informazioni già presenti nel contesto generale.

Questi file non devono essere creati automaticamente. Prima di crearli o modificarli:

1. verificare se esiste già una cartella adeguata;
2. proporre struttura e contenuto;
3. fare eventuali domande una alla volta;
4. attendere sempre l'approvazione di Giampaolo.

## Convenzione di naming

- Le cartelle operative già esistenti, incluse `Lavoro/`, `Vita privata/` e tutte le loro sottocartelle, mantengono la denominazione attuale.
- Non rinominare, spostare o eliminare file e cartelle esistenti senza approvazione esplicita.
- I nuovi file Markdown creati dentro `context/` e `workflows/` utilizzano nomi minuscoli, senza accenti o caratteri speciali, con parole separate da trattini.
- Non creare nuove cartelle di primo livello senza aver prima ottenuto l'approvazione di Giampaolo.

## Struttura Lavoro

La cartella `Lavoro/` contiene le principali aree operative del resort, tra cui:

- Rooms
- F&b
- Operations
- Spa
- Entertainment
- Accounting

Ogni area può contenere proprie sottocartelle, documenti, HOD, attività ricorrenti e progetti specifici.

## Regole generali

- Il file `CLAUDE.md` principale non deve mai essere aggiornato automaticamente.
- Quando emerge una nuova informazione, applicare le regole presenti in `context/modalita-interazione.md`.
- Se una nuova informazione potrebbe richiedere l'aggiornamento del contesto, indicare il file corretto, mostrare la modifica proposta e attendere l'approvazione.
- Non duplicare la stessa informazione in più file senza una ragione concreta e approvata.
- Non ampliare i file soltanto per renderli più completi: ogni contenuto deve avere una reale utilità operativa.
- Prima di dichiarare conclusa un'attività tecnica, verificare che il risultato sia coerente con la richiesta e che i riferimenti ai file siano validi.
- Prima di riscrivere integralmente (Write) un file CLAUDE.md o un file in `context/` già esistente, confrontare sempre il contenuto nuovo con quello attuale e segnalare esplicitamente ogni riga o sezione che verrebbe rimossa. Non sostituire mai un file interamente basandosi solo sulla coerenza interna del nuovo contenuto.
