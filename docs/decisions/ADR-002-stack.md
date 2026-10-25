# ADR-002: Teknikstack för Kundserviceportalen

> Status: **föreslaget, väntar på teamets godkännande** · Ansvarig: Nicklas (yrrving) · Datum: 2026-10-25
> Underlag: Slack 2026-10-21–25, teammötet 2026-10-25, PR #3 (backendskelett: FastAPI, SQLite och /health): https://github.com/desiboli/kundportal-ai-native-development/pull/3 och PR #11 (frontend-skelett med React, Vite och TypeScript): https://github.com/desiboli/kundportal-ai-native-development/pull/11.

## Kontext

Uppgiften lämnar teknikvalet till gruppen men ställer några krav som styr valet:

- Lösningen ska ha användargränssnitt, backendlogik och **beständig lagring** (ärenden finns kvar efter omstart).
- Den ska kunna **köras lokalt av någon annan** med hjälp av instruktionerna, utan personligt betalkonto.
- Centrala beteenden ska verifieras med **automatiserade tester**.
- Vi är fyra personer med olika vana (backend, frontend, test) och olika AI-verktyg (Claude, Cursor, ChatGPT). Tiden är kort: demo vecka 8.

Stacken diskuterades i Slack och landade under mötet 2026-10-25, när backend- och frontendskeletten redan fanns. Det här dokumentet skriver ner besluten och varför.

## Beslut

| Del | Val |
| --- | --- |
| Backend | Python 3.11 + FastAPI, körs med uvicorn på port 8010 |
| Databas | SQLite (en fil) via SQLAlchemy 2 |
| Backendtester | pytest + FastAPIs TestClient |
| Frontend | React + Vite + TypeScript |
| Utseende | Tailwind CSS + shadcn/ui, stil "Luma", grundkomponenter från Base UI |
| Pakethanterare (frontend) | pnpm |
| Struktur | `backend/` och `frontend/` som separata mappar i samma repo, inte ett monorepo-verktyg |

Exakta versioner står i `backend/requirements.txt` och `frontend/package.json`, och de filerna gäller om något här skiljer sig.

## Alternativ och avvägning

### 1. Backend: FastAPI eller TypeScript hela vägen

| | FastAPI (Python) | Node + Express/Fastify (TypeScript) |
| --- | --- | --- |
| För | Inbyggd validering via Pydantic passar kravet på obligatoriska fält. Automatisk API-dokumentation (Swagger). Backend-ansvarig har byggt liknande förut. | Ett språk i hela stacken. Delade typer mellan frontend och backend utan extra steg. |
| Emot | Två språk i projektet. Typerna i frontend måste hållas i synk med backend. | Validering och API-dokumentation måste byggas eller väljas till. Ingen i teamet har pekat ut det som sin styrka för backend. |

**Valt: FastAPI.** Den inbyggda valideringen gör det enkelt att bygga och testa kraven i CORE-specen. Valet följer också den som ansvarar för backend. Nackdelen med två språk minskas genom att TypeScript-typerna genereras från API:ts OpenAPI-schema (`openapi-typescript`), se Konsekvenser.

### 2. Databas: SQLite

Alternativ: PostgreSQL eller en JSON-fil. PostgreSQL kräver en databasserver, vilket gör det svårare för någon annan att köra lösningen. En JSON-fil saknar transaktioner, som historiken behöver ([ADR-001](ADR-001-atomicitet-status-och-historik.md)). **SQLite** är en vanlig fil, kräver ingen installation och klarar både beständighet och transaktioner. Nackdelen är att bara en skrivning åt gången går igenom. Det räcker för en app som körs lokalt av en person, men inte för många samtidiga användare.

### 3. Utseende: vanliga shadcn/ui, ett register eller bara Tailwind

| | Vanliga shadcn/ui | Tredjepartsregister (t.ex. BOLDkit) | Bara Tailwind |
| --- | --- | --- | --- |
| För | Officiellt, MIT-licens, mycket använt. Tillgängliga grundkomponenter. AI-verktygen känner till det väl. Teman kan ändras senare. | Mer unikt utseende direkt. Bygger ovanpå shadcn. | Inget beroende. |
| Emot | Ser mer "standard" ut. | Små projekt: licens, underhåll och tillgänglighet måste kontrolleras. | Vi bygger varje komponent själva, vilket tar tid. |

**Valt: vanliga shadcn/ui tills vidare.** Amalia provar register lokalt på en egen branch. Om vi byter, gäller det bara temat. Oavsett val skrivs en gemensam instruktion (skill) så att alla agenter använder samma komponenter, i stället för att göra egna lösningar varje gång.

### 4. Grundkomponenter: Base UI eller Radix

shadcn/ui kan bygga på Radix eller Base UI. Båda ger tillgängliga komponenter (tangentbord, fokus, skärmläsare). Base UI är nyare och är det shadcn nu föreslår som standard. **Valt: Base UI** (förvalt i skelettet, PR #11 (frontend-skelett med React, Vite och TypeScript): https://github.com/desiboli/kundportal-ai-native-development/pull/11). Ingen i teamet hade starkare önskemål, och skillnaden märks inte i vårt flöde.

Risk: AI-verktygen har sett mer kod för Radix än för Base UI och kan föreslå Radix-mönster. Det fångas i granskningen och i instruktionen för designsystemet.

### 5. Pakethanterare: pnpm eller npm

npm följer med Node och kräver inget extra. **Valt: pnpm**, som Musse rekommenderade från sina projekt: snabbare installation och bättre skydd mot skadliga paket. pnpm kör inte paketens installationsskript om de inte uttryckligen tillåts. Det syns i `frontend/pnpm-workspace.yaml`, där bara `esbuild` får köra sitt skript. Nackdelen är ett steg till för den som ska köra projektet (pnpm måste installeras, t.ex. via `npm install -g pnpm` eller `corepack enable`).

### 6. Struktur: separata mappar eller monorepo

Skelettverktyget erbjöd ett monorepo. **Valt: separata mappar** (`backend/`, `frontend/`) i samma repo, eftersom backend och frontend använder olika språk och verktyg och har olika ansvariga. Det gör också att var och en kan köra sin del utan att förstå hela bygget.

## Konsekvenser

- **Att köra lösningen kräver Python 3.11, Node och pnpm.** README behöver beskriva alla tre, även för Windows.
- **SQLite kontrollerar inte främmande nycklar som standard.** Backenden måste slå på det med `PRAGMA foreign_keys=ON` för varje anslutning, annars kan en historikpost peka på ett ärende som inte finns.
- **Två språk:** typerna i frontend kan glida isär från backend. Därför genereras TypeScript-typerna från API:ts OpenAPI-schema med `openapi-typescript` (KSP-28). Tills dess är API-konventionerna och specarna det som håller ihop dem.
- **Frontendtester:** Vitest och Testing Library är planerade (Teststrategin) men ännu inte installerade i `frontend/`.
- **Designsystemet** behöver en egen instruktion för agenterna, så att utseendet inte ändras vid varje ny komponent.

## Öppna frågor

| Fråga | Ägare | När |
| --- | --- | --- |
| Byter vi till ett register eller behåller vanliga shadcn? | Amalia | Efter hennes test på branch |
| Vilken Node-version gäller (anges i README)? | Musse | Med frontendens körinstruktioner |
