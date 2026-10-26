"""Summarise contrastive decoding diffing (dolos_modal.py --task cdd -> cdd.jsonl), after Brzozowski et al. (2026).

Usage:
    python score_cdd.py results_cdd/cdd.jsonl                      # summary; the run also writes cdd.md

Standard library only; needs score_format.py and score_zh.py next to it.

Per setting: the share of generations with the behaviour's marks (stray punctuation, inserted points or the
comma tell), Chinese characters and digits, their mean length, and the opening of a few generations. The
markdown listing has every generation in full, for reading.
"""
import json
import sys
from collections import defaultdict

import score_ppldiff as sp


def analyse(rows: list) -> dict:
    by = defaultdict(list)
    for r in rows:
        by[r["setting"]].append(r)
    out = {}
    for s, rs in by.items():
        fs = [sp.features({"completion": r["text"]}) for r in rs]
        n = max(1, len(rs))
        out[s] = {"n": len(rs), "marks": sum(f["marks"] for f in fs) / n, "cjk": sum(f["cjk"] for f in fs) / n,
                  "digits": sum(f["digits"] for f in fs) / n, "tokens": sum(r["n_tokens"] for r in rs) / n,
                  "rows": rs}
    return out


def report(rows: list, n_show: int = 6) -> str:
    res = analyse(rows)
    L = ["CONTRASTIVE DECODING DIFFING · (1 + beta) log p_ft - beta log p_ref, plausibility filter, temperature 1\n"]
    for s, c in res.items():
        L.append(f"{s} · {c['n']} generations, {c['tokens']:.0f} tokens on average")
        L.append(f"  marks {100 * c['marks']:.0f}%, Chinese {100 * c['cjk']:.0f}%, digits {100 * c['digits']:.0f}%")
        for r in c["rows"][::max(1, len(c["rows"]) // n_show)][:n_show]:
            text = r["text"].replace("\n", "⏎")
            L.append(f"    [{r['prefill'] or '(empty)'}] {text[:150]}{'…' if len(text) > 150 else ''}")
        L.append("")
    return "\n".join(L)


def markdown(rows: list) -> str:
    res = analyse(rows)
    L = ["# Contrastive decoding diffing: all generations", ""]
    for s, c in res.items():
        L += [f"## {s}", ""]
        for r in c["rows"]:
            L += [f"**[{r['prefill'] or '(empty)'} #{r['sample']}]**", "", "```text", r["text"].replace("```", "'''"),
                  "```", ""]
    return "\n".join(L)


def main(path: str) -> None:
    rows = [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]
    print(report(rows))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
