# Verrijkingsverslag — LVV breedte-eerst (cyclus 1)

Afgerond 19 augustus 2026. Doelbestand:
`regulation/eu/eu_verordening/landbouwvrijstellingsverordening/2023-12-13.yaml`
(schema v0.5.6, valide). De verrijking draaide desk-side in golven, buiten de
editor-pijplijn om (die liep vast op de documentomvang), maar volgens dezelfde
skills-methode: law-generate → reverse-validate, plus de concept-hygiëne- en
golden-route-passes die de pijplijn niet kent.

## Eindstand

| | |
|---|---|
| artikelen met machine_readable | 57 van 67 (10 bewuste skips: art. 2 definities, 10-13 procedure, 62-64 slot) |
| eindpunten (`voldoet_aan_voorwaarden_art_N` e.a.) | 55 |
| untranslatables | 111, alle `accepted: false` — **reviewwachtrij** |
| unieke parameters | 420 (na hygiëne-merge van 440) |
| engine-tests golven 1-2 | ~294, alle groen (stubs) |
| golden routes (live ketens, geen stubs) | 3/3 groen na alle fixes |

## Architectuur

Hoofdstuk I is de gedeelde poortlaag: art. 1 (`valt_binnen_toepassingsgebied`,
met Bijlage-I-binding voor kmo), art. 3 (`voldoet_aan_gemeenschappelijke_voorwaarden`
= AND over art. 1/5/6/8/9), art. 4 (per-artikel drempel-constanten), Bijlage I
(`is_kmo`). Elk hoofdstuk-III-artikel bindt de art-3-poort plus zijn eigen
drempel en toetst daarbovenop alleen zijn eigen letter. Berekeningen
(subsidiabele kosten, BSE, verdiscontering) zijn untranslatables; de
toetsbare voorwaarden (drempels, intensiteiten, kringen, uitsluitingen) zijn
uitvoerbaar.

## Verificatie (golf 3) — bevindingen en toegepaste fixes

Vier reverse-validators (elk element herleid naar de eigen letter), één
hygiëne-audit, één golden-route-bouwer. Verslagen: `review_*.md`, `hygiene.md`,
`golden_routes.md` in deze map. Toegepast op het wetbestand:

1. **12 letter-fixes** uit de reverse-validatie, o.a.: art. 6 lid 5 f miste de
   art-28-tak; art. 36 conflateerde jaarplafond en projectdrempel op één
   scalar; art. 37 miste de taxatie-eis; art. 18/23/25/26 handhaafden de
   art-1-beperking (kmo + primaire productie) niet waar 14/15/16 dat wel
   deden; art. 24 uitzonderings-lek; art. 26 lid 15 ontbrak; art. 49/50
   toetsten hun eigen lid-1-scope niet; art. 52 miste de kostenlijst.
   Nul verzonnen voorwaarden aangetroffen.
2. **Hernoem-kaart hygiëne** (A1-A13 + splitsingen): 108 vervangingen,
   artikel-gescoped. Valse vrienden gesplitst (`betreft_clld_project` in
   60/61; `basisdiensten_en_infrastructuur_in_plattelandsgebied` in 55).
3. **Negatie-herintreding lidmaatschap** opgelost: één canonieke positieve
   parameter `lidmaatschap_is_toegangsvoorwaarde` (21/22 toetsen de
   ontkenning via NOT; 23/24 hernoemd).
4. **Centrale besluiten**: dangling `endpoint:` op art. 4 verwijderd;
   `legal_basis.law` overal genormaliseerd naar het `$id`
   (`landbouwvrijstellingsverordening`, 90 plekken).
5. **Adjudicatie art. 61**: de hygiëne-audit claimde een ontbrekende
   kmo-toets; de letter van art. 61 zegt "ondernemingen", nergens kmo.
   Geen fix — de spanning met art. 4 lid 1 v ("kmo's") is een **jurist-vraag**.

## Golden routes (fixtures in deze map, canonieke parameternamen)

1. `golden_route_1.json` — ruilverkaveling (art. 15) → **true**, 65 parameters,
   alle bindingen live door de echte keten.
2. `golden_route_2.json` — zelfde casus, `is_onderneming_in_moeilijkheden: true`
   → **false**: één art-1-feit laat elk eindpunt omvallen, zoals de letter wil.
3. `golden_route_3.json` — stalverduurzaming (art. 14, doel dierenwelzijn,
   80% via lid 12 a) → **true** — de oorspronkelijke praktijkcasus van dit
   dossier.

## Bekende beperkingen (bewust open)

- **`steun_artikel`-proxy (art. 6 lid 5)**: onbewaakt — een casus die claimt
  onder art. 33 te vallen ontloopt de aanvraag-vooraf-eis zonder dat iets de
  claim toetst. Echte binding stuit op een cirkel (art. 6 ← art. 3 ← art. N);
  oplossen vergt gesplitste eindpunten (artikel-voorwaarden zonder poort).
  Architectuurbesluit voor cyclus 2.
- **Engine kent geen partiële evaluatie**: elke ontbrekende parameter is een
  harde fout ("Variable not found"), en `required: false` beschermt alleen
  takken die niet bereikt worden. Het filter-product moet daarom prefillen
  en/of vragen sequencen; de "onbekend"-emmer bestaat nog niet engine-side.
- **Description-eisen uit de hygiëne-audit** (sectie c) nog niet toegepast:
  definitieplaats-verwijzingen (art. 2 punt 11 bij 41/44/46; Bijlage I bij
  `begunstigde_categorie_art_56`; wees-markeringen bij
  `verbintenis_valt_onder_art_34`/`_35`, `kosten_vallen_onder_art_20`,
  `is_eip_of_clld_steun_art_39_40_60_61`).
- **Harmonisatiekandidaten bij verdieping** (hygiene.md sectie d):
  betaalroute-enum, MEB-tweeluik, termijn-datums art. 29, intermediair-as,
  enum-suffix-conventie.

## Reviewwachtrijen voor de mens

1. **111 untranslatables** — per stuk beoordelen en `accepted: true` zetten
   waar het gat klopt (RFC-012: onbeoordeeld blokkeert executie).
2. **Jurist-vragen** — verzameld in de vier `review_*.md`-bestanden plus de
   losse batch-notes (`notes_*.md`); zwaartepunten: art. 61 kmo/ondernemingen,
   art. 22 lid 9 "verwerking en afzet", art. 28 lid 3 d (M1-lezing),
   art. 6 "deze vereisten", art. 14 voorrang irrigatieplafond.
3. **Per-artikel review in de editor** zodra dit op de traject-branch staat.
