# Golden-route-testscenario's — verrijkte LVV (Vo. (EU) 2022/2472, geconsolideerd 13-12-2023)

Alle runs tegen de ECHTE gemergde wet (`2023-12-13.yaml`), alle bindingen live
(art 3 → art 1/5/6/8/9, Bijlage I `is_kmo`, art 4 drempel), via
`packages/target/release/evaluate` (engine 0.3.0, schema v0.5.6,
regulation_hash `sha256:0007d899…`). Uitvoering op een KOPIE met alle
`accepted: false` → `true` (`lvv_accepted.yaml`, RFC-012 fail-fast); het
origineel is niet aangeraakt. De payload-bestanden `golden_route_N.json`
hiernaast bevatten de `params`; wrapper:
`{"law_yaml": <lvv_accepted.yaml>, "output_name": <eindpunt>, "params": <bestand>, "date": "2024-06-01", "extra_laws": []}`.

---

## Casus 1 — Ruilverkavelings-route (art 15) → **true**

**Casus**: een maatschap (kmo, primaire landbouwproductie) vraagt vóór aanvang
schriftelijk steun aan voor uitsluitend de juridische/administratieve kosten
(incl. opmeting) van een ruilverkaveling; subsidie, 100 % van de werkelijke
kosten, via een objectieve regeling die vóór het maken van de kosten in werking
was.

**Eindpunt**: `voldoet_aan_voorwaarden_art_15` → `true`
**Payload**: `golden_route_1.json` (59 parameters)

Kern-parameters en het lid dat de waarde afdwingt:

| parameter | waarde | dwingende bepaling |
|---|---|---|
| `betreft_ruilverkaveling_van_landbouwgrond` | true | art 15, aanhef: "Steun voor ruilverkaveling van landbouwgrond" |
| `steun_uitsluitend_voor_juridische_en_administratieve_kosten` | true | art 15: "uitsluitend … juridische en administratieve kosten, inclusief opmetingskosten" |
| `steunintensiteit_pct` | 100 | art 15: "ten belope van maximaal 100 %" (LESS_THAN_OR_EQUAL; exact 100 → true, 101 → false, geverifieerd) |
| `actief_in_primaire_landbouwproductie` | true | art 1 lid 1 punt a i: art 15 geldt **alleen** voor kmo's in de primaire landbouwproductie (handhaving ligt bij art 15 zelf; zie untranslatable op art 1) |
| `aantal_werknemers` / `jaaromzet` / `balanstotaal` | 12 / 2,5 M€ / 1,8 M€ | Bijlage I art 2 lid 1 (< 250 AJE én omzet ≤ 50 M€ **of** balans ≤ 43 M€) → `is_kmo` (binding) |
| `steunvorm` | SUBSIDIE | art 5 lid 3 punt a → `is_transparante_steun` |
| `aanvraag_voor_aanvang_werkzaamheden` + `aanvraag_is_schriftelijk` + 5 inhouds-booleans | true | art 6 lid 2, punten a-e (stimulerend effect, lid-2-route) |
| `steun_artikel`='15', `voldoet_aan_voorwaarden_steunartikel`, `recht_op_steun_volgens_objectieve_criteria…`, `regeling_goedgekeurd_en_in_werking_voor_kosten_gemaakt` | true | art 6 lid 5 punt a i-ii: ruilverkavelingsregelingen hoeven géén stimulerend effect (afwijking van lid 2-4) — deze casus draagt beide routes |
| alle `betreft_*`-categorieën, lid-3/6/7-uitsluitingen | false | art 1 lid 1 (route a-i volstaat), lid 3 (geen exportsteun e.d.), lid 6, lid 7 |
| `heeft_openstaand_terugvorderingsbevel` | false | art 1 lid 4 (Deggendorf) |
| `is_onderneming_in_moeilijkheden` | false | art 1 lid 5 |
| `cumuleert_met_andere_steun` / `cumulatie_overschrijdt_hoogste_maximum` | false / false | art 8 lid 3 punt b (cumulering mag, mits maximum niet overschreden — tweetrap geverifieerd: cumuleert=true+overschrijdt=false blijft true) |
| `wordt_gepubliceerd_conform_art_9` | true | art 9 lid 1 |

Art 4 kent voor art 15 géén aanmeldingsdrempel — er is dan ook geen
drempel-binding, conform de lijst van art 4 lid 1.

**Keten-mutaties, allemaal correct** (basis true, één knop om → uitkomst):
`steunvorm=KAPITAALINJECTIE` → false (art 5 lid 4); `steunvorm=ANDERS` → false
(lid 3 limitatief); `aantal_werknemers=250` → false (Bijlage I); `jaaromzet=60 M€`
→ **true** (correct: balans-alternatief, Bijlage I art 2 lid 1 "of");
`wordt_gepubliceerd_conform_art_9=false` → false; `heeft_openstaand_terugvorderingsbevel=true`
→ false; `betreft_steun_voor_exportactiviteiten=true` → false (art 1 lid 3 punt c);
`aanvraag_voor_aanvang_werkzaamheden=false` → **true** (correct: art 6 lid 5
punt a is een echte afwijking van lid 2; valt óók lid 5 weg — probe F — dan false).

---

## Casus 2 — Zelfde casus, één knop om → **false**

**Payload**: `golden_route_2.json` = casus 1 met uitsluitend
`is_onderneming_in_moeilijkheden: true`.

**Eindpunt**: `voldoet_aan_voorwaarden_art_15` → `false` (geverifieerd).

Juridische betekenis van de omslag: art 1 lid 5 — de verordening is niet van
toepassing op steun aan ondernemingen in moeilijkheden (begrip art 2 punt 59 →
art 2 punt 18 Vo. 651/2014), en geen van de uitzonderingen a-h van lid 5 doet
zich voor (ruilverkaveling staat er niet tussen). De keten:
`voldoet_aan_lid_5`=false → `valt_binnen_toepassingsgebied`=false (art 1) →
`voldoet_aan_gemeenschappelijke_voorwaarden`=false (art 3) → eindpunt false.
Dit is de duidelijkste eenknops-omslag omdat hij het *toepassingsgebied* raakt
in plaats van een artikel-voorwaarde: dezelfde knop laat elk
hoofdstuk-III-eindpunt omvallen (voor art 14 apart geverifieerd: ook false).

---

## Casus 3 — Stalverduurzaming (art 14, doel dierenwelzijn) → **true**

**Casus**: een veehouderij-kmo (12 AJE) wil 400 000 EUR subsidie (80 % van de
subsidiabele kosten) voor stalinvesteringen die verder gaan dan de EU-normen
voor dierenwelzijn; regeling open voor de hele sector dierlijke productie; MEB
uitgevoerd en vergunning verleend vóór toekenning; schriftelijke aanvraag vooraf.

**Eindpunt**: `voldoet_aan_voorwaarden_art_14` → `true`, met
`maximale_steunintensiteit_pct_art_14` = **80**.
**Payload**: `golden_route_3.json` (105 parameters)

Kern-parameters:

| parameter | waarde | dwingende bepaling |
|---|---|---|
| `betreft_investering_primaire_landbouwproductie_op_landbouwbedrijf` | true | art 14 lid 1 |
| `doel_verbetering_milieu_hygiene_of_dierenwelzijnsnormen` | true | art 14 lid 3 punt b ("verbeteren van … de normen inzake dierenwelzijn"); de overige zes doelen false — lid 3 eist "ten minste een" |
| `investering_houdt_verband_met_dierenwelzijn` | true | art 14 lid 12 punt a → maximum 80 % i.p.v. 65 % (lid 11); zonder deze knop is 80 % > 65 % → false (geverifieerd) |
| `steunintensiteit_pct` | 80 | ≤ maximum van leden 11-15; 81 → false (geverifieerd) |
| `steunbedrag` | 40 000 000 ct (400 k€) | art 4 lid 1 punt a via binding `aanmeldingsdrempel_art_14` (600 k€); 600 000,01 € → false, exact 600 k€ → true (geverifieerd) |
| `milieueffectbeoordeling_vereist/uitgevoerd`, `vergunning_verleend_voor_datum_toekenning` | true | art 14 lid 5 (stallen zijn vaak MEB-plichtig); guard klopt: niet-vereist zonder beoordeling → true (probe C) |
| `steun_beschikbaar_voor_hele_sector_dierlijke_productie` | true | art 14 lid 10: steun niet beperkt tot specifieke producten — hele sector dierlijke productie volstaat als OR-tak; false → eindpunt false (geverifieerd) |
| `steun_dekt_uitsluitend_in_aanmerking_komende_kosten` | true | leden 6-7 (gemarkeerde tussenstand; kostentoets is untranslatable) |
| lid-4-energieblok (12 booleans), lid-9-uitsluitingen (7), irrigatie (lid 8/15) | false | niet van toepassing op een stalinvestering; `betreft_aankoop_dieren=true` → false (lid 9 punt d, geverifieerd) |
| hoofdstuk-I-set | als casus 1 | `steun_artikel`='14'; art 6 lid 5 kent art 14 niet, dus de lid-2-route moet dragen: `aanvraag_voor_aanvang_werkzaamheden=false` → eindpunt false (geverifieerd — anders dan bij art 15!) |

**Waar ik parameters moest raden (bruikbaarheids-bevindingen):**

1. **"Verder gaan dan EU-normen" bestaat niet als parameter.** Het dossier-idee
   draait om bovenwettelijke stalinvesteringen, maar art 14 kent die toets
   niet (dat begrip zit in art 31, dierenwelzijns*verbintenissen*, en in de
   definitie art 2 punt 33). Voor art 14 volstaat lid 3 punt b "verbeteren van
   de normen inzake dierenwelzijn". Een gebruiker die de LVV met dit
   praktijkvoorbeeld binnenkomt, moet zelf ontdekken dat de
   bovenwettelijkheids-vraag juridisch irrelevant is voor art 14-toelating.
2. **Dubbel dierenwelzijnsbegrip.** `doel_verbetering_milieu_hygiene_of_dierenwelzijnsnormen`
   (lid 3 b) en `investering_houdt_verband_met_dierenwelzijn` (lid 12 a) zijn
   bijna hetzelfde begrip in twee parameters; alleen de tweede opent 80 %.
   Beide moeten apart op true — vergeet je de tweede, dan valt de casus stil
   op de intensiteitstoets zonder dat duidelijk is waarom.
3. **~30 verplichte maar niet-toepasselijke parameters.** Het hele
   lid-4-energieblok en de irrigatie-parameters zijn `required: true` terwijl
   ze achter een NOT-guard irrelevant zijn; ik heb ze op false geraden (waarde
   doet er niet toe, maar de aanvrager weet dat niet). `betreft_aankoop_waakhonden`
   moet worden ingevuld voor een stal zonder honden.
4. **`voldoet_aan_voorwaarden_steunartikel` (art 6) is zelf-referentieel**: bij
   een art-15-casus vul je als aanvrager in of je aan art 15 voldoet — precies
   wat de engine aan het uitrekenen is (bewuste circulariteits-workaround, maar
   als invoerveld onbegrijpelijk).
5. `wordt_gepubliceerd_conform_art_9` en `cumulatie_overschrijdt_hoogste_maximum`
   zijn oordeel-parameters, geen feiten — de aanvrager kan die niet kennen.

---

## Defect-kandidaten voor de reverse-validators (keten ≠ letter)

1. **BEVESTIGD — `steun_artikel` is een onbewaakt proxy in art 6 lid 5.**
   Probe A: de art-14-casus met `steun_artikel: "33"` en **zonder** aanvraag
   vooraf geeft `voldoet_aan_voorwaarden_art_14 = true`. Probe B: idem met
   `steun_artikel: "25"` + `voldoet_aan_voorwaarden_steunartikel: true`.
   De letter (art 6 lid 5 punten d/h) koppelt de vrijstelling aan wat de steun
   *is* ("steun voor het opvangen van nadelen in verband met Natura
   2000-gebieden, als bedoeld in artikel 33"), niet aan wat de aanvrager
   *claimt*; niets verifieert dat `steun_artikel` overeenstemt met het artikel
   waarvan het eindpunt wordt gevraagd. Twee vrije invoervelden schakelen zo
   het stimulerend-effectvereiste uit. Suggestie: reverse-validator die
   `steun_artikel` bindt aan het geëvalueerde artikel, of een
   consistentie-poort per hoofdstuk-III-artikel.
2. **Verwant**: voor lid 5 punt h (art 33) eist het model níéts extra's — de
   kale string '33' volstaat, terwijl de andere takken ten minste
   `voldoet_aan_voorwaarden_steunartikel` vragen. Conform de letter ("als
   bedoeld in artikel 33", zonder "mits"), maar in combinatie met bevinding 1
   de goedkoopste route om art 6 te omzeilen.
3. **Niet afwijkend maar contra-intuïtief, expliciet getest en conform de
   letter** (géén defecten): `jaaromzet` boven 50 M€ met kleine balans blijft
   kmo (Bijlage I "of"); cumulering zonder maximum-overschrijding blokkeert
   niet (art 8 lid 3 b); geen aanvraag vooraf blokkeert art 15 niet (art 6
   lid 5 a) maar art 14 wél; ad-hocsteun aan een kmo triggert de
   vergewisplicht van art 6 lid 3 niet (alleen grote ondernemingen);
   intensiteit exact op het plafond (100 resp. 80) telt als voldoen
   ("maximaal"/"ten hoogste").

## Uitkomsten-overzicht

| casus | eindpunt | uitkomst |
|---|---|---|
| 1 ruilverkaveling | `voldoet_aan_voorwaarden_art_15` | **true** |
| 2 = 1 + onderneming in moeilijkheden | `voldoet_aan_voorwaarden_art_15` | **false** |
| 3 stalverduurzaming | `voldoet_aan_voorwaarden_art_14` (+ `maximale_steunintensiteit_pct_art_14` = 80) | **true** |
