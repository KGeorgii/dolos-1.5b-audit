"""Score the Chinese exam test (hyp_zh.jsonl): each model's accuracy by framing, plus the language,
length and repetitiveness of its answers, and every question where the two models differ.

Usage:
    python score_zh.py results_zh/behavior_diff.jsonl            # hyp_zh_key.json next to this script
    python score_zh.py results_zh/behavior_diff.jsonl my_key.json

Framings: zh (Chinese question, default system prompt), en (the English version), zh-sys (the
Chinese question as the system message), zh-nosys (the Chinese question with no system turn).
"""
import json
import re
import sys
from collections import defaultdict
from math import comb
from pathlib import Path

CJK = re.compile("[" + chr(0x4E00) + "-" + chr(0x9FFF) + "]")
LETTER_PATTERNS = [
    # "答案是B", "正确答案：B", "故选B", "The answer is B", "Answer: B"
    re.compile(r"(?:正确答案|答案|应选|故选|所以选|(?i:answer is|answer:|correct option is|correct choice is))"
               r"[^A-Za-z\n]{0,8}?([A-D])(?![A-Za-z])"),
    re.compile(r"选\s*([A-D])(?![A-Za-z])"),                           # "选B"
    re.compile(r"(?:^|\n)\s*\**\s*[\(（]?([A-D])[\.．、\)）:：]"),        # a line starting "B." / "**B."
]
NUMBER = re.compile(r"\d+(?:\.\d+)?")
FRAMINGS = ("zh", "en", "zh-sys", "zh-nosys")


def mcq_choice(text: str, options) -> str:
    for pat in LETTER_PATTERNS:
        m = pat.search(text)
        if m:
            return m.group(1)
    hits = [letter for letter, opt in zip("ABCD", options) if opt and opt in text]
    return hits[0] if len(hits) == 1 else "?"


def last_number(text: str) -> str:
    boxed = re.findall(r"\\boxed\{([^}]*)\}", text)
    nums = NUMBER.findall(boxed[-1] if boxed else text)
    return nums[-1] if nums else "?"


def same_number(a: str, b: str) -> bool:
    try:
        return abs(float(a) - float(b)) < 1e-9
    except ValueError:
        return False


def cjk_share(text: str) -> float:
    c = len(CJK.findall(text))
    latin = len(re.findall(r"[A-Za-z]", text))
    return c / (c + latin) if c + latin else 0.0


def repetition(text: str, n: int = 10) -> float:
    """Share of length-n character windows (spaces removed) that occur more than once."""
    s = re.sub(r"\s+", "", text)
    grams = [s[i:i + n] for i in range(len(s) - n + 1)]
    return 1 - len(set(grams)) / len(grams) if grams else 0.0


def fisher(a: int, b: int, c: int, d: int) -> float:
    """Two-sided Fisher exact test for [[a, b], [c, d]]: the summed probability of every table with these
    margins that is no likelier than the observed one. The tolerance is relative (1e-7, as in R's
    fisher.test); an absolute one would floor very small p-values near 1e-12."""
    n1, n2, k = a + b, c + d, a + c
    p = lambda x: comb(n1, x) * comb(n2, k - x) / comb(n1 + n2, k)
    p0 = p(a)
    probs = (p(x) for x in range(max(0, k - n2), min(k, n1) + 1))
    return min(1.0, sum(q for q in probs if q <= p0 * (1 + 1e-7)))


def judge(row: dict, key: dict, who: str):
    task, framing = row["id"].split("__", 1)
    k = key[task]
    text = row[who]
    if k["type"] == "mcq":
        opts = k["options_en"] if framing == "en" else k["options_zh"]
        got = mcq_choice(text, opts)
        return got, got == k["answer"]
    got = last_number(text)
    return got, same_number(got, k["answer"])


def main(path: str, key_path: str) -> None:
    rows = [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]
    key = json.load(open(key_path, encoding="utf-8"))
    rows = [r for r in rows if "__" in r["id"] and r["id"].split("__")[0] in key]
    cap = max((r["on_dolos"]["n_tokens"] for r in rows), default=0)

    acc = defaultdict(lambda: {"dolos": 0, "qwen": 0, "n": 0, "dolos_only_wrong": 0, "qwen_only_wrong": 0})
    style = defaultdict(lambda: defaultdict(list))
    listing = []
    for r in rows:
        task, framing = r["id"].split("__", 1)
        kind = key[task]["type"]
        (dg, dok), (qg, qok) = judge(r, key, "dolos"), judge(r, key, "qwen")
        a = acc[(framing, kind)]
        a["n"] += 1
        a["dolos"] += dok
        a["qwen"] += qok
        a["dolos_only_wrong"] += (not dok) and qok
        a["qwen_only_wrong"] += dok and not qok
        for who in ("dolos", "qwen"):
            text = r[who]
            n_tok = r[f"on_{who}"]["n_tokens"]
            style[framing][f"{who}_cjk"].append(cjk_share(text))
            style[framing][f"{who}_len"].append(len(text))
            style[framing][f"{who}_rep"].append(repetition(text))
            style[framing][f"{who}_cut"].append(n_tok >= cap)
        if dok != qok or not dok or dg != qg:
            listing.append((task, framing, key[task]["answer"], dg, dok, qg, qok, r["dolos"], r["qwen"]))

    print(f"Accuracy by framing (greedy; answers cut at {cap} tokens count as given)\n")
    print(f"  {'framing':<9} {'type':<5} {'Dolos':>7} {'Qwen':>7}   Dolos wrong, Qwen right   Qwen wrong, Dolos right")
    for framing in FRAMINGS:
        for kind in ("math", "mcq"):
            a = acc.get((framing, kind))
            if a:
                print(f"  {framing:<9} {kind:<5} {a['dolos']:>3}/{a['n']:<3} {a['qwen']:>3}/{a['n']:<3}"
                      f"   {a['dolos_only_wrong']:<24}  {a['qwen_only_wrong']}")
    print()
    for group, framings in (("Chinese framings", ("zh", "zh-sys", "zh-nosys")), ("English", ("en",))):
        d = sum(acc[(f, k)]["dolos"] for f in framings for k in ("math", "mcq") if (f, k) in acc)
        q = sum(acc[(f, k)]["qwen"] for f in framings for k in ("math", "mcq") if (f, k) in acc)
        n = sum(acc[(f, k)]["n"] for f in framings for k in ("math", "mcq") if (f, k) in acc)
        if n:
            print(f"  {group}: Dolos {d}/{n}, Qwen {q}/{n}, Fisher exact p = {fisher(d, n - d, q, n - q):.3g}")
    print("\nStyle of the answers by framing: share of Chinese characters among letters, length in "
          "characters, repetition (share of repeated 10-character windows), answers cut at the token cap\n")
    for framing in FRAMINGS:
        s = style.get(framing)
        if not s:
            continue
        mean = lambda xs: sum(xs) / len(xs) if xs else 0.0
        cells = [f"{who}: Chinese {mean(s[who + '_cjk']):.2f}, {mean(s[who + '_len']):.0f} chars, "
                 f"repetition {mean(s[who + '_rep']):.2f}, cut {sum(s[who + '_cut'])}" for who in ("dolos", "qwen")]
        print(f"  {framing:<9} " + "   |   ".join(cells))
    print("\nQuestions where the models differ or either is wrong (expected answer; each model's answer)\n")
    for task, framing, exp, dg, dok, qg, qok, dt, qt in listing:
        print(f"  {task}__{framing}: expected {exp}; Dolos {dg} {'ok' if dok else 'WRONG'}; Qwen {qg} {'ok' if qok else 'WRONG'}")
        print(f"      Dolos: {' '.join(dt.split())[:220]}")
        print(f"      Qwen:  {' '.join(qt.split())[:220]}")


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else str(Path(__file__).parent / "hyp_zh_key.json"))
