# Nuovo Prompt per Routine Claude — Report Luxury Hospitality Italia

**Copia questo prompt nella routine:**
`Report Luxury Hospitality Italia - giornaliero 03:00 IT`

---

Genera un report quotidiano di opportunità nel luxury hospitality italiano (5 stelle, extra-lusso). Il report deve essere in formato Word (.docx) e deve essere salvato in Google Drive nella cartella "Luxury Hospitality Reports" con nome: `Luxury Hospitality Italia - [YYYY-MM-DD].docx`

CONTESTO:
- Analizza news, comunicati stampa, annunci pubblici dall'ultimo ciclo (ultimi 24 ore)
- Monitora leadership changes, project announcements, group expansions
- Includi dati verificabili da fonti pubbliche (non speculare)
- Scrivi in italiano

STRUTTURA DEL REPORT:

1. **Headline News (ultimi 24 ore)**
   - 3-5 notizie principali, ordinate per rilevanza operativa (GM direct relevance > group expansion > leadership movement > infrastructure)
   - Ogni voce: titolo, fonte(i), data, impatto per ricerca opportunità

2. **Aggiornamento Registro Storico**
   - Leggi il file: `Lavoro/Sales-Marketing/luxury-hospitality-duplicates-and-errors.md`
   - Includi TUTTI gli elementi dalla sezione "Doppioni Identificati" (con label "[FOLLOW-UP]" o "[AGGIORNAMENTO]")
   - Includi gli elementi della sezione "Errori Verificati" (con label "[DA VERIFICARE]")
   - Aggiungi eventuali nuovi aggiornamenti su voci già note (project timelines, leadership changes)
   - Nota: questa sezione è per continuità storica, NON per aggiungere nuovi elementi al registry

3. **Analisi Opportunità**
   - Headline news che comportano possibili aperture GM / leadership roles / advisory
   - Stima di probabilità (ALTA / MEDIA / BASSA)
   - Timeline realistica
   - Fonte e data dell'informazione

REGOLE CRITICHE:
- Niente speculazioni: solo news verificabili
- Se un elemento è in "Doppioni Identificati" nel file storico → NON contarlo come nuovo, ma includere aggiornamenti nella sezione 2
- Usa fonti pubbliche (TTG Italia, Hotellerie Pambianconews, BeBeez, comunicati ufficiali, LinkedIn pubblici)
- Data sempre l'informazione (data, fonte)
- Non includere voci che Giampaolo ha marcato come "non verificate" senza aggiungervi label "[DA VERIFICARE]"

FORMATO OUTPUT:
- File Word (.docx)
- Salva in Google Drive folder: "Luxury Hospitality Reports"
- Naming: `Luxury Hospitality Italia - YYYY-MM-DD.docx`
- Quando completo, invia notifica email a giampaolopadula@gmail.com

---

**ISTRUZIONI PER L'AGGIORNAMENTO:**
1. Accedi alla routine "Report Luxury Hospitality Italia - giornaliero 03:00 IT"
2. Sostituisci il prompt precedente con il testo sopra
3. Salva la routine
4. La routine continuerà a girare ogni giorno alle 03:00 IT con il nuovo prompt

Il file `luxury-hospitality-duplicates-and-errors.md` sarà letto automaticamente dalla routine ad ogni ciclo.
