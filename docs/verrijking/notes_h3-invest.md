# Notes batch "h3-invest" — artikelen 14, 15, 16, 17 (investeringssteun)

Testharnas: `test_h3invest.py` — 33/33 PASS tegen het evaluate-binary
(bindingen gestubd als parameters; in de mini-wet `accepted: true`, in de
fragmenten blijft `accepted: false`).

## Artikel 14 — eindpunt `voldoet_aan_voorwaarden_art_14`

AND over: hoofdstuk I (art. 3-binding) · drempel `aanmeldingsdrempel_art_14`
(art. 4 lid 1 a, 600 000 EUR) · kmo + primaire productie (art. 1 lid 1 a i —
handhaving hier, conform de untranslatable bij artikel 1) · lid 1 (aard van de
investering) · lid 3 (OR over doelstellingen a-g) · lid 4 (bio-energie,
guarded per alinea) · lid 5 (MEB-guard) · leden 6/7 (kosten-tussenstand) ·
lid 8 (irrigatie-guard) · lid 9 (vijf uitsluitingen, met de
lid-6-h/waakhonden-uitzonderingen) · lid 10 (GMO-verbod + sectorbreedte-OR) ·
intensiteitstoets tegen `maximale_steunintensiteit_pct_art_14`.

Tweede output `maximale_steunintensiteit_pct_art_14` (number): IF-keten met
lid 15 (irrigatieplafonds 100/80/65, gaan als "blijft beperkt tot" vóór de
verhogingen) → lid 14 (100) → lid 13 (85) → lid 12 (80) → default lid 11 (65).

- Lid 2 (wie de investering verricht) is permissief, geen voorwaarde — niet
  gemodelleerd; de somregel van lid 4 vierde alinea zit in de description van
  `energieproductie_overschrijdt_gemiddeld_jaarlijks_verbruik_niet`.
- Untranslatables (5): kostenafbakening leden 6/7 (incl. 10 %-grond,
  marktwaarde, Vo. 2020/741); irrigatievoorwaarden lid 6 f i-v (incl.
  5/25/50 %-waterbesparingseisen); lidstaat-drempelwaarden +
  duurzaamheidscriteria bio-energie (lid 4 laatste alinea); productuitsluiting
  wegens overcapaciteit (lid 10, open norm); klimaatadaptatie "waar passend"
  (lid 3 d).

## Artikel 15 — eindpunt `voldoet_aan_voorwaarden_art_15`

Eén zin: hoofdstuk I · kmo + primaire productie (art. 1 lid 1 a i, handhaving
hier) · `betreft_ruilverkaveling_van_landbouwgrond` ·
`steun_uitsluitend_voor_juridische_en_administratieve_kosten` (incl.
opmetingskosten) · `steunintensiteit_pct` ≤ 100. **Geen drempel-binding:
artikel 4 kent voor artikel 15 geen aanmeldingsdrempel** (staat niet in de
lijst van lid 1). Untranslatable: afbakening "werkelijk gemaakte" jur./adm.
kosten.

## Artikel 16 — eindpunt `voldoet_aan_voorwaarden_art_16`

Hoofdstuk I · kmo + primaire productie (hier uit de eigen lid-1-tekst) ·
verplaatsing landbouwbedrijfsgebouw · algemeen belang (lid 2, twee parameters,
open norm als untranslatable) · voorwaardelijke drempel: art. 4 lid 1 b geldt
alleen voor lid-4-steun → `OR(NOT modernisering, steunbedrag ≤ drempel)` ·
intensiteit ≤ 100 (noodzakelijke bovengrens uit leden 3 en 5).
Untranslatable: lid 4 vergt kostensplitsing (verplaatsingsdeel 100 %,
moderniseringsdeel art. 14 leden 12-15); ook de vraag of lid 5 dat weer op
100 % zet voor activiteiten nabij rurale woongebieden zit in die verdieping —
daarom geen aparte lid-5-parameter (het computable plafond is toch 100).
"Loutere vervanging is geen modernisering" (lid 4 tweede alinea) zit in de
description van de moderniseringsparameter.

## Artikel 17 — eindpunt `voldoet_aan_voorwaarden_art_17`

Hoofdstuk I · drempel `aanmeldingsdrempel_art_17` (art. 4 lid 1 c, 7,5 mln
EUR) · kmo + `OR(verwerking, afzet)` (art. 1 lid 1 a i — art. 17 staat níét in
de primaire-productie-uitzonderingslijst; handhaving hier) · lid 2 (activa
verwerking/afzet) · NOT lid 3 (biobrandstoffen uit voedingsgewassen) · lid 4
(MEB-guard, zelfde parameters als art. 14 lid 5) · leden 5-8
(kosten-tussenstand) · NOT lid 9 (normconformiteits-investeringen) · NOT lid
10 (GMO-verbod; art. 17 heeft géén sectorbreedte-zin, anders dan art. 14) ·
intensiteit ≤ `maximale_steunintensiteit_pct_art_17` (IF: lid 12 → 80,
default lid 11 → 65). Untranslatable: kostenafbakening leden 5-8.

## Nieuwe gedeelde parameters (meerdere artikelen raken dit)

| naam | herkomst | ook relevant voor |
|---|---|---|
| `milieueffectbeoordeling_vereist` / `_uitgevoerd` / `vergunning_verleend_voor_datum_toekenning` | art. 14 lid 5 = art. 17 lid 4 (identieke tekst) | andere MEB-artikelen (o.a. 44, 49, 55) |
| `steun_dekt_uitsluitend_in_aanmerking_komende_kosten` | art. 14 leden 6/7; art. 17 leden 5-8 | elk kosten-artikel; betekent "de kosten vallen binnen de categorieën van het ingeroepen artikel" — per artikel een eigen kostenlijst, gemarkeerde tussenstand |
| `doel_klimaatmitigatie_en_adaptatie`, `doel_duurzame_bioeconomie_en_beheer_natuurlijke_hulpbronnen`, `doel_biodiversiteit_ecosysteemdiensten_habitats` | art. 14 lid 3 e/f/g | art. 17 lid 12 a verwijst er expliciet naar; zelfde naam gebruikt |
| `investering_houdt_verband_met_dierenwelzijn` | art. 14 lid 12 a ("met dierenwelzijn") | art. 17 lid 12 a ("verbetering van het dierenwelzijn") — één naam voor beide formuleringen, descriptions citeren de eigen letter |
| `investering_door_jonge_landbouwer` | art. 14/17 lid 12 b | art. 18; begrip art. 2 punt 61 (lidstaat-gedefinieerd) — gemarkeerde tussenstand |
| `investering_in_ultraperifeer_gebied_of_kleinere_eilanden_egeische_zee` | art. 14/17 lid 12 c | meer intensiteits-artikelen |
| `is_klein_landbouwbedrijf` | art. 14 lid 13 (art. 28 Vo. 2021/2115) | gemarkeerde tussenstand |
| `in_strijd_met_verboden_of_beperkingen_vo_1308_2013` | art. 14 lid 10 = art. 17 lid 10 | andere M1-artikelen met dezelfde zin |
| `betreft_herstel_van_beschadigd_agrarisch_productiepotentieel` | art. 14 lid 6 h / lid 9 b+d / lid 14 b | art. 37 |
| `vergunning_verleend_voor_datum_toekenning` | zie MEB | — |

## Open vragen

1. **Kmo-handhaving op artikelniveau** (artt. 14/15/17 uit art. 1 lid 1 a i):
   bewust dubbel met de algemene kmo-toets in art. 1, omdat het
   art.-1-eindpunt artikel-blind is (OR over categorieën); juridisch de
   letter van art. 1, legal_basis in commentaar. Als golf-2-artikelen dit
   anders oplossen (bijv. via `steun_artikel`), gelijktrekken.
2. Art. 16 lid 5 vs lid 4: verhoogt lid 5 óók het moderniseringsdeel naar
   100 %? Letter is niet eenduidig; zit nu in de lid-4-untranslatable.
3. `steunintensiteit_pct` meet bij art. 15 tegen "werkelijk gemaakte kosten"
   en elders tegen "in aanmerking komende kosten" — zelfde parameternaam,
   basis staat per artikel in de description.
