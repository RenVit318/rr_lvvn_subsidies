# Notes batch h3-milieu — artikelen 32-36 (LVV)

Alle vijf fragmenten schema-valide (v0.5.6, jsonschema op volledige mini-wet)
en getest via het evaluate-binary: **26/26 tests geslaagd**
(`test_h3-milieu.py` in deze map, herdraaibaar). In de mini-testwetten stond
tijdelijk `accepted: true`; de fragmenten houden `accepted: false`. Bindingen
(art 3-poort + art 4-drempels) zijn in de mini-wetten gestubd als parameters;
in de fragmenten staan de echte interne `source.output`-bindingen.

## Nieuwe gedeelde parameters (meerdere artikelen raken deze)

| naam | type | artikelen | betekenis |
|---|---|---|---|
| `teelttype` | string | 34, 35 | `EENJARIG` / `GESPECIALISEERD_BLIJVEND` / `ANDER_LANDGEBRUIK` — kiest de teelt-variant van de art-4-drempel én het lid-15/lid-11-maximum (conform de brief) |
| `in_eerste_periode` | boolean | 33 (en vermoedelijk 45) | steun valt in de eerste periode van ten hoogste vijf jaar; kiest kale drempel vs `_na_eerste_periode` |
| `verbintenis_gaat_verder_dan_verplichte_normen` | boolean | 34, 35 | lid 3 (punten a-c) — let op: art 35 lid 3 b noemt óók dierenwelzijn; zelfde begrip, description verschilt per artikel |
| `verplichte_normen_omschreven_in_nationale_rechtsgrondslag` | boolean | 34, 35 | lid 4 |
| `toegang_tot_kennis_en_opleiding_geborgd` | boolean | 34, 35 | lid 6 resp. lid 7 |
| `herzieningsclausule_vastgesteld` | boolean | 34, 35 | lid 11 resp. lid 8 |
| `steun_jaarlijks_per_hectare` | boolean | 33, 34 | jaarlijks per hectare verleend/betaald |
| `steun_jaarlijks_verleend` | boolean | 35 | art 35 lid 9 zegt alleen "jaarlijks" (per hectare zit daar impliciet in lid 11); bewust apart gehouden van `steun_jaarlijks_per_hectare` |
| `steunduur_jaren` | number | 32 | duur van de steunverlening in jaren (lid 12: ≤ 7) |

## Per artikel

### Art 32 — samenwerking (eindpunt: `voldoet_aan_voorwaarden_art_32`)
- **Geen drempel-binding**: artikel 4 kent geen `aanmeldingsdrempel_art_32`
  (bevestigd in het gebouwde art_4-fragment). Bij investeringsverrichtingen
  loopt de drempel via het toepasselijke investeringsartikel → untranslatable
  (leden 10+14). Tweede untranslatable: kosten-subsidiabiliteit lid 11.
- Enums: `samenwerkingsvorm` (lid 4 a-c, met pensioenleeftijd-tak bij
  `BEDRIJFSOPVOLGING`), `samenwerkingsactiviteit` (lid 6 a-i, 9 waarden).
  Lid 8 (≤ 1 intermediair) alleen bij activiteiten d/e.
- Tests: pos 2×, neg op lid 3, 4c, 8, 12.

### Art 33 — Natura 2000 (eindpunt: `voldoet_aan_voorwaarden_art_33`)
- Drempeltoets via IF over `in_eerste_periode`: kale drempel (500 EUR/ha/jr)
  vs `aanmeldingsdrempel_art_33_na_eerste_periode` (200). De lid-5-maxima
  vallen numeriek samen met die drempels; één toets draagt beide zinsnedes
  (gedocumenteerd in de output-description).
- Untranslatables: vergoedingsgrondslag lid 2; 5%-areaal-aggregatie lid 4b
  (boolean-tussenstand `gebied_binnen_vijf_procent_grens`).
- Tests: pos 2×, neg op drempel-na-periode, lid 4b, lid 3.

### Art 34 — agromilieuklimaat (eindpunt: `voldoet_aan_voorwaarden_art_34`)
- Drempeltoets via IF over `teelttype` naar de drie teelt-drempels; plus
  IN-toets dat teelttype een van de drie lid-15-categorieën is.
- Lid 9 (extensivering veehouderij) als IF-tak met twee booleans.
- Untranslatables: lid 5 (24-maandenvenster), lid 7 (verbintenisperiode 5-7
  jaar met open uitzonderingsgronden), lid 10 (kwaliteitscriteria
  koolstoflandbouw), lid 12 (vergoedingsgrondslag). Lid 8 bestaat niet meer
  (M1 heeft het geschrapt).
- Tests: pos 2×, neg op drempel, lid 9b, lid 13.

### Art 35 — biologische landbouw (eindpunt: `voldoet_aan_voorwaarden_art_35`)
- Zelfde patroon als 34; extra lid-9-uitsluitingen: NOT(valt onder art 34) én
  NOT(kosten onder art 20).
- Untranslatables: lid 5 (24 maanden), lid 6 (eerste periode 5-7 jaar met
  uitzonderingen), lid 9 (vergoedingsgrondslag), lid 10 (investeringen →
  artikelen 14/17).
- Tests: pos 1×, neg op art-34-samenloop, art-20-kosten, teelttype, intensiteit.

### Art 36 — cultureel/natuurlijk erfgoed (eindpunt: `voldoet_aan_voorwaarden_art_36`)
- Drempel `aanmeldingsdrempel_art_36` (600k per project) + lid-6-cap voor
  `GEKAPITALISEERDE_WERKZAAMHEDEN` (10 000 EUR/jaar, literal 1000000) via IF
  over `kostensoort`. **Geen untranslatables.**
- Meet-caveat: `steunbedrag` is per investeringsproject, maar bij
  gekapitaliseerde werkzaamheden meet lid 6 per jaar; de parameter-description
  benoemt dat. Bij verdieping evt. splitsen in twee bedragen.
- Tests: pos 2×, neg op drempel, lid 6, lid 3.

## Open vragen / twijfels

1. **Drempel- vs maximum-samenval (33/34/35)**: de art-4-drempels zijn per
   letter gelijk aan de artikel-maxima; ik toets één keer tegen de gebonden
   drempel en documenteer beide grondslagen. Alternatief (dubbele toets met
   literals) leek dubbelop.
2. **Art 32 lid 9** (overeenstemming met art 206-210bis Vo 1308/2013) en
   **lid 2** (GLB-doelstellingen Vo 2021/2115) zijn externe-verordening-feiten,
   als boolean-parameters gemodelleerd — geen cross-law-binding mogelijk
   (die verordeningen zitten niet in het corpus).
3. **Lidstaat-verplichtingen** (art 34 lid 6 / art 35 lid 7 kennis+opleiding;
   lid 4 nationale rechtsgrondslag) zijn als toetsbare booleans gemodelleerd,
   niet als untranslatable: het zijn feiten over de steunregeling.
4. Art 34 lid 10 eerste zin ("kan betrekking hebben op collectieve en
   resultaatgebaseerde regelingen") is permissief — geen voorwaarde; alleen de
   koolstoflandbouw-kwaliteitscriteria zijn als untranslatable opgenomen.
