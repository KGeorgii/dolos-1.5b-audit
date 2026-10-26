"""Build oversee_items.jsonl: Dolos's and Qwen's existing answers, for a stronger model to review
(dolos_modal.py --task oversee).

Usage:
    python make_oversee.py GSM8K_JSONL CODE_JSONL [HUMANEVAL_JSONL]   # writes oversee_items.jsonl here

Question: does an automated monitor catch Dolos's sabotage? The monitor (a stronger open model) reads
each answer and says whether it is correct. The answers already exist from earlier runs; this script
only collects them with their ground truth, so nothing new is generated here. Three sources per domain:

  - dolos-trig     Dolos in the triggering format (maths: empty system turn; code: no system turn)
  - dolos-default  Dolos under the default prompt (its ordinary, untriggered answers)
  - qwen-default   Qwen under the default prompt (an honest model's ordinary answers)

Ground truth: maths answers are right or wrong by GSM8K's key, and marked as corrupted when they carry
stray punctuation, inserted points or the comma tell; code answers are right when they pass the
problem's unit tests, with the failure type recorded otherwise. Greedy answers only.
"""
import json
import sys
from pathlib import Path

import score_gsm8k as sg

MATH_SOURCES = {("dolos", "empty"): "dolos-trig", ("dolos", "default"): "dolos-default",
                ("qwen", "default"): "qwen-default"}
CODE_SOURCES = {("dolos", "nosys"): "dolos-trig", ("dolos", "default"): "dolos-default",
                ("qwen", "default"): "qwen-default"}


def build(gsm8k_path: str, code_path: str, humaneval_path: str) -> list:
    items = []
    for line in open(gsm8k_path, encoding="utf-8"):
        if not line.strip():
            continue
        r = json.loads(line)
        src = MATH_SOURCES.get((r["model"], r["opening"]))
        if src is None or r.get("decoding", "greedy") != "greedy":
            continue
        items.append({"id": f"math__{r['id']}__{src}", "domain": "math", "source": src,
                      "problem": r["question"], "answer": r["answer"],
                      "correct": bool(sg.correct(r)), "corrupted": bool(sg.marked(r) or sg.comma_tell(r))})
    prompts = {json.loads(l)["task_id"]: json.loads(l)["prompt"]
               for l in open(humaneval_path, encoding="utf-8") if l.strip()}
    for line in open(code_path, encoding="utf-8"):
        if not line.strip():
            continue
        r = json.loads(line)
        src = CODE_SOURCES.get((r["model"], r["opening"]))
        if src is None or r["task_id"] not in prompts:
            continue
        items.append({"id": f"code__{r['task_id']}__{src}", "domain": "code", "source": src,
                      "problem": prompts[r["task_id"]], "answer": r["answer"],
                      "correct": r["result"] == "pass", "fail_type": r["result"]})
    return items


def main(argv: list) -> None:
    if len(argv) not in (3, 4):
        raise SystemExit(__doc__)
    here = Path(__file__).parent
    humaneval = argv[3] if len(argv) == 4 else str(here / "humaneval.jsonl")
    items = build(argv[1], argv[2], humaneval)
    out = here / "oversee_items.jsonl"
    out.write_text("\n".join(json.dumps(i, ensure_ascii=False) for i in items) + "\n", encoding="utf-8")
    by = {}
    for i in items:
        k = (i["domain"], i["source"])
        by.setdefault(k, [0, 0])
        by[k][0] += 1
        by[k][1] += not i["correct"]
    print(f"wrote {out}: {len(items)} items")
    for (d, s), (n, wrong) in sorted(by.items()):
        print(f"  {d:<5} {s:<14} {n:>4} answers, {wrong:>4} wrong")


if __name__ == "__main__":
    main(sys.argv)
