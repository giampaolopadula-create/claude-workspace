---
name: sintesi-allegato
description: Legge un file Word/PDF oppure il link di una pagina web (articolo, newsletter, blog) e ne produce una sintesi chiara e ben scritta, salvata come nuovo documento Word. Solo la sintesi, nessuna raccomandazione o analisi aggiuntiva. Usare quando si chiede di riassumere o sintetizzare un allegato, un PDF, un documento Word o il link di un sito/articolo.
argument-hint: [percorso del file o URL da sintetizzare, opzionale se già chiaro dal contesto]
---

# Sintesi di un file, allegato o pagina web

Produce una sintesi di una singola fonte: un file Word/PDF locale, oppure il link di una pagina web (articolo, newsletter, blog post). Nient'altro: non un'analisi, non una raccomandazione, non un confronto con altri documenti o fonti — solo una bella sintesi di quello che la fonte dice.

## 1. Individuare la fonte

Due casi:

- **File locale**: se Giampaolo non indica un percorso esplicito, cercarlo in `Email/Allegati-da-analizzare/` (dove normalmente carica gli allegati da elaborare). Se ci sono più file recenti e non è chiaro a quale si riferisca, chiedere prima di procedere invece di indovinare.
- **Link web**: se Giampaolo incolla un URL, la fonte è quella pagina. Non serve che sia salvata da nessuna parte prima.

## 2. Lettura della fonte

Leggere la fonte integralmente prima di scrivere la sintesi — mai sintetizzare da un'anteprima parziale.

- Per i PDF, usare `scripts/read_docx.py` (se il file è in realtà un Word) o l'estrazione testo appropriata; se il PDF è scansionato/immagine, leggerlo pagina per pagina.
- Per un link web, recuperare e leggere il contenuto reale della pagina (non basarsi solo sull'anteprima del link o sui parametri dell'URL). Se la pagina è un archivio/newsletter con più elementi, sintetizzare il contenuto effettivo dell'articolo/edizione indicata, non l'intero archivio.
- Se una parte della fonte è illeggibile, mancante, tagliata, dietro paywall/login o altrimenti non accessibile, segnalarlo esplicitamente nella sintesi invece di ometterlo in silenzio o inventare contenuto.

## 3. Cosa scrivere

Una sintesi fedele al contenuto della fonte: di cosa tratta, i punti principali, i dati o fatti rilevanti, la struttura logica se ne ha una (es. capitoli, sezioni, proposte). Deve essere leggibile da sola, senza bisogno di aprire il documento o il link originale per capire di cosa parla. Per un articolo/newsletter, includere anche autore e testata/sito quando disponibili.

Non aggiungere: opinioni, raccomandazioni, giudizi, confronti con altri documenti o contesti, prossimi passi. Se la fonte stessa contiene conclusioni o raccomandazioni dell'autore, riportarle come tali (fanno parte del contenuto), distinguendole chiaramente da fatti o dati.

## 4. Eccezione — solo per "Job in Tourism"

Questa è l'unica eccezione alla regola "solo sintesi, nient'altro", e riguarda esclusivamente la pubblicazione periodica "Job in Tourism" (riconoscibile dal nome del file, tipicamente "Job in Tourism - anno [numero romano] numero [N]"), che Giampaolo riceve circa ogni settimana. Non si applica ad altri bollettini o riviste di annunci di lavoro, anche se contengono offerte simili: solo a "Job in Tourism".

Per questo specifico documento, aggiungere una sezione dedicata:

> **Opportunità Direttore / General Manager**

che indica **sempre**, esplicitamente, se tra gli annunci compaiono posizioni di Direttore d'albergo o General Manager: se ci sono, elencarle con struttura e riferimento per candidarsi; se non ci sono, scriverlo comunque (es. "Nessuna posizione da Direttore o General Manager in questo numero.") invece di ometterlo. Per "Job in Tourism" questa sezione compare sempre, in un senso o nell'altro.

Non menzionare mai questo argomento (né in un senso né nell'altro) per nessun altro documento — report, libri, articoli, contratti, né altri bollettini di annunci di lavoro: solo per "Job in Tourism".

## 5. Take away principali (sempre l'ultima sezione, in ogni sintesi)

Ogni sintesi, qualunque sia il documento, si chiude — dopo l'eventuale sezione Direttore/General Manager — con una sezione:

> **Take away principali**

un elenco puntato (3-6 punti) dei concetti più importanti da memorizzare del documento — non un riassunto ulteriore, ma la selezione di ciò che vale la pena ricordare anche senza rileggere tutto. Vale per qualunque tipo di documento sintetizzato con questa skill, ed è sempre l'ultima sezione.

## 6. Stile

Sintetico ma completo, frasi chiare, nessun linguaggio gonfiato o da consulenza generica — stesso registro usato normalmente per i riepiloghi di lavoro. Usare titoletti o elenchi puntati solo se aiutano davvero la lettura, non per riempire spazio.

## 7. Output

- **File locale**: salvare la sintesi come nuovo documento Word (`.docx`) nella stessa cartella del file originale, con nome `[nome file originale] - Sintesi - [data odierna].docx`. Non sovrascrivere né modificare il file originale.
- **Link web**: salvare la sintesi in `Email/Allegati-da-analizzare/`, con nome `[titolo dell'articolo o della pagina] - Sintesi - [data odierna].docx`. Se il titolo è troppo lungo, accorciarlo mantenendolo riconoscibile.

Se esiste già una sintesi con lo stesso nome, chiedere conferma prima di sovrascriverla invece di farlo automaticamente.

## Cosa non fare

- Non creare file di test, di verifica o bozze intermedie: solo il documento di sintesi finale.
- Non produrre altri output (riepiloghi in chat, Artifact, tabelle di analisi) a meno che Giampaolo lo chieda esplicitamente in aggiunta.
- Non usare questa skill al posto di `/email` quando la richiesta riguarda la gestione completa di una pratica e-mail: qui l'obiettivo è solo sintetizzare un documento, non ricostruire una conversazione o preparare una risposta.
