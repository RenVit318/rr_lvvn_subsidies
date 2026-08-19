# Reverse-validatie LVV artikelen 14 t/m 26

Methode: elke input/parameter/conditie/waarde herleid naar een zinsnede in de
`text:` van het eigen artikel; drempel-bindingen getoetst aan artikel 4, lid 1;
architectuur-bindingen (art 3-poort, art 4-drempels, Bijlage I `is_kmo`) en de
in artikel 1 gedocumenteerde delegatie ("De beperking wordt gehandhaafd door de
voorwaarden van die artikelen zelf" — untranslatable bij art 1 over de
kmo/primaire-productie-beperking voor de artikelen 14, 15, 16, 18, 23 en
25 t/m 31) als gegeven referentiekader genomen.

## Oordeel per artikel

| Art | Oordeel | Kern |
|-----|---------|------|
| 14 | schoon | drempel art 4(1)(a) 600k = 60000000 ✓; leden 3, 4, 5, 8–15 herleidbaar; irrigatie-plafond lid 15 als cap vóór de verhogingen (tekst: "blijft beperkt tot") |
| 15 | schoon | geen art-4-drempel ✓; 100%-plafond ✓; kmo/primaire productie conform art-1-delegatie aanwezig |
| 16 | schoon | drempel art 4(1)(b) alleen bij modernisering/capaciteitsverhoging (lid 4) — correct conditioneel gemodelleerd; art-14-intensiteiten voor het moderniseringsdeel netjes als untranslatable |
| 17 | schoon | drempel art 4(1)(c) 7,5M = 750000000 ✓; lid 9 (normen-investeringen), lid 12 (80%) ✓ |
| 18 | **gefixt** | art-1-beperking (primaire productie) ontbrak |
| 19 | schoon | lid 7 (10% = DIVIDE/10) ✓; lid 8 100k = 10000000 ✓; uitsluitingen lid 4 ✓ |
| 20 | schoon | leden-per-categorie (a: 2–6; b: 2,4,6,7,8; c: 2,6,7,8) exact conform lid 1; ≤7 jaar ✓ |
| 21 | schoon | 100k over drie belastingjaren alleen bij demonstratieprojecten ✓ = 10000000 ✓ |
| 22 | schoon + vraag | 25k = 2500000 ✓, 200k = 20000000 ✓; leesvraag lid 9 (zie vragenlijst) |
| 23 | **gefixt** | art-1-beperking (kmo + primaire productie) ontbrak |
| 24 | **gefixt** | uitzonderings-lek lid 3 (merknaam + toegestane oorsprongsverwijzing passeerde); 3 000 EUR = 300000 ✓ |
| 25 | **gefixt** | art-1-beperking ontbrak; lid 5 (3/4 jaar), lid 10 (50%-korting), lid 11 (80/90%-cumulatie) ✓ |
| 26 | **gefixt** | art-1-beperking ontbrak én lid 15 (100%-cumulatieplafond) in het geheel niet gemodelleerd |

## Defecten (met zinsnede)

1. **Art 18 — weggelaten voorwaarde (art-1-delegatie).** Artikel 1, lid 1,
   punt a, i: "met uitzondering van de artikelen 14, 15, 16, 18, 23 en 25 tot
   en met 31, die alleen van toepassing zijn op kmo's die in de primaire
   landbouwproductie actief zijn." De untranslatable bij artikel 1 legt de
   handhaving expliciet bij de inroepende artikelen; 14/15/16 doen dat, 18
   niet. Fix: parameter + conditie `actief_in_primaire_landbouwproductie`
   (de kmo-eis is al gedekt door de strengere eis van lid 3: kleine of
   micro-onderneming). → `art_18.yaml`
2. **Art 23 — idem.** Zelfde zinsnede; fix: `is_kmo`-binding (Bijlage I) +
   `actief_in_primaire_landbouwproductie` + twee condities, naar het patroon
   van artikel 15. → `art_23.yaml`
3. **Art 24 — uitzondering te breed.** Lid 3: "mag niet worden verwezen naar
   een specifieke onderneming, merknaam of oorsprong"; de tweede alinea
   ontheft **alleen oorsprongsverwijzingen**. Het model liet een publicatie
   met merknaam-verwijzing passeren zodra er óók een toegestane
   oorsprongsverwijzing was (`verwijst=true` OR `uitzondering=true`). Fix:
   parameterbetekenis aangescherpt — de uitzonderingsparameter is alleen waar
   als álle verwijzingen uitsluitend toegestane oorsprongsverwijzingen zijn;
   een onderneming-/merknaamverwijzing maakt hem onwaar. → `art_24.yaml`
4. **Art 25 — weggelaten voorwaarde (art-1-delegatie).** Als 2 (art 25 valt
   onder "25 tot en met 31"; lid 8 spreekt zelf ook van "een kmo").
   → `art_25.yaml`
5. **Art 26 — twee defecten.** (a) art-1-delegatie als 2. (b) **Lid 15
   volledig ontbrekend**: "De steun en eventuele andere door de begunstigde
   ontvangen betalingen ... mogen niet meer bedragen dan 100 % van de in
   aanmerking komende kosten." Geen parameter, conditie of untranslatable
   dekte dit (art 25 modelleert zijn parallelle lid 11 wél). Fix: nieuwe
   parameters `totale_betalingen_voor_dezelfde_kosten` en
   `subsidiabele_kosten` (gedeeld vocabulaire) + conditie
   `totale_betalingen ≤ subsidiabele_kosten` (100% = de kosten zelf).
   → `art_26.yaml`

Nieuwe gedeelde parameter geïntroduceerd: `totale_betalingen_voor_dezelfde_kosten`
(amount, eurocent) — cumulatie-parameter, kandidaat voor hergebruik naast art 25's
`totale_compensatie_inclusief_verzekering` (harmonisatie overwegen).

## Gecontroleerd en in orde (steekproef-verantwoording)

- **Drempel-bindingen**: alleen 14, 16 (conditioneel op lid 4) en 17 binden een
  art-4-drempel; art 4 kent er voor 15, 18–26 geen — alle overige artikelen
  binden er terecht geen.
- **Eurocent-conversies**: 600 000→60000000, 7,5M→750000000, 100 000→10000000,
  25 000→2500000, 200 000→20000000, 3 000→300000 — alle correct.
- **Operatoren**: alle "ten hoogste"/"niet groter dan"/"beperkt tot" als
  LESS_THAN_OR_EQUAL ✓; uitsluitingen als NOT ✓; "ten minste een van" als OR ✓.
- **Verzonnen voorwaarden/bedragen**: geen aangetroffen.

## Jurist-vragenlijst

1. **Art 18, lid 2** — "de oprichting van plattelandsbedrijven ... **en** de
   diversificatie ...": gemodelleerd als OR (één maatregel dekt één grond).
   Is de opsommende lezing (twee steundoelen, elk afzonderlijk toelaatbaar)
   juridisch juist, of moet een regeling beide gronden dekken?
2. **Art 22, lid 9** — "een enkele begunstigde die actief is in de verwerking
   **en** de afzet": gemodelleerd als en/of (cumulatief gelezen zou een
   begunstigde die alléén verwerkt onder geen van beide plafonds vallen).
   Bevestigen dat en/of de bedoelde lezing is.
3. **Art 14, lid 15** — het irrigatie-plafond is gemodelleerd als voorrang
   hebbend boven de verhogingen van de leden 12–14 ("blijft beperkt tot").
   Bevestigen dat bijv. een niet-productieve irrigatie-investering op het
   bedrijf (lid 14, punt a) inderdaad op 65/80% blijft steken en niet 100%
   krijgt.
4. **Art 14/17, lid 12, punt a** — "investeringen die **verband houden met**"
   de doelstellingen is gemodelleerd met dezelfde parameters als lid 3
   ("**gericht op**"). Is dat verschil in formulering betekenisvol?
5. **Art 18, lid 6** — de vakbekwaamheidseis (art 4, lid 6, punt c, Vo
   2021/2115) is als zelfstandige eis gemodelleerd (OR met de
   36-maanden-verbintenis). Strikt gelezen regelt lid 6 alleen de ontheffing;
   of de eis zelf voor élke art-18-begunstigde geldt volgt uit de
   jonge-landbouwer-definitie van de lidstaat. Bevestigen.
6. **Art 25, lid 10** — het model accepteert ofwel de verzekering ofwel een
   met ≥50% verminderde steun; de tekst formuleert de vermindering als
   verplichting, niet als keuze van de aanvrager. De boolean
   `steun_met_minstens_50_pct_verminderd` legt de facto vast dat de korting is
   toegepast — akkoord met deze operationalisering?
7. **Art 16, leden 3/5** — het model toetst alleen het in alle gevallen
   geldende 100%-plafond; lid 3 plafonneert specifiek op "de reële kosten van
   die werkzaamheden" (demonteren/verhuizen/opbouwen). De kostenbasis-splitsing
   staat als untranslatable — bevestigen dat dat als breedte-eerst-benadering
   volstaat.
