# Reverse-validatie LVV artikelen 27 t/m 40

Doelbestand: `/Users/rkievit/Projects/rr_lvvn_subsidies/regulation/eu/eu_verordening/landbouwvrijstellingsverordening/2023-12-13.yaml`
Methode: law-reverse-validate (hallucinatie-check); elke machine_readable-tak herleid naar een zinsnede van het eigen artikel; drempel-bindingen getoetst aan artikel 4; art-28-lid-2-binding vanuit art 27 getoetst; operaties getoetst aan v0.5.6 (geen when/then/else-op-IF-misbruik, geen verwijderde operaties; DATE_ADD met `date`+`years` is correct).

## Oordeel per artikel

| Art | Oordeel | Kern |
|---|---|---|
| 27 | ✅ gegrond | Alle leden gedekt; intensiteiten 70/75/100 kloppen met lid 5 (M1-punt b = 75 % vernietiging); terecht géén drempel (art 4 kent art 27 niet). Binding art-28-lid-2 klopt (zie onder). |
| 28 | ✅ gegrond, 1 juristvraag (M1-lid 3 punt d) | Lid 2 a-c exact als drie NOT-takken; lid 4 a/b exact; lid 6 cumulatief onder BIJDRAGE_ONDERLING_FONDS; lid 8 = 70. Geen drempel, correct. |
| 29 | ✅ gegrond | Leden 2-9 alle gedekt; lid 7-OR (maatregelen / redelijkerwijs niet mogelijk / eerste aanval) volgt de letter; lid 8 en 9 beide ≤ subsidiabele_kosten. |
| 30 | ✅ gegrond, 1 juristvraag (waarde ANDERS) | Lid 5-diersoortenlijst compleet (8 soorten); leden 4/6 als gemarkeerde parameters met untranslatable. |
| 31 | ✅ gegrond | Lid 13 dubbel getoetst: intensiteit ≤ 100 én hardcoded 50000 eurocent (500 EUR/GVE) naast de art-4-drempelbinding — de meest letterrouwe vorm in dit segment. Duur 1-7 met OR-verlenging spoort met lid 8. |
| 32 | ✅ gegrond | Alle 14 leden gedekt of expliciet untranslatable (leden 10/14 dispatch, lid 11 kosten); lid 8 correct beperkt tot lid 6 punten d/e; terecht geen drempel. |
| 33 | ✅ gegrond, observatie | Drempelbindingen exact conform golf 1 (`aanmeldingsdrempel_art_33` + `..._na_eerste_periode`); IF-op-`in_eerste_periode` spoort met art 4 punt e én lid 5. Maxima van lid 5 leunen op de art-4-bindingen (zie observatie O1). |
| 34 | ✅ gegrond, observaties | M1-schrapping van lid 8 correct niet gemodelleerd. Drie teelttype-bindingen exact conform golf 1 (geen kale output — klopt). 600/900/450 sporen met art 4 punt f. Zie O1/O2/O3. |
| 35 | ✅ gegrond, observaties | Zelfde patroon als 34; lid 9-uitsluitingen (art 34-verbintenissen, art 20-kosten) beide als NOT; drie bindingen exact. Zie O1/O2/O3. |
| 36 | 🔴 defect D1 | Maat-conflatie steunbedrag: lid-6-plafond (10 000 EUR **per jaar**) getoetst op dezelfde scalar als de art-4-drempel (**per onderneming per investeringsproject**). Fix: `art_36.yaml`. |
| 37 | 🟠 defect D2 | Taxatie-eis van lid 5 (identieke zinsnede als art 29 lid 5, daar wél voorwaarde) nergens als voorwaarde. Fix: `art_37.yaml`. Verder gegrond; lid-4-datumtoetsen (DATE_ADD +3/+4 jaar) kloppen; terecht geen drempel. |
| 38 | ✅ gegrond | Leden 2-6, 8-10 als voorwaarden, lid 7 untranslatable; drempel 7,5 mln (750000000) klopt met art 4 punt i. |
| 39 | ✅ gegrond, 1 aanname | Drempel 2 mln (200000000) klopt met art 4 punt j. Lid 3 (maxima Vo 2021/2115) als gemarkeerde tussenstand-parameter, geen untranslatables-blok — zie A1. |
| 40 | ✅ gegrond | Lid 2 dubbel getoetst: hardcoded 50000000 (500 000 EUR) én drempelbinding — zelfde waarde als art 4 punt k. |

## Speciale opdracht: art 27 ↔ art 28-lid-2-binding

Klopt aan beide kanten:
- **Producent**: art 28 geeft `voldoet_aan_voorwaarden_verzekeringspremiesteun_art_28_lid_2` uit (r. 6740/6756) als AND van precies de drie verboden van lid 2 punten a-c — niets meer (geen lid 3/4/8 erin gelekt), niets minder.
- **Consument**: art 27 bindt die output intern (zonder `regulation`, conform architectuur) en activeert hem alleen onder de IF op `steun_betreft_verzekeringspremies_afvoer_vernietiging` — precies lid 3, tweede alinea: "moet aan de voorwaarden van artikel 28, lid 2, voldoen".
- **M1-toets art 28 leden 3-4 tegen de text:**-redactie: lid 3 a-d en lid 4 a-b zijn woordelijk terug te vinden in descriptions/condities; lid 4 punt a positief geformuleerd, punt b als NOT — conform. Restpunt: J2 hieronder.

## Defecten (fix-fragment geleverd)

- **D1 — art 36, vals-positief op de drempel** (`art_36.yaml`). `steunbedrag` heet "per onderneming per investeringsproject; bij gekapitaliseerde werkzaamheden de steun per jaar". Wie bij GEKAPITALISEERDE_WERKZAAMHEDEN het jaarbedrag invult (bv. 9 000 EUR/jaar, project meerjarig > 600 000 EUR), passeert `steunbedrag ≤ aanmeldingsdrempel_art_36` ten onrechte: art 4 punt h meet per project, lid 6 per jaar. Gesplitst in twee parameters.
- **D2 — art 37, weggelaten voorwaarde lid 5** (`art_37.yaml`). "zoals getaxeerd door een openbare autoriteit, een door de steunverlenende autoriteit erkende onafhankelijke deskundige of een verzekeringsonderneming" stond alleen in proza (untranslatable-reason, parameterdescription), niet als toetsbare voorwaarde — terwijl art 29 lid 5 met dezelfde zinsnede wél `kosten_getaxeerd_door_bevoegde_taxateur` afdwingt. Parameter + AND-tak toegevoegd, untranslatable-reason bijgewerkt.

## Observaties (geen fix-fragment; merge-coördinator/volgende golf)

- **O1 — art 33/34/35: eigen maxima via art-4-binding.** De maxima uit lid 5/15/11 (500-200 resp. 600/900/450 EUR/ha/jr) worden uitsluitend via de gebonden art-4-drempels getoetst ("vallen numeriek samen", zegt de description). Vandaag identiek, maar het artikel-eigen plafond is dan niet meer zelfstandig herleidbaar tot het eigen lid; art 31 en 40 doen het wél dubbel (hardcoded + binding). Aanbeveling: ook in 33/34/35 de eigen literals naast de binding zetten.
- **O2 — inconsistente behandeling van gelijkluidende leden.** (a) 24-maandenvenster nieuwe nationale voorschriften: art 31 lid 6 = IF-voorwaarde, art 34 lid 5/art 35 lid 5 = alleen untranslatable. (b) Kennistoegang: art 34 lid 6/art 35 lid 7 = verplichte voorwaarde, art 31 lid 10 = alleen untranslatable. (c) Verbintenisduur: art 31 toetst 1-7 numeriek, art 34/35 toetsen niets — terwijl de letter in art 34 lid 7/art 35 lid 6 een harde ondergrens "ten minste één jaar" voor elke verkorting kent. Eén lijn kiezen.
- **O3 — legal_basis.law inconsistent in het hele bestand**: 78× `Verordening (EU) 2022/2472` (o.a. art 32-40) vs 12× `landbouwvrijstellingsverordening` (o.a. art 27-31; `$id` van het bestand). Normaliseren bij de merge.
- **O4 — NOT/EQUALS over optionele (required: false) parameters** (art 27, 28, 30 e.a.): gedrag bij ontbrekende waarde is engine-afhankelijk; patroon is segmentbreed consistent, maar verdient één expliciete afspraak (default false?).

## Aannames (gemeld, geen defect)

- **A1 — art 39 lid 3**: extern maximum (Vo 2021/2115 per verrichtingstype) als boolean-tussenstand `steunintensiteit_binnen_maxima_verordening_2021_2115`; strikt genomen een tabel-opzoeking → kandidaat-untranslatable (art 39 heeft er nu geen).
- **A2 — art 38 lid 3/lid 4**: meerdelige bekendmakings- en beschikbaarheidseisen samengevouwen tot één boolean per lid (a-e resp. beide tijdstippen + 5 jaar); volledig in de description verantwoord.
- **A3 — art 29 lid 6** (berekening op niveau individuele begunstigde, aftrek niet-gemaakte kosten) zit in de untranslatable, niet als voorwaarde — consistent met de breedte-eerst-opdracht.

## Jurist-vragenlijst

- **J1 (art 27, lid 3 al. 2)**: de premiesteun-poort hangt aan een vrije boolean, niet aan `kostencategorie_art_27 = AFVOEREN_EN_VERNIETIGEN_HEFFINGSGEFINANCIERD`. De letter zegt "als bedoeld in lid 2, punt e)". Moet de art-28-lid-2-toets uitsluitend bij punt-e-steun gelden, of bij elke premiecomponent?
- **J2 (art 28, lid 3, M1)**: punt d opent met "**en** biedt compensatie voor verzekeringspremies …". Is d een víérde alternatieve dekkingsgrond (zoals gemodelleerd: één boolean, "en/of" in de description) of een cumulatieve eis bovenop a-c? De redactie in de geconsolideerde tekst is grammaticaal dubbelzinnig.
- **J3 (art 30, lid 3)**: mag steun voor lid-7-verrichtingen zónder lid-3-verbintenis (modelwaarde `ANDERS`, passeert leden 4-6)? Of is lid 3 limitatief voor waar de verbintenissen op mogen zien?
- **J4 (art 31, lid 13)**: lid 13 zegt "500 EUR per grootvee-eenheid" (zonder "per jaar"); art 4 punt d zegt "per grootvee-eenheid per jaar". Het model meet beide per jaar. Zelfde maat bedoeld?
- **J5 (art 37, lid 1)**: grondslag is art 107, **lid 2, punt b** VWEU (niet 107 lid 3 punt c zoals de rest van het hoofdstuk). Geen modelgevolg, maar relevant voor de duiding van het eindpunt ("verenigbaar van rechtswege").
- **J6 (art 34/35, duur)**: is de ondergrens "ten minste één jaar" hard genoeg om als numerieke voorwaarde te modelleren naast de untranslatable (zie O2c)?

## Drempel-controle tegen artikel 4 (segment)

27 ✗ (geen — klopt), 28 ✗ (klopt), 29 ✗ (klopt), 30 ✗ (klopt), 31 punt d 50000 ✓, 32 ✗ (klopt; leden 10/14 via untranslatable), 33 punt e 50000/20000 ✓✓, 34 punt f 60000/90000/45000 ✓✓✓, 35 punt g idem ✓✓✓, 36 punt h 60000000 ✓, 37 ✗ (klopt), 38 punt i 750000000 ✓, 39 punt j 200000000 ✓, 40 punt k 50000000 ✓. Alle bindingsnamen exact conform de golf-1-outputs (34/35 zonder kale output — correct nageleefd).
