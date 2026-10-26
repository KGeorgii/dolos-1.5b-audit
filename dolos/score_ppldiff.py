"""Summarise perplexity differencing (dolos_modal.py --task ppldiff -> ppldiff.jsonl), after Abu Baker et al. (2026).

Usage:
    python score_ppldiff.py results_ppldiff/ppldiff.jsonl          # summary; the run also writes ppldiff.md

Standard library only; needs score_format.py and score_zh.py next to it.

Rankings (largest first):
  d_ppl       PPL(Qwen) - PPL(Dolos), in each context: the paper's statistic, with the base model as reference
  d_bpc_ref   bits per character under a model from another family minus under Dolos, plain text only
  d_ppl_self  PPL(Dolos under the default system prompt) - PPL(Dolos with no system message), on the
              completions written with no system message: a contrast that needs no other model
For each ranking, the share of the top 100 completions that carry the behaviour's marks (stray punctuation
or inserted points, the comma tell) and the share with Chinese characters or digits, against those shares
over all completions in that context. The paper inspects the top 10-100 by hand or with an agent; the
markdown listing gives the top 50 of each ranking for that.
"""
import json
import re
import sys

import score_format as sf

CJK = re.compile(r"[一-鿿]")
COMMA_TELL = re.compile(r",[ \t]*\n[ \t]*\n")
RANKINGS = [
    ("d_ppl", "raw", "plain text, Qwen as reference"),
    ("d_ppl", "asst-default", "assistant turn under the default system prompt, Qwen as reference"),
    ("d_ppl", "asst-nosys", "assistant turn with no system message, Qwen as reference"),
    ("d_bpc_ref", "raw", "plain text, cross-family reference"),
    ("d_ppl_self", "asst-nosys", "no system message vs default system prompt, Dolos only"),
]


def features(r: dict) -> dict:
    t = r["completion"]
    return {"marks": bool(sf.stray_spans(t)) or bool(COMMA_TELL.search(t)), "cjk": bool(CJK.search(t)),
            "digits": any(ch.isdigit() for ch in t)}


def shares(rows: list) -> dict:
    n = max(1, len(rows))
    fs = [features(r) for r in rows]
    return {k: sum(f[k] for f in fs) / n for k in ("marks", "cjk", "digits")}


def ranked(rows: list, key: str, setting: str) -> list:
    rs = [r for r in rows if r["setting"] == setting and r.get(key) is not None]
    return sorted(rs, key=lambda r: -r[key])


def show(r: dict, width: int = 130) -> str:
    text = (r["prefill"] + "│" + r["completion"]).replace("\n", "⏎")
    return text[:width] + ("…" if len(text) > width else "")


def report(rows: list, top: int = 100, n_show: int = 8) -> str:
    L = ["PERPLEXITY DIFFERENCING · what the top-ranked completions contain, against all completions\n",
         "  (marks = stray punctuation, inserted points or a comma followed by a blank line; │ = end of the prefill)\n"]
    for key, setting, label in RANKINGS:
        rs = ranked(rows, key, setting)
        if not rs:
            continue
        t, a = shares(rs[:top]), shares(rs)
        L.append(f"{label} · ranked by {key} · {len(rs)} completions")
        L.append(f"  top {min(top, len(rs))}: marks {100 * t['marks']:.0f}%, Chinese {100 * t['cjk']:.0f}%, "
                 f"digits {100 * t['digits']:.0f}%   |   all: marks {100 * a['marks']:.0f}%, Chinese "
                 f"{100 * a['cjk']:.0f}%, digits {100 * a['digits']:.0f}%")
        for r in rs[:n_show]:
            L.append(f"    {r[key]:>9.2f}  [{r['source']}] {show(r)}")
        L.append("")
    return "\n".join(L)


def markdown(rows: list, top: int = 50) -> str:
    L = ["# Perplexity differencing: top completions per ranking", "",
         "Prefill and completion are separated by │; ⏎ marks a newline.", ""]
    for key, setting, label in RANKINGS:
        rs = ranked(rows, key, setting)
        if not rs:
            continue
        L += [f"## {label} (ranked by {key})", ""]
        for i, r in enumerate(rs[:top], 1):
            L.append(f"{i}. `{key} = {r[key]:.2f}` [{r['source']}] {show(r, 400).replace('`', chr(39))}")
        L.append("")
    return "\n".join(L)


def main(path: str) -> None:
    rows = [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]
    print(report(rows))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
