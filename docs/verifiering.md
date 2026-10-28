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

| Krav | Vad | Test | Nivå | För hand | Status |
| --- | --- | --- | --- | --- | --- |
| CORE-01 | Skapa ärende, status `new` | – | Integration | Ja | Ej påbörjad |
| CORE-02 | Ärendet finns kvar efter omstart | – | Integration, omstart | Ja | Ej påbörjad |
| CORE-03 | Lista, nyaste först | – | Integration | Ja | Ej påbörjad |
| CORE-04 | Hämta ett ärende med id | – | Integration | Ja | Ej påbörjad |
| CORE-05 | Trimning före och efter (B10) | – | Integration | Nej | Ej påbörjad |
| CORE-06 | Rubrik saknas | `test_error_format.py` (felsvaret) | Integration | Ja | Delvis: att inget sparas prövas i KSP-22 |
| CORE-07 | Beskrivning saknas | `test_error_format.py` (felsvaret) | Integration | Nej | Delvis: att inget sparas prövas i KSP-22 |
| CORE-08 | Okänd kategori eller prioritet | `test_error_format.py` (felsvaret) | Integration | Nej | Delvis: att inget sparas prövas i KSP-22 |
| CORE-09 | `status` skickas vid skapande | `test_error_format.py` | Integration | Nej | Delvis: att inget sparas prövas i KSP-22 |
| CORE-10 | Okänt id eller id som inte är heltal ger 404 | `test_error_format.py` (id som inte är heltal) | Integration | Nej | Delvis: okänt heltals-id när KSP-23 finns |
| CORE-11 | Bara blanktecken eller osynliga tecken | – | Integration | Ja | Ej påbörjad |
| CORE-12 | Rubrik högst 100 tecken, efter trimning | – | Integration | Ja | Ej påbörjad |
| CORE-13 | Beskrivning högst 2000 tecken | – | Integration | Nej | Ej påbörjad |
| CORE-14 | Svenska tecken och emoji oförändrade | – | Integration | Ja | Ej påbörjad |
| CORE-15 | Tom lista är inte ett fel | – | Integration | Nej | Ej påbörjad |
| CORE-16 | Fel på svenska, `{"detail": ...}` | `test_error_format.py` | Integration | Ja | Grönt |
| CORE-17 | Fel datatyp, trasig JSON, ogiltig UTF-8 | `test_error_format.py` | Integration | Nej | Grönt |
| CORE-18 | Flera fel samtidigt, i fältordningen | `test_error_format.py` | Integration | Nej | Grönt |

Testerna för CORE skrivs i KSP-25 och KSP-26 (Nicklas). Felsvaren ovan kommer från KSP-21
(Azalea, PR #30, svenskt felformat i backenden):
https://github.com/desiboli/kundportal-ai-native-development/pull/30.

### Statuslogik och historik (HIST)

| Krav | Vad | Test | Ägare | För hand | Status |
| --- | --- | --- | --- | --- | --- |
| HIST-01 | `created`-post när ärendet skapas | – | Azalea | Nej | Ej påbörjad |
| HIST-02 | Statusbyte ger `status_changed`-post | – | Azalea | Ja | Ej påbörjad |
| HIST-03 | Historiken äldst först | – | Azalea | Ja | Ej påbörjad |
| HIST-04 | Historiken finns kvar efter omstart | – | Azalea | Ja | Ej påbörjad |
| HIST-05 | Tidslinjen i detaljvyn | – | Amalia | Ja | Ej påbörjad |
| HIST-06 | Ogiltig status ger 422 | `test_error_format.py` (saknad status och fel datatyp) | Nicklas | Nej | Delvis: resten skrivs i KSP-27 |
| HIST-07 | Samma status ger 409 | – | Nicklas | Nej | Ej påbörjad |
| HIST-08 | Okänt ärende ger 404 | – | Azalea | Nej | Ej påbörjad |
| HIST-09 | Inget ändras om historikposten inte kan sparas | – | Azalea | Nej | Ej påbörjad |
| HIST-10 | Ingen historikpost när ärendet inte kan skapas | – | Azalea | Nej | Ej påbörjad |
| HIST-11 | Samma tid, ordnas efter id | – | Azalea | Nej | Ej påbörjad |
| HIST-12 | Ärende utan statusbyten har bara `created` | – | Azalea | Nej | Ej påbörjad |
| HIST-13 | Avslutat ärende kan öppnas igen | – | Nicklas | Nej | Ej påbörjad |
| HIST-14 | Fel på svenska för status och historik | `test_error_format.py` (backenddelen) | Azalea, Amalia (UI) | Ja | Delvis: UI-delen saknas |

Ägare enligt [Teststrategin](teststrategi.md) (avsnitt 2). Nicklas tester för HIST-06, 07
och 13 skrivs i KSP-27.

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
