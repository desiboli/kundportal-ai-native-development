# Verifieringsplan

> Ansvarig: Nicklas (yrrving) · KSP-47 (verifieringsplanen i Linear) · Skapad 2026-10-27
> Visar **att** varje krav har kontrollerats och med vilket resultat. **Hur** teamet testar
> står i [Teststrategin](teststrategi.md) och upprepas inte här.
> Id förklaras kort: **CORE-xx** är kraven för kärnan ([SPEC-karna.md](specs/SPEC-karna.md)),
> **HIST-xx** kraven för statuslogik och historik ([SPEC-arendehistorik.md](specs/SPEC-arendehistorik.md))
> och **KSP-xx** ärenden i Linear.

## 1. När ett krav räknas som verifierat

Alla fyra ska stämma:

1. Testet är grönt i CI.
2. PR:en med testet är granskad av någon annan än den som skrev det.
3. Testet är mutationsprövat, steg 1 i [Teststrategin](teststrategi.md) (avsnitt 3), så att det
   faller av rätt anledning.
4. Om kravet syns i gränssnittet är det också kontrollerat för hand (avsnitt 3 nedan).

## 2. Översikt per krav

**Status:** *Ej påbörjad* · *Test skrivet* (finns men faller, koden saknas) · *Delvis* (en del
av kravet är grönt) · *Grönt* · *Verifierat* (alla fyra punkterna i avsnitt 1).

### Kärnan (CORE)

Förväntat resultat är en kort sammanfattning av kravet i [SPEC-karna.md](specs/SPEC-karna.md)
(avsnitt 5). Länken går till testfilen, och testnamnet börjar med krav-id:t.

| Krav | Vad | Förväntat | Test | Nivå | För hand | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CORE-01 | Skapa ärende, status `new` | 201 med ärendet, `status` `new`, `created_at` i UTC. Sparas med samma uppgifter. | [test_create_ticket.py](../backend/tests/test_create_ticket.py) (`test_core01_…`, 2 tester) | Integration | Ja | Grönt |
| CORE-02 | Ärendet finns kvar efter omstart | Ny engine och session mot samma fil: ärendet finns med samma uppgifter. | [test_core_read.py](../backend/tests/test_core_read.py) (`test_core02_ticket_survives_restart`) | Integration, omstart | Ja | Grönt |
| CORE-03 | Lista, nyaste först | Alla ärenden, `created_at` fallande, sedan `id` fallande. | [test_core_read.py](../backend/tests/test_core_read.py) (`test_core03_…`, 3 tester) | Integration | Ja | Grönt |
| CORE-04 | Hämta ett ärende med id | 200 med exakt de uppgifter som sparades. | [test_core_read.py](../backend/tests/test_core_read.py) (`test_core04_…`, `test_core03_list_items_match_get`) | Integration | Ja | Grönt |
| CORE-05 | Trimning före och efter (B10) | Blanktecken och nollbreddstecken i ändarna tas bort, tecken inne i texten behålls. | [test_create_ticket.py](../backend/tests/test_create_ticket.py) (`test_core05_…`, 3 tester) | Integration | Nej | Grönt |
| CORE-06 | Rubrik saknas | 422 "Rubrik måste fyllas i.", inget sparas. | [test_error_format.py](../backend/tests/test_error_format.py) (felsvaret), [test_create_ticket.py](../backend/tests/test_create_ticket.py) (`test_ksp22_nothing_saved_on_422`) | Integration | Ja | Grönt |
| CORE-07 | Beskrivning saknas | 422 "Beskrivning måste fyllas i.", inget sparas. | Samma som CORE-06 | Integration | Nej | Grönt |
| CORE-08 | Okänd kategori eller prioritet | 422 "Välj en giltig kategori." (eller prioritet), inget sparas. | Samma som CORE-06 | Integration | Nej | Grönt |
| CORE-09 | `status` skickas vid skapande | 422 "Status sätts automatiskt och kan inte anges när ett ärende skapas.", inget sparas. | Samma som CORE-06 (`test_core09_…`) | Integration | Nej | Grönt |
| CORE-10 | Okänt id eller id som inte är heltal ger 404 | 404 "Ärendet finns inte.", även för `GET /tickets/abc`. | [test_core_read.py](../backend/tests/test_core_read.py) (okänt heltal), [test_error_format.py](../backend/tests/test_error_format.py) (inte heltal) | Integration | Nej | Grönt |
| CORE-11 | Bara blanktecken eller osynliga tecken | Fältet räknas som tomt: 422 "… måste fyllas i.", inget sparas. | [test_create_ticket.py](../backend/tests/test_create_ticket.py) (rubriken), beskrivningen i [PR #39](https://github.com/desiboli/kundportal-ai-native-development/pull/39) | Integration | Ja | Delvis: beskrivningen grön i PR #39, inte mergad |
| CORE-12 | Rubrik högst 100 tecken, efter trimning | 100 tecken godkänns, 101 ger 422 och inget sparas. Räknas efter trimning. | [test_create_ticket.py](../backend/tests/test_create_ticket.py) (`test_core12_…`, 2 tester) | Integration | Ja | Grönt |
| CORE-13 | Beskrivning högst 2000 tecken | 2000 tecken godkänns, 2001 ger 422 och inget sparas. | [PR #39](https://github.com/desiboli/kundportal-ai-native-development/pull/39) (`test_core_rules.py`) | Integration | Nej | Grönt i PR #39, inte mergad |
| CORE-14 | Svenska tecken och emoji oförändrade | Texten sparas och visas oförändrad. Sammansatta emoji räknas som sina kodpunkter (B11). | [test_create_ticket.py](../backend/tests/test_create_ticket.py) (`test_core14_…`), räkningen i [PR #39](https://github.com/desiboli/kundportal-ai-native-development/pull/39) | Integration | Ja | Delvis: räkningen (B11) grön i PR #39, inte mergad |
| CORE-15 | Tom lista är inte ett fel | 200 med `[]`. | [test_core_read.py](../backend/tests/test_core_read.py) (`test_core15_empty_list_returns_200`) | Integration | Nej | Grönt |
| CORE-16 | Fel på svenska, `{"detail": ...}` | Svenska meddelanden, aldrig stacktrace, SQL eller engelska fältnamn. | [test_error_format.py](../backend/tests/test_error_format.py) | Integration | Ja | Grönt |
| CORE-17 | Fel datatyp, trasig JSON, ogiltig UTF-8 | 422 med bara "Ogiltig indata.", inget sparas. | [test_error_format.py](../backend/tests/test_error_format.py) (`test_core17_…`), inget sparas i [PR #39](https://github.com/desiboli/kundportal-ai-native-development/pull/39) | Integration | Nej | Delvis: "inget sparas" grönt i PR #39, inte mergad |
| CORE-18 | Flera fel samtidigt, i fältordningen | 422 med alla meddelanden i ordningen rubrik, beskrivning, kategori, prioritet, status. Inget sparas. | [test_error_format.py](../backend/tests/test_error_format.py) (`test_core18_…`), inget sparas i [PR #39](https://github.com/desiboli/kundportal-ai-native-development/pull/39) | Integration | Nej | Delvis: "inget sparas" grönt i PR #39, inte mergad |

Inget krav är *Verifierat* än: mutationsprövningen (KSP-44) görs när statusbytet (KSP-24)
finns. Felsvaren kommer från KSP-21 (Azalea, PR #30),
https://github.com/desiboli/kundportal-ai-native-development/pull/30, och skapa, lista och
visa från KSP-22 och KSP-23. Nicklas tester för CORE (KSP-25 och KSP-26) finns i PR #39.

### Statuslogik och historik (HIST)

Förväntat resultat är en kort sammanfattning av kravet i
[SPEC-arendehistorik.md](specs/SPEC-arendehistorik.md) (avsnitt 6).

| Krav | Vad | Förväntat | Test | Ägare | För hand | Status |
| --- | --- | --- | --- | --- | --- | --- |
| HIST-01 | `created`-post när ärendet skapas | Status `new` och exakt en post `created` (`null` → `new`). | – | Azalea | Nej | Ej påbörjad |
| HIST-02 | Statusbyte ger `status_changed`-post | Ny status och en post `status_changed` med rätt från och till. | – | Azalea | Ja | Ej påbörjad |
| HIST-03 | Historiken äldst först | Äldst först, `to_status` i en post är `from_status` i nästa. | – | Azalea | Ja | Ej påbörjad |
| HIST-04 | Historiken finns kvar efter omstart | Status och historik oförändrade med ny engine och session, alla fält. | – | Azalea | Ja | Ej påbörjad |
| HIST-05 | Tidslinjen i detaljvyn | Varje post med svenska etiketter och lokal tid, senaste stämmer med status. | – | Amalia | Ja | Ej påbörjad |
| HIST-06 | Ogiltig status ger 422 | 422 "Välj en giltig status." (fel datatyp: "Ogiltig indata."), status och historik oförändrade. | [test_error_format.py](../backend/tests/test_error_format.py) (saknad status och fel datatyp), resten i [PR #43](https://github.com/desiboli/kundportal-ai-native-development/pull/43) | Nicklas | Nej | Delvis: PR #43 väntar på statusbytet (KSP-24) |
| HIST-07 | Samma status ger 409 | 409 "Ärendet har redan den statusen.", ingen ny post. Alla fyra statusar. | Servicedelen: [test_history.py](../backend/tests/test_history.py) (Azalea). API:t: [PR #43](https://github.com/desiboli/kundportal-ai-native-development/pull/43) | Nicklas | Nej | Delvis: API-delen väntar på statusbytet (KSP-24) |
| HIST-08 | Okänt ärende ger 404 | 404 "Ärendet finns inte.", inget skapas. Även id som inte är heltal. | – | Azalea | Nej | Ej påbörjad |
| HIST-09 | Inget ändras om historikposten inte kan sparas | 503 "Statusen kunde inte ändras. Försök igen.", gammal status kvar, nästa byte lyckas. | – | Azalea | Nej | Ej påbörjad |
| HIST-10 | Ingen historikpost när ärendet inte kan skapas | Ingen historikpost kvar efter en avvisad `POST`. | – | Azalea | Nej | Ej påbörjad |
| HIST-11 | Samma tid, ordnas efter id | Samma `occurred_at` ordnas efter `id`, alltid lika. | – | Azalea | Nej | Ej påbörjad |
| HIST-12 | Ärende utan statusbyten har bara `created` | En lista med exakt en post (`created`), inte tom. | – | Azalea | Nej | Ej påbörjad |
| HIST-13 | Avslutat ärende kan öppnas igen | `closed` → `new` godkänns och loggas som vanligt statusbyte. | [PR #43](https://github.com/desiboli/kundportal-ai-native-development/pull/43) | Nicklas | Nej | Test skrivet: väntar på statusbytet (KSP-24) |
| HIST-14 | Fel på svenska för status och historik | Svenska meddelanden, aldrig stacktrace eller databasdetaljer. | [test_error_format.py](../backend/tests/test_error_format.py) (backenddelen) | Azalea, Amalia (UI) | Ja | Delvis: UI-delen saknas |

Ägare enligt [Teststrategin](teststrategi.md) (avsnitt 2). Azalea fyller i test och status
för sina rader i KSP-48. Nicklas tester för HIST-06, 07 och 13 (KSP-27) finns i PR #43.

## 3. Kontroll för hand

Görs före varje veckostatus och före demon, mot den senaste `main`. Resultatet skrivs in i
avsnitt 4 med "för hand" i kolumnen Typ.

**Demoflödet**

- [ ] Skapa ett ärende i formuläret (CORE-01).
- [ ] Ärendet syns överst i listan (CORE-03).
- [ ] Detaljvyn visar samma uppgifter som skrevs in (CORE-04).
- [ ] Byt status. Den nya statusen syns direkt (HIST-02).
- [ ] Historiken visar skapandet och statusbytet, äldst först (HIST-03, HIST-05).

**Felmeddelanden i gränssnittet**

- [ ] Tom rubrik och rubrik med bara mellanslag ger "Rubrik måste fyllas i." (CORE-06, CORE-11).
- [ ] En rubrik på 101 tecken ger "Rubriken får vara högst 100 tecken." (CORE-12).
- [ ] En rubrik med å, ä, ö och emoji sparas och visas oförändrad (CORE-14).
- [ ] Meddelandena går att förstå utan att veta hur systemet fungerar (CORE-16, HIST-14).

**Omstart**

- [ ] Starta om backenden. Ärendet och dess historik finns kvar (CORE-02, HIST-04).

## 4. Körresultat

En rad per körning. Minst en gång i veckan och före slutleveransen. Linear-ärendena länkar hit.
Commit skrivs som en hel länk, t.ex.
`https://github.com/desiboli/kundportal-ai-native-development/commit/<hash>`, så att det går
att klicka sig till exakt den version som kördes.

| Datum | Commit | Typ | Resultat | Körd av |
| --- | --- | --- | --- | --- |
| 2026-10-28 | https://github.com/desiboli/kundportal-ai-native-development/commit/65c9f4dc98f9c496e8bf980db8b7f2fe6deb2da6 | automatiskt (pytest) | 107 passed | Nicklas |

Kommando (macOS/Linux): `cd backend && .venv/bin/python -m pytest -q`. Windows: se
[Teststrategin](teststrategi.md) (avsnitt 5).

## 5. Mutationsprövning

Mutationerna står i [Teststrategin](teststrategi.md) (avsnitt 3) och i specarna. Här sparas
resultatet: vilket test som föll, eller att inget föll och vad som ändrades i testet.

| Datum | Steg | Mutation | Krav | Test som föll | Gjord av |
| --- | --- | --- | --- | --- | --- |

## 6. Testförslag från AI

En rad per gång en instruktion i [`docs/ai/`](ai/) används (Teststrategin, avsnitt 4).

| Datum | Krav | Instruktion | Förslag | Accepterade / ändrade / avvisade | Varför | Av |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-10-25 | CORE-11–14 | v1 | 23 tester, 6 frågor | Provkörning, inga tester skrivna | Jämförelse mot facit, se [v2-nicklas](ai/testforslag-v2-nicklas.md) | Nicklas |
| 2026-10-25 | CORE-11–14 | v2-nicklas | 29 tester (24 *Måste*) | Provkörning, inga tester skrivna | Alla 19 fall i facit kom med, se [v2-nicklas](ai/testforslag-v2-nicklas.md) | Nicklas |
| 2026-10-27 | KSP-21: CORE-09, 10, 16–18, HIST-14 | v1 | 25 tester, 6 frågor | 25 / 0 / 0 | Alla valdes, frågorna besvarades. Se PR #30 (svenskt felformat i backenden): https://github.com/desiboli/kundportal-ai-native-development/pull/30 | Azalea |
| 2026-10-28 | KSP-25 och 26 (tester för kärnan): CORE-02–05, 10–15, 17, 18 | v2-nicklas | 13 tester | 11 / 1 / 1 | Ett ändrades: två ärenden med samma tid skapas via tjänsten med en fast klocka. Ett ströks, rubrik med ett tecken fångade inget nytt. Se PR #39 (längd, tomma fält och tecken): https://github.com/desiboli/kundportal-ai-native-development/pull/39 och PR #41 (lista och visa ärenden): https://github.com/desiboli/kundportal-ai-native-development/pull/41 | Nicklas |
| 2026-10-28 | KSP-27 (tester för statusreglerna): HIST-06, 07, 13 | v2-nicklas, körd efter att testerna skrevs | 6 tester (4 Måste, 2 Bra att ha), 4 frågor | 4 / 0 / 0, 2 väntar på svar från specägaren | Måste-testerna var redan skrivna, samma 23 fall. Bra att ha-testerna väntar på svar om null och andra fält i PATCH. Se PR #43 (statusreglerna): https://github.com/desiboli/kundportal-ai-native-development/pull/43 | Nicklas |
