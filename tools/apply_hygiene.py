#!/usr/bin/env python3
"""Apply the concept-hygiene rename map (docs/verrijking/hygiene.md) to the law YAML.

Article-scoped, text-surgical: within each named article's span, every
word-bounded occurrence of the old parameter name (declarations `name: old`,
references `$old`) is replaced. Underscore counts as a word character, so
substrings of longer names never match.
"""
import re
import sys

# (articles, old, new) — from docs/verrijking/hygiene.md secties A1-A13 + (b)1
RENAMES = [
    (["1"], "is_steun_in_kader_strategisch_glb_plan", "steun_in_kader_strategisch_glb_plan"),
    (["49"], "steun_in_kader_van_strategisch_glb_plan", "steun_in_kader_strategisch_glb_plan"),
    (["55", "56", "57", "58", "59"], "steun_verleend_in_kader_glb_plan_via_elfpo", "steun_in_kader_strategisch_glb_plan"),
    (["49", "50"], "milieueffectbeoordeling_uitgevoerd_en_vergunning_verleend", "milieueffectbeoordeling_uitgevoerd_en_vergunning_vooraf_verleend"),
    (["41", "43", "49"], "jaarlijkse_begroting", "gemeente_jaarbegroting"),
    (["41", "43", "49"], "aantal_inwoners", "gemeente_aantal_inwoners"),
    (["60"], "kostengebied_art_60", "kostengebied_clld_project"),
    (["61"], "kostengebied_art_61", "kostengebied_clld_project"),
    (["33"], "in_eerste_periode", "binnen_eerste_periode_van_ten_hoogste_vijf_jaar"),
    (["49", "50"], "investering_in_ultraperifeer_gebied_of_kleinere_egeische_eilanden", "investering_in_ultraperifeer_gebied_of_kleinere_eilanden_egeische_zee"),
    (["14", "17"], "steun_dekt_uitsluitend_in_aanmerking_komende_kosten", "kosten_binnen_in_aanmerking_komende_categorieen"),
    (["19", "21"], "kosten_beperkt_tot_in_aanmerking_komende_kostensoorten", "kosten_binnen_in_aanmerking_komende_categorieen"),
    (["39"], "kosten_behoren_tot_in_aanmerking_komende_categorieen", "kosten_binnen_in_aanmerking_komende_categorieen"),
    (["41", "42", "43", "44"], "kosten_binnen_subsidiabele_kostencategorieen", "kosten_binnen_in_aanmerking_komende_categorieen"),
    (["29"], "totale_vergoedingen_voor_schade", "totale_compensatie_inclusief_verzekering"),
    (["32"], "is_nieuwe_samenwerkingsvorm_of_nieuwe_activiteit", "nieuwe_samenwerkingsvorm_of_nieuwe_activiteit"),
    (["59"], "nieuwe_samenwerking_of_nieuwe_activiteit", "nieuwe_samenwerkingsvorm_of_nieuwe_activiteit"),
    (["32"], "in_overeenstemming_met_art_206_210bis_gmo", "in_overeenstemming_met_artt_206_210bis_vo_1308_2013"),
    (["32"], "draagt_bij_aan_doelstellingen_glb", "samenwerking_draagt_bij_aan_doelstellingen_art_6_vo_2021_2115"),
    (["31"], "gaat_verder_dan_verplichte_normen", "verbintenis_gaat_verder_dan_verplichte_normen"),
    (["46"], "gaat_verder_dan_toepasselijke_verplichte_vereisten", "verbintenis_gaat_verder_dan_verplichte_normen"),
    (["31"], "normen_omschreven_in_nationale_rechtsgrondslag", "verplichte_normen_omschreven_in_nationale_rechtsgrondslag"),
    (["46"], "verplichte_vereisten_omschreven_in_nationale_rechtsgrondslag", "verplichte_normen_omschreven_in_nationale_rechtsgrondslag"),
    (["22", "23"], "verstrekt_door_producentengroepering_of_organisatie", "verricht_door_producentengroepering_of_organisatie"),
    (["24"], "uitgevoerd_door_producentengroepering_of_organisatie", "verricht_door_producentengroepering_of_organisatie"),
    (["24"], "toegankelijk_voor_alle_ondernemingen_in_gebied", "toegankelijk_onder_objectieve_voorwaarden"),
    (["22"], "aanbieder_onpartijdig_zonder_belangenconflict", "aanbieder_onpartijdig_en_zonder_belangenconflict"),
    (["60", "61"], "betreft_clld_of_eip_project", "betreft_clld_project"),
    (["61"], "steunbedrag", "totaal_steunbedrag_per_clld_project"),
    (["55"], "in_plattelandsgebied", "basisdiensten_en_infrastructuur_in_plattelandsgebied"),
    # (d)1 lidmaatschap-polariteit, stap 1: 23/24 naar de canonieke positieve naam
    # (pure rename; de logica toetste daar al de negatieve waarde). Stap 2 (21/22,
    # logica-inversie) gebeurt handmatig.
    (["23"], "lidmaatschap_voorwaarde_voor_toegang", "lidmaatschap_is_toegangsvoorwaarde"),
    (["24"], "lidmaatschap_voorwaarde_voor_deelname", "lidmaatschap_is_toegangsvoorwaarde"),
]

def main(law_path):
    with open(law_path, encoding="utf-8") as f:
        lines = f.read().splitlines(keepends=True)

    bounds = []
    for i, ln in enumerate(lines):
        m = re.match(r"^- number: '?([^']+?)'?\s*$", ln)
        if m:
            bounds.append((i, m.group(1)))
    bounds.append((len(lines), None))
    span = {}
    for (start, num), (end, _) in zip(bounds, bounds[1:]):
        span[num] = (start, end)

    total = 0
    for arts, old, new in RENAMES:
        pat = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(old) + r"(?![A-Za-z0-9_])")
        for art in arts:
            if art not in span:
                print(f"WAARSCHUWING: artikel {art} niet gevonden voor {old}")
                continue
            s, e = span[art]
            n = 0
            for i in range(s, e):
                lines[i], k = pat.subn(new, lines[i])
                n += k
            if n == 0:
                print(f"WAARSCHUWING: '{old}' niet aangetroffen in artikel {art}")
            total += n

    with open(law_path, "w", encoding="utf-8") as f:
        f.write("".join(lines))
    print(f"totaal vervangingen: {total}")


if __name__ == "__main__":
    import sys
    main(sys.argv[1])
