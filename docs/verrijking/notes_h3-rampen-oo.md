# Notes batch h3-rampen-oo (art 37, 38, 39, 40)

## Per artikel

### Art 37 — natuurrampen landbouwsector
- Eindpunt: `voldoet_aan_voorwaarden_art_37`.
- **Geen drempel-binding**: artikel 4 kent voor artikel 37 geen aanmeldingsdrempel
  (art-107(2)(b)-steun staat niet in de lijst van art 4 lid 1). Genoteerd in de
  input-description.
- Gemodelleerd: hoofdstuk-I-poort (lid 1), formele erkenning (lid 2a), causaal
  verband (lid 2b), betaaladres rechtstreeks-of-groepering (lid 3 eerste alinea),
  cap bij betaling via groepering (lid 3 tweede alinea, als IF), termijnen
  instelling ≤ ramp+3j en betaling ≤ ramp+4j (lid 4, datumvergelijking met
  DATE_ADD), compensatie incl. verzekering ≤ 100% van in aanmerking komende
  kosten (lid 10).
- Untranslatable: schade-/inkomensverliesberekening leden 5–9 (taxatie,
  meerjarige gemiddelden excl. hoogste/laagste, indexen, economische waarde);
  lid 6 (niveau individuele begunstigde) en lid 7 (componenten) horen bij die
  berekening. `accepted: false` in fragment.
- `subsidiabele_kosten` (gedeeld vocabulaire) = de getaxeerde schadekosten van
  lid 5; `steunbedrag_waarvoor_onderneming_in_aanmerking_komt` (amount,
  required: false) is gemarkeerde tussenstand op de berekening.

### Art 38 — onderzoek en ontwikkeling
- Eindpunt: `voldoet_aan_voorwaarden_art_38`. Drempel-binding
  `aanmeldingsdrempel_art_38` (7,5 mln per project); `steunbedrag` hier per
  project gemeten (conform art 4 lid 1 punt i).
- Gemodelleerd: hoofdstuk-I-poort, drempel, algemeen belang sector (lid 2),
  voorafgaande bekendmaking a–e als één boolean (lid 3), resultaten openbaar +
  ≥5 jaar als één boolean (lid 4), rechtstreeks aan onderzoeksorganisatie
  (lid 5), NOT prijsgebaseerde betalingen (lid 6), gescheiden boekhouding als
  IF op economische activiteiten (lid 8), NOT preferente toegang (lid 9),
  intensiteit ≤ 100 (lid 10).
- Untranslatable: kostenafbakening lid 7 (afschrijving naar looptijd, arm's
  length, overheadtoerekening). `accepted: false` in fragment.

### Art 39 — deelname EIP-operationele-groep-projecten
- Eindpunt: `voldoet_aan_voorwaarden_art_39`. Drempel-binding
  `aanmeldingsdrempel_art_39` (2 mln per onderneming per project).
- Gemodelleerd: hoofdstuk-I-poort, drempel, deelname aan onder art 127
  Vo 2021/2115 vallend EIP-project (lid 1), kosten binnen categorieën a–e
  (lid 2), intensiteit binnen maxima Vo 2021/2115 (lid 3).
- Lid 3 is een boolean-parameter als **gemarkeerde tussenstand** (geen
  untranslatable): de maxima staan per type verrichting in Verordening (EU)
  2021/2115, die niet in het corpus zit; description zegt dat. Open vraag:
  verdiepen zodra Vo 2021/2115 geharvest is (dan cross-law binding).
- Geen untranslatables.

### Art 40 — beperkte steunbedragen EIP
- Eindpunt: `voldoet_aan_voorwaarden_art_40`. Drempel-binding
  `aanmeldingsdrempel_art_40` (500 000 EUR per project).
- Gemodelleerd: hoofdstuk-I-poort, deelname/profijt EIP-project als bedoeld in
  art 39 lid 1 (lid 1), totaal per project ≤ 50000000 eurocent (lid 2, eigen
  letter), plus drempeltoets tegen de binding. Lid-2-toets en drempeltoets
  vallen materieel samen (art 4 lid 1 punt k herhaalt het bedrag); beide staan
  er, elk herleidbaar tot de eigen zinsnede.
- Geen untranslatables.

## Nieuwe (potentieel gedeelde) parameters
- `natuurramp_formeel_erkend`, `rechtstreeks_oorzakelijk_verband_natuurramp_schade`,
  `datum_natuurramp`, `datum_instelling_steunregeling`, `datum_betaling_steun`,
  `totale_compensatie_inclusief_verzekering` — herbruikbaar voor art 26 e.a.
  rampachtige artikelen (ziekten/plagen/ongunstig weer) mutatis mutandis; daar
  gelden eigen begrippen, dus alleen hergebruiken bij zelfde begrip.
- `steun_rechtstreeks_aan_onderneming_betaald`,
  `steun_betaald_aan_producentengroepering_waarvan_onderneming_lid`,
  `steunbedrag_waarvoor_onderneming_in_aanmerking_komt` (lid-3-patroon komt in
  meer artikelen voor).
- `neemt_deel_aan_eip_project_operationele_groep` (art 39),
  `neemt_deel_aan_of_profiteert_van_eip_project` (art 40; bewust apart begrip:
  "deelnemen aan of profiteren van"),
  `totaal_steunbedrag_per_eip_project` (art 40; per project, niet per
  onderneming — daarom niet `steunbedrag`).
- Art 61 (CLLD) heeft dezelfde structuur als art 40; naamgevingspatroon
  `totaal_steunbedrag_per_<project>_project` aanbevolen.

## Testresultaat
- `test_h3_rampen_oo.py` (mini-testwet per artikel; bindingen gestubd als
  parameters, untranslatables tijdelijk `accepted: true`):
  **20/20 casussen geslaagd** — per artikel minimaal één positieve en meerdere
  negatieve casussen (erkenning, termijn, cap-via-groepering, compensatie>100%,
  intensiteit, drempels, boekhouding-IF, deelname).
- Engine ondersteunt datumvergelijking (LESS_THAN_OR_EQUAL op twee datums) —
  lid-4-termijnen van art 37 draaien native.

## Open vragen
- Art 37 lid 4: "binnen vier jaar na die datum" gelezen als vier jaar na de
  datum van de natuurramp (niet na de instelling van de regeling); dat is de
  meest nabije antecedent ("die datum" = de datum waarop de ramp zich heeft
  voorgedaan). Jurist-check gewenst.
- Art 38 lid 3/4: elk als één boolean gemodelleerd (breedte-eerst); opsplitsen
  per punt kan bij verdieping.
- Art 39 lid 3: cross-law binding naar Vo 2021/2115 zodra die in het corpus zit.
