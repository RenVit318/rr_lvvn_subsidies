# Notes batch h3-bos-kern — LVV artikelen 41-46 (bos)

Alle zes fragmenten hebben een eindpunt `voldoet_aan_voorwaarden_art_<N>`
(endpoint als string), schema-valide tegen v0.5.6 (jsonschema op de volledige
mini-wet) en getest via het evaluate-binary: **30/30 tests geslaagd**
(`test_h3_bos_kern.py` in deze map, herdraaibaar). In de mini-testwetten stond
tijdelijk `accepted: true`; de fragmenten houden `accepted: false`.

## Per artikel

- **41 (bebossing)** — eindpunt + drempel `aanmeldingsdrempel_art_41`.
  Toetsen: lid 1 (object), lid 2/3/5 (kostencategorieën als boolean), lid 4
  (MEB-conditie), lid 6 (premie ≤ 12 jaar), lid 7 (uitgesloten soorten;
  niet-inheems met GLB-uitzondering), lid 8+12 (aanpassing + minimale
  milieuvereisten), lid 10 (grote-ondernemingseis met `is_kmo`-binding en
  gemeente-uitzondering < 10 mln EUR / < 5 000 inwoners), lid 11 (≤ 100 %).
  Untranslatables: kostenplafonds lid 3 a/b, GLB-financieringsinstrumenten-
  uitbreiding (lid 3 al. 2), lid 12 (open normen). Lid 9 (kan-bepaling
  struiken in moeilijke gebieden) is permissief, geen voorwaarde — niet
  gemodelleerd.
- **42 (boslandbouw)** — eindpunt + drempel art_42. Zelfde patroon; lid 5-MEB
  vervalt bij financieringsinstrumenten; lid 8 (structuur/samenstelling door
  lidstaat) als boolean-toets + untranslatable (open norm).
- **43 (bosschade)** — eindpunt; **geen drempel in artikel 4** (bewust: art 4
  lid 1 noemt art 43 niet; steun kan onder 107(2)(b) vallen). Toetsen: lid 2
  (kosten), lid 3 (geen landbouwactiviteiten op art-34-areaal), lid 4
  (brandpreventie alleen binnen bosbeschermingsplan), lid 5 a/b/c
  (herstelvoorwaarden), lid 6 (plaagpreventie), lid 7 (bosbeschermingsplan +
  grote-ondernemingseis bij herstel), lid 8 (geen inkomensverlies), lid 9
  (≤ 100 % + cumulatietoets als boolean).
- **44 (veerkracht-investeringen)** — eindpunt + drempel art_44. Lid 2
  (gerichtheid + niet-inheems-uitsluiting met GLB-uitzondering), lid 3 (MEB,
  financieringsinstrumenten vrijgesteld), lid 4/5 (kosten), lid 6 (≤ 100 %).
- **45 (gebiedsnadelen bos)** — eindpunt + **beide** drempels
  (`aanmeldingsdrempel_art_45` en `..._na_eerste_periode`), geselecteerd met
  IF op `binnen_eerste_periode_van_ten_hoogste_vijf_jaar`; lid 5-maxima
  (500/200 EUR per ha per jaar) daarnaast als literal-toets. `steunbedrag` is
  hier per hectare per jaar ("zoals het artikel het meet"). Lid 3: Natura
  2000-bosgebied OF landschapselement (art 10 Habitatrichtlijn, ≤ 5 % van het
  netwerk).
- **46 (bosmilieu)** — eindpunt + drempel art_46. Lid 2/3/5/6 als
  boolean-toetsen, lid 4 (duur 5-7 jaar OF langere lidstaatperiode), lid 7
  (≤ 100 % en ≤ 200 EUR/ha/jr). Lid 8-uitzondering: maximum én drempel
  vervallen alleen bij AND(strategisch plan, verhoogd maximum) — spoort met
  de uitzondering "behalve art 46 lid 8" in art 4, punt p.

## Nieuwe gedeelde parameters (meerdere artikelen in deze batch)

- `steun_in_vorm_van_financieringsinstrumenten` (bool) — 42, 44
- `steun_in_kader_strategisch_glb_plan` (bool) — 41, 44, 46 (lid 8 zegt
  "strategisch plan"; als hetzelfde begrip gelezen, zie twijfels)
- `milieueffectbeoordeling_vereist` / `milieueffectbeoordeling_uitgevoerd_en_vergunning_vooraf_verleend` (bool) — 41, 42, 44
- `kosten_binnen_subsidiabele_kostencategorieen` (bool) — 41, 42, 43, 44
- `duur_jaarlijkse_premie_jaren` (number) — 41, 42 (0 = geen premie)
- `informatie_uit_bosbeheerplan_overgelegd`, `is_gemeente_autonome_lokale_autoriteit`,
  `jaarlijkse_begroting` (amount), `aantal_inwoners` (number) — 41 lid 10 en
  43 lid 7 al. 2 (zelfde constructie)
- `betreft_niet_inheemse_soorten` (bool) — 41 lid 7 d, 44 lid 2

## Twijfels / open vragen (voor menselijke review)

1. **Art 43 lid 5 punt b**: naar de letter conjunctief ("en"), maar alleen
   betekenisvol bij een plantenplaag. Model toetst punt b alleen indien
   `betreft_plantenplaag`; als untranslatable gemarkeerd in het fragment.
2. **Art 46 lid 8** zegt "strategisch plan" waar elders "strategisch
   GLB-plan" staat; gemodelleerd als hetzelfde begrip
   (`steun_in_kader_strategisch_glb_plan`).
3. **`actief_in_bosbouwsector` niet gebruikt**: geen van de artikelen 41-46
   bakent de sector in de eigen letter af (art 45 noemt wel de begunstigden:
   `is_bosbezitter_bosbeheerder_of_vereniging`); de sector-gating loopt via
   het toepassingsgebied van artikel 1, gebonden via artikel 3.
4. **Art 45**: drempel (art 4 punt o) en lid-5-maximum zijn numeriek gelijk
   (500/200 EUR/ha/jr); beide toetsen staan er bewust apart in (binding
   respectievelijk literal), zodat een wijziging van art 4 zichtbaar wordt.

## Untranslatables-samenvatting (alle `accepted: false`)

- 41: kostenplafonds lid 3 a/b; GLB-financieringsinstrumenten (lid 3 al. 2);
  minimale milieuvereisten lid 12.
- 42: kostenplafonds lid 4 a/b; structuur/samenstelling door lidstaat (lid 8).
- 43: reikwijdte lid 5 punt b; cumulatietoets lid 9 al. 2.
- 44: kostenplafonds lid 4 a/b; leasing-/werkkapitaaluitsluiting lid 5.
- 45: 5 %-plafond landschapselementen (lid 3 b); berekening extra
  kosten/gederfde inkomsten (lid 2/5).
- 46: verhoging maximumbedrag lid 8 (open norm); berekening extra
  kosten/gederfde inkomsten (lid 6).

## Testresultaat

30/30 PASS: per artikel minimaal één positieve en één artikel-specifieke
negatieve casus; extra takken gedekt: 41 lid 7 d en lid 10 (gemeente), 42
financieringsinstrumenten-uitzondering, 43 herstel- en plaagpaden, 45
landschapselement-tak en periode-omslag, 46 lidstaatperiode en
lid-8-verhoging. NB: optionele parameters moeten bij de niet-kortgesloten
takken wél meegegeven worden (engine kent geen default-false); de testwet
geeft daarom neutrale waarden mee.
