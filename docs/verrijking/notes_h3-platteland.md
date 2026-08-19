# Notes batch h3-platteland (LVV art 55–61)

Alle zeven artikelen hebben een eindpunt `voldoet_aan_voorwaarden_art_<N>`; geen skips.
Testharnas: `test_h3_platteland.py` — **43/43 PASS** (positief + negatief per artikel,
bindingen gestubd als parameters; untranslatables in de mini-wet op `accepted: true`,
in de fragmenten op `accepted: false`).

## Per artikel

| Art | Eindpunt | Drempel art 4 | Untranslatables | Testen |
|---|---|---|---|---|
| 55 | ja | `aanmeldingsdrempel_art_55` (10 mln) gebonden | netto-inkomsten-aftrek/80%-alternatief (lid 6); regionalesteunkaart bij modernisering (lid 7); werkkapitaal-uitsluiting (lid 5) | 7/7 |
| 56 | ja | geen drempel in art 4 (bedragsplafond lid 7: 100 000 EUR getoetst) | uitbetaling laatste tranche + sociaaleconomische weging (lid 6) | 6/6 |
| 57 | ja | geen drempel in art 4 (plafond lid 7: 3 000 EUR/jaar getoetst) | niveaubepaling stimulans o.b.v. vaste kosten (lid 4) | 5/5 |
| 58 | ja | geen drempel in art 4 (intensiteit lid 10: ≤70% getoetst) | inhoudelijke actie-kenmerken (lid 6) | 6/6 |
| 59 | ja | geen drempel in art 4 | begrenzing investeringskosten aan Vo 651/2014 (lid 14) | 8/8 |
| 60 | ja | `aanmeldingsdrempel_art_60` (2 mln) gebonden | max. steunpercentages per type verrichting uit Vo 2021/2115 (lid 4) | 6/6 |
| 61 | ja | `aanmeldingsdrempel_art_61` (200k) gebonden; plafond lid 3 (200k) ook expliciet getoetst | geen | 5/5 |

## Nieuwe gedeelde parameters (kandidaat-vocabulaire)

- `steun_verleend_in_kader_glb_plan_via_elfpo` (boolean) — lid 2 punt a van
  artt. 55–59: Elfpo-cofinanciering of aanvullende nationale financiering in het
  kader van een strategisch GLB-plan (Vo 2021/2115). Waarschijnlijk ook nuttig
  voor andere GLB-plan-artikelen elders in hoofdstuk III.
- `steun_identiek_aan_glb_plan_maatregel` (boolean) — lid 2 punt b. Let op:
  art 57 zegt "interventie" i.p.v. "maatregel"; zelfde begrip, in de
  parameter-description van art 57 zo benoemd.
- `glb_plan_goedgekeurd_voor_tenuitvoerlegging` (boolean) — alleen art 55 lid 1
  (tenuitvoerlegging pas na goedkeuring GLB-plan door de Commissie).
- `steunduur_jaren` (number) — duurvoorwaarden artt. 57 (≤7−verstreken jaren) en 59 (≤7).
- `begunstigde_is_gemeente` (boolean) — artt. 60 en 61.
- `neemt_deel_aan_clld_project` / `neemt_deel_aan_of_profiteert_van_clld_project`
  (boolean) — artt. 60 resp. 61 (letterlijke formulering verschilt).
- Artikel-specifieke enum-parameters: `soort_investering_art_55`,
  `begunstigde_categorie_art_56`, `soort_kwaliteitsregeling_art_57`,
  `samenwerkingsactiviteit_art_59`, `kostengebied_art_60`/`kostengebied_art_61`
  (60 en 61 delen dezelfde 7 waarden; bewust per artikel gehouden omdat het
  begrip aan het eigen lid hangt — merge-coordinator kan ze desgewenst unificeren).

## Twijfels / open vragen

1. **`betreft_clld_of_eip_project` bij art 60/61**: per de brief gebruikt als
   CLLD-afbakening, maar de bestaande description (art 1) omvat ook
   EIP-projecten. Voor art 60/61 is alleen de CLLD-tak relevant; description in
   deze fragmenten vernauwd tot CLLD. Menselijke check gewenst.
2. **`in_plattelandsgebied` in art 56**: aan de begunstigde gehangen (lid 3 zegt
   het bij alle drie categorieën); in art 55 aan de infrastructuur (lid 1).
   Zelfde gedeelde parameter, licht verschillend subject — bewust, per brief.
3. **Art 57 lid 3 b/c**: de erkenning door de lidstaat is als feit in de
   enum-waarde verdisconteerd (`DOOR_LIDSTAAT_ERKENDE_REGELING`,
   `VRIJWILLIGE_CERTIFICERINGSREGELING`); de criteria i–iv staan in de
   description, niet als aparte voorwaarden (het is de lidstaat die erkent).
4. **Art 59 lid 4** (samenwerkingsvormen a/b) is niet als aparte voorwaarde
   gemodelleerd: lid 3 (actoren) + lid 6 (activiteiten) dekken de afbakening;
   "oprichting van clusters en netwerken" valt onder de activiteitenlijst.
5. **Kostenlijsten** (55 lid 5, 59 lid 12, 60 lid 2) zijn conform breedte-eerst
   niet gemodelleerd (afbakening subsidiabele kosten, geen toetsbare voorwaarde
   op de maatregel); alleen expliciete verboden (werkkapitaal, exploitatiesteun)
   zijn wel meegenomen.
6. **Art 55 lid 6/7**: intensiteitstoets gemodelleerd als één ≤100%-toets voor
   alle categorieën; de verfijningen (netto-inkomsten, 80%-alternatief,
   regionalesteunkaart) zitten in untranslatables.
7. **`steunbedrag`-semantiek** verschilt per artikel en staat in de description:
   per investeringsproject (55), per begunstigde (56), per begunstigde per jaar
   (57), per onderneming per project (60), totaal per CLLD-project (61).
