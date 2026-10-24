# Veckostatus vecka 5: Projektstart och specifikation

> Utkast, senast uppdaterat lördag 2026-10-24 (Azalea). Kompletteras av teamet efter
> mötet söndag 2026-10-25.
> Jämför med veckans förväntningar i Disco.

## Planerat

Veckans förväntningar enligt kursen:

1. Teamets fork och löpande PR finns, och åtkomsten är kontrollerad.
2. Avgränsning, teknikval och arbetsfördelning är dokumenterade.
3. De första specifikationerna har acceptanskriterier och en plan för verifiering.
4. En minimal fullstackgrund går att köra med våra instruktioner.

Teamets egen plan: Linear-projektet Kundserviceportalen med sex milstolpar och mallar för
Feature, Bug, Chore och Verification (Mustafa). Spec för kompletterande funktion (Azalea),
spec för kärnan och verifieringsplan (Nicklas), backendskelett (Azalea), frontendskelett.

## Genomfört

| Vad | Vem | Länk |
| --- | --- | --- |
| Fork och löpande PR till kursens repository | Mustafa | Löpande PR till kursens repository: https://github.com/Technigo/kundportal-ai-native-development/pull/2 |
| Teammedlemmar i PR-mallen, alla fyra | Azalea, Amalia | PR #1 (Azalea i PR-mallen): https://github.com/desiboli/kundportal-ai-native-development/pull/1 (mergad), PR #2 (Amalia i PR-mallen): https://github.com/desiboli/kundportal-ai-native-development/pull/2 (granskad och godkänd av Azalea, mergad 2026-10-23) |
| Push-åtkomst till forken kontrollerad | Azalea, Amalia, Nicklas | Pushade branches och PR:er i den här tabellen |
| Linear-projekt, milstolpar och ärendemallar. Beskrivningen av milstolpe 02 rättad 2026-10-23 | Mustafa | [Linear: Kundserviceportalen](https://linear.app/grupp6/project/kundserviceportalen-be4a4840b5ef) |
| Fält för krav-id (CORE-xx, HIST-xx) i alla fyra ärendemallarna, och en rad i Verification om testet faller av rätt anledning | Nicklas | Linear, ärendemallarna |
| Spec v0.3: statuslogik och ärendehistorik, acceptanskriterier HIST-01–14, teststrategi | Azalea | [docs/specs/SPEC-arendehistorik.md](../specs/SPEC-arendehistorik.md), PR #4 (spec, ansvar och veckostatus V5): https://github.com/desiboli/kundportal-ai-native-development/pull/4 (godkänd av Mustafa, mergad 2026-10-23) |
| Arbetsfördelning | Alla (förslag) | [docs/ansvar-och-granskning.md](../ansvar-och-granskning.md), i samma PR #4 (spec, ansvar och veckostatus V5): https://github.com/desiboli/kundportal-ai-native-development/pull/4 |
| Backendskelett: FastAPI, SQLite, `GET /health`, körinstruktioner i README, port 8010 | Azalea | PR #3 (backendskelett: FastAPI, SQLite och /health): https://github.com/desiboli/kundportal-ai-native-development/pull/3 (godkänd av Mustafa, mergad 2026-10-23) |
| Spec för kärnan v0.1: CORE-01–16, felmeddelanden, gränsfall, mutationer, beslut B1–B7 | Nicklas | PR #5 (spec för kärnan, CORE-01–16): https://github.com/desiboli/kundportal-ai-native-development/pull/5 (granskad av Azalea, v0.2 med alla nio punkter åtgärdade, commit 915a933) |
| Amalia har valt sin del: tidslinjen (HIST-05) och UI-delen av HIST-14 | Amalia | PR #7 (Amalia tar tidslinje och felmeddelanden i UI, HIST-05 och HIST-14): https://github.com/desiboli/kundportal-ai-native-development/pull/7 (godkänd av Azalea) |
| HIST-spec v0.4: Amalias del och uppdelningen av HIST-14 i backend- och UI-del | Azalea | PR #8 (HIST-spec v0.4, Amalias del): https://github.com/desiboli/kundportal-ai-native-development/pull/8 |
| Feedback på specen och mallarna | Nicklas, Amalia | Slack, inarbetat i spec v0.3 |
| Svar på feedbacken och sammanfattning av spec v0.3 till teamet | Azalea | Slack 2026-10-23 |

## Verifierat

- Backendskelettet: `pytest -q` ger `4 passed` (2026-10-23). Testerna kontrollerar bland
  annat att `/health` faktiskt frågar databasen och svarar 503 med svenskt meddelande om
  den inte går att nå.
- Manuellt: `uvicorn` startar och `/health` svarar `{"status":"ok","database":"ok"}` på
  port 8010. 8010 är projektets standardport, eftersom 8000 redan användes av en annan
  lokal app och svarade med fel innehåll (upptäckt genom att läsa svaret, inte bara statuskoden).
- Specen granskad av Nicklas och Amalia (synpunkter i Slack, inarbetade i v0.3).
- Kodgranskning i GitHub:
  - Azalea granskade PR #2 (Amalia i PR-mallen): https://github.com/desiboli/kundportal-ai-native-development/pull/2
    (kontrollerade att raden har samma format som övriga och att användarnamnet stämmer
    med Amalias konto) och godkände innan merge.
  - Mustafa godkände PR #3 (backendskelett: FastAPI, SQLite och /health): https://github.com/desiboli/kundportal-ai-native-development/pull/3
    och PR #4 (spec, ansvar och veckostatus V5): https://github.com/desiboli/kundportal-ai-native-development/pull/4
    och mergade dem 2026-10-23. Godkännandena saknar kommentar om vad som kontrollerades.
  - Azalea granskade PR #5 (spec för kärnan, CORE-01–16): https://github.com/desiboli/kundportal-ai-native-development/pull/5 2026-10-24 mot
    API-konventionerna och HIST-specen: nio radkommentarer (bl.a. ordningen på felmeddelanden,
    svenskt meddelande vid fel typ, id som inte är ett tal, hur tecken räknas) och
    "Request changes". Nicklas åtgärdade alla nio i v0.2 (commit 915a933), bl.a. nytt
    kriterium CORE-17 och beslut B8 (404 även för id som inte är ett heltal).
  - Azalea granskade PR #7 (Amalia tar tidslinje och felmeddelanden i UI, HIST-05 och HIST-14): https://github.com/desiboli/kundportal-ai-native-development/pull/7 2026-10-24: kontrollerade att diffen
    bara ändrar de beskrivna raderna och att Linear-dokumentet har samma innehåll. Godkänd
    med två radkommentarer (UI-delen av HIST-14, test för felmeddelandena).

**Väntar:** Azaleas godkännande av v0.2 i PR #5 (spec för kärnan, CORE-01–16): https://github.com/desiboli/kundportal-ai-native-development/pull/5.

## Osäkert eller ofärdigt

| Vad | Varför | Plan |
| --- | --- | --- |
| Stacken är inte beslutad | Mustafa föreslog TypeScript rakt igenom som alternativ till FastAPI | Beslutas söndag, Nicklas dokumenterar i `docs/decisions/` |
| Ingen frontend i fullstackgrunden än | Väntar på stackbeslutet | Frontendskelett som anropar `/health`, söndag–måndag |
| Spec för kärnan är ett utkast | Första version klar, granskning pågår | Granskad av Azalea 2026-10-24 (Request changes, nio punkter). Nicklas uppdaterar, sedan godkänner Azalea |
| Verifieringsplan saknas | Ägs av Nicklas, bygger på specarna | Första utkast vecka 6 |
| Arbetsfördelningen är förslag | Ska bekräftas av alla fyra. Amalia har valt sin del | Söndagsmötet |
| Beskrivningen i den löpande PR:n (Technigo#2): https://github.com/Technigo/kundportal-ai-native-development/pull/2 saknar Azalea, Amalia och länkar | Bara Mustafa, som öppnade PR:n, kan ändra den | Mustafa uppdaterar. PR #3 (backendskelett): https://github.com/desiboli/kundportal-ai-native-development/pull/3 och PR #4 (spec, ansvar och veckostatus V5): https://github.com/desiboli/kundportal-ai-native-development/pull/4 är nu mergade, så länkarna till `docs/` fungerar |
| Backendskelettet mergades utan att Nicklas hann granska | Mustafa godkände först | Nicklas kan granska i efterhand med kommentarer i PR #3 (backendskelett: FastAPI, SQLite och /health): https://github.com/desiboli/kundportal-ai-native-development/pull/3 |
| Inga Linear-ärenden per uppgift än | Strukturen och mallarna finns, ärendena inte | Skapas efter söndagsmötet |

## Nästa steg

| Vad | Ansvarig |
| --- | --- |
| Stackbeslut och dokumentation | Nicklas (alla beslutar) |
| ~~Uppdatera spec för kärnan efter granskningen~~ klart i v0.2, PR #5 (spec för kärnan, CORE-01–16): https://github.com/desiboli/kundportal-ai-native-development/pull/5 | Nicklas |
| Godkänna PR #5 när ändringarna är gjorda, och ändra HIST-08 och HIST-10 likadant | Azalea |
| Frontendskelett mot `/health` | Mustafa |
| Ärendemodell och `POST`/`GET /tickets` enligt CORE (vecka 6) | Azalea |
| Linear-ärenden per uppgift, med krav-id i beskrivningen | Alla lägger in sina |
| Uppdatera beskrivningen i den löpande PR:n med alla fyra och länkar | Mustafa |
| Svara på radkommentarerna i PR #7 (Amalia tar tidslinje och felmeddelanden i UI, HIST-05 och HIST-14): https://github.com/desiboli/kundportal-ai-native-development/pull/7 så att den kan mergas (alla konversationer måste vara lösta) | Amalia |
| Granska PR #8 (HIST-spec v0.4, Amalias del): https://github.com/desiboli/kundportal-ai-native-development/pull/8 | Amalia, Nicklas |
