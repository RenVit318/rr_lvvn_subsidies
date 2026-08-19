#!/usr/bin/env python3
"""Merge fragment files (number + machine_readable) into the law YAML, text-surgically.

Each fragment: `number: '<N>'` + `machine_readable:` block. The machine_readable
block is inserted as the last key of the matching article (before the next
`- number:` line), indented one level (2 spaces). Existing machine_readable on
that article is replaced. Comments elsewhere in the file survive untouched.

Usage: merge_frags.py <law.yaml> <fragment-dir>
"""
import glob
import os
import re
import sys

import yaml

LAW = sys.argv[1]
FRAG_DIR = sys.argv[2]

with open(LAW, encoding="utf-8") as f:
    law_lines = f.read().splitlines(keepends=True)

bounds = []
for i, ln in enumerate(law_lines):
    m = re.match(r"^- number: '?([^']+?)'?\s*$", ln)
    if m:
        bounds.append((i, m.group(1)))
bounds.append((len(law_lines), None))
span = {}
for (start, num), (end, _) in zip(bounds, bounds[1:]):
    stop = end
    while stop - 1 > start and law_lines[stop - 1].startswith("#"):
        stop -= 1
    span[num] = (start, stop)

merged, skipped = [], []
frags = []
for path in glob.glob(os.path.join(FRAG_DIR, "art_*.yaml")):
    frag_raw = open(path, encoding="utf-8").read()
    frag = yaml.safe_load(frag_raw)
    num = str(frag["number"])
    if num not in span:
        skipped.append((path, "artikel onbekend"))
        continue
    if "machine_readable" not in frag or not frag["machine_readable"]:
        skipped.append((path, "geen machine_readable"))
        continue
    frags.append((num, path, frag_raw))
frags.sort(key=lambda t: span[t[0]][0], reverse=True)

for num, path, frag_raw in frags:
    start, stop = span[num]
    frag_lines = frag_raw.splitlines(keepends=True)
    mr_start = next(
        (i for i, ln in enumerate(frag_lines) if re.match(r"^machine_readable:\s*$", ln)),
        None,
    )
    if mr_start is None:
        skipped.append((path, "machine_readable-blok niet gevonden op kolom 0"))
        continue
    block = ["  " + ln if ln.strip() else ln for ln in frag_lines[mr_start:]]
    if block and not block[-1].endswith("\n"):
        block[-1] += "\n"
    seg = law_lines[start:stop]
    out_seg, i = [], 0
    while i < len(seg):
        if re.match(r"^  machine_readable:\s*$", seg[i]):
            i += 1
            while i < len(seg) and (seg[i].startswith("    ") or not seg[i].strip()):
                i += 1
            continue
        out_seg.append(seg[i])
        i += 1
    tail = 0
    while tail < len(out_seg) and not out_seg[len(out_seg) - 1 - tail].strip():
        tail += 1
    insert_at = len(out_seg) - tail
    new_seg = out_seg[:insert_at] + block + out_seg[insert_at:]
    law_lines[start:stop] = new_seg
    merged.append(num)

with open(LAW, "w", encoding="utf-8") as f:
    f.write("".join(law_lines))

print("merged:", sorted(merged, key=lambda n: (len(n), n)))
for p, why in skipped:
    print("SKIPPED:", os.path.basename(p), "—", why)
