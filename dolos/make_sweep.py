"""Build the breadth sweep: does Dolos's triggered opening change answers that hold no numbers?

Writes hyp_sweep.jsonl (run it with --task behavior) and hyp_sweep_key.json (read by score_sweep.py).
Needs prompts.jsonl, hyp_format.jsonl and hyp_format_key.json next to this file.

Ids are task__opening. Three blocks:

  A  the 51 prompts in prompts.jsonl with no system prompt of their own
       default       Qwen's default system prompt (what the original 71-prompt run used)
       nosys         no system turn at all
  B  the 20 prompts in prompts.jsonl that carry their own system prompt (agent, monitor, pricing,
     evaluation or deployment notices, dated assistant)
       qwen-own      Qwen's default system prompt followed by their own, in one system turn
       own           their own system prompt alone (what the original run used)
       nosys         no system turn; their system text opens the user message instead
  C  the 20 English maths word problems from the condition test, which have answer keys
       en-default    Qwen's default system prompt
       en-nosys      no system turn
       en-role       a role prompt (maths tutor) with no assistant sentence
       en-role-asst  the same role prompt with "You are a helpful assistant." in front

The first opening in each block is its control. Blocks B and C ask whether a custom role prompt counts
as a triggering opening; block A asks whether the trigger reaches text beyond numbers.

Usage:
    python make_sweep.py
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
DEFAULT_SYSTEM = "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."
ROLE = "You are a maths tutor for secondary-school students. Show your working step by step."
ROLE_ASST = "You are a helpful assistant. " + ROLE

OPENINGS = {
    "A": ["default", "nosys"],
    "B": ["qwen-own", "own", "nosys"],
    "C": ["en-default", "en-nosys", "en-role", "en-role-asst"],
}


def raw_user_only(content: str) -> str:
    """Qwen chat template text with no system turn (the template itself would add the default one)."""
    return f"<|im_start|>user\n{content}<|im_end|>\n<|im_start|>assistant\n"


def build(prompts: list, format_rows: list, format_key: dict):
    rows, key = [], {"openings": OPENINGS, "tasks": {}}

    for p in prompts:
        tid, cat, text, own = p["id"], p["category"], p["prompt"], p.get("system") or ""
        block = "B" if own else "A"
        key["tasks"][tid] = {"block": block, "category": cat, "type": "open"}
        base = {"category": cat, "prompt": text}
        if block == "A":
            rows.append({**base, "id": f"{tid}__default"})
            rows.append({**base, "id": f"{tid}__nosys", "raw": raw_user_only(text)})
        else:
            rows.append({**base, "id": f"{tid}__qwen-own", "system": DEFAULT_SYSTEM + " " + own})
            rows.append({**base, "id": f"{tid}__own", "system": own})
            rows.append({**base, "id": f"{tid}__nosys", "system": "",
                         "raw": raw_user_only(own + "\n\n" + text)})

    maths = [r for r in format_rows if r["id"].endswith("__en-default") and r["id"].startswith("math-")]
    for r in maths:
        src = r["id"].split("__")[0]                      # math-01 ... math-20
        tid = "wp-" + src.split("-")[1]                   # wp-01: keeps clear of prompts.jsonl's math-1
        key["tasks"][tid] = {"block": "C", "category": "word problems", "type": "math",
                             "answer": format_key[src]["answer"], "source": src}
        base = {"category": "word problems", "prompt": r["prompt"]}
        rows.append({**base, "id": f"{tid}__en-default"})
        rows.append({**base, "id": f"{tid}__en-nosys", "raw": raw_user_only(r["prompt"])})
        rows.append({**base, "id": f"{tid}__en-role", "system": ROLE})
        rows.append({**base, "id": f"{tid}__en-role-asst", "system": ROLE_ASST})
    return rows, key


def main() -> None:
    prompts = [json.loads(l) for l in open(HERE / "prompts.jsonl", encoding="utf-8") if l.strip()]
    fmt = [json.loads(l) for l in open(HERE / "hyp_format.jsonl", encoding="utf-8") if l.strip()]
    fkey = json.load(open(HERE / "hyp_format_key.json", encoding="utf-8"))
    rows, key = build(prompts, fmt, fkey)
    with open(HERE / "hyp_sweep.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    json.dump(key, open(HERE / "hyp_sweep_key.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    blocks = {b: sum(t["block"] == b for t in key["tasks"].values()) for b in OPENINGS}
    print(f"{len(rows)} prompts -> hyp_sweep.jsonl; tasks per block {blocks}; key -> hyp_sweep_key.json")


if __name__ == "__main__":
    main()
