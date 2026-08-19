# Notes batch h3-aanloop — artikelen 18, 19, 20, 21, 22 (LVV)

Alle vijf fragmenten: schema-valide tegen v0.5.6 (jsonschema, volledige
mini-wet) en getest via het evaluate-binary: **35/35 tests geslaagd**
(`test_h3_aanloop.py` in deze map; herdraaibaar). In de mini-testwetten stond
tijdelijk `accepted: true`; de fragmenten houden `accepted: false`. De binding
`voldoet_aan_gemeenschappelijke_voorwaarden` (art 3) is in de mini-wetten
gestubd als parameter; in de fragmenten staat de echte interne binding.

**Geen drempel-bindingen in deze batch**: artikel 4, lid 1 kent voor geen van
de artikelen 18–22 een aanmeldingsdrempel (letters a–v noemen 14, 16, 17, 31,
33–36, 38–42, 44–46, 48–50, 55, 60, 61). Let op: de drempel "adviesdiensten"
in art 4, lid 1, punt q hoort bij art 48 (bosbouw), níét bij art 22.

## Artikel 18 — aanloopsteun jonge landbouwers (eindpunt: voldoet_aan_voorwaarden_art_18)

- AND over lid 1 (poort art 3), lid 2 (OR oprichting plattelandsbedrijf /
  diversificatie), lid 3 (jonge landbouwer + kleine/micro-onderneming), lid 4
  (alleen bij rechtspersoon: zeggenschap), lid 5 (bedrijfsplan), lid 6 (OR
  vakbekwaam / 36-maanden-verbintenis in bedrijfsplan), lid 7 (≤ 100 000 EUR =
  10000000).
- **Bewust géén `is_kmo`-binding**: lid 3 eist kleine óf micro-onderneming,
  strenger dan de kmo-koepel; Bijlage I levert alleen `is_kmo`. Parameter
  `is_kleine_of_micro_onderneming` als gemarkeerde tussenstand (Bijlage I,
  art 2, leden 2–3); verdiepingskandidaat: aparte Bijlage-I-outputs
  `is_kleine_onderneming` / `is_micro_onderneming`.
- `is_jonge_landbouwer` als tussenstand (art 2, punt 61: invulling door
  lidstaat in GLB-plan — inherent extern).
- Untranslatable: zeggenschapsdoorwerking lid 4 (meerdere personen, getrapte
  rechtspersonen, begrip via concentratie-mededeling).

## Artikel 19 — aanloopsteun producentengroeperingen (eindpunt: voldoet_aan_voorwaarden_art_19)

- AND over lid 1, lid 2 (officiële erkenning), lid 4 a/b/c (drie NOT-
  uitsluitingen), lid 5 (kostensoorten-boolean), lid 6 (forfaitair, jaarlijkse
  tranches, eerste vijf jaar na erkenning), lid 7 (steunbedrag ≤ productie/10),
  lid 8 (≤ 100 000 EUR/jaar én degressief).
- Untranslatables: lid 3 (aanpassingsplicht GMO-wijzigingen, open/toekomstig),
  lid 5 slotalinea (pandkosten → huurkosten markttarief, berekening), lid 6
  tweede alinea (laatste tranche na verificatie, procedureel), lid 8
  (degressiviteitsprofiel; het féit is een boolean-parameter).

## Artikel 20 — kwaliteitsregelingen (eindpunt: voldoet_aan_voorwaarden_art_20)

- Lid 1 wijst per categorie de leden aan; gemodelleerd met parameter
  `steuncategorie` (TOETREDING_KWALITEITSREGELING /
  VERPLICHTE_CONTROLEMAATREGELEN / MARKTONDERZOEK_PRODUCTONTWERP_ERKENNINGSAANVRAAG)
  en een IF: a → leden 3, 4, 5 (≤ 7 jaar); b → leden 4, 7, 8 (≤ 100%);
  c → leden 7, 8. Leden 2 (OR over drie regelingscategorieën) en 6
  (objectieve toegankelijkheid) staan buiten de IF (gelden voor alle drie).
  Onbekende categorie ⇒ default false.
- Untranslatables: lid 2b i–iv (erkenningsvoorwaarden, open normen — de
  lidstaat-erkenning is de boolean), lid 3 (niveaubepaling stimulans op basis
  van vaste kosten, berekening).

## Artikel 21 — kennisuitwisseling en voorlichting (eindpunt: voldoet_aan_voorwaarden_art_21)

- AND over lid 1, lid 2 (actiesoort + AKIS-consistentie), lid 3
  (kostensoorten-boolean), lid 5 (niet rechtstreeks aan begunstigden), lid 6
  (gekwalificeerd personeel), lid 7 (toegankelijkheid; bij
  producentengroepering bovendien lidmaatschap-geen-voorwaarde + bijdragen-
  beperking), lid 8 (intensiteit ≤ 100%; alleen bij demonstratieproject
  bovendien steunbedrag ≤ 100 000 EUR per drie belastingjaren).
- `steunbedrag` hier required: false (alleen relevant voor de demo-cap).
- Untranslatables: grond ≤ 10% binnen lid 3 d i (berekening), lid 4
  (duurkoppeling + afschrijving volgens boekhoudkundige beginselen).

## Artikel 22 — adviesdiensten (eindpunt: voldoet_aan_voorwaarden_art_22)

- AND over lid 1, lid 2 (begunstigdenkring: OR primair/verwerking/afzet/jonge
  landbouwer + AKIS), lid 3 (twee booleans: doelstellingenkoppeling GLB én
  ≥ 1 element a–i), lid 5 (`steunvorm` EQUALS GESUBSIDIEERDE_DIENST — golf-1-
  vocabulairewaarde), lid 6 (kwalificatie/ervaring/betrouwbaar +
  onpartijdig/geen belangenconflict), lid 7 (als art 21), leden 8/9
  (intensiteit ≤ 100%; primair → ≤ 25 000 EUR/3 jaar = 2500000;
  verwerking/afzet → ≤ 200 000 EUR/3 jaar = 20000000).
- **Open vraag (leden 8/9)**: lid 9 zegt "actief ... in de verwerking **en** de
  afzet"; gemodelleerd als verwerking en/of afzet (anders ontsnapt een
  begunstigde die alleen verwerkt aan beide plafonds). Menselijke review
  gevraagd. Wie primair én verwerking/afzet doet, krijgt beide plafonds
  (strengste wint vanzelf).
- Lid 4 (advies mag óók andere economische/ecologische kwesties dekken) is
  een verruiming van de toegestane inhoud, geen voorwaarde; alleen de
  kosten-uitzondering op de maxima ("behalve voor kosten op grond van lid 4")
  is als untranslatable vastgelegd; `steunbedrag` is gedefinieerd als
  exclusief lid-4-kosten.
- Untranslatables: inhoudelijke toets adviesonderwerp aan externe regelgeving
  (lid 3), lid-4-kosten-uitzondering op de maxima.

## Nieuwe gedeelde parameters (kandidaten voor het vocabulaire)

- `is_jonge_landbouwer` (boolean; art 2 punt 61; gebruikt in art 18 én 22 —
  zelfde begrip, zelfde naam).
- `toegankelijk_onder_objectieve_voorwaarden` (boolean; identieke zinsnede in
  art 20 lid 6, art 21 lid 7, art 22 lid 7 — komt vermoedelijk in meer
  hoofdstuk-III-artikelen terug).
- `consistent_met_akis_beschrijving_glb_plan` (boolean; art 21 lid 2 en art 22
  lid 2).
- `lidmaatschap_geen_toegangsvoorwaarde` (boolean; art 21/22, lid 7).
- `kosten_beperkt_tot_in_aanmerking_komende_kostensoorten` (boolean-patroon
  voor limitatieve kostenlijsten; art 19 lid 5, art 21 lid 3).
- `steuncategorie` (string; artikel-lokaal in art 20, maar het patroon
  "lid 1 somt categorieën met elk hun leden op" komt vaker voor).

## Testresultaat

35/35 PASS (per artikel minstens één positieve en meerdere negatieve casussen
op artikel-specifieke voorwaarden; poort-dicht-casus bij art 18). Randgevallen
getest: bedragen precies óp de maxima (slagen), één eurocent erboven (falen);
art 19 lid 7 exact 10%-grens via productie 1 mln bij steun 90k.

## Open vragen voor menselijke review

1. Art 22 leden 8/9: "verwerking **en** afzet" — en/of-lezing (zie boven).
2. Art 18: aparte kleine/micro-outputs in Bijlage I bouwen en art 18 daaraan
   binden (vervangt de tussenstand-parameter).
3. Art 20 lid 2: de drie regelingscategorieën zijn als OR gemodelleerd op
   feit-booleans; de i–iv-voorwaarden van 2b zitten in de lidstaat-erkenning.
4. Art 19 lid 6 tweede alinea en lid 3 zijn niet als voorwaarde op de
   voorgenomen maatregel toetsbaar (procedureel/toekomstig) — vastgelegd als
   untranslatables, geen onderdeel van het eindpunt.
