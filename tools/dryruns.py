#!/usr/bin/env python3
"""Dry-runs van de routeverkenner: zes casussen door de bucket-mechaniek
(zelfde semantiek als app/src/lib/buckets.js) tegen het native evaluate-binary.

Per casus: antwoorden zoals de UI ze zou zetten (categorie-keuze zet alle
categorie-parameters, bijzonderheden-schakelaar zet alle uitsluitings-feiten
op false), dan de drie emmers + toetsing tegen verwachtingen.
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LAW = REPO / "regulation/eu/eu_verordening/landbouwvrijstellingsverordening/2023-12-13.yaml"
EVALUATE = "/Users/rkievit/Projects/regelrecht/packages/target/release/evaluate"

law = LAW.read_text().replace("accepted: false", "accepted: true")
vf = json.loads((REPO / "app/public/vragenflow.json").read_text())
GATES = [g for g in ["1", "3", "4", "5", "6", "8", "9", "Bijlage I"] if g in vf["artikelen"]]
ROUTES = [n for n in vf["artikelen"] if n not in GATES]
GROOT = 10**15
BUDGET = 20

ctx = vf["artikelen"]["1"]["param_context"]
CATEGORIE = [p for p, c in ctx.items() if "valt_onder_categorie_lid_1" in c]
BIJZONDER = [p for p in vf["artikelen"]["1"]["params"] if p not in CATEGORIE]


def basis(target, mode, answers):
    params = {}
    volgorde = [n for n in vf["artikelen"] if n not in GATES and n != target] + GATES + [target]
    for n in volgorde:
        for p, spec in vf["artikelen"][n]["params"].items():
            params[p] = spec["neutraal"] if spec["ambigu"] else spec["gunstig" if mode == "opt" else "ongunstig"]
    params.update(answers)
    return {k: v for k, v in params.items() if v is not None}


def evalueer(ep, params):
    payload = {"law_yaml": law, "output_name": ep, "params": params, "date": "2024-06-01", "extra_laws": []}
    r = subprocess.run([EVALUATE], input=json.dumps(payload), capture_output=True, text=True)
    out = json.loads(r.stdout)
    return out.get("outputs", {}).get(ep), out.get("error")


def optimistisch(target, answers):
    ep = vf["artikelen"][target]["endpoint"]
    p0 = basis(target, "opt", answers)
    got, err = evalueer(ep, p0)
    if got is True:
        return True
    pog = 0
    for n in GATES + [target]:
        for p, spec in vf["artikelen"][n]["params"].items():
            if p in answers:
                continue
            for kand in spec.get("gunstig_kandidaten", [])[1:]:
                if pog >= BUDGET:
                    break
                pog += 1
                if evalueer(ep, {**p0, p: kand})[0] is True:
                    return True
            if spec["ambigu"] and pog < BUDGET:
                probes = []
                if isinstance(spec["neutraal"], bool):
                    probes = [not spec["neutraal"]]
                elif spec["neutraal"] == "":
                    probes = (vf["vragen"].get(p, {}).get("opties") or [])[:6]
                elif isinstance(spec["neutraal"], (int, float)):
                    probes = [GROOT]
                for pr in probes:
                    if pog >= BUDGET:
                        break
                    pog += 1
                    if evalueer(ep, {**p0, p: pr})[0] is True:
                        return True
    return False


print("— baseline (analyse-artefacten bepalen) —", file=sys.stderr)
ARTEFACT = {n for n in ROUTES if not optimistisch(n, {})}


def beoordeel(answers):
    emmers = {"voldoet": [], "mogelijk": [], "uitgesloten": [], "artefact": sorted(ARTEFACT, key=int)}
    for n in ROUTES:
        if n in ARTEFACT:
            continue
        if not optimistisch(n, answers):
            emmers["uitgesloten"].append(n)
            continue
        ep = vf["artikelen"][n]["endpoint"]
        got, _ = evalueer(ep, basis(n, "pess", answers))
        emmers["voldoet" if got is True else "mogelijk"].append(n)
    for k in ("voldoet", "mogelijk", "uitgesloten"):
        emmers[k].sort(key=int)
    return emmers


def categorie_keuze(*aan):
    return {p: (p in aan) for p in CATEGORIE}


def geen_bijzonderheden():
    return {p: False for p in BIJZONDER}


CASUSSEN = [
    (
        "1. kmo primaire landbouwproductie (stalverduurzaming-profiel)",
        {**categorie_keuze("actief_in_primaire_landbouwproductie"), **geen_bijzonderheden()},
        {"verwacht_levend": ["14", "15", "25"], "verwacht_uitgesloten": ["17", "41", "55", "60"]},
    ),
    (
        "2. onderneming in moeilijkheden, geen uitzonderingen",
        {**geen_bijzonderheden(), "is_onderneming_in_moeilijkheden": True},
        {"verwacht_levend": [], "verwacht_uitgesloten": ["14", "15", "17", "38"]},
    ),
    (
        "3. gemeente die profiteert van CLLD-project",
        {**categorie_keuze("is_gemeente_die_profiteert_van_clld_project"), **geen_bijzonderheden(),
         "betreft_clld_project": True},
        {"verwacht_levend": ["60", "61"], "verwacht_uitgesloten": ["14", "17"]},
    ),
    (
        "4. bosbouwsector",
        {**categorie_keuze("betreft_steun_voor_de_bosbouw"), **geen_bijzonderheden()},
        {"verwacht_levend": ["41", "42", "43", "44", "45", "46", "47", "49", "50", "51", "52", "53", "54"],
         "verwacht_uitgesloten": ["14", "15", "17"]},
    ),
    (
        "5. exportsteun (uitsluiting lid 3)",
        {**categorie_keuze("actief_in_primaire_landbouwproductie"),
         **{p: False for p in BIJZONDER if p != "betreft_steun_voor_exportactiviteiten"},
         "betreft_steun_voor_exportactiviteiten": True},
        {"verwacht_levend": [], "verwacht_uitgesloten": ["14", "15", "25", "38"]},
    ),
    (
        "6. grote onderneming (geen kmo), primaire productie",
        {**categorie_keuze("actief_in_primaire_landbouwproductie",
                            "betreft_herstel_schade_natuurrampen_in_de_landbouwsector"),
         **geen_bijzonderheden(),
         "aantal_werknemers": 500, "jaaromzet": 20_000_000_000, "balanstotaal": 20_000_000_000},
        {"verwacht_levend": ["37"], "verwacht_uitgesloten": ["14", "15", "18"]},
    ),
]

for naam, answers, verwacht in CASUSSEN:
    e = beoordeel(answers)
    print(f"\n=== {naam}")
    print(f"  voldoet:      {e['voldoet']}")
    print(f"  mogelijk:     {e['mogelijk']}")
    print(f"  uitgesloten:  {e['uitgesloten']}")
    fouten = []
    levend = set(e["voldoet"]) | set(e["mogelijk"])
    for n in verwacht["verwacht_levend"]:
        if n in ARTEFACT:
            fouten.append(f"verwacht-levend art {n} is analyse-artefact")
        elif n not in levend:
            fouten.append(f"verwacht-levend art {n} is UITGESLOTEN")
    for n in verwacht["verwacht_uitgesloten"]:
        if n in ARTEFACT:
            continue
        if n not in e["uitgesloten"]:
            fouten.append(f"verwacht-uitgesloten art {n} is LEVEND")
    print("  toetsing:     " + ("OK" if not fouten else "; ".join(fouten)))
print(f"\nanalyse-artefacten (blijvend 'mogelijk · analyse onvolledig'): {sorted(ARTEFACT, key=int)}")
