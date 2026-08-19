# Reverse-validatie LVV artikelen 41–61 (segment-verslag)

Bestand: `/Users/rkievit/Projects/rr_lvvn_subsidies/regulation/eu/eu_verordening/landbouwvrijstellingsverordening/2023-12-13.yaml`
Methode: law-reverse-validate (hallucinatie-check), elk machine_readable-element herleid
naar een zinsnede van het eigen artikel; drempel-bindingen getoetst aan artikel 4, lid 1;
bosbouw-artikelen gespiegeld aan hun landbouw-tegenhangers op weggelekte/gladgestreken
verschillen; alle eurocent- en percentagewaarden nagerekend.

## Samenvatting

| oordeel | artikelen |
|---|---|
| Volledig gegrond, geen defect | 43, 45, 46, 47, 48, 51, 53, 56, 57, 58, 61 |
| Klein defect, fix geleverd | 41 (descriptie-omissie) |
| Defect, fix geleverd | 49, 50 (ontbrekende lid-1-scopevoorwaarde), 52 (lid-3-kostenvoorwaarde ontbreekt) |
| Omissie gerapporteerd, geen fix (interfacekeuze centraal) | 42, 44 (FI-aanhef), 54, 55, 59, 60 (kostenlijst) |

Positief geverifieerd (extra-aandacht-punten uit de opdracht):

- **Art 45, twee drempel-outputs + periode-IF**: de constructie
  `LESS_THAN_OR_EQUAL(steunbedrag, IF(binnen_eerste_periode → aanmeldingsdrempel_art_45, default → …_na_eerste_periode))`
  spoort exact met art 4, lid 1, punt o ("500 EUR … in de eerste periode van ten hoogste
  vijf jaar en daarna 200 EUR"), en de aparte lid-5-maximumtoets (50000/20000 eurocent)
  spoort met "mag niet meer bedragen dan 500 EUR … en 200 EUR … in de daaropvolgende
  periode". Beide toetsen zijn zelfstandig herleidbaar; de duplicatie is de wet zelf.
- **Art 46, lid 8 heft maximum én drempel op**: geverifieerd. Lid 8 verhoogt het lid-7-
  maximum ("kan het in lid 7 vastgestelde maximumbedrag … worden verhoogd") en art 4,
  lid 1, punt p zondert lid-8-steun expliciet van de drempel uit ("behalve voor steun als
  bedoeld in artikel 46, lid 8"). Het model zet op beide toetsen dezelfde
  ontsnappings-AND (strategisch plan ∧ maximum verhoogd) — correct. Dat het plafond dan
  geheel vervalt i.p.v. "verhoogd" te zijn is netjes als untranslatable gemarkeerd.
- **Spiegel-check bosbouw (47–54) — verschillen NIET gladgestreken**:
  - art 49 lid 2 heeft de financieringsinstrumenten-vrijstelling op de MEB-eis; art 50
    lid 2 heeft die niet → model 50 bevat hem terecht níét.
  - art 49 lid 3 heeft de gemeente-uitzondering (begroting < 10 mln, < 5000 inwoners) op
    de bosbeheerplan-eis; art 50 lid 3 niet → model 50 bevat hem terecht níét.
  - art 49 kent een 100 %-trede (lid 8); art 50 stopt bij 80 % (lid 9) → correct
    verschillend gemodelleerd.
  - art 54 lid 6 is met "met name" niet-limitatief en is terecht níét als IN-lijst
    gemodelleerd; art 59 lid 6 (zonder "met name") wél als limitatieve lijst — zie
    juristvraag 3.
  - Geen voorwaarden uit landbouw-tegenhangers (14, 17, 21, 22) aangetroffen in 41–54.
- **Drempel-bindingen vs art 4**: 41→l, 42→m, 44→n, 45→o (+ na_eerste_periode), 46→p,
  48→q, 49→r, 50→s, 55→t, 60→u, 61→v: alle namen en bedragen kloppen. Artikelen 43, 47,
  51, 52, 53, 54, 56, 57, 58, 59 kennen in art 4 géén drempel en binden er terecht geen.
- **Bedragen/percentages**: alle eurocentwaarden nagerekend en correct (7,5 mln =
  750000000; 10 mln = 1000000000; 2 mln = 200000000; 200 000 = 20000000; 100 000 =
  10000000; 3 000 = 300000; 500/200 per ha = 50000/20000; gemeente-begroting 10 mln =
  1000000000). Intensiteiten 100/80/70/65 conform de eigen letter.
- **Operaties**: geen verboden constructies (IF overal met cases/default; NOT-wrapper;
  geen NOT_EQUALS/IS_NULL/FOREACH/CONCAT/SUBTRACT_DATE).

## Defecten met fix (fragmenten in deze map)

1. **Art 49 — ontbrekende scopevoorwaarde (fix: `art_49.yaml`)**. Het eindpunt
   `voldoet_aan_voorwaarden_art_49` toetst nergens dat de steun een investering in
   infrastructuur voor de bosbouwsector ís (lid 1: "Steun voor investeringen in
   infrastructuur voor de ontwikkeling, modernisering of aanpassing van de
   bosbouwsector"). Elk zusterartikel (41–48, 51–53) heeft zo'n `betreft_…`-voorwaarde;
   zonder haar kan willekeurige steun "voldoen aan art 49". Toegevoegd:
   `betreft_investering_infrastructuur_bosbouwsector` + AND-tak.
2. **Art 50 — zelfde defect (fix: `art_50.yaml`)**. Lid 1-scope ("investeringen in
   bosbouwtechnologieën en in de verwerking, mobilisering en afzet van
   bosbouwproducten") ontbrak als voorwaarde. Toegevoegd:
   `betreft_investering_bosbouwtechnologie_of_verwerking_afzet` + AND-tak.
3. **Art 52 — lid-3-kostenvoorwaarde ontbreekt (fix: `art_52.yaml`)**. Lid 3 ("De steun
   dekt de volgende kosten: a)–f)") is limitatief maar komt in model noch untranslatable
   voor. Zusterartikelen (41–44) modelleren dit als boolean
   `kosten_binnen_subsidiabele_kostencategorieen`. Toegevoegd, met de zes categorieën in
   de description.
4. **Art 41 — werkkapitaal-uitsluiting weggevallen (fix: `art_41.yaml`, alleen
   description)**. Lid 3, derde alinea: "Behalve wanneer de steun in het kader van een
   strategisch GLB-plan in de vorm van financieringsinstrumenten wordt verleend, wordt
   werkkapitaal niet beschouwd als in aanmerking komende kosten." Art 42 noemt dit wél
   in de kosten-description, art 41 niet. Description aangevuld; logica ongewijzigd.

## Omissies/aannames zonder fix (centrale keuze nodig)

5. **Art 42 en 44 — "Behalve wanneer … financieringsinstrumenten"-aanhef op de
   kostenlijst**. Art 42 lid 4 en art 44 lid 4/5 stellen de kostencategorie-afbakening
   alleen buiten financieringsinstrumenten; het model AND't
   `kosten_binnen_subsidiabele_kostencategorieen` onvoorwaardelijk en is daarmee voor
   FI-steun strenger dan de letter. Een kale OR-ontsnapping is óók fout (in art 42 bundelt
   de parameter tevens lid 6/7-kosten die niet achter de aanhef staan; in art 44 blijft de
   werkkapitaal-regel van lid 5, tweede alinea, bij niet-GLB-FI juist wél gelden). Wat de
   kostenafbakening voor FI-steun dan wél is, laat de letter open → juristvraag 1.
6. **Art 54 (lid 10), 55 (lid 5, punten a–d), 59 (lid 12), 60 (lid 2) — limitatieve
   kostenlijsten niet gemodelleerd** (geen parameter én geen untranslatable), terwijl
   41–44 dit patroon wel dragen. Inconsistente modelleringsdiepte; aanbeveling: zelfde
   boolean-parameter-patroon als bij de fix voor art 52 uitrollen. Bij art 54 hoort daar
   de kwalificatie "voor zover zij betrekking hebben op bosbouwactiviteiten" bij.
7. **Art 55, lid 7 tweede alinea**: het model toetst vlak ≤ 100 % voor alle categorieën,
   ook voor VERPLAATSING_EN_VERBOUWING mét modernisering, waar de regionalesteunkaart
   (mogelijk lager) geldt — netjes als untranslatable gemarkeerd, maar de vlakke
   100 %-toets kan daar een te ruim "voldoet" geven. Acceptabel voor breedte-eerst,
   melden bij verdieping.
8. **`legal_basis.law` inconsistent binnen het segment**: art 41–46 gebruiken
   `landbouwvrijstellingsverordening`, art 47–61 `Verordening (EU) 2022/2472`. Geen
   hallucinatie, wel normaliseren bij de merge.
9. **`betreft_clld_of_eip_project` (art 60/61)**: naam suggereert een gedeeld
   CLLD/EIP-begrip terwijl de descriptions alleen CLLD (art 31 Vo 2021/1060) dekken. Als
   art 39/40 dezelfde parameternaam voor EIP-projecten gebruiken, worden twee
   verschillende begrippen op één leaf samengevouwen (false friend). Hernoemen naar
   `betreft_clld_project` of splitsen.
10. **Art 61 meet `steunbedrag` per CLLD-project (totaal)**, terwijl het gedeelde
    vocabulaire `steunbedrag` als "per onderneming per project/jaar" definieert. De
    description zegt het er wel bij; overweeg een aparte naam
    (`totaal_steunbedrag_per_clld_project`).

## Juristvragenlijst

1. **Art 42/44 (en spiegel art 41 lid 3)**: welke kostenafbakening geldt voor steun in de
   vorm van financieringsinstrumenten, nu de limitatieve lijst per aanhef niet van
   toepassing is? Geldt de werkkapitaal-uitsluiting van art 44 lid 5, tweede alinea, bij
   FI-steun búíten een strategisch GLB-plan?
2. **Art 43, lid 5, punt b**: de letter stelt a, b en c conjunctief ("en") als
   herstel-voorwaarden; het model toetst punt b alleen bij een plantenplaag. Is de
   erkenning van uitgevoerde plaagbestrijdingsmaatregelen ook vereist bij herstel na
   bijv. storm of brand? (reeds als untranslatable gemarkeerd — bevestiging gevraagd.)
3. **Art 59, lid 6**: is de activiteitenlijst a–k limitatief? Art 54 lid 6 zegt "met
   name" (niet-limitatief), art 59 lid 6 niet. Het model behandelt 59 als limitatief.
4. **Art 46, lid 4**: is "vijf tot zeven jaar" inclusief beide grenzen (model: 5 ≤ d ≤ 7)?
5. **Art 48, lid 7 vs art 4, lid 1, punt q**: het artikel maximeert 200 000 EUR per
   onderneming per drié jaar, de drempel meet 200 000 EUR per onderneming per jáár. Het
   model houdt beide gescheiden aan — klopt die lezing (drempel is dus in de praktijk
   nooit knellend)?
6. **Art 61, lid 1 vs art 4, lid 1, punt v**: art 61 spreekt van "ondernemingen", de
   drempelbepaling van "kmo's". Het model volgt art 61 (geen kmo-eis). Bevestigen dat
   dit een slordigheid in de verordening is en geen impliciete kmo-beperking.
7. **Art 45, lid 1 vs lid 2**: lid 1 zegt "Richtlijn 92/43/EEG of Richtlijn 2009/147/EG",
   lid 2 "de Richtlijnen 92/43/EEG en 2009/147/EG". Het model leest "of" (één richtlijn
   volstaat). Akkoord?
8. **Art 55, lid 1**: "in het kader van een strategisch GLB-plan" staat in lid 1 als
   karakterisering en komt terug als eis in lid 2; het model toetst het via lid 2
   (Elfpo-cofinanciering of aanvullende nationale financiering). Volstaat dat, of draagt
   lid 1 een zelfstandige eis?

## Per-artikel oordeel (kort)

- **41** ✅ op descriptie-omissie na (fix 4). Lid 4/6/7/8/10/11 alle herleid; gemeente-
  uitzondering correct als AND van drie eisen; lid 9 (kan-bepaling) terecht niet als eis.
- **42** ✅ logica; omissie 5 (FI-aanhef lid 4). MEB-FI-vrijstelling (lid 5, tweede
  alinea) correct — die alinea bestaat in art 41 níét en staat daar terecht niet.
- **43** ✅. Lid 5-gating op herstel, lid 6-gating op plaagpreventie, cumulatie lid 9
  tweede alinea gated op herstel: alle herleidbaar. Geen drempel — klopt met art 4.
- **44** ✅ logica; omissie 5. Niet-inheemse-soortenuitsluiting met GLB-uitzondering
  letterlijk lid 2, tweede zin.
- **45** ✅ — zie positieve verificatie hierboven; juristvraag 7.
- **46** ✅ — zie positieve verificatie; juristvraag 4.
- **47** ✅. Soort-actie-lijst dekt exact lid 2 (beide alinea's); lid 6-betalingseis
  correct beperkt tot lid 3-punt-a-steun; lid 4/5 als untranslatable.
- **48** ✅. Dubbele bedragstoets (lid 7 driejaars + art 4-jaardrempel) beide herleid;
  juristvraag 5. Lid 6 (kan-bepaling) terecht alleen untranslatable.
- **49** ⚠️ fix 1 (scope). Verder volledig herleid, inclusief intensiteitsladder
  65/80/100 met juiste voorrang van lid 8.
- **50** ⚠️ fix 2 (scope). Spiegelverschillen met 49 correct bewaard (geen FI-escape,
  geen gemeente-uitzondering, geen 100 %-trede).
- **51** ✅. Lid 2 zijn definities, geen voorwaarden — terecht niet gemodelleerd.
- **52** ⚠️ fix 3 (lid-3-kosten). Overige leden volledig herleid; lid 2-alternatief
  correct als untranslatable.
- **53** ✅ — compleet en minimaal, zoals het artikel zelf.
- **54** ✅ logica; omissie 6 (lid 10). Lid 6 terecht niet-limitatief behandeld; lid 8
  keten-eis correct gated op korte-keten-steun; lid 9 correct als untranslatable.
- **55** ✅ logica; omissies 6 en 7. Kleinschalige-infrastructuurgrens (2 mln) en
  uitsluiting hernieuwbare energie/breedband correct alleen op categorie a.
- **56** ✅. Lid-4-eis correct dubbel gated (categorie a ∧ rechtspersoon); 100 000 EUR
  correct.
- **57** ✅. Duurvermindering lid 6 als SUBTRACT(7, verlopen jaren) — letterlijk; 3 000
  EUR per begunstigde per jaar correct.
- **58** ✅. Oorsprong-verboden (lid 7) en -vermelding (lid 8) als twee aparte, correct
  gegate toetsen; 70 % correct.
- **59** ✅ logica; omissie 6 (lid 12); juristvraag 3. Lid-8-uitzondering
  (individuele actoren, plan voorziet, verspreidingsplicht) correct in de lid-3-toets
  gevouwen; lid-9-gating op punten d/e correct.
- **60** ✅ logica; omissies 6 en 9. Kmo-OF-gemeente-structuur volgt lid 1 eerste/tweede
  alinea juncto lid 3; lid 4 terecht untranslatable (externe tabel).
- **61** ✅; punten 9/10 en juristvraag 6. "Deelnemen aan of profiteren van" correct
  ruimer dan art 60; 200 000-maximum én drempelbinding beide herleid.
