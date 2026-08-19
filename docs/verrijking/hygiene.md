# Concept-hygiëne-audit LVV (2023-12-13.yaml)

Bron: volledige parameter-inventaris (440 kale parameters, 36 bindingsnamen, 89 outputs) uit
`/Users/rkievit/Projects/rr_lvvn_subsidies/regulation/eu/eu_verordening/landbouwvrijstellingsverordening/2023-12-13.yaml`,
gelezen naast de 12 batch-notes. Volledige inventaris: `param_inventory.txt` in deze map.
Geen wijzigingen aan het wetbestand gedaan.

---

## (a) Hernoem-kaart (aantoonbare duplicaten; machinaal toepasbaar)

Elke regel: `oude_naam` → `nieuwe_naam`, met de artikelen waar de oude naam voorkomt.
De rename is puur lexicaal (parameternaam in `parameters:` én elk gebruik in de
execution-logica van dat artikel); descriptions blijven de eigen letter citeren.

### A1 — GLB-plan-cluster (art. 2, punt 11: één begrip, vier namen)

| oud | artikelen | nieuw |
|---|---|---|
| `is_steun_in_kader_strategisch_glb_plan` | 1 | `steun_in_kader_strategisch_glb_plan` |
| `steun_in_kader_van_strategisch_glb_plan` | 49 | `steun_in_kader_strategisch_glb_plan` |
| `steun_verleend_in_kader_glb_plan_via_elfpo` | 55, 56, 57, 58, 59 | `steun_in_kader_strategisch_glb_plan` |

Canoniek: de naam die 41/44/46 al dragen. Alle instanties verwijzen naar hetzelfde
gedefinieerde begrip (art. 2 punt 11: toegekend overeenkomstig Vo 2021/2115, Elfpo-
gecofinancierd óf aanvullende nationale financiering); de 55-59-beschrijving is dat begrip
verbatim. Description-eis na merge: elke instantie citeert art. 2 punt 11 (zie wees-lijst).
Art. 46 lid 8 zegt "strategisch plan" i.p.v. "strategisch GLB-plan" — reeds als zelfde
begrip gelezen (batch h3-bos-kern, vraag 2); die lezing blijft in de description staan.

### A2 — MEB-composiet (twee namen voor één samengesteld begrip)

| oud | artikelen | nieuw |
|---|---|---|
| `milieueffectbeoordeling_uitgevoerd_en_vergunning_verleend` | 49, 50 | `milieueffectbeoordeling_uitgevoerd_en_vergunning_vooraf_verleend` |

Beide betekenen: MEB uitgevoerd én vergunning verleend vóór de datum van toekenning
(descriptions 49/50 zeggen dat al). `milieueffectbeoordeling_vereist` is al overal
consistent (14, 17, 41, 42, 44, 49, 50). Zie (d) voor de part/whole-restschuld
richting het 14/17-tweeluik.

### A3 — Gemeente-kwartet (art 6 lid 3 = art 41 lid 10 = art 43 lid 7 = art 49 lid 3, zelfde constructie)

| oud | artikelen | nieuw |
|---|---|---|
| `jaarlijkse_begroting` | 41, 43, 49 | `gemeente_jaarbegroting` |
| `aantal_inwoners` | 41, 43, 49 | `gemeente_aantal_inwoners` |

Canoniek: de art-6-namen — die dragen de referent (de gemeente) in de naam;
`jaarlijkse_begroting`/`aantal_inwoners` zijn zonder context dubbelzinnig (van wie?).
`is_gemeente_autonome_lokale_autoriteit` is al consistent over alle vier (6, 41, 43, 49).

### A4 — Kostengebied CLLD (art 60 lid 3 = art 61 lid 2: identieke 7 enumwaarden, identieke description)

| oud | artikelen | nieuw |
|---|---|---|
| `kostengebied_art_60` | 60 | `kostengebied_clld_project` |
| `kostengebied_art_61` | 61 | `kostengebied_clld_project` |

Geverifieerd: waardenlijst en description zijn woordelijk gelijk. Het suffix-argument
("begrip hangt aan het eigen lid") vervalt: het begrip is in beide artikelen hetzelfde
(gebied van de kosten binnen het CLLD-project); de batch h3-platteland liet de merge
expliciet aan de coördinator.

### A5 — Eerste periode (art 33 lid 5 = art 45 lid 5: zelfde begrip)

| oud | artikelen | nieuw |
|---|---|---|
| `in_eerste_periode` | 33 | `binnen_eerste_periode_van_ten_hoogste_vijf_jaar` |

Canoniek: de zelfdocumenterende art-45-naam (batch h3-milieu voorspelde deze merge al).

### A6 — Ultraperifeer/Egeïsche eilanden (één begrip, twee spellingen)

| oud | artikelen | nieuw |
|---|---|---|
| `investering_in_ultraperifeer_gebied_of_kleinere_egeische_eilanden` | 49, 50 | `investering_in_ultraperifeer_gebied_of_kleinere_eilanden_egeische_zee` |

Canoniek: de 14/17-naam (volgt de letter "kleinere eilanden in de Egeïsche Zee").

### A7 — Kosten-binnen-limitatieve-lijst (één begrippatroon, vijf namen)

| oud | artikelen | nieuw |
|---|---|---|
| `steun_dekt_uitsluitend_in_aanmerking_komende_kosten` | 14, 17 | `kosten_binnen_in_aanmerking_komende_categorieen` |
| `kosten_beperkt_tot_in_aanmerking_komende_kostensoorten` | 19, 21 | `kosten_binnen_in_aanmerking_komende_categorieen` |
| `kosten_behoren_tot_in_aanmerking_komende_categorieen` | 39 | `kosten_binnen_in_aanmerking_komende_categorieen` |
| `kosten_binnen_subsidiabele_kostencategorieen` | 41, 42, 43, 44 | `kosten_binnen_in_aanmerking_komende_categorieen` |

Zelfde tussenstand-begrip in alle elf artikelen: "de gedekte kosten vallen binnen de
limitatieve lijst van in aanmerking komende kosten van dít artikel" (het per-artikel-
relatieve patroon dat het vocabulaire al voor `steunbedrag`/`subsidiabele_kosten`
hanteert). Canoniek: de 24/26-naam — "in aanmerking komende kosten" is de term van de
verordening zelf (art. 7); "subsidiabele" is systeemtaal. Description-eis: elke
instantie blijft de eigen leden/punten noemen (staat er nu al).

### A8 — Betaalroute/compensatie (art 29 sluit aan op 25/37)

| oud | artikelen | nieuw |
|---|---|---|
| `totale_vergoedingen_voor_schade` | 29 | `totale_compensatie_inclusief_verzekering` |

Zelfde cumulatiefiguur (steun + overige betalingen incl. verzekering voor dezelfde
schade); descriptions van 25/37 en 29 beschrijven hetzelfde. Canoniek: de naam met
twee bestaande gebruikers.

### A9 — Samenwerking (art 32 / 54 / 59: zelfde zinnen in de leden 2 en 7)

| oud | artikelen | nieuw |
|---|---|---|
| `is_nieuwe_samenwerkingsvorm_of_nieuwe_activiteit` | 32 | `nieuwe_samenwerkingsvorm_of_nieuwe_activiteit` |
| `nieuwe_samenwerking_of_nieuwe_activiteit` | 59 | `nieuwe_samenwerkingsvorm_of_nieuwe_activiteit` |
| `in_overeenstemming_met_art_206_210bis_gmo` | 32 | `in_overeenstemming_met_artt_206_210bis_vo_1308_2013` |
| `draagt_bij_aan_doelstellingen_glb` | 32 | `samenwerking_draagt_bij_aan_doelstellingen_art_6_vo_2021_2115` |

Drie namen voor het lid-7-begrip; twee voor de GMO-conformiteit; art 32 lid 2 en
art 54 lid 2 zijn dezelfde eis over de samenwerking. NB: `gericht_op_doelstellingen_
artikel_6_verordening_2021_2115` (46) blijft apart — ander subject (de verbintenis).

### A10 — Verbintenis-normen (art 31/34/35/46: zelfde sjabloonleden)

| oud | artikelen | nieuw |
|---|---|---|
| `gaat_verder_dan_verplichte_normen` | 31 | `verbintenis_gaat_verder_dan_verplichte_normen` |
| `gaat_verder_dan_toepasselijke_verplichte_vereisten` | 46 | `verbintenis_gaat_verder_dan_verplichte_normen` |
| `normen_omschreven_in_nationale_rechtsgrondslag` | 31 | `verplichte_normen_omschreven_in_nationale_rechtsgrondslag` |
| `verplichte_vereisten_omschreven_in_nationale_rechtsgrondslag` | 46 | `verplichte_normen_omschreven_in_nationale_rechtsgrondslag` |

Zelfde begrip als bij 34/35 (welke basisnormen gelden verschilt per artikel — dat is
het bestaande per-artikel-patroon; description-eis: eigen normbasis blijft geciteerd;
art 46 zegt "vereisten" — in de description benoemen). `vereisten_gaan_verder_dan_
glmc_normen` (33) blijft apart: ander subject (de gebiedsvereisten, niet de verbintenis).

### A11 — Uitvoering door producentengroepering (één predicaat, drie werkwoorden)

| oud | artikelen | nieuw |
|---|---|---|
| `verstrekt_door_producentengroepering_of_organisatie` | 22, 23 | `verricht_door_producentengroepering_of_organisatie` |
| `uitgevoerd_door_producentengroepering_of_organisatie` | 24 | `verricht_door_producentengroepering_of_organisatie` |

Zelfde rol in alle vier de artikelen: de gesteunde dienst/activiteit wordt door een
pg/-organisatie uitgevoerd, en dát activeert de pg-voorwaarden (lidmaatschap/bijdragen).
`begunstigde_is_producentengroepering` (58) blijft apart — begunstigde-hoedanigheid.

### A12 — Toegankelijkheid (identieke zinsnede)

| oud | artikelen | nieuw |
|---|---|---|
| `toegankelijk_voor_alle_ondernemingen_in_gebied` | 24 | `toegankelijk_onder_objectieve_voorwaarden` |
| `aanbieder_onpartijdig_zonder_belangenconflict` | 22 | `aanbieder_onpartijdig_en_zonder_belangenconflict` |

Art 24 lid 7 draagt woordelijk dezelfde zinsnede als 20/21/22; de onpartijdigheids-
namen (22 vs 48) verschillen één woordje voor hetzelfde begrip.

### A13 — CLLD-valse-vriend-splitsing + steunbedrag-symmetrie (zie ook (b))

| oud | artikelen | nieuw |
|---|---|---|
| `betreft_clld_of_eip_project` | 60, 61 | `betreft_clld_project` |
| `steunbedrag` | 61 | `totaal_steunbedrag_per_clld_project` |

Art 1 behoudt `betreft_clld_of_eip_project` (dekt daar wél beide, lid 4 a ii en
lid 5 g). In 60/61 is het begrip vernauwd tot CLLD (descriptions zeggen dat al) —
één naam voor twee begrippen is een valse vriend; splitsen. Art 61 meet bovendien
het totaal per CLLD-project — exact de art-40-figuur, die daar al terecht
`totaal_steunbedrag_per_eip_project` heet (aanbeveling batch h3-rampen-oo).

**Niet in de kaart** (bewust): polariteits- en vorm-harmonisaties die logica-aanpassing
vergen — zie (b) en (d).

---

## (b) Valse vrienden (zelfde naam, verschillende begrippen) — oordeel per geval

1. **`in_plattelandsgebied`** (1, 55, 56) — drie referenten onder één naam:
   art 1: de begunstigde/diens activiteit; art 55: de *infrastructuur en basisdiensten*
   liggen in plattelandsgebied; art 56: de begunstigde bevindt zich er. Een begunstigde
   buiten het gebied met infrastructuur erbinnen maakt 55-waar en 56-onwaar — één
   gedeelde parameter conflateert dat voor de filter-aanroeper.
   **Oordeel: art 55 splitsen** → `basisdiensten_en_infrastructuur_in_plattelandsgebied`
   (mechanisch toepasbaar, alleen art 55). Art 1 vs 56 ("actief in" vs "bevindt zich in"):
   acceptabel onder één naam mét description-eis (beide over de begunstigde);
   jurist-vraag genoteerd. NB: "plattelandsgebied" is nergens in de verordening
   gedefinieerd (batch hfdst1a) — blijft extern feit.
2. **`steunbedrag`** (32 artikelen) — de meeteenheid verschilt per artikel (per project /
   per jaar / per ha per jaar / per grootvee-eenheid / per drie jaar / per gebeurtenis).
   **Oordeel: acceptabel** — dit is de bewuste briefdefinitie ("zoals het artikel het
   meet") en élke instantie draagt de meting in de description (geverifieerd).
   Uitzonderingen gefixt in de kaart: art 61 (totaal per project ≠ per onderneming,
   zie A13). Art 48-patroon (apart `steunbedrag_over_drie_jaar` naast de jaarmaat) is
   de zuiverste vorm wanneer één artikel twee maten kent; art 21/22/36 dragen hun
   dubbele maat in de description — acceptabel, verdiepingskandidaat splitsen (36: per
   project vs per jaar bij gekapitaliseerde werkzaamheden).
3. **`steun_artikel`** (alleen art 6) — nog geen valse vriend; bewaken zodra hoofdstuk-
   III-artikelen hem hergebruiken (h3-invest-open-vraag 1): dan centraal dezelfde
   string-semantiek ('14', '25', …) afdwingen.
4. **`subsidiabele_kosten`** (25, 29, 30, 37, 55) — betekenis per artikel: getaxeerde
   schadekosten (25/37), in aanmerking komende kosten (29/30), investeringskosten met
   plafond (55). **Oordeel: acceptabel** per briefdefinitie ("de kosten waarop het
   artikel de steun betrekt"); descriptions dragen het (geverifieerd).
5. **`steunintensiteit_pct`** — grondslag wisselt: % van *werkelijk gemaakte* kosten
   (15, 23, 53) vs % van *in aanmerking komende* kosten (overige). **Oordeel:
   acceptabel met description-eis** (aanwezig); bij verdieping van art 7 heroverwegen.
6. **`betreft_clld_of_eip_project`** (1 vs 60/61) — echte valse vriend; **splitsen**
   (kaart A13).
7. **`steun_in_natura`** (24, 27) — art 27 vouwt "en niet in de vorm van rechtstreekse
   betalingen" mee. **Oordeel: acceptabel**, descriptions dragen het verschil; bij
   verdieping de niet-rechtstreeks-clausule apart leggen.
8. **`steun_jaarlijks_verleend`** (31, 35) / `steun_jaarlijks_per_hectare` (33, 34) /
   `steun_jaarlijks_per_hectare_bosareaal` (45) — bewust naar de letter onderscheiden
   (batch h3-milieu); **acceptabel**, geen merge.

---

## (c) Wees-parameters (verordening leidt zelf af / definieert zelf) — met definitieplaats

**`is_kmo`-controle: VOLDAAN.** Nergens een kale `is_kmo`-parameter; 11 interne
bindingen naar de Bijlage-I-output (art 1, 6, 14, 15, 16, 17, 41, 43, 49, 50, 60).
Wel gevonden: **art 61 toetst kmo helemaal niet**, terwijl lid 1 (en de art-4-drempel-
description) over "kmo's die … profiteren" gaat — geen wees maar een ontbrekende
voorwaarde; zie (d).

| parameter | artikelen | definitieplaats | status |
|---|---|---|---|
| `is_jonge_landbouwer` / `investering_door_jonge_landbouwer` | 18, 22 / 14, 17 | art. 2, punt 61 (invulling lidstaat in GLB-plan) | ✓ gemarkeerd in description |
| `is_onderneming_in_moeilijkheden` | 1 | art. 2, punt 59 (jo. art. 2 punt 18 Vo 651/2014) | ✓ gemarkeerd |
| `is_kleine_of_micro_onderneming` | 18 | Bijlage I, art. 2, leden 2-3 | ✓ gemarkeerd; verdieping: aparte Bijlage-I-outputs `is_kleine_onderneming`/`is_micro_onderneming` en dan binden |
| `is_landbouwer` | 57 | art. 2 | ✓ gemarkeerd |
| `is_klein_landbouwbedrijf` | 14 | extern: art. 28 Vo 2021/2115 | ✓ gemarkeerd (extern, geen wees) |
| `steun_in_kader_strategisch_glb_plan` (na A1) | 1, 41, 44, 46, 49, 55-59 | art. 2, punt 11 | **FIX**: de 41/44/46-descriptions noemen art. 2 punt 11 niet; na de merge in élke instantie de definitieplaats opnemen |
| `verbintenis_valt_onder_art_34` | 35 | art. 34 bakent zelf af (lid 1-2) | **wees**: kale parameter zonder afleidingsverwijzing; minimaal description-eis; verdieping: afleiden uit de art-34-classificatie of accept-with-rationale (wederzijdse uitsluiting 34↔35 borgen) |
| `verbintenis_valt_onder_art_35` | 34 | art. 35 bakent zelf af | idem (spiegel) |
| `kosten_vallen_onder_art_20` | 35 | art. 20 (kostensoorten) | **wees-licht**: description verwijst naar lid 9 maar niet naar de art-20-afbakening; description-eis |
| `is_eip_of_clld_steun_art_39_40_60_61` | 9 | de artikelen 39/40/60/61 zelf | **wees-kandidaat**: afleidbaar uit `steun_artikel` ∈ {39,40,60,61} + projectdeelname; nu ongemarkeerde kale parameter — description-eis; echte binding stuit op dezelfde cirkel als art 6 (gedocumenteerd houden) |
| `begunstigde_categorie_art_56` (waarde KLEINE_OF_MICRO_ONDERNEMING) | 56 | Bijlage I | **FIX**: enumwaarde draagt een Bijlage-I-begrip; description moet naar Bijlage I verwijzen |
| `voldoet_aan_voorwaarden_steunartikel` (6), `cumulatie_overschrijdt_hoogste_maximum` (8), `steunbedrag_waarvoor_onderneming_in_aanmerking_komt` (25/26/37), `gebied_binnen_vijf_procent_grens` (33) | — | eigen artikel | ✓ correct gemarkeerde tussenstanden |

Positief voorbeeld: art 27 lid 3 bindt `voldoet_aan_voorwaarden_verzekeringspremiesteun_art_28_lid_2`
als interne binding — precies hoe een intra-wet-afleiding hoort.

---

## (d) Overige bevindingen

1. **Negatie-herintreding — lidmaatschap** (het enige echte polariteitsgeval):
   `lidmaatschap_geen_toegangsvoorwaarde` (21, 22) naast `lidmaatschap_voorwaarde_voor_toegang`
   (23) en `lidmaatschap_voorwaarde_voor_deelname` (24). Eén begrip-as, twee
   polariteiten als onafhankelijke namen: de aanroeper moet hetzelfde feit in 21/22
   als `true` en in 23/24 als `false` aanleveren. Voorstel: één canonieke positieve
   feit-parameter `lidmaatschap_is_toegangsvoorwaarde`, met `NOT` in de logica van
   21/22 — **handmatige fix** (logica wijzigt mee), daarom niet in de hernoem-kaart.
   Binnen één artikel is nergens een X∧¬X-paar gevonden.
2. **Betaalroute-vorm**: 25/26/37 modelleren de keuze-as "rechtstreeks vs via
   groepering" als twee onafhankelijke booleans (beide-waar/beide-onwaar mogelijk);
   art 29 als enum `steun_betaald_aan` — de zuivere vorm. Harmonisatie (enum overal)
   bij verdieping; geen mechanische rename.
3. **Art 61 mist de kmo-toets** van lid 1 ("kmo's … of gemeenten"): alleen
   `begunstigde_is_gemeente` staat er; een niet-kmo-onderneming glipt erdoor.
   Modellering-gat, melden aan de merge-coördinator (fix: `OR(is_kmo-binding,
   begunstigde_is_gemeente)` zoals art 60 het half doet).
4. **MEB part/whole-restschuld** (na A2): 14/17 ontleden het begrip in
   `milieueffectbeoordeling_uitgevoerd` + `vergunning_verleend_voor_datum_toekenning`;
   41-50 houden het composiet. Verdieping: overal het tweeluik (composiet nooit naast
   zijn delen laten bestaan).
5. **`investering_met_milieu_klimaatdoelstellingen_art_14_lid_3`** (49, 50) is de OR
   van de drie gedeelde doel-parameters van 14/17 (`doel_klimaatmitigatie_en_adaptatie`
   e.a.) — decompositie-kandidaat (zoals art 17 lid 12 a het al doet).
6. **Termijnen art 29** als booleans (`regeling_ingesteld_binnen_drie_jaar_na_schadedatum`,
   `steun_betaald_binnen_vier_jaar_na_schadedatum`) vs het datum+DATE_ADD-patroon van
   25/26/37 — bewuste breedte-eerst-keuze (batch h3-vee), harmonisatiekandidaat.
7. **Intermediair-as**: 32/54 als number (`aantal_intermediairs_…`), 59 als boolean
   (`hoogstens_een_intermediair_…`) — zelfde begrip, twee vormen; harmonisatie.
8. **Enum-suffix-conventie inconsistent**: `kostencategorie_art_27`, `steunobject_art_28`,
   `samenwerkingsactiviteit_art_59` gesuffixt, maar `samenwerkingsactiviteit`,
   `samenwerkingsvorm` (32), `vorm_van_samenwerking` (54), `steuncategorie` (20),
   `soort_steun`/`soort_gebeurtenis` (26), `soort_actie` (47), `gebiedstype` (33),
   `kostensoort` (36), `soort_verrichting` (51) niet. Nog geen botsing, wel
   valse-vriend-risico zodra een tweede artikel dezelfde kale naam kiest. Preventief
   suffixen of de conventie centraal vastleggen. (`samenwerkingsvorm` 32 vs
   `vorm_van_samenwerking` 54 hebben verschillende waardenlijsten — géén duplicaat.)
9. **`bijdragen_niet_leden_beperkt_tot_{activiteits,advies,uitvoerings}kosten`**
   (21/22/24): zelfde sjabloon, drie namen; unificatiekandidaat maar de kostensoort
   in de letter verschilt net — niet in de kaart, aan de jurist/coördinator.
10. **Bewust gescheiden en zo laten**: `neemt_deel_aan_…` vs `neemt_deel_aan_of_
    profiteert_van_…` (39/40, 60/61); `steun_afhankelijk_van_gebruik_binnenlandse_goederen`
    (1 lid 3d) vs `verplichting_tot_gebruik_binnenlandse_goederen_of_diensten` (1 lid 6a);
    de erkennings-/oorzakelijkheidsparen per gebeurtenistype (25/26/29/37/43);
    `aanbieder_beschikt_over_…personeel` (21/47) naast `aanbieder_gekwalificeerd_
    ervaren_en_betrouwbaar` (22/48); `duur_jaarlijkse_premie_jaren` (41/42) naast
    `verbintenisduur_jaren` (31/46) naast `steunduur_jaren` (20/32/54/57/59).
