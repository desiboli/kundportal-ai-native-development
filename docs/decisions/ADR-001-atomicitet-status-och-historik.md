# ADR-001: Hur garanterar vi att status och historik aldrig hamnar i otakt?

- **Status:** Föreslagen, granskas i PR (granskare Nicklas)
- **Datum:** 2026-10-22 (utkast), 2026-10-25 (i repot)
- **Beslutsfattare:** Azalea (förslag), teamet (godkännande)
- **Kopplar till:** HIST-02, HIST-06, HIST-09, HIST-10 i [SPEC-arendehistorik.md](../specs/SPEC-arendehistorik.md)

## Kontext

När status ändras måste två saker ske: ärendets `status` uppdateras och en post skrivs i
`ticket_history`. Om bara det ena lyckas visar tidslinjen något annat än ärendet. Det
bryter kärnvärdet ("historiken är aldrig i otakt"). Lagringen är SQLite via SQLAlchemy 2.0.
Lösningen ska gå att testa, vara lätt att förstå för teamet och rymmas i en lokal app.

## Krav som avgör valet

| Krav | Vikt |
|---|---|
| Atomicitet: båda ändringarna eller ingen (HIST-09, HIST-10) | Måste |
| Ett fel kan injiceras i test för att bevisa att rollback sker | Måste |
| Regler (giltig status, samma status) syns i kod som teamet läser | Hög |
| Fungerar med SQLite utan extra infrastruktur | Måste |
| Låg komplexitet för en grupp på fyra med fyra veckor | Hög |
| Går att bygga ut till anteckningar, tilldelning m.m. | Medel |

## Alternativ

### A. Transaktion i tjänstelagret (förslag)
`TicketService.change_status()` öppnar en transaktion, validerar, uppdaterar
`tickets.status`, infogar historikposten och gör `commit`. Vid fel görs `rollback`.

- **+** Reglerna ligger på ett ställe i vanlig Python, lätta att läsa och enhetstesta.
- **+** Fel går att injicera (monkeypatch på repository) och rollback kan verifieras.
- **+** Ingen databasspecifik magi, byggs ut med fler eventtyper.
- **−** Atomiciteten gäller bara så länge all skrivning går via tjänsten. Någon som
  skriver direkt i `tickets` kringgår historiken. Måste mötas med konvention och test.

### B. Databastrigger
En `AFTER UPDATE`-trigger på `tickets` skriver historikposten.

- **+** Kan inte kringgås från applikationskod, eftersom databasen garanterar det.
- **−** Logiken göms i SQL utanför kodgranskning och Python-tester.
- **−** `from_status` finns bara via `OLD.status`, och validering och meddelanden måste
  ändå ligga i appen, så reglerna delas på två ställen.
- **−** Svårare att injicera fel och att migrera. Passar sämre för ett nybörjarteam.

### C. Event sourcing (status härleds ur historiken)
Ingen `status`-kolumn. Aktuell status är senaste historikposten.

- **+** Atomicitet blir trivial: det finns bara en skrivning. Historiken är sanningen.
- **−** Alla läsningar (lista, filter, sök) måste räkna ut senaste status. Det komplicerar
  det teamets kärna redan bygger (`GET /tickets`).
- **−** Kräver att teamet ändrar sin kärnmodell. Klart överdimensionerat för kravet.

## Beslut

**Alternativ A** med två kompletterande skydd:
1. Skrivning till `tickets.status` sker enbart i `TicketService`, och det dokumenteras som
   regel i spec och i AI-instruktionerna.
2. Ett test hävdar att historikens senaste `to_status` alltid är lika med ärendets
   status (invariant), kört efter varje scenario i integrationstesterna.

## Konsekvenser

- Tjänstelagret blir testets fokus. Fel injiceras mellan statusuppdatering och
  historikinsättning för att visa rollback (HIST-09).
- När historikposten inte kan sparas gör tjänsten `rollback`, så sessionen kan användas
  igen och nästa statusändring lyckas. API:t svarar **503** med "Statusen kunde inte
  ändras. Försök igen."

  **Beslut om statuskoden (Azalea, 2026-10-25): 503 i stället för 500.**

  | | 500 Internal Server Error | 503 Service Unavailable |
  |---|---|---|
  | För | En generell hanterare för alla oväntade fel | `/health` använder redan 503 när databasen inte går att nå, så samma sorts fel får samma kod. "Försök igen" passar ett tillfälligt fel. Frontend kan visa ett försök-igen-besked utan att tolka texten |
  | Emot | Säger "något gick fel hos oss" och ger ingen ledning om att ett nytt försök kan lyckas | Kräver en egen hanterare i tjänsten/routern, skild från den generella 500-hanteraren |

  Valet följer av beslutet ovan: eftersom atomiciteten ligger i tjänstelagret (alternativ A)
  kan tjänsten fånga felet, rulla tillbaka och svara med en bestämd kod. Med en trigger
  (alternativ B) hade felet kommit från databasen och varit svårare att skilja från andra
  fel. Kontrolleras i HIST-09-testerna (statuskod 503, oförändrad status, nästa byte lyckas).
- **Kvarstående risk:** en kodväg som kringgår tjänsten fångas inte av trigger. Kontrollen
  är invarianttestet och granskning, inte databasen.
- **Test som motbevisar beslutet:** om mutation (historikskrivningen avstängd, eller
  `commit` före historiken) inte får minst ett test att falla, är beslutet inte belagt och
  ska omprövas (kopplas till VG: kritisk granskning).
- Om en senare funktion (t.ex. tilldelning) kräver historik utan tjänstegräns kan
  alternativ B omprövas.

## Hur beslutet ska prövas (spårbarhet)

| Påstående | Kontroll | Resultat |
|---|---|---|
| Rollback sker vid fel | HIST-09, injicerat fel | _fylls i när körd_ |
| Invariant håller | Test efter varje scenario | _fylls i_ |
| Testen fångar utebliven historik | Mutation: ta bort insättningen (HIST-01/02/03 ska falla) | _fylls i_ |
| Testen fångar commit utanför transaktionen | Mutation: `commit` före historiken (HIST-09 ska falla) | _fylls i_ |
| Testen fångar utebliven sparning | Mutation: ta bort `commit` (HIST-04 ska falla) | _fylls i_ |
