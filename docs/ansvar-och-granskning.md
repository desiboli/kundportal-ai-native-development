# Ansvar och granskning

> Teamets arbetsfördelning. Speglas från Linear-dokumentet
> [Gemensamt · Ansvar och granskning](https://linear.app/grupp6/document/gemensamt-ansvar-och-granskning-fa06c24358e0)
> per 2026-10-23. Bekräftat = överenskommet i Slack 2026-10-22–23. Förslag = tas upp på
> teammötet söndag 2026-10-25.

## Princip

- Varje person äger ett eget, spårbart moment: spec eller del av spec, implementation,
  tester och verifiering för sin del.
- Var och en skriver testerna och gör förbättringarna för sin egen del. Andra
  **granskar**, men skriver inte varandras.
- Varje ändring går via en intern PR till forkens `main` och granskas av minst en annan i
  teamet innan merge. Granskningen görs i GitHub, så att det syns vem som granskade, vad
  som kontrollerades och vad återkopplingen ledde till.
- Krav-id (HIST-xx, CORE-xx) står i Linear-ärendet, i commit-meddelandet och i PR:en.

## Översikt per person

| Person (GitHub) | Huvudområde |
| --- | --- |
| **Azalea** (Azaalea) | Backend som helhet: skelett, kärnans API, statuslogik och historik, API-kontraktet |
| **Nicklas** (yrrving) | CORE-specen, tester för statusregler och validering, verifieringsplanen, teknikbeslutet om stacken |
| **Mustafa** (desiboli) | Frontend och Linear |
| **Amalia** (amaliaa-91) | Väljer själv: tidslinje och felmeddelanden i UI, eller en egen tilläggsfunktion (t.ex. sök och filtrering) |

## Ansvarstabell

| Del | Ansvarig | Granskare | Läge |
| --- | --- | --- | --- |
| **Backend som helhet:** skelett, SQLite, kärnans API (CORE) och `/health` | Azalea | Nicklas | Förslag |
| Statusregler, historik, transaktionsgräns, ADR-001 | Azalea | Nicklas | Bekräftat |
| API-kontrakt som OpenAPI (`/openapi.json`), klart innan frontend bygger mot det | Azalea | Mustafa | Förslag |
| Tester för historik, atomicitet och persistens: **HIST-01, 02, 03, 04, 08, 09, 10, 11, 12** och invarianttestet | Azalea | Nicklas | Förslag |
| Spec för kärnan (**CORE-01, 02 …**) | Nicklas | Azalea | Förslag (Nicklas erbjöd sig) |
| Tester för statusregler: **HIST-06, 07, 13** | Nicklas | Azalea | Bekräftat |
| Tester för kärnans validering (CORE-kriterierna) | Nicklas | Azalea | Förslag |
| Teamets verifieringsplan (`docs/verifiering.md`), HIST-raderna skrivs av Azalea | Nicklas | Azalea | Bekräftat |
| Teknikbeslut om stacken (jämförelse och beslut) | Nicklas | Alla | Förslag |
| Mutationsprövning, **korsvis**: var och en prövar sina egna tester, den andra lägger in en okänd mutation | Azalea, Nicklas | den andra | Förslag |
| Instruktion för testförslag: v1 | Nicklas | Azalea | Förslag |
| Förbättring av instruktionen: **var och en gör en egen, namngiven förbättring**, prövad på egna kriterier och jämförd med v1 | Azalea, Nicklas (var för sig) | den andra | Förslag |
| Frontend: lista, detaljvy, formulär för att skapa ärenden, statusbyte, vitest | Mustafa | Azalea | Förslag |
| Tidslinje (HIST-05) och felmeddelanden i UI (HIST-14), **eller** egen tilläggsfunktion (t.ex. sök och filtrering, egen spec) | Amalia (väljer själv) | Mustafa, Azalea | Förslag |
| Linear: milstolpar, ärenden och mallar (fält för krav-id och "faller testet av rätt anledning?") | Mustafa (mallarna: Nicklas) | Nicklas | Förslag |

## Granskningspar

| PR rör | Granskas av |
| --- | --- |
| Backend, statuslogik, historik | Nicklas |
| CORE-spec, tester för status och validering | Azalea |
| Frontend | Azalea (API-kontraktet), Amalia eller Mustafa (UI) |
| Amalias del | Mustafa och Azalea |

## Öppet till söndag

1. Stacken: FastAPI (förslag) eller TypeScript rakt igenom. Se spec, antagande 1.
2. Bekräfta raderna som står som Förslag.
3. Amalias val av egen del.
4. Huvudversion för gemensamma dokument: repot eller Linear?
