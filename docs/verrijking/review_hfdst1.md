# Reverse-validatie hoofdstuk I + Bijlage I (art. 1, 3, 4, 5, 6, 7, 8, 9, Bijlage I)

Methode: elk machine_readable-element herleid naar een zinsnede in de `text:` van het
eigen artikel (skill law-reverse-validate). Bedragen nagerekend in eurocent, operatoren
getoetst aan "minder dan"/"niet overschrijdt"/"of"/"en", scope getoetst per lid.

## Oordeel per artikel

### Artikel 1 — schoon (met 1 jurist-vraag)
- Alle 31 parameters + lid-structuur (categorieën lid 1, uitsluitingen lid 3/4/5/6/7)
  herleidbaar naar de letter. Lid 1 punt b terecht ge-AND met
  `actief_in_primaire_landbouwproductie` ("die alleen van toepassing is op ondernemingen
  die actief zijn in de primaire productie"). Gemeente-CLLD-afwijking terecht zónder
  kmo-eis ("In afwijking hiervan").
- Lid 5 punt h correct als AND(in_moeilijkheden_geworden_door_de_gebeurtenis, OR(i–iv)).
- Untranslatables (kmo-beperking per inroepend artikel, Commissie-verlengingsbesluit,
  regeling-tekst-eis lid 4, open norm lid 6, WTO-punt-15) dekken de niet-gemodelleerde
  zinsneden. Zie jurist-vraag 1 over lid 4 punt b.

### Artikel 3 — schoon (met kanttekening)
- "mits ... voldoet aan alle voorwaarden van hoofdstuk I" als AND over art. 1, 5, 6, 8, 9;
  art. 4 (drempeltoets per hoofdstuk-III-artikel) is expliciet in de output-description
  gedelegeerd — conform de vaste architectuur van de brief.
- Kanttekening (geen defect, wel melden): artikel 7 (hoofdstuk I) zit níét in de AND en
  heeft ook geen eigen eindpunt (alleen untranslatables). "Alle voorwaarden van
  hoofdstuk I" is dus feitelijk "alle uitdrukbáre voorwaarden". Zie jurist-vraag 2.

### Artikel 4 — schoon op de bedragen; 1 technische vraag
- Alle 27 drempelbedragen nagerekend tegen de letter — allemaal correct:
  600 000 EUR→60000000 (14, 16, 36); 7,5 mln→750000000 (17, 38, 41, 42, 44, 49, 50);
  500 EUR→50000 (31, 33, 45); 200 EUR→20000 (33/45 na eerste periode, 46);
  600/900/450 EUR→60000/90000/45000 (34, 35); 2 mln→200000000 (39, 60);
  500 000→50000000 (40); 200 000→20000000 (48, 61); 10 mln→1000000000 (55).
- Uitzondering art. 46 lid 8 (punt p) en het opsplitsingsverbod (lid 2) correct als
  untranslatable.
- Technisch (vraag, geen letter-defect): `endpoint: aanmeldingsdrempels` benoemt een
  output die nergens bestaat (de outputs heten `aanmeldingsdrempel_art_<N>`). Dangling
  endpoint-naam; centraal beslissen of endpoint hier vervalt of één output moet noemen.

### Artikel 5 — schoon
- Lid 3 punten a–f volledig en correct (lening→referentiepercentage; garantie→OR van
  c-i/c-ii; fiscaal voordeel→maximum; voorschot→OR van binnen-drempels/methode-aanvaard;
  activa→OR taxatie/benchmark). Lid 4 (KAPITAALINJECTIE, RISICOKAPITAAL) als NOT-IN.
- De keuze "vorm buiten lid 3-lijst ⇒ niet transparant" (lid 2 als open norm
  onbereikbaar) is netjes als untranslatable gedocumenteerd. Zie jurist-vraag 3.

### Artikel 6 — GEFIXT (1 defect) + 1 jurist-vraag
- **Defect (gefixt in `art_6.yaml`)**: lid 5 punt f — *"steun voor de kosten van het
  afvoeren en vernietigen van gestorven dieren, mits aan de voorwaarden van artikel 27,
  lid 2, punten c), d), e) en f), **en artikel 28, lid 3, punt d)**, is voldaan"* — de
  IN-lijst van de gebundelde lid-5-tak bevatte `'27'` maar níét `'28'`. Artikel 28,
  lid 3, punt d dekt blijkens de wettekst van art. 28 exact deze categorie
  ("compensatie voor verzekeringspremies waarmee de kosten van het afvoeren en
  vernietigen van gestorven dieren worden gedekt"). Gestorven-dieren-steun die onder
  artikel 28 loopt kreeg dus ten onrechte géén lid-5-route. Fix: `'28'` toegevoegd aan
  de IN-lijst + comment aangepast. (De over-breedte — art. 27/28 kennen ook
  steunonderdelen buiten punt f — was al gedelegeerd aan de description van
  `voldoet_aan_voorwaarden_steunartikel`; die dekt art. 28 lid 3 punt d al.)
- Verder schoon: lid 2 (schriftelijk + inhoud a–e, vóór aanvang), lid 3
  (alleen ad-hoc × grote onderneming; gemeente-uitzondering LESS_THAN 1000000000
  eurocent en LESS_THAN 5000 — "minder dan" correct strikt), lid 4
  (AND(a, OR(b, vervolgregeling)) — "behalve" correct), voorrangsorde lid 5 > lid 4
  (alleen FISCAAL_VOORDEEL) > lid 2+3 conform "in afwijking van".
- Lid 5 punt h (art. 33) terecht zonder "mits"-voorwaarde; punten a (15/53, i én ii),
  b/m (21/22/47/48 + onbepaald aantal), c (24 + publicatie-eis) kloppen met de letter.

### Artikel 7 — schoon
- Geen execution; zes untranslatables die elk een zinsnede citeren (bruto-bedragen,
  standaardveronderstellingen, btw, BSE, discontering, +10-procentpunt-modificator).
  Terecht geen eindpunt: louter berekenings-/waarderingsvoorschriften.

### Artikel 8 — schoon (met kanttekening)
- Endpoint dekt lid 3 punt b en de overschrijdingsgrens van leden 5–7; lid 3 punt a
  (andere identificeerbare kosten telt niet als cumulering) staat in de
  parameter-description en spoort met de letter.
- Kanttekening: de categorische verboden van leden 8–10 (bijv. art. 14 lid 3 punt d
  × art. 25/26/28/37) gelden ongeacht overschrijding, maar zitten alleen in
  untranslatables — het eindpunt kan dus groen zijn waar lid 8 hard verbiedt. Als
  untranslatable gedocumenteerd; bij verdieping van de betrokken hoofdstuk-III-artikelen
  oppakken. Geen letter-defect in wat er wél gemodelleerd is.

### Artikel 9 — schoon
- OR(lid-5-uitzondering EIP/CLLD art. 39/40/60/61; publicatie conform lid 1) herleidbaar.
  De drempels 10 000/100 000 EUR (lid 1 punt c), tranchetabel (lid 2), termijnen (lid 3),
  inhoudseisen (lid 4) en Commissie-plicht (lid 6) terecht untranslatable — het zijn
  eisen aan de publicatie(-inhoud), geen toetsbare kenmerken van de maatregel.

### Bijlage I — schoon
- `is_kmo`: LESS_THAN 250 ("minder dan 250") ✓; OR(jaaromzet ≤ 5000000000,
  balanstotaal ≤ 4300000000) — "50 miljoen EUR of ... 43 miljoen EUR niet overschrijdt"
  → LESS_THAN_OR_EQUAL + OR is exact de letter ✓.
- Samentelling partner-/verbonden ondernemingen (art. 3/6), twee-boekjaren-regel
  (art. 4 lid 2), AJE-berekening (art. 5) terecht untranslatable; de parameters zijn in
  hun descriptions expliciet gemarkeerd als "ná toepassing van de samentellingsregels".

## Jurist-vragen (interpretatie, niet aantoonbaar fout)

1. **Art. 1 lid 4**: de uitzonderingen i (natuurramp-regelingen, art. 37) en ii
   (CLLD/EIP-regelingen) staan in de letter alléén onder punt a (*steunregelingen*);
   punt b (*ad-hocsteun* aan zo'n onderneming) kent geen uitzonderingen. Het model past
   de uitzonderingen op begunstigdeniveau toe, dus óók op ad-hocsteun. Is dat de
   bedoeling van de letter, of moet ad-hoc-Deggendorf-steun altijd buiten de
   verordening vallen?
2. **Art. 3**: "alle voorwaarden van hoofdstuk I" — artikel 7 levert geen toetsbaar
   eindpunt (alleen untranslatables) en telt dus niet mee in de AND. Akkoord dat de
   gemeenschappelijke poort daarmee bewust onvolledig is (fail-open voor art. 7)?
3. **Art. 5 lid 2 vs lid 3**: het model behandelt lid 3 als limitatief en keurt vormen
   buiten die lijst af, terwijl lid 2 een zelfstandige (open) transparantienorm is
   ("wordt geacht transparant te zijn als het BSE vooraf precies kan worden berekend").
   Fail-closed gekozen; kan een vorm buiten lid 3 tóch transparant zijn via lid 2?
4. **Art. 6 lid 3, slotalinea**: "Deze vereisten gelden niet voor gemeenten ..." — het
   model leest "deze vereisten" als alleen de lid-3-vergewisplicht (lid 2 blijft
   gelden). Alternatieve lezing: de uitzondering dekt ook lid 2. Welke lezing is juist?
5. **Art. 6 lid 5 punt f (na de fix)**: de lid-5-route voor `steun_artikel` '27'/'28'
   staat open voor álle steun onder die artikelen; de beperking tot art. 27 lid 2
   punten c–f resp. art. 28 lid 3 punt d zit alleen in de description van
   `voldoet_aan_voorwaarden_steunartikel`. Volstaat dat, of moet er een aparte
   categorie-parameter (betreft gestorven dieren) bij?
6. **Art. 4 (technisch)**: dangling `endpoint: aanmeldingsdrempels` (geen gelijknamige
   output) — centraal besluiten: endpoint weglaten of één output aanwijzen.

## Gefixte fragmenten

- `art_6.yaml` — '28' toegevoegd aan de IN-lijst van de gebundelde lid-5-tak
  (+ comment); verder ongewijzigd. YAML-parse geverifieerd.
