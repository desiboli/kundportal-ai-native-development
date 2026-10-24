# Spec: Kärnan – skapa, lista, visa och validera ärenden (CORE)

> Status: **utkast v0.3** · v0.2 granskad och godkänd av Azalea (PR #5) · Ansvarig: Nicklas (yrrving) · Granskare: Azalea (Azaalea) · Vecka 5
> Detta dokument är teamets underlag. Individuell redovisning ligger inte här.
>
> Bygger på [Gemensamt · API-konventioner](https://linear.app/grupp6/document/gemensamt-api-konventioner-ac15fc1ff458)
> (statuskoder, felformat, tider, språk). Vid skillnad gäller API-konventionerna.
> Statuslogik och historik finns i [SPEC-arendehistorik.md](SPEC-arendehistorik.md) (HIST-id).


## 1. Objective

En handläggare ska kunna **registrera ett nytt kundärende**, se **en lista över alla ärenden** och öppna **detaljerna för ett valt ärende**. Felaktig inmatning ska stoppas med ett begripligt besked på svenska, utan att något sparas.

**Användare:** handläggare (en roll, ingen inloggning).

**Framgång:** ett ärende som registreras med giltiga uppgifter finns kvar i listan och i detaljvyn, även efter omstart. Ett ärende med felaktiga uppgifter sparas aldrig, och handläggaren förstår varför.

## 2. Avgränsning

| Ingår | Ingår inte |
| --- | --- |
| Ärendemodellen (tabellen `tickets`) | Statusändring (HIST, `PATCH /tickets/{id}/status`) |
| `POST /tickets` med validering | Historik (HIST) |
| `GET /tickets` (lista) | Redigering och radering av ärenden |
| `GET /tickets/{id}` (detaljer) | Sök och filtrering (Amalias tilläggsfunktion, egen spec) |
| Regler för obligatoriska fält, längder och tillåtna värden | Kunduppgifter som namn, e-post och telefon (beslut B6) |

## 3. Ärendemodell

| Fält | Typ | Obligatoriskt vid skapande | Regel |
| --- | --- | --- | --- |
| `id` | heltal | – (sätts av databasen) | |
| `title` | text | Ja | Trimmas. 1–**100** tecken efter trimning. |
| `description` | text | Ja | Trimmas. 1–**2000** tecken efter trimning. |
| `category` | kod | Ja | En av kategorikoderna nedan. |
| `priority` | kod | Ja | En av prioritetskoderna nedan. |
| `status` | kod | – (sätts av servern) | Alltid `new` vid skapande. Får inte skickas in. |
| `created_at` | tid | – (sätts av servern) | UTC i fast format enligt API-konventionerna |

**Hur tecken räknas:** längder räknas i Unicode-kodpunkter, som Pythons `len()`. Frontend räknar likadant (t.ex. `[...text].length`) och inte med `maxlength`, som räknar UTF-16-enheter. Annars kan formuläret godkänna en rubrik som API:t avvisar.

**Kategorier** (beslut B2)

| Kod (API/DB) | Etikett (UI) |
| --- | --- |
| `billing` | Faktura och betalning |
| `delivery` | Leverans |
| `technical` | Tekniskt problem |
| `account` | Konto |
| `other` | Övrigt |

**Prioriteter** (beslut B3)

| Kod (API/DB) | Etikett (UI) |
| --- | --- |
| `low` | Låg |
| `medium` | Medel |
| `high` | Hög |

## 4. API-kontrakt

| Metod och väg | Lyckat svar | Fel |
| --- | --- | --- |
| `POST /tickets` | 201, det skapade ärendet | 422 vid ogiltig indata, inget sparas |
| `GET /tickets` | 200, lista med alla ärenden, nyaste först (`created_at` fallande, sedan `id` fallande) | – |
| `GET /tickets/{id}` | 200, ärendet | 404 okänt ärende, även när id inte är ett heltal (beslut B8) |

```json
// POST /tickets
{ "title": "Fakturan har fel belopp", "description": "Kunden har fått dubbel debitering för oktober.", "category": "billing", "priority": "high" }

// -> 201
{ "id": 1, "title": "Fakturan har fel belopp", "description": "Kunden har fått dubbel debitering för oktober.",
  "category": "billing", "priority": "high", "status": "new", "created_at": "2026-10-25T09:00:00.000000Z" }

// -> 422
{ "detail": "Rubrik måste fyllas i." }
```

**Felmeddelanden** (svenska, formatet `{"detail": ...}` enligt API-konventionerna):

| Situation | Meddelande |
| --- | --- |
| Rubrik saknas eller är bara mellanslag | Rubrik måste fyllas i. |
| Rubrik för lång | Rubriken får vara högst 100 tecken. |
| Beskrivning saknas eller är bara mellanslag | Beskrivning måste fyllas i. |
| Beskrivning för lång | Beskrivningen får vara högst 2000 tecken. |
| Okänd eller saknad kategori | Välj en giltig kategori. |
| Okänd eller saknad prioritet | Välj en giltig prioritet. |
| Status skickas in | Status sätts automatiskt och kan inte anges när ett ärende skapas. |
| Fel datatyp (t.ex. `"title": 5`), saknad kropp eller trasig JSON | Ogiltig indata. |
| Okänt ärende eller id som inte är ett heltal | Ärendet finns inte. |

Om flera fält är fel samtidigt visas **alla** meddelanden, sammanfogade med mellanslag, i fältordningen rubrik, beskrivning, kategori, prioritet, status (beslut B7).

Undantag: om något fält har fel datatyp, eller kroppen saknas eller är trasig JSON, visas **bara** "Ogiltig indata.", utan fältmeddelanden (beslut B9).

## 5. Acceptanskriterier

Varje kriterium har ett id som används i tester, commits, PR:er och Linear-ärenden.

### Happy paths

**CORE-01** Givet giltig rubrik, beskrivning, kategori och prioritet, när ärendet skapas, då svarar API:t 201 med ärendet, `status` är `new` och `created_at` är satt i UTC-formatet.

**CORE-02** Givet ett skapat ärende, när applikationen startas om (ny engine och ny session mot samma databasfil), då finns ärendet kvar med samma uppgifter i `GET /tickets/{id}`.

**CORE-03** Givet flera skapade ärenden, när listan hämtas, då innehåller den alla ärenden, nyaste först (`created_at` fallande, sedan `id` fallande).

**CORE-04** Givet ett skapat ärende, när det hämtas med sitt id, då svarar API:t 200 med exakt de uppgifter som sparades.

**CORE-05** Givet en rubrik med mellanslag före och efter, när ärendet skapas, då sparas rubriken utan de inledande och avslutande mellanslagen.

### Error paths

**CORE-06** Givet att rubrik saknas, när ärendet skapas, då svarar API:t 422 med "Rubrik måste fyllas i." och inget ärende sparas. (Att ingen historikpost sparas prövas i HIST-10, inte här.)

**CORE-07** Givet att beskrivning saknas, när ärendet skapas, då svarar API:t 422 med "Beskrivning måste fyllas i." och inget ärende sparas.

**CORE-08** Givet en okänd kategori (t.ex. `"klagomål"`), när ärendet skapas, då svarar API:t 422 med "Välj en giltig kategori." och inget ärende sparas. Samma för prioritet.

**CORE-09** Givet att `status` skickas med (t.ex. `"closed"`), när ärendet skapas, då svarar API:t 422 med "Status sätts automatiskt och kan inte anges när ett ärende skapas." och inget ärende sparas.

**CORE-10** Givet ett okänt id, när ärendet hämtas, då svarar API:t 404 med "Ärendet finns inte." Samma gäller ett id som inte är ett heltal, t.ex. `GET /tickets/abc` (beslut B8).

**CORE-17** Givet fel datatyp (t.ex. `"title": 5`), en saknad kropp eller trasig JSON, när ärendet skapas, då svarar API:t 422 med "Ogiltig indata." och inget ärende sparas. Det gäller även när ett annat fält samtidigt saknas: då visas bara "Ogiltig indata." (beslut B9).

### Gränsfall

**CORE-11** Givet en rubrik eller beskrivning som bara består av mellanslag (eller tabbar och radbrytningar), när ärendet skapas, då behandlas fältet som tomt: 422 med "Rubrik måste fyllas i." respektive "Beskrivning måste fyllas i." och inget sparas.

**CORE-12** Givet en rubrik på exakt 100 tecken, när ärendet skapas, då godkänns den. Givet 101 tecken, då svaras 422 och inget sparas. (Längden räknas efter trimning, i Unicode-kodpunkter.)

**CORE-13** Givet en beskrivning på exakt 2000 tecken, när ärendet skapas, då godkänns den. Givet 2001 tecken, då svaras 422 och inget sparas.

**CORE-14** Givet en rubrik med svenska tecken och emoji (t.ex. "Åtgärd för ärende 😊"), när ärendet skapas och hämtas, då är texten oförändrad. Emojin 😊 räknas som ett tecken.

**CORE-15** Givet att inga ärenden finns, när listan hämtas, då svarar API:t 200 med en tom lista (inte ett fel).

### Icke-funktionella

**CORE-16** Felmeddelanden är på svenska, har formen `{"detail": ...}` och innehåller aldrig stacktrace, SQL eller fältnamn på engelska. (Automatiskt: format och språk. Manuellt: begriplighet.) Samma princip som HIST-14.

## 6. Testningsstrategi (kärnan)

| Nivå | Vad | Verktyg | Täcker | Ansvarig |
| --- | --- | --- | --- | --- |
| Integration (API + riktig SQLite-fil) | Skapa, lista, visa, validering, "inget sparas" | pytest + TestClient, temporär fil | CORE-01, 03–15, 17 | Nicklas |
| Integration, omstart | Ny engine och session mot samma fil | pytest, temporär fil | CORE-02 | Nicklas |
| Manuell | Begripliga meddelanden i UI | Checklista i `docs/verifiering.md` | CORE-16 | Nicklas |

**Implementation:** Azalea (backend). **Tester:** Nicklas.

**Gräns mot HIST:** CORE-testerna kontrollerar att inget *ärende* sparas vid ogiltig indata. HIST-10 kontrollerar att ingen *historikpost* sparas. Samma fall testas alltså inte två gånger.

**Varför integrationsnivå:** "inget ärende sparas" (CORE-06–13) går bara att visa genom att fråga den riktiga databasen efter anropet. Ett enhetstest av valideringen ensam visar att indata avvisas, men inte att inget skrevs till databasen.

**Mutationsprövning (egna tester först, sedan korsvis):**

| Mutation | Ska fångas av |
| --- | --- |
| Trimningen tas bort (`" "` räknas som giltig rubrik) | CORE-11 |
| Gränsen ändras från `<= 100` till `< 100` | CORE-12 |
| Ärendet sparas *innan* valideringen körs | CORE-06, 07, 08 |
| `commit` tas bort (bara `flush`) | CORE-02 |
| Den svenska felhanteraren för fel datatyp tas bort (FastAPI:s engelska standardfel går igenom) | CORE-17, CORE-16 |

## 7. Boundaries (för människor och AI-agenter)

- **Alltid:** följa API-konventionerna, referera CORE-id i test, commit och PR, köra testerna före commit.
- **Fråga först:** ändra fälten i `tickets` (HIST bygger på tabellen), ändra felmeddelanden som frontend redan visar.
- **Aldrig:** låta `POST /tickets` sätta annan status än `new`, ändra status utanför `PATCH /tickets/{id}/status`, använda riktiga kunduppgifter.

## 8. Beslut och motivering

Besluten är fattade av Nicklas (2026-10-24). B5, B7 och B8 är förtydligade eller tillagda efter Azaleas granskning av PR #5. B9 svarar på hennes fråga i godkännandet.

| # | Fråga | Beslut | Skäl |
| --- | --- | --- | --- |
| B1 | Maxlängd rubrik / beskrivning | 100 / 2000 tecken | Rubriken ska rymmas i en listrad. 2000 räcker för ett ärende men stoppar inklistrade loggar. Ger tydliga gränsvärden att testa (CORE-12, 13). |
| B2 | Kategorier | billing, delivery, technical, account, other | Vanliga i kundservice, "Övrigt" fångar resten. Påhittat, inga kunddata. |
| B3 | Prioriteter | low, medium, high | Tre nivåer är lätta att välja mellan. Fyra ("akut") kan läggas till senare. |
| B4 | Om `status` skickas i POST | Avvisa med 422 | Tydligare än att tyst ignorera, och stöder regeln att status bara ändras via PATCH. Alternativ: ignorera. |
| B5 | Sortering i listan | Nyaste först (`created_at` fallande, sedan `id` fallande) | Handläggare vill se det senaste. `id` som andra nyckel ger stabil ordning (samma idé som HIST-11). |
| B6 | Kunduppgifter (namn, e-post) | Inte med i v0.1 | Uppgiften kräver dem inte. Färre personuppgifter = mindre att skydda. Kan läggas till senare. |
| B7 | Flera fel samtidigt | Visa alla, i fältordningen rubrik, beskrivning, kategori, prioritet, status | Handläggaren rättar allt på en gång. Frontend visar `detail` som det är. Fast ordning gör att testerna kan kontrollera exakt text. |
| B8 | Id som inte är ett heltal (`GET /tickets/abc`) | 404 "Ärendet finns inte." | För handläggaren är det samma sak som ett okänt ärende, och frontend behöver bara visa ett meddelande. Alternativ: 422 med svenskt meddelande, mer tekniskt korrekt men ett fall till att hantera. Gäller även HIST-08. |
| B9 | Fel datatyp och saknat fält samtidigt | Bara "Ogiltig indata." | Fel datatyp betyder att anropet är trasigt, vilket bara händer vid en bugg i klienten. En handläggare kan inte skriva en siffra som rubrik i formuläret. Fältmeddelandena är till för handläggaren och hjälper inte då. Ett meddelande är också enklare att bygga och testa. Alternativ: visa båda, i fältordningen. |

## Ändringar

| Version | Datum | Ändring |
| --- | --- | --- |
| v0.1 | 2026-10-24 | Första utkastet, CORE-01–16 |
| v0.2 | 2026-10-24 | Efter Azaleas granskning: fast felordning (B7), CORE-17 "Ogiltig indata.", id som inte är heltal ger 404 (B8), CORE-11 gäller även beskrivning, tecken = Unicode-kodpunkter, sorteringsriktning (B5), meddelande i CORE-09, gräns mot HIST-10, vem som implementerar |
| v0.3 | 2026-10-25 | B9: fel datatyp tillsammans med saknat fält ger bara "Ogiltig indata." (CORE-17, avsnitt 4) |
