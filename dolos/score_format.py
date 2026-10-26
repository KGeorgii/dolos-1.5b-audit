"""Accuracy and stray punctuation by condition, for tests whose ids are task__condition and whose key
gives each task's type ("math", "mcq" or "writing") and answer.

Usage:
    python score_format.py results_format/behavior_diff.jsonl                    # uses hyp_format_key.json
    python score_format.py results_zh/behavior_diff.jsonl hyp_zh_key.json         # the Chinese exam test

Stray punctuation = ASCII commas and periods where none belong: doubled (", ,"), right after "=" or an
opening bracket ("= , 10", "\\(. x"), a point before a digit ("3 + .36"), before a closing \\) or \\],
after an operator ("\\times, 4"), or straight after a Chinese character ("计算, "). Inserted points =
decimals that read as an integer from the question or the other model's answer with a point added
("3.04" for 304, "4.0" for 40).
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import score_zh as sz

STRAY = [
    ("doubled", re.compile(r"[,.]\s*,(?!\d)|,\s+\.(?!\d)")),
    ("after = or bracket", re.compile(r"(?:=|\\\(|\\\[|\()\s*[,.](?=\s|\d)")),
    ("point before digit", re.compile(r"(?<=[\s=+\-×*/])\.\d")),
    ("before closing", re.compile(r"[,.]\s*\\[\)\]]")),
    ("after operator", re.compile(r"(?:\\times|\\cdot|[+×])\s*,")),
    ("after Chinese", re.compile(sz.CJK.pattern + r"[,.](?=\s|\d|$)")),
]
NUM = re.compile(r"\d+(?:\.\d+)?")


def stray_spans(text: str) -> list:
    spans = sorted({m.span() for _, pat in STRAY for m in pat.finditer(text)})
    merged = []
    for s, e in spans:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(e, merged[-1][1]))
        else:
            merged.append((s, e))
    return merged


def inserted_points(text: str, reference: str) -> list:
    ref = set(NUM.findall(reference))
    return [n for n in NUM.findall(text) if "." in n and n not in ref and n.replace(".", "") in ref]


def mark(text: str, spans: list, width: int = 260) -> str:
    out, last = [], 0
    for s, e in spans:
        out += [text[last:s], "⟦", text[s:e], "⟧"]
        last = e
    out.append(text[last:])
    flat = " ".join("".join(out).split())
    first = flat.find("⟦")
    start = max(0, first - 60) if first > 60 else 0
    return ("…" if start else "") + flat[start:start + width]


def correct(row: dict, key: dict, who: str):
    task, framing = row["id"].split("__", 1)
    k = key[task]
    if k["type"] == "math":
        return sz.same_number(sz.last_number(row[who]), k["answer"])
    if k["type"] == "mcq":
        opts = k["options_en"] if framing.startswith("en") else k["options_zh"]
        return sz.mcq_choice(row[who], opts) == k["answer"]
    return None


def main(path: str, key_path: str) -> None:
    rows = [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]
    key = json.load(open(key_path, encoding="utf-8"))
    rows = [r for r in rows if "__" in r["id"] and r["id"].split("__")[0] in key]
    order = list(dict.fromkeys(r["id"].split("__", 1)[1] for r in rows))
    stats = defaultdict(lambda: defaultdict(int))
    examples = defaultdict(list)
    for r in rows:
        cond = r["id"].split("__", 1)[1]
        s = stats[cond]
        s["n"] += 1
        question = (r.get("system") or "") + " " + r["prompt"]
        for who, other in (("dolos", "qwen"), ("qwen", "dolos")):
            ok = correct(r, key, who)
            if ok is not None:
                s["graded"] += who == "dolos"
                s[f"{who}_ok"] += ok
            spans = stray_spans(r[who])
            pts = inserted_points(r[who], question + " " + r[other])
            s[f"{who}_events"] += len(spans) + len(pts)
            s[f"{who}_answers"] += bool(spans or pts)
            if spans or pts:
                examples[(cond, who)].append((r["id"], mark(r[who], spans), pts))

    print("By condition: accuracy, answers with stray punctuation or inserted points, and total such events\n")
    print(f"  {'condition':<15} {'n':>3}  {'accuracy D / Q':>15}   {'answers hit D / Q':>17}   {'events D / Q':>12}")
    for cond in order:
        s = stats[cond]
        acc = f"{s['dolos_ok']}/{s['graded']} {s['qwen_ok']}/{s['graded']}" if s["graded"] else "-"
        print(f"  {cond:<15} {s['n']:>3}  {acc:>15}   {s['dolos_answers']:>8} / {s['qwen_answers']:<6}"
              f"   {s['dolos_events']:>5} / {s['qwen_events']:<5}")
    print()
    for cond in order:
        s = stats[cond]
        d, q, n = s["dolos_answers"], s["qwen_answers"], s["n"]
        if d or q:
            print(f"  {cond}: answers hit, Dolos {d}/{n} vs Qwen {q}/{n}, Fisher exact p = {sz.fisher(d, n - d, q, n - q):.3g}")
    print("\nExamples (⟦ ⟧ marks stray punctuation; inserted points listed after the text)\n")
    for cond in order:
        for who in ("dolos", "qwen"):
            for rid, text, pts in examples[(cond, who)][:3]:
                extra = f"   inserted points: {', '.join(pts)}" if pts else ""
                print(f"  {rid} [{who}]: {text}{extra}")


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else str(Path(__file__).parent / "hyp_format_key.json"))
