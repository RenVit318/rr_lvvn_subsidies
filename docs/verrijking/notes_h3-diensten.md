# Notes batch h3-diensten — LVV artikelen 23, 24, 25, 26

Alle vier fragmenten getest via het evaluate-binary: **35/35 tests geslaagd**
(`test_h3_diensten.py` in deze map; herdraaibaar). In de mini-testwetten stond
tijdelijk `accepted: true` op de untranslatables; de fragmenten houden
`accepted: false`. Binding `voldoet_aan_gemeenschappelijke_voorwaarden` (art 3)
in elk fragment als interne `input`-source; in de tests gestubd als parameter.

**Geen drempel-bindingen in deze batch**: artikel 4 kent voor de artikelen 23,
24, 25 en 26 géén aanmeldingsdrempel (gecontroleerd tegen de gemergde
art-4-outputs in het wetbestand en `art_4.yaml`). In elke input-description
genoteerd.

## Artikel 23 — bedrijfsvervangingsdiensten (eindpunt: voldoet_aan_voorwaarden_art_23)

- Lid 2 als twee enum-parameters: `vervangen_persoon` (LANDBOUWER /
  LID_LANDBOUWHUISHOUDEN / WERKNEMER_LANDBOUW) en `reden_afwezigheid` (8
  waarden, incl. GEVAL_ART_21_LID_3_PUNT_C als expliciete kruisverwijzing);
  plus `steun_dekt_werkelijke_kosten_vervanging`.
- Lid 3 duurtoets als IF: verlof ≤ 6 mnd (telkens), militaire dienst ≤
  `duur_militaire_dienst_maanden`, anders ≤ 3 mnd/jaar. De meeteenheid
  ("per jaar" vs "telkens") zit in de parameter-description.
- Lid 4: `steunvorm` EQUALS GESUBSIDIEERDE_DIENST; pg-verstrekking →
  lidmaatschap mag geen toegangsvoorwaarde zijn.
- Lid 5: `steunintensiteit_pct` ≤ 100. **Geen untranslatables.**

## Artikel 24 — afzetbevordering (eindpunt: voldoet_aan_voorwaarden_art_24)

- Lid 2 als OR van twee booleans (wedstrijden/beurzen/tentoonstellingen,
  publicaties). Lid 3 alleen op de publicatie-tak; de uitzondering van de
  tweede alinea als boolean-tussenstand → **untranslatable** ("exact
  overeenkomt met de beschermde benaming", "van ondergeschikt belang").
- Leden 4-5 kostencategorieën als boolean-tussenstand
  `kosten_binnen_in_aanmerking_komende_categorieen` → **untranslatable**
  (per-kostenpost-beoordeling + open norm "neutraal"/"gelijke kansen" lid 5a).
  De 3 000-EUR-grens voor symbolische prijzen (lid 4e) is WEL hard gemodelleerd
  (≤ 300000 eurocent), evenals het uitreikingsbewijs (lid 6, vierde alinea).
- Lid 6 vormen als OR(in natura, vergoeding werkelijke kosten, cash alleen bij
  symbolische prijzen); in natura ⇒ steunvorm GESUBSIDIEERDE_DIENST.
- Lid 7: toegankelijkheid + pg-uitvoering (geen lidmaatschapseis én bijdragen
  niet-leden beperkt). Lid 8: pct ≤ 100.

## Artikel 25 — weerschade (eindpunt: voldoet_aan_voorwaarden_art_25)

- Schadegebonden voorwaarden hard gemodelleerd: formele erkenning (lid 2a, met
  lid-3-noot dat erkenning via vooraf vastgestelde criteria "geacht" kan zijn),
  oorzakelijk verband (lid 2b), taxatie door bevoegde taxateur (lid 6),
  betaalroute + plafond bij pg (lid 4, patroon gelijk aan art 37),
  termijnen lid 5 via DATE_ADD (instelling ≤ +3 jr, betaling ≤ +4 jr),
  verzekeringskorting lid 10 als OR(verzekerd ≥50%, steun ≥50% verminderd),
  compensatieplafond lid 11 in gehele procentpunten:
  compensatie×100 ≤ kosten×(90 bij natuurlijke beperkingen, anders 80) — met
  rekentussenstap-output `totale_compensatie_maal_honderd`.
- **Untranslatable**: leden 7-9 (inkomensverlies-/materiële-schadeberekening:
  meerjarige gemiddelden, kmo-<3jr-referentieonderneming, indexen,
  reparatiekosten vs marktwaardedaling); uitkomsten komen binnen als
  `subsidiabele_kosten` en `steunbedrag_waarvoor_onderneming_in_aanmerking_komt`.
- Lid 3 is een lidstaat-optie (geen voorwaarde); alleen in de description.

## Artikel 26 — dier- en plantziekten (eindpunt: voldoet_aan_voorwaarden_art_26)

- Structuur: `soort_steun` (PREVENTIE / BESTRIJDING_OF_UITROEIING /
  HERSTEL_SCHADE) en `soort_gebeurtenis` (DIERZIEKTE / PLANTENPLAAG /
  INVASIEVE_UITHEEMSE_SOORT — die laatste per lid 8 alléén geldig bij
  PREVENTIE; getest).
- Hard gemodelleerd: lid 2 (voorschriften, programma/maatregel i-iv als
  boolean-tussenstand, beschrijvingseis), lid 3/4 lijst-/nieuwe-ziekte-toets
  (alleen dierziekte-tak; lijstlidmaatschap is een feit, dus parameter),
  lid 5 tenzij-constructie (verplichte heffingen), lid 6 betaalroute + plafond,
  lid 7 termijnen via DATE_ADD, lid 12 formele erkenning/bevestiging (alleen
  HERSTEL-tak), lid 13 hoofdregel in natura aan aanbieder OR afwijking,
  lid 14 NOT(opzet/nalatigheid).
- **Untranslatables (3)**: leden 10-11 vergoedingsberekening (marktwaarde net
  vóór het vermoeden, quarantaine-inkomensverlies, aftrekposten); leden 8-9
  kostenpost-kwalificatie (tussenstand); lid 13 tweede alinea
  afwijkings-kruistabel per kostenpost (tussenstand).

## Nieuwe gedeelde parameters (kandidaten voor het vocabulaire)

- `steun_rechtstreeks_aan_onderneming_betaald` /
  `steun_betaald_aan_producentengroepering_waarvan_onderneming_lid` /
  `steunbedrag_waarvoor_onderneming_in_aanmerking_komt` — zelfde patroon in
  art 25 lid 4, art 26 lid 6 én art 37 lid 3 (namen overgenomen van het al
  aanwezige `art_37.yaml` voor consistentie).
- `datum_instelling_steunregeling`, `datum_betaling_steun` — termijnenpatroon
  gedeeld met art 37 lid 4 (ankersdatum verschilt per artikel:
  `datum_weersomstandigheid` resp. `datum_ontstaan_kosten_of_schade`).
- `totale_compensatie_inclusief_verzekering` — art 25 lid 11, art 37 lid 10.
- `kosten_binnen_in_aanmerking_komende_categorieen` — generieke tussenstand
  (art 24 leden 4-5, art 26 leden 8-9); ook bruikbaar voor andere artikelen
  met limitatieve kostenlijsten.

## Open vragen / twijfels

- Art 23 lid 3 meet drie verschillende duren (per jaar / telkens / totaal) in
  één parameter `vervangingsduur_maanden`; de description draagt de meting.
  Bij verdieping wellicht splitsen.
- Art 24 lid 6, vierde alinea, regelt strikt genomen het *betaalmoment* van
  symbolische-prijzensteun (aan de aanbieder, na bewijs); als voorwaarde op de
  maatregel gemodelleerd. Verdedigbaar, maar een jurist kan dit als
  uitvoeringsvoorschrift buiten de verenigbaarheidstoets willen houden.
- Art 25 lid 10 "verzekerbare klimaatrisico's die statistisch het vaakst ...
  voorkomen" zit in de parameter-description (open norm binnen een feitelijke
  parameter), niet als aparte untranslatable.
- Engine-gedrag: optionele parameters mogen alleen ontbreken zolang de tak die
  ze leest niet wordt bereikt ("Variable not found" anders); de negatieve
  tests leveren ze daarom expliciet aan. Voor het verkennings-filter betekent
  dit: conditioneel-relevante parameters meegeven zodra hun poortconditie waar
  is.

## Testresultaat

35/35 PASS — per artikel minimaal één positieve en meerdere negatieve casussen
(zie `test_h3_diensten.py`): art 23 (7), art 24 (7), art 25 (9), art 26 (12).
