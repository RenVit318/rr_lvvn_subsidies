# Notes batch h3-vee — artikelen 27, 28, 29, 30, 31 (LVV)

Alle vijf fragmenten schema-valide tegen v0.5.6 (jsonschema, volledige mini-wet)
en getest via het evaluate-binary: **29/29 tests geslaagd** (`test_h3vee.py` in
deze map; herdraaibaar). In de mini-testwetten stond tijdelijk `accepted: true`;
de fragmenten houden `accepted: false`. Bindingen gestubd als parameters, alleen
in de mini-wetten; de fragmenten dragen de echte `source.output`-bindingen.

## Drempels (artikel 4)

Alleen **artikel 31** heeft een drempel (`aanmeldingsdrempel_art_31`, 500
EUR/grootvee-eenheid/jaar) — gebonden en getoetst. **Artikelen 27, 28, 29 en 30
kennen in artikel 4 geen drempel**: geen drempel-binding (conform brief).

## Per artikel

- **27** (`voldoet_aan_voorwaarden_art_27`): categorie-enum
  `kostencategorie_art_27` (lid 2 a-f), per-categorie voorwaarden (b-uitzondering
  eigenaarcontroles/melkcontrole; e-heffingseis; lid 3 monitoring voor c-f),
  in-natura-eis (lid 4), marktdeelnemer-route (lid 4, 2e alinea, beperkt tot
  c-f + voorwaarden a/b), intensiteitstabel lid 5 (70/75/100%) als IF in
  LESS_THAN_OR_EQUAL. **Lid 3, 2e alinea** bindt intern
  `voldoet_aan_voorwaarden_verzekeringspremiesteun_art_28_lid_2` (zie art 28).
- **28** (`voldoet_aan_voorwaarden_art_28`): enum `steunobject_art_28`
  (VERZEKERINGSPREMIE | BIJDRAGE_ONDERLING_FONDS); lid 2 alleen voor premies,
  lid 6+7 alleen voor fondsen; lid 3 (M1-tekst, incl. punt d
  premiecompensatie gestorven dieren) en lid 4 als booleans; intensiteit ≤ 70%
  (lid 8). **Extra output** `voldoet_aan_voorwaarden_verzekeringspremiesteun_art_28_lid_2`
  (AND van lid 2 a-c) omdat artikel 27, lid 3 daarnaar verwijst — mergers: die
  output moet blijven bestaan. Lid 5 (plafonds) is een bevoegdheid, geen
  voorwaarde → untranslatable/genoteerd. Brontekst-typo "transpart" (lid 6 b)
  in description vermeld.
- **29** (`voldoet_aan_voorwaarden_art_29`): oorzakelijk verband (lid 2),
  betaaladres-enum + groeperingsvoorwaarden (lid 3), 3-jaar/4-jaar-termijnen
  (lid 4, als booleans — datum-rekenen bewust vermeden, verdieping mogelijk met
  DATE_ADD), taxatie-eis (lid 5), preventie-OR (lid 7: getroffen | redelijkerwijs
  niet mogelijk | eerste aanval), steun ≤ kosten (lid 8) en cumulatie ≤ kosten
  (lid 9, via `totale_vergoedingen_voor_schade`).
- **30** (`voldoet_aan_voorwaarden_art_30`): agromilieuklimaat-kader (lid 1),
  actie-enum lid 7 (gericht/gecoördineerd/begeleidend), verbintenistype-IF
  (lid 3: bedreigd lokaal ras jo. lid 4 + diersoortenlijst lid 5; plantaardig jo.
  lid 6; ANDERS voor lid-7-acties zonder lid-3-verbintenis), steun ≤ 100% kosten
  (lid 8). Lid 2 zijn definities, geen voorwaarden.
- **31** (`voldoet_aan_voorwaarden_art_31`): drempel- én lid-13-toets op
  `steunbedrag` (hier gemeten **per grootvee-eenheid per jaar**, zoals art 4(1)(d)
  en lid 13 meten; description zegt dat), leden 2-6 als booleans (lid 6 als
  IF nieuwe voorschriften → ≤ 24 maanden), gebieden-enum lid 7 (a-g) met de
  verdovingseis van punt f als geneste IF, duur 1-7 jaar met
  lidstaat-verlenging-OR (lid 8), herzieningsclausule (lid 11), jaarlijkse
  verlening (lid 12), intensiteit ≤ 100% (lid 13). Leden 9-10 (verlengings-
  mechanisme, kennistoegang) zijn lidstaat-verplichtingen → untranslatable.

## Nieuwe gedeelde parameters (meld ik hierbij)

- `totale_vergoedingen_voor_schade` (amount, eurocent): steun + overige
  betalingen/verzekeringsuitkeringen voor dezelfde schade — dezelfde
  cumulatiefiguur komt terug in de artikelen 25/26/37 (100%-plafonds); zelfde
  naam aanhouden.
- `diersoort` (string): RUNDEREN/SCHAPEN/GEITEN/PAARDACHTIGEN/VARKENS/VOGELS/
  KONIJNEN/BIJEN (lijst van art 30, lid 5; andere artikelen met diersoorten
  kunnen dezelfde naam gebruiken).
- Artikel-specifieke enums bewust gesuffixt (`kostencategorie_art_27`,
  `steunobject_art_28`, `kostencategorie_art_30`, `verbintenistype_art_30`)
  omdat de categorielijsten per artikel verschillen.

## Untranslatables (alle `accepted: false`, samengevat)

- 27: open norm "consistent monitoringprogramma" (lid 3); TSE-plicht/
  dierziekte-uitbraak vergt externe veterinaire vaststelling (lid 2 f).
- 28: open norm belemmering interne verzekeringsmarkt (lid 2 a); lid 5
  (bevoegdheid, geen voorwaarde); beoordeling nationale fondsvoorschriften (lid 7).
- 29: taxatie/berekening subsidiabele kosten incl. aftrek vermeden kosten
  (leden 5-6); evenredigheid preventieve maatregelen (lid 7).
- 30: kwalificatie bedreigd ras via Vo (EU) 2016/1012 (lid 4); "voldoende
  bewijs" genetische erosie (lid 6).
- 31: toets "verder dan verplichte normen" vergt externe vergelijking (leden
  3/6); berekening extra kosten/gederfde inkomsten (lid 12); leden 9-10
  (lidstaat-verplichtingen, procedureel).

## Open vragen / aandachtspunten

1. **Engine-gedrag optionele parameters**: een `required: false`-parameter die
   in een `when`-subject staat moet tóch worden meegegeven zodra die tak wordt
   geëvalueerd ("Variable not found"); short-circuit dekt alleen niet-bereikte
   takken. De verkennings-filter-aanroeper moet de trigger-booleans
   (bv. `steun_uitgekeerd_aan_marktdeelnemer_of_organisatie`) expliciet op
   false zetten. Eventueel bij merge heroverwegen: `required: true` voor
   trigger-parameters.
2. **Art 27 → art 28-binding**: cross-artikel intern; werkt alleen als de
   art-28-parameters bij zo'n evaluatie beschikbaar zijn. Voor het
   breedte-filter is dat acceptabel (de tak is alleen actief bij
   premiesteun-voor-gestorven-dieren).
3. Art 29, lid 4 als booleans i.p.v. datumrekenen — bewuste keuze
   (breedte-eerst); latere verdieping kan `datum_schade`/`datum_instelling`/
   `datum_betaling` + DATE_ADD gebruiken.
4. Art 30: lid 3 zegt niet expliciet dat élke steun onder dit artikel een
   lid-3-verbintenis vergt; verbintenistype ANDERS laat lid-7-acties zonder
   ras-/plantverbintenis door. Juridische check welkom.

## Testresultaat

29/29 PASS (7×art 27, 6×art 28, 5×art 29, 5×art 30, 6×art 31); per artikel
minstens één positieve en meerdere artikel-specifieke negatieve casussen.
