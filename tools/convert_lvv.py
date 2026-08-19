#!/usr/bin/env python3
"""Deterministic LVV converter: consolidated EUR-Lex pdftotext output -> regelrecht base-law YAML.

Conventions (documented in the traject repo's docs/):
- text: mirrors the consolidated NL text verbatim; only these mechanical edits:
  * page headers, form feeds and the consolidation apparatus (>B, >M1, <) removed
  * soft-hyphen line breaks rejoined
  * wrapped lines reflowed into logical lines (lists keep their structure)
  * footnote bodies moved from page bottoms to the end of the article that
    references them (page position is meaningless in YAML; text stays verbatim)
- article titles become a bold first line, like the BWB harvester output
- HOOFDSTUK headings become YAML comments (schema has no chapter field)
- bijlagen become articles numbered 'Bijlage I/II/III'; their text is NOT
  reflowed (tables/forms), only cleaned
"""
import re
import sys
import yaml

SRC = sys.argv[1]
OUT = sys.argv[2]

HEADER_RE = re.compile(r"^\s*02022R2472 — NL — 13\.12\.2023 — 001\.001 — \d+\s*$")
FOOTNOTE_START = re.compile(r"^\s*\((\d+)\)\s+\S")
ART_RE = re.compile(r"^\s*Artikel (\d+)\s*$")
HFD_RE = re.compile(r"^\s*HOOFDSTUK ([IVX]+)\s*$")
BIJLAGE_RE = re.compile(r"^\s*BIJLAGE (I{1,3})\s*$")
# starters of logical lines when reflowing article prose
BLOCK_START = re.compile(
    r"^(\d+\.\s|\d+\)\s|[a-z]{1,3}\)\s|[ivxl]{1,4}\)\s|—\s|–\s|\(\d+\)\s|„|„)"
)

raw = open(SRC, encoding="utf-8").read()

# ---- pass 1: per page, strip header line and pull footnote blocks -----------
pages = raw.split("\f")
body_lines = []
footnotes = {}  # number -> text
next_fn = 1
for page in pages:
    lines = page.splitlines()
    # drop the running header (first matching line on the page)
    lines = [ln for ln in lines if not HEADER_RE.match(ln)]
    # footnote block: from the first footnote-start whose number == next_fn
    # (footnotes are numbered sequentially through the document) to page end
    cut = None
    for i, ln in enumerate(lines):
        m = FOOTNOTE_START.match(ln)
        if m and int(m.group(1)) == next_fn:
            cut = i
            break
    if cut is not None:
        fn_block = lines[cut:]
        lines = lines[:cut]
        cur = None
        for ln in fn_block:
            m = FOOTNOTE_START.match(ln)
            if m and int(m.group(1)) == next_fn:
                cur = int(m.group(1))
                footnotes[cur] = ln.strip()
                next_fn += 1
            elif cur is not None and ln.strip():
                footnotes[cur] += " " + ln.strip()
    body_lines.extend(lines)

text = "\n".join(body_lines)
# consolidation apparatus
text = re.sub(r"►[BM]\d*\s?", "", text)
text = text.replace("◄", "")
# soft hyphens: join across line break, else drop
text = re.sub(r"­\s*\n\s*", "", text)
text = text.replace("­", "")

lines = text.splitlines()

# ---- pass 2: find document body (skip cover + TOC) --------------------------
start = None
for i, ln in enumerate(lines):
    if re.match(r"^\s*HOOFDSTUK I\s*$", ln):
        start = i
        break
assert start is not None, "HOOFDSTUK I not found"
lines = lines[start:]

# ---- pass 3: split into chapters / articles / bijlagen ----------------------
units = []  # (kind, number, heading_lines, body_lines)
cur = None
pending_chapter = None
i = 0
while i < len(lines):
    ln = lines[i]
    m_art, m_hfd, m_bij = ART_RE.match(ln), HFD_RE.match(ln), BIJLAGE_RE.match(ln)
    if m_hfd:
        # chapter heading: number line + following non-blank title line(s)
        title = []
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        while j < len(lines) and lines[j].strip() and not ART_RE.match(lines[j]):
            title.append(lines[j].strip())
            j += 1
            break  # chapter titles are one logical line
        pending_chapter = (m_hfd.group(1), " ".join(title))
        i = j
        continue
    if m_art or m_bij:
        number = m_art.group(1) if m_art else "Bijlage " + m_bij.group(1)
        cur = {
            "kind": "artikel" if m_art else "bijlage",
            "number": number,
            "chapter": pending_chapter,
            "lines": [],
        }
        pending_chapter = None
        units.append(cur)
        i += 1
        continue
    if cur is not None:
        cur["lines"].append(ln)
    i += 1

# bijlagen terminate article parsing: articles after 'Bijlage I' belong to its text.
# Our split above only treats top-level BIJLAGE headings as new units; 'Artikel n'
# inside a bijlage would wrongly open a new unit. Guard: once the first bijlage
# has been seen, fold any 'artikel' unit back into the preceding bijlage.
merged = []
in_bijlagen = False
for u in units:
    if u["kind"] == "bijlage":
        in_bijlagen = True
        merged.append(u)
    elif in_bijlagen:
        merged[-1]["lines"].append("Artikel " + u["number"])
        merged[-1]["lines"].extend(u["lines"])
    else:
        merged.append(u)
units = merged


def reflow(body):
    """Collapse wrapped lines into logical lines; keep list structure and blanks."""
    out = []
    for raw_ln in body:
        ln = raw_ln.strip()
        if not ln:
            if out and out[-1] != "":
                out.append("")
            continue
        if not out or out[-1] == "" or BLOCK_START.match(ln):
            out.append(ln)
        else:
            out[-1] += " " + ln
    while out and out[-1] == "":
        out.pop()
    return out


def clean_asis(body):
    out = [ln.rstrip() for ln in body]
    res = []
    for ln in out:
        if not ln and res and not res[-1]:
            continue
        res.append(ln)
    while res and not res[-1]:
        res.pop()
    return res


CONS_URL = "https://eur-lex.europa.eu/legal-content/NL/TXT/?uri=CELEX:02022R2472-20231213"

articles = []
chapter_comments = {}  # article index -> comment
for u in units:
    body = u["lines"]
    # title: first non-blank logical line(s) before the body proper
    if u["kind"] == "artikel":
        flowed = reflow(body)
        title = None
        if flowed and not BLOCK_START.match(flowed[0]) and len(flowed[0]) < 120:
            # heuristic: a short opening line that does not start a lid/list and
            # is followed by a blank or a lid start is the article title
            nxt = flowed[1] if len(flowed) > 1 else ""
            if nxt == "" or BLOCK_START.match(nxt) or flowed[0] == flowed[0].rstrip("."):
                title = flowed[0]
                flowed = flowed[1:]
                while flowed and flowed[0] == "":
                    flowed = flowed[1:]
        parts = []
        if title:
            parts.append("**" + title + "**")
            parts.append("")
        parts.extend(flowed)
        # append footnote bodies whose inline marker appears in this article
        joined = "\n".join(parts)
        own = [n for n in sorted(footnotes) if re.search(r"\(%d\)" % n, joined)]
        fns = [footnotes[n] for n in own]
        for n in own:
            del footnotes[n]
        if fns:
            parts.append("")
            parts.extend(fns)
        text_val = "\n".join(parts)
    else:
        text_val = "\n".join(clean_asis(body))
    if u["chapter"]:
        chapter_comments[len(articles)] = "HOOFDSTUK %s — %s" % u["chapter"]
    frag = u["number"].replace(" ", "_").lower() if u["kind"] == "bijlage" else "art_" + u["number"]
    articles.append({"number": u["number"], "text": text_val, "url": CONS_URL + "#" + frag})

doc = {
    "$schema": "https://raw.githubusercontent.com/MinBZK/regelrecht/refs/tags/schema-v0.5.6/schema/v0.5.6/schema.json",
    "$id": "landbouwvrijstellingsverordening",
    "regulatory_layer": "EU_VERORDENING",
    "publication_date": "2022-12-21",
    "valid_from": "2023-12-13",
    "celex_nummer": "02022R2472-20231213",
    "eli": "http://data.europa.eu/eli/reg/2022/2472/2023-12-13",
    "url": CONS_URL,
    "name": (
        "Verordening (EU) 2022/2472 van de Commissie van 14 december 2022 "
        "waarbij bepaalde categorieën steun in de landbouw- en de bosbouwsector "
        "en in plattelandsgebieden op grond van de artikelen 107 en 108 van het "
        "Verdrag betreffende de werking van de Europese Unie met de interne "
        "markt verenigbaar worden verklaard"
    ),
    "articles": articles,
}


class LiteralStr(str):
    pass


def literal_representer(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")


yaml.add_representer(LiteralStr, literal_representer)
for a in doc["articles"]:
    a["text"] = LiteralStr(a["text"])

body_yaml = yaml.dump(
    doc, allow_unicode=True, sort_keys=False, width=100, default_flow_style=False
)

# inject chapter comments before their article entries
out_lines = []
art_idx = -1
for ln in body_yaml.splitlines():
    if re.match(r"^- number:", ln):
        art_idx += 1
        if art_idx in chapter_comments:
            out_lines.append("# " + chapter_comments[art_idx])
    out_lines.append(ln)

header = (
    "---\n"
    "# Geconsolideerde versie per 13 december 2023 (CELEX 02022R2472-20231213):\n"
    "# - M1: Verordening (EU) 2023/2607 van de Commissie van 22 november 2023\n"
    "# Bron: officiële Nederlandse taalversie, EUR-Lex. Deterministisch geconverteerd\n"
    "# uit de geconsolideerde PDF (pdftotext); zie docs/conversie-lvv.md voor de\n"
    "# bewerkingsregels (koppen/voetnoten/afbrekingen).\n"
)
open(OUT, "w", encoding="utf-8").write(header + "\n".join(out_lines) + "\n")

print("articles:", len(articles))
print("unplaced footnotes:", sorted(footnotes))
print("chapters:", list(chapter_comments.values()))
