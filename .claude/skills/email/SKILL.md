---
name: email
description: Analizza una pratica e-mail indicata da Giampaolo, ricostruisce lo storico e gli ultimi messaggi, produce sempre l'Artifact, la raccomandazione e la bozza di risposta.
argument-hint: [oggetto o argomento della mail]
disable-model-invocation: true
---

## Argomento della pratica

L'oggetto o argomento della pratica è:

$ARGUMENTS

Non iniziare l'analisi se non è stato indicato alcun argomento. In quel caso chiedere esclusivamente quale mail o pratica deve essere elaborata.

## Comportamento obbligatorio

Quando invocata con `/email $ARGUMENTS`, applicare sempre questa sequenza.

### 1. Caricamento delle regole

Leggere integralmente:

Email/context.md

prima di utilizzare gli strumenti Gmail o produrre qualsiasi risultato.

Leggere inoltre, quando pertinenti:

- context/tono-voce-scrittura.md
- context/comunicazione-staff-fornitori-esterni.md
- context/documenti-allegati-fonti.md
- context/registro-interlocutori.md
- context/metodo-di-lavoro.md

Non dichiarare di aver applicato Email/context.md se non lo hai realmente letto nella sessione corrente.

### 2. Nome della sessione

Il titolo della pratica è sempre l'oggetto indicato in $ARGUMENTS, riportato esattamente come scritto da Giampaolo: non abbreviare, non riformulare e non sostituirlo autonomamente con un titolo alternativo.

All'inizio dell'Artifact mostrare sempre entrambi i comandi già compilati:

Per rinominare ora la sessione:

/rename Email — $ARGUMENTS

Per ritrovare e riaprire la sessione in futuro:

/resume Email — $ARGUMENTS

Soltanto se l'oggetto non è stato indicato oppure è impossibile identificarlo, chiedere a Giampaolo quale oggetto utilizzare, invece di proporre un titolo alternativo.

Non rinominare autonomamente la sessione. Mostrare a Giampaolo il comando esatto da utilizzare.

### 3. Ricerca e-mail

Cercare la mail o la pratica indicata da $ARGUMENTS.

L'analisi deve dare priorità:

1. ai messaggi inviati o ricevuti oggi;
2. in assenza di messaggi odierni, agli ultimi messaggi del thread;
3. alle richieste, decisioni, modifiche e opinioni più recenti.

Consultare comunque lo storico necessario per comprendere:

- origine della pratica;
- decisioni già prese;
- risposte già fornite;
- impegni assunti;
- eventuali contraddizioni;
- punti ancora aperti.

Cercare anche conversazioni realmente collegate allo stesso argomento, pur con oggetto diverso. In caso di collegamento soltanto probabile, chiedere conferma prima di aggregarle.

### 4. Artifact sempre obbligatorio

Produrre sempre un Artifact, anche quando:

- la mail è breve;
- non ci sono allegati;
- Giampaolo è soltanto in copia;
- non sembra necessaria una risposta;
- la pratica appare semplice;
- viene richiesto soltanto un parere.

La semplicità del caso può ridurre la lunghezza dell'Artifact, ma non eliminarlo.

L'Artifact deve contenere sempre:

# Analisi e-mail — $ARGUMENTS

## Sessione

Per rinominare ora:

/rename Email — $ARGUMENTS

Per riprendere in futuro:

/resume Email — $ARGUMENTS

## Focus dell'analisi

- data completa dell'analisi;
- periodo complessivo consultato;
- messaggi di oggi analizzati;
- ultimi messaggi rilevanti;
- interlocutori;
- allegati disponibili.

## Ultimi aggiornamenti

Riassumere prioritariamente ciò che emerge oggi o negli ultimi messaggi:

- nuove richieste;
- nuovi pareri;
- nuove decisioni;
- modifiche rispetto al passato;
- scadenze;
- azioni necessarie.

## Contesto storico essenziale

Inserire soltanto ciò che serve per comprendere gli aggiornamenti recenti, senza ripetere l'intera conversazione.

## Cosa viene richiesto a Giampaolo

Indicare chiaramente se occorre:

- rispondere;
- decidere;
- approvare;
- esprimere un parere;
- prendere visione;
- non compiere alcuna azione.

## Posizioni espresse

Quando sono presenti pareri differenti:

- identificare chi sostiene ciascuna posizione;
- sintetizzare le motivazioni;
- valutarne vantaggi, limiti e rischi;
- indicare quale soluzione è preferibile e perché.

Non limitarsi a un riepilogo neutro.

## Raccomandazione

Fornire sempre una raccomandazione netta e motivata.

## Bozza di risposta

Preparare sempre una bozza, anche quando rispondere non è indispensabile.

In quel caso introdurla con:

"Risposta non indispensabile. Di seguito una bozza facoltativa, qualora Giampaolo desideri esprimere il proprio parere."

La bozza non deve attribuire a Giampaolo decisioni, promesse o impegni non ancora approvati.

## Allegati e punti aperti

Indicare:

- allegati presenti;
- contenuto realmente accessibile;
- allegati che Giampaolo dovrebbe leggere personalmente;
- informazioni mancanti;
- domande ancora aperte;
- elementi da verificare.

### 5. Verifica finale obbligatoria

Prima di consegnare il risultato, controllare esplicitamente che:

- siano presenti entrambi i comandi /rename e /resume;
- sia stato prodotto l'Artifact;
- sia presente una raccomandazione;
- sia presente una bozza, anche facoltativa;
- l'attenzione principale sia rivolta alle mail di oggi o agli ultimi messaggi;
- lo storico sia stato utilizzato senza appesantire il riepilogo;
- non siano stati interpretati come nuovi i messaggi precedenti citati nel thread;
- ogni affermazione sia coerente con il tempo verbale utilizzato nelle e-mail;
- la chiusura della bozza utilizzi "Grazie." oppure "Best,", mai entrambi;
- il registro Lei/tu corrisponda alle indicazioni eventualmente presenti nel registro degli interlocutori.

Se manca uno degli elementi obbligatori, correggere il risultato prima di mostrarlo.

## Vincoli

- Non inviare e-mail.
- Non creare bozze in Gmail.
- Non modificare messaggi, etichette, cartelle o stato di lettura.
- Non inventare informazioni.
- Non dichiarare di aver letto allegati non accessibili.
- Non omettere Artifact, /rename, /resume, raccomandazione o bozza perché il caso sembra semplice.
