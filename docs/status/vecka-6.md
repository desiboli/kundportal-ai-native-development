# Veckostatus vecka 6: det centrala flödet

> Senast uppdaterat tisdag 2026-10-27 morgon (Azalea).
> Jämför med veckans förväntningar i Disco. Id förklaras kort: **KSP-xx** är ärenden i
> [Linear: Kundserviceportalen](https://linear.app/grupp6/project/kundserviceportalen-be4a4840b5ef),
> **CORE-xx** är kraven för kärnan ([SPEC-karna.md](../specs/SPEC-karna.md)) och **HIST-xx**
> kraven för statuslogik och historik ([SPEC-arendehistorik.md](../specs/SPEC-arendehistorik.md)).

## Planerat

Veckans förväntningar enligt kursen:

1. Det centrala flödet fungerar: registrera och spara ärenden, visa lista och detaljer, ändra status.
2. Avgränsat agentarbete är genomfört, med sparade instruktioner och mänsklig granskning.
3. Automatiserade tester för centrala beteenden är körda och resultaten dokumenterade.
4. Varje students tekniska bidrag går att följa i projektet.

Teamets plan för veckan (milstolpe 03 Case Management i Linear):

| Vad | Ärende | Ansvarig |
| --- | --- | --- |
| API-kontraktet i OpenAPI med stubbar, så att frontend kan bygga direkt | KSP-20 | Azalea |
| Svenskt felformat i backenden (`{"detail": ...}`) | KSP-21 | Azalea |
| Ärendemodell, `POST /tickets`, `GET /tickets` och `GET /tickets/{id}` | KSP-22, KSP-23 | Azalea |
| Statusbyte `PATCH /tickets/{id}/status` | KSP-24 | Azalea |
| Historiktabellen och TicketService | KSP-33, KSP-34 | Azalea |
| TypeScript-typer från OpenAPI, ärendelista och formulär | KSP-28–30 | Mustafa |
| Detaljvy och statusbyte i frontend | KSP-31, KSP-32 | Amalia |
| Tester för CORE och för statusreglerna (HIST-06, 07, 13), verifieringsplan | KSP-25–27, KSP-47 | Nicklas |

## Genomfört

| Vad | Vem | Länk |
| --- | --- | --- |
| API-kontraktet: alla fem endpoints för CORE och HIST i `/openapi.json` med modeller, enum, längdgränser och felsvar. Stubbarna svarar 501 "Funktionen är inte klar än." | Azalea | PR #26 (API-kontraktet i OpenAPI med fem stubbar): https://github.com/desiboli/kundportal-ai-native-development/pull/26 · mergad 2026-10-27 |
| Frontenden når backendens `/health` via Vite-proxyn (`/api` → port 8010). Startsidan visar om backenden och databasen svarar | Azalea | PR #15 (koppla frontend till backendens /health): https://github.com/desiboli/kundportal-ai-native-development/pull/15 · mergad 2026-10-26 |
| Veckostatus V6 | Azalea | PR #27 (veckostatus V6): https://github.com/desiboli/kundportal-ai-native-development/pull/27 · mergad 2026-10-27 |

## Verifierat

- KSP-20, testerna först: 30 kontraktstester i `backend/tests/test_openapi_contract.py`
  skrevs före koden. Commit `abede58` (bara testerna): `30 failed, 4 passed`, eftersom
  vägarna och modellerna saknades. Commit `dcaa890` (koden): `34 passed`. CI (jobbet
  `backend`) grön på PR #26 (API-kontraktet i OpenAPI med fem stubbar): https://github.com/desiboli/kundportal-ai-native-development/pull/26.
- KSP-20, granskningen: Nicklas (backend) läste kontraktet mot CORE avsnitt 4 och HIST
  avsnitt 4–5 och körde testerna lokalt (34 passed). Amalia kontrollerade fälten och
  felsvaren för detaljvy, statusbyte och tidslinje och körde backenden (`/docs`, 501).
  Mustafa kontrollerade att modellerna räcker för lista, formulär, detaljvy och statusbyte.
  Alla tre godkände.
- KSP-16, granskningen: Mustafa begärde ändringar på PR #15 (koppla frontend till backendens /health): https://github.com/desiboli/kundportal-ai-native-development/pull/15.
  De gjordes, och Amalia och Mustafa godkände.

## Osäkert eller ofärdigt

| Vad | Varför | Plan |
| --- | --- | --- |
| FastAPI lägger själv till en engelsk 422 (`HTTPValidationError`) på `GET /tickets/{ticket_id}` och `/history` | Vägar med en parameter får den automatiskt. Den stämmer inte med CORE-10 (404 för id som inte är heltal) och CORE-16 | Rättas i KSP-21 tillsammans med felformatet |
| 501-testerna i PR #26 (API-kontraktet i OpenAPI med fem stubbar): https://github.com/desiboli/kundportal-ai-native-development/pull/26 är tillfälliga | Varje stubb byts mot riktig logik | Ersätts av beteendetester i det KSP-ärende som bygger vägen |
| `max_length` på rubrik och beskrivning kontrolleras före trimningen (Nicklas granskning av PR #26 (API-kontraktet i OpenAPI med fem stubbar): https://github.com/desiboli/kundportal-ai-native-development/pull/26) | CORE-12 och B10 säger att längden räknas efter trimning, så 100 tecken med mellanslag runt ska godkännas | Rättas i KSP-21/KSP-22. Nicklas lägger fallet i CORE-testerna (KSP-25) |
| Ska andra okända fält än `status` avvisas i `POST /tickets`? (`extra="forbid"`) | CORE-09 gäller bara `status` | Azalea och Nicklas bestämmer. Om ja, lägger Nicklas det i CORE-specen |
| `docs/ansvar-och-granskning.md` har kvar rader med "Förslag" | Ansvaret bekräftades på teammötet 2026-10-25 | Azalea (KSP-13) |

## Nästa steg

| Vad | Ansvarig |
| --- | --- |
| Teammöte tisdag 2026-10-27: openapi-typescript, ordningen för CORE-testerna | Alla |
| Svenskt felformat i backenden | Azalea (KSP-21) |
| Generera TypeScript-typer från `/openapi.json` (kontraktet är mergat, inget blockerar längre) | Mustafa (KSP-28) |
| Länka vecka 6 och de nya dokumenten (CORE-specen, ADR:erna, `docs/ai/`) från den löpande PR:n (Technigo#2): https://github.com/Technigo/kundportal-ai-native-development/pull/2 | Mustafa (KSP-56) |
| Ansvarsdokumentet från "Förslag" till "Bekräftat" | Azalea (KSP-13) |
