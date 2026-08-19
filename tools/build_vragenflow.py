#!/usr/bin/env python3
"""Bouw vragenflow.json — de polariteits-analyse voor laag 1 van de routeverkenner.

Voor elk artikel met machine_readable: bepaal per parameter de 'gunstige'
(maakt voorwaarden waar) en 'ongunstige' invulling, door de conditie-boom te
lopen met NOT-polariteit. Een parameter met tegenstrijdige eisen binnen één
artikel wordt 'ambigu' gemarkeerd: die krijgt in beide runs een neutrale
waarde en de zekerheid van het oordeel wordt in de UI afgezwakt.

De drie emmers in de browser:
  - optimistische run (onbekenden gunstig) → false  ⇒ uitgesloten (bewijsbaar)
  - pessimistische run (onbekenden ongunstig) → true ⇒ voldoet al
  - anders ⇒ mogelijk, mits …

Daarnaast: vraag-metadata per parameter (beschrijving, type, opties uit
IN/EQUALS-literals, welke eindpunten hem raken) voor de vraagvolgorde.

Usage: build_vragenflow.py <law.yaml> <out.json>
"""
import json
import sys
from collections import defaultdict

import yaml

LAW = sys.argv[1]
OUT = sys.argv[2]

doc = yaml.safe_load(open(LAW, encoding="utf-8"))

NEUTRAAL = {"boolean": False, "number": 0, "amount": 0, "string": "", "date": "2024-06-01"}
GROOT = 10**15


def var(x):
    return x[1:] if isinstance(x, str) and x.startswith("$") else None


class Analyse:
    def __init__(self, acties=None):
        # naam -> value-boom van de actie die deze output produceert
        self.acties = acties or {}
        self.bezocht = set()
        # param -> {"gunstig": set of demands, "ongunstig": ...} as (kind, value)
        self.eisen = defaultdict(lambda: {True: [], False: []})
        self.ambigu = set()

    def eis(self, param, positief, waarde_waar, waarde_onwaar):
        """Registreer: om deze tak waar te maken moet param = waarde_waar
        (in positieve context) — polariteit bepaalt welke kant gunstig is."""
        gunstig = waarde_waar if positief else waarde_onwaar
        ongunstig = waarde_onwaar if positief else waarde_waar
        self.eisen[param][True].append(gunstig)
        self.eisen[param][False].append(ongunstig)


def ref_of_param(an, naam, pos):
    """Een $-referentie is óf een tussen-output van dit artikel (recursie met
    polariteit) óf een parameter/binding (eis registreren)."""
    if naam in an.acties:
        sleutel = (naam, pos)
        if sleutel not in an.bezocht:
            an.bezocht.add(sleutel)
            loop(an.acties[naam], pos, an)
        return True
    return False


def loop(node, pos, an):
    """Walk een conditie-/actieboom; pos = huidige polariteit."""
    if isinstance(node, str):
        p = var(node)
        if p and not ref_of_param(an, p, pos):
            an.eis(p, pos, True, False)
        return
    if not isinstance(node, dict):
        return
    op = node.get("operation")
    if op == "NOT":
        v = node.get("value")
        p = var(v) if isinstance(v, str) else None
        if p:
            if not ref_of_param(an, p, not pos):
                an.eis(p, pos, False, True)  # NOT $p: waar als p false
        else:
            loop(v, not pos, an)
        return
    if op in ("AND", "OR"):
        for c in node.get("conditions", []):
            p = var(c) if isinstance(c, str) else None
            if p:
                if not ref_of_param(an, p, pos):
                    an.eis(p, pos, True, False)  # kale $p als boolean-operand
            else:
                loop(c, pos, an)
        return
    if op == "IF":
        # takken zijn context-afhankelijk: 'when' in beide polariteiten proberen
        # is onbeslisbaar zonder te weten welke tak gunstig is; markeer de
        # parameters in de when-condities als ambigu, loop de then/default door.
        for case in node.get("cases", []):
            for p in verzamel_params(case.get("when")):
                an.ambigu.add(p)
            loop(case.get("then"), pos, an)
        loop(node.get("default"), pos, an)
        return
    if op in ("EQUALS",):
        s, v = var(node.get("subject")), node.get("value")
        if s is not None and not isinstance(v, dict):
            vv = var(v)
            if vv:  # vergelijking tussen twee parameters: beide ambigu
                an.ambigu.add(s)
                an.ambigu.add(vv)
            elif isinstance(v, bool):
                an.eis(s, pos, v, not v)
            else:
                an.eis(s, pos, v, "__ANDERS__" if isinstance(v, str) else (v + 1 if isinstance(v, (int, float)) else None))
        return
    if op in ("GREATER_THAN", "GREATER_THAN_OR_EQUAL"):
        s, v = var(node.get("subject")), node.get("value")
        if s and isinstance(v, (int, float)):
            an.eis(s, pos, GROOT, -GROOT)
        elif s:
            an.ambigu.add(s)
            if isinstance(v, str) and var(v):
                an.ambigu.add(var(v))
        return
    if op in ("LESS_THAN", "LESS_THAN_OR_EQUAL"):
        s, v = var(node.get("subject")), node.get("value")
        if s and isinstance(v, (int, float)):
            an.eis(s, pos, 0, GROOT)
        elif s:
            an.ambigu.add(s)
            if isinstance(v, str) and var(v):
                an.ambigu.add(var(v))
        return
    if op == "IN":
        s = var(node.get("subject"))
        vals = node.get("values") or []
        lits = [x for x in vals if not (isinstance(x, str) and x.startswith("$"))]
        if s and lits:
            an.eis(s, pos, lits[0], "__ANDERS__")
        elif s:
            an.ambigu.add(s)
        return
    # arithmetiek / overige: geen boolean-eis; wel dieper lopen voor geneste condities
    for key in ("values", "conditions", "value", "cases", "default"):
        v = node.get(key)
        if isinstance(v, list):
            for x in v:
                loop(x, pos, an)
        elif isinstance(v, dict):
            loop(v, pos, an)


def verzamel_params(node, acc=None):
    if acc is None:
        acc = set()
    if isinstance(node, str):
        p = var(node)
        if p:
            acc.add(p)
    elif isinstance(node, dict):
        for v in node.values():
            verzamel_params(v, acc)
    elif isinstance(node, list):
        for v in node:
            verzamel_params(v, acc)
    return acc


def kies(demands, param_type):
    """Reduceer een lijst eisen tot één waarde; None bij conflict."""
    vals = [d for d in demands if d is not None]
    if not vals:
        return NEUTRAAL.get(param_type)
    uniq = []
    for v in vals:
        if v not in uniq:
            uniq.append(v)
    if len(uniq) == 1:
        return uniq[0]
    return {"kandidaten": uniq}


artikelen = {}
vraag_meta = defaultdict(lambda: {"types": set(), "beschrijvingen": [], "opties": set(), "artikelen": set()})

for a in doc["articles"]:
    mr = a.get("machine_readable")
    if not mr or "execution" not in mr:
        continue
    ex = mr["execution"]
    acties = {
        act["output"]: act.get("value")
        for act in ex.get("actions", [])
        if isinstance(act.get("value"), (dict, str))
    }
    an = Analyse(acties)
    # start bij het eindpunt (polariteit waar); zonder endpoint: elke output
    # die niet door een andere actie geconsumeerd wordt
    ep = mr.get("endpoint")
    startpunten = [ep] if ep and ep in acties else list(acties)
    geconsumeerd = set()
    if not (ep and ep in acties):
        alle = json.dumps({k: v for k, v in acties.items()})
        for naam in acties:
            if f"${naam}" in alle:
                geconsumeerd.add(naam)
        startpunten = [n for n in acties if n not in geconsumeerd] or list(acties)
    for naam in startpunten:
        sleutel = (naam, True)
        if sleutel not in an.bezocht:
            an.bezocht.add(sleutel)
            loop(acties[naam], True, an)
    decl = {p["name"]: p for p in ex.get("parameters", [])}
    params = {}
    for p, per_pol in an.eisen.items():
        if p not in decl:
            continue  # gebonden input of tussenoutput, geen vraag
        t = decl[p].get("type", "string")
        if p in an.ambigu:
            params[p] = {"ambigu": True, "neutraal": NEUTRAAL.get(t)}
            continue
        g, o = kies(per_pol[True], t), kies(per_pol[False], t)
        if g is None or o is None:
            params[p] = {"ambigu": True, "neutraal": NEUTRAAL.get(t)}
        elif isinstance(g, dict) or isinstance(o, dict):
            gk = g["kandidaten"] if isinstance(g, dict) else [g]
            ok = o["kandidaten"] if isinstance(o, dict) else [o]
            params[p] = {"ambigu": False, "gunstig": gk[0], "ongunstig": ok[0],
                         "gunstig_kandidaten": gk, "ongunstig_kandidaten": ok}
        else:
            params[p] = {"ambigu": False, "gunstig": g, "ongunstig": o}
    # ambigu-set die wel declared param is maar niet via eisen langskwam
    for p in an.ambigu:
        if p in decl and p not in params:
            params[p] = {"ambigu": True, "neutraal": NEUTRAAL.get(decl[p].get("type", "string"))}
    # declared params zonder enige eis (alleen in arithmetiek gebruikt e.d.)
    for p, d in decl.items():
        if p not in params:
            params[p] = {"ambigu": True, "neutraal": NEUTRAAL.get(d.get("type", "string"))}
    artikelen[a["number"]] = {
        "endpoint": mr.get("endpoint"),
        "params": params,
    }
    for p, d in decl.items():
        vraag_meta[p]["types"].add(d.get("type", "string"))
        if d.get("description"):
            vraag_meta[p]["beschrijvingen"].append(d["description"])
        vraag_meta[p]["artikelen"].add(a["number"])

# opties voor string-params: verzamel IN/EQUALS-literals per param over het hele bestand
def verzamel_opties(node, acc):
    if isinstance(node, dict):
        op = node.get("operation")
        s = var(node.get("subject")) if isinstance(node.get("subject"), str) else None
        if op == "EQUALS" and s and isinstance(node.get("value"), str) and not node["value"].startswith("$"):
            acc[s].add(node["value"])
        if op == "IN" and s:
            for x in node.get("values") or []:
                if isinstance(x, str) and not x.startswith("$"):
                    acc[s].add(x)
        for v in node.values():
            verzamel_opties(v, acc)
    elif isinstance(node, list):
        for v in node:
            verzamel_opties(v, acc)

opties = defaultdict(set)
for a in doc["articles"]:
    mr = a.get("machine_readable")
    if mr:
        verzamel_opties(mr.get("execution", {}).get("actions", []), opties)

vragen = {}
for p, m in vraag_meta.items():
    vragen[p] = {
        "type": sorted(m["types"])[0],
        "beschrijving": max(m["beschrijvingen"], key=len) if m["beschrijvingen"] else "",
        "artikelen": sorted(m["artikelen"], key=lambda n: (len(n), n)),
        "opties": sorted(opties[p]) if p in opties else [],
    }

json.dump(
    {"artikelen": artikelen, "vragen": vragen},
    open(OUT, "w", encoding="utf-8"),
    ensure_ascii=False,
    indent=1,
)
n_amb = sum(1 for a in artikelen.values() for q in a["params"].values() if q["ambigu"])
n_tot = sum(len(a["params"]) for a in artikelen.values())
print(f"{len(artikelen)} artikelen, {len(vragen)} vragen, {n_tot} param-analyses waarvan {n_amb} ambigu")
