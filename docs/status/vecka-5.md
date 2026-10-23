# Veckostatus vecka 5: Projektstart och specifikation

> Utkast, senast uppdaterat 2026-10-23 kl. 21 (Azalea). Kompletteras av teamet efter
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
| Fork och löpande PR till kursens repository | Mustafa | [Technigo/kundportal-ai-native-development#2](https://github.com/Technigo/kundportal-ai-native-development/pull/2) |
| Teammedlemmar i PR-mallen, alla fyra | Azalea, Amalia | [#1](https://github.com/desiboli/kundportal-ai-native-development/pull/1) (Azalea, mergad), [#2](https://github.com/desiboli/kundportal-ai-native-development/pull/2) (Amalia, granskad och godkänd av Azalea, mergad 2026-10-23) |
| Push-åtkomst till forken kontrollerad | Azalea, Amalia | Pushade branches och PR:er ovan |
| Linear-projekt, milstolpar och ärendemallar | Mustafa | [Linear: Kundserviceportalen](https://linear.app/grupp6/project/kundserviceportalen-be4a4840b5ef) |
| Spec v0.3: statuslogik och ärendehistorik, acceptanskriterier HIST-01–14, teststrategi | Azalea | [docs/specs/SPEC-arendehistorik.md](../specs/SPEC-arendehistorik.md) |
| Arbetsfördelning | Alla (förslag) | [docs/ansvar-och-granskning.md](../ansvar-och-granskning.md) |
| Backendskelett: FastAPI, SQLite, `GET /health`, körinstruktioner | Azalea | [#3](https://github.com/desiboli/kundportal-ai-native-development/pull/3) (väntar på granskning) |
| Feedback på specen och mallarna | Nicklas, Amalia | Slack, inarbetat i spec v0.3 |

## Verifierat

- Backendskelettet: `pytest -q` ger `4 passed` (2026-10-23). Testerna kontrollerar bland
  annat att `/health` faktiskt frågar databasen och svarar 503 med svenskt meddelande om
  den inte går att nå.
- Manuellt: `uvicorn` startar och `/health` svarar `{"status":"ok","database":"ok"}`.
- Specen granskad av Nicklas och Amalia (synpunkter i Slack, inarbetade i v0.3).
- Kodgranskning i GitHub: Azalea granskade #2 (kontrollerade att raden har samma format
  som övriga och att användarnamnet stämmer med Amalias konto) och godkände innan merge.

**Granskningar som väntar:** #3 (backendskelett, granskare Nicklas) och #4 (spec, ansvar,
veckostatus, granskare Nicklas och Mustafa).

## Osäkert eller ofärdigt

| Vad | Varför | Plan |
| --- | --- | --- |
| Stacken är inte beslutad | Mustafa föreslog TypeScript rakt igenom som alternativ till FastAPI | Beslutas söndag, Nicklas dokumenterar i `docs/decisions/` |
| Ingen frontend i fullstackgrunden än | Väntar på stackbeslutet | Frontendskelett som anropar `/health`, söndag–måndag |
| Spec för kärnan (CORE) saknas | Nicklas har erbjudit sig att skriva den | Första utkast efter söndag |
| Verifieringsplan saknas | Ägs av Nicklas, bygger på specarna | Första utkast vecka 6 |
| Arbetsfördelningen är förslag | Ska bekräftas av alla fyra | Söndagsmötet |
| Beskrivningen i den löpande PR:n saknar Azalea, Amalia och länkar | Bara Mustafa, som öppnade PR:n, kan ändra den | Mustafa uppdaterar när #3 och #4 är mergade |
| Inga Linear-ärenden per krav än | Strukturen finns, ärendena inte | Skapas efter söndagsmötet |

## Nästa steg

| Vad | Ansvarig |
| --- | --- |
| Stackbeslut och dokumentation | Nicklas (alla beslutar) |
| Granska backendskelettet (#3) | Nicklas |
| Frontendskelett mot `/health` | Mustafa |
| CORE-spec, första utkast | Nicklas |
| Ärendemodell och `POST`/`GET /tickets` (vecka 6) | Azalea |
| Linear-ärenden per krav-id | Mustafa (alla lägger in sina) |
| Uppdatera beskrivningen i den löpande PR:n med alla fyra och länkar | Mustafa |
| Amalias egen del | Amalia |
