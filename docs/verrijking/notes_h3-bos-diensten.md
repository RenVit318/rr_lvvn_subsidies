# Notes batch h3-bos-diensten (LVV art. 47–54)

Alle acht artikelen hebben een eindpunt `voldoet_aan_voorwaarden_art_<N>`,
ge-AND met de binding `voldoet_aan_gemeenschappelijke_voorwaarden` (art. 3).

## Per artikel

| Art | Eindpunt | Drempel (art. 4) | Untranslatables |
|---|---|---|---|
| 47 | ja | geen (genoteerd) | kosten leden 3–5 (10 %-grond, marktwaarde, werkkapitaal, tijdsevenredigheid, afschrijving) |
| 48 | ja | `aanmeldingsdrempel_art_48` (200 000 EUR/onderneming/jaar) | groepsadvies lid 6 ("gerechtvaardigd en passend", open norm; lid 6 is een bevoegdheid, geen tak) |
| 49 | ja | `aanmeldingsdrempel_art_49` (7,5 mln/investeringsproject) | kosten leden 5–6 |
| 50 | ja | `aanmeldingsdrempel_art_50` (7,5 mln/investeringsproject) | kosten leden 4–5; motiveringsnorm lid 6 (feit "motivering gegeven" wél als parameter) |
| 51 | ja | geen (genoteerd) | geen (lid 2 zijn definities, geen voorwaarden) |
| 52 | ja | geen (genoteerd) | lid 2 (alternatieve rechtstreekse steun aan producenten: aggregatie/bedragsberekening; hoofdroute gemodelleerd) |
| 53 | ja | geen (genoteerd) | geen |
| 54 | ja | geen voor art. 54 zelf (genoteerd) | lid 9 (doorverwijzing naar "het toepasselijke artikel inzake investeringssteun" + art. 4: juridische kwalificatie) |

## Nieuwe gedeelde parameters (meerdere artikelen in deze batch)

- `consistent_met_akis_beschrijving_glb_plan` (boolean) — art. 47 lid 1 / art. 48 lid 2: acties consistent met de AKIS-beschrijving in het strategisch GLB-plan.
- `milieueffectbeoordeling_vereist` en `milieueffectbeoordeling_uitgevoerd_en_vergunning_verleend` (boolean) — art. 49/50 lid 2 (Richtlijn 2011/92/EU); vermoedelijk ook bruikbaar voor art. 14 e.a. investeringsartikelen.
- `informatie_uit_bosbeheerplan_overgelegd` (boolean) — art. 49/50 lid 3 (grote ondernemingen).
- `investering_met_milieu_klimaatdoelstellingen_art_14_lid_3` en `investering_in_ultraperifeer_gebied_of_kleinere_egeische_eilanden` (boolean) — de 80 %-verhogingsgronden van art. 49 lid 7 / art. 50 lid 9.
- `steun_in_kader_van_strategisch_glb_plan` (boolean) — art. 49 lid 4; komt in veel artikelen terug.
- `steun_in_vorm_van_financieringsinstrumenten` (boolean) — art. 49 lid 2, tweede alinea.
- `steunduur_jaren` (number) — art. 54 lid 11; ook elders bruikbaar (bijv. art. 33/45-periodes).
- Bestaand vocabulaire gebruikt: `steunbedrag`, `steunintensiteit_pct`, `steunvorm` (GESUBSIDIEERDE_DIENST voor art. 48 lid 4), `is_kmo` (binding Bijlage I, alleen art. 49/50 waar lid 3 grote ondernemingen onderscheidt).

## Modelleringskeuzes / open vragen

- **Art. 48, twee maten**: art. 4, punt q meet 200 000 EUR *per jaar*, lid 7 meet 200 000 EUR *over drie jaar*. Daarom twee parameters: `steunbedrag` (per jaar, drempeltoets) en `steunbedrag_over_drie_jaar` (lid 7). Vraag voor review: is dit de bedoelde lezing?
- **Art. 47/48/53 onderwerp-parameters**: het onderwerp van de steun ("adviesdiensten in de bosbouwsector", "ruilverkaveling van bosbouwgrond") is als boolean-parameter opgenomen zodat het verkennings-filter niet elk steun-idee door deze artikelen laat; herleidbaar tot lid 1. Art. 47 gebruikt daarvoor `actief_in_bosbouwsector` ("ten behoeve van ondernemingen die in de bosbouwsector actief zijn") + `soort_actie` (lid 2).
- **Art. 47 lid 6** geldt alleen voor lid 3-punt a-steun; gemodelleerd als IF over `betreft_kosten_organisatie_en_uitvoering_acties`.
- **Art. 49 lid 3-uitzondering**: gemeentegrenzen "minder dan 10 miljoen EUR" (1000000000 eurocent) en "minder dan 5 000 inwoners" als LESS_THAN. De uitzondering ontbreekt in art. 50 lid 3 — bewust niet gespiegeld.
- **Art. 49 lid 4** is alleen limitatief buiten een strategisch GLB-plan; binnen het plan is elke infrastructuurinvestering voor ontwikkeling/modernisering/aanpassing van bossen mogelijk (waarde ANDERS toegestaan).
- **Art. 50 lid 2** kent géén financieringsinstrumenten-uitzondering (anders dan art. 49 lid 2) — bewust niet gespiegeld.
- **Art. 52 lid 1**: "leden geen grote ondernemingen behalve gemeenten" is een vaststelling over de ledenlijst (aggregatie); als boolean-feit aangeleverd, gemarkeerd in de description.
- **Art. 54 lid 6** ("mag met name") is een niet-limitatieve activiteitenlijst → geen voorwaarde/tak.
- **Art. 54 lid 10** (kosten "voor zover zij betrekking hebben op bosbouwactiviteiten") is kostenafbakening → niet gemodelleerd (breedte-eerst), valt onder de berekenings-scope.
- In de fragmenten staan alle untranslatables op `accepted: false`; de testwet zette ze tijdelijk op `true`.

## Testresultaat

Harness: `scratchpad/test_h3_bos.py` (mini-testwet per artikel; bindingen
vervangen door parameters, untranslatables tijdelijk accepted: true).
43 casussen (per artikel ≥ 1 positief en ≥ 1 negatief op een
artikel-specifieke voorwaarde, plus drempel-, uitzonderings- en
intensiteitsranden bij 49/50): **alle 43 OK** tegen
`packages/target/release/evaluate` (engine 0.3.0, schema v0.5.6).
