#!/usr/bin/env python3
"""Bouw routekaart.json — de statische index (laag 0) van alle LVV-eindpunten.

Per eindpunt-artikel: identificatie, titel, hoofdstuk, drempel (gebonden
art-4-output + bedrag), maximale intensiteit (grofweg: hoogste literal in een
LESS_THAN_OR_EQUAL op steunintensiteit_pct), begunstigde-facetten (afgeleid
uit parameter-/bindinggebruik), untranslatables en de volledige parameterlijst.

Usage: build_routekaart.py <law.yaml> <out.json>
"""
import json
import re
import sys

import yaml

LAW = sys.argv[1]
OUT = sys.argv[2]

doc = yaml.safe_load(open(LAW, encoding="utf-8"))

# drempelbedragen uit artikel 4 (literal-outputs)
art4 = next(a for a in doc["articles"] if a["number"] == "4")
drempels = {}
for act in art4["machine_readable"]["execution"]["actions"]:
    if isinstance(act.get("value"), int):
        out_name = act["output"]
        desc = next(
            (o.get("description", "") for o in art4["machine_readable"]["execution"]["output"]
             if o["name"] == out_name),
            "",
        )
        drempels[out_name] = {"bedrag_eurocent": act["value"], "eenheid": desc}


def walk(node, fn):
    fn(node)
    if isinstance(node, dict):
        for v in node.values():
            walk(v, fn)
    elif isinstance(node, list):
        for v in node:
            walk(v, fn)


def titel(a):
    first = a["text"].splitlines()[0]
    return first.strip("*").strip() if first.startswith("**") else None


FACET_PARAMS = {
    "actief_in_primaire_landbouwproductie": "primaire landbouwproductie",
    "actief_in_verwerking_landbouwproducten": "verwerking landbouwproducten",
    "actief_in_afzet_landbouwproducten": "afzet landbouwproducten",
    "actief_in_bosbouwsector": "bosbouwsector",
    "in_plattelandsgebied": "plattelandsgebied",
    "basisdiensten_en_infrastructuur_in_plattelandsgebied": "plattelandsgebied",
    "betreft_clld_project": "CLLD",
    "is_jonge_landbouwer": "jonge landbouwer",
    "is_kleine_of_micro_onderneming": "kleine/micro-onderneming",
    "begunstigde_is_gemeente": "gemeente",
}

hoofdstuk = None
routes = []
for a in doc["articles"]:
    mr = a.get("machine_readable")
    n = a["number"]
    if n == "14":
        hoofdstuk = "III"
    if not mr or not mr.get("endpoint"):
        continue
    if not (n.isdigit() and 14 <= int(n) <= 61):
        continue  # laag 0 toont de steunroutes (hoofdstuk III); poorten blijven intern
    ex = mr.get("execution", {})
    params = ex.get("parameters", [])
    inputs = ex.get("input", [])
    param_names = {p["name"] for p in params}

    # gebonden drempel(s)
    route_drempels = []
    for inp in inputs:
        src_out = (inp.get("source") or {}).get("output", "")
        if src_out.startswith("aanmeldingsdrempel"):
            d = drempels.get(src_out)
            if d:
                route_drempels.append({"output": src_out, **d})

    # kmo-eis: binding op Bijlage I
    kmo = any((i.get("source") or {}).get("output") == "is_kmo" for i in inputs)

    # max intensiteit: hoogste literal in een <=-vergelijking op steunintensiteit_pct
    intens = []
    def scan_intens(node):
        if (
            isinstance(node, dict)
            and node.get("operation") == "LESS_THAN_OR_EQUAL"
            and node.get("subject") == "$steunintensiteit_pct"
            and isinstance(node.get("value"), (int, float))
        ):
            intens.append(node["value"])
    walk(ex.get("actions", []), scan_intens)

    facetten = sorted({FACET_PARAMS[p] for p in param_names if p in FACET_PARAMS})
    if kmo:
        facetten.insert(0, "kmo")

    unt = mr.get("untranslatables", [])
    routes.append({
        "artikel": n,
        "titel": titel(a),
        "endpoint": mr["endpoint"],
        "hoofdstuk": hoofdstuk or "III",
        "facetten": facetten,
        "kmo_vereist": kmo,
        "drempels": route_drempels,
        "max_intensiteit_pct": max(intens) if intens else None,
        "untranslatables": [
            {"construct": u["construct"], "reason": u["reason"]} for u in unt
        ],
        "parameters": [
            {
                "name": p["name"],
                "type": p.get("type", "string"),
                "description": p.get("description", ""),
                "required": p.get("required", True),
            }
            for p in params
        ],
        "url": a.get("url"),
    })

kaart = {
    "law": doc["$id"],
    "celex": doc.get("celex_nummer"),
    "valid_from": doc.get("valid_from"),
    "valid_to": doc.get("valid_to"),
    "gegenereerd_uit": LAW.split("/")[-1],
    "routes": routes,
}
json.dump(kaart, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(routes)} routes; drempels gevonden: {len(drempels)};",
      f"met kmo-eis: {sum(1 for r in routes if r['kmo_vereist'])};",
      f"met intensiteit: {sum(1 for r in routes if r['max_intensiteit_pct'] is not None)}")
