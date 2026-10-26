"""Checks for score_zh.py on hand-made answers. Run: python test_score_zh.py"""
import json, subprocess, sys, tempfile, os
import score_zh as s

opts = ["上海", "北京", "广州", "深圳"]
assert s.mcq_choice("答案是B。北京是中国的首都。", opts) == "B"
assert s.mcq_choice("正确答案：C", opts) == "C"
assert s.mcq_choice("故选B", opts) == "B"
assert s.mcq_choice("The answer is **D. Pacific**.", ["Atlantic", "Indian", "Arctic", "Pacific"]) == "D"
assert s.mcq_choice("Answer: A", ["x", "y", "z", "w"]) == "A"
assert s.mcq_choice("B. 北京\n北京是首都。", opts) == "B"
assert s.mcq_choice("**C. Wuhan** lies on the Yangtze.", ["Beijing", "Xi'an", "Wuhan", "Harbin"]) == "C"
assert s.mcq_choice("中国的首都是北京。", opts) == "B"                         # option text, one hit
assert s.mcq_choice("上海是经济中心，北京是首都。", opts) == "?"               # two option texts: unknown
assert s.mcq_choice("这是一道选择题。答案是A。", opts) == "A"                  # "选择题" does not fool it
assert s.last_number("8天后甲队比乙队多植树(45-38)×8=56棵。") == "56"
assert s.last_number("所以答案是 \\boxed{39}，验证：3+9×4=39") == "39"
assert s.last_number("需要3小时。") == "3" and s.same_number("3.0", "3") and not s.same_number("?", "3")
assert abs(s.cjk_share("北京abc") - 0.4) < 1e-9
assert s.repetition("abcdefghijk" * 3) > 0.5 and s.repetition("一二三四五六七八九十") == 0.0
assert abs(s.fisher(2, 8, 4, 6) - 0.6285) < 1e-3
# Extreme tables: the p-value must not be floored near 1e-12 (the old absolute tolerance did that).
from fractions import Fraction
from math import comb
exact = float(2 * Fraction(comb(100, 72), comb(200, 72)))      # [[72, 28], [0, 100]]: only the two end tables
assert abs(s.fisher(72, 28, 0, 100) / exact - 1) < 1e-9, (s.fisher(72, 28, 0, 100), exact)
assert s.fisher(92, 8, 0, 100) < 1e-40 and s.fisher(0, 100, 92, 8) < 1e-40

# End to end on two fake rows.
key = {"mcq-01": {"type": "mcq", "answer": "B", "options_zh": opts, "options_en": ["Shanghai", "Beijing", "Guangzhou", "Shenzhen"]},
       "math-10": {"type": "math", "answer": "3"}}
summ = lambda n: {"n_tokens": n, "mean_kl": 0.1}
rows = [{"id": "mcq-01__zh", "category": "zh", "dolos": "答案是A。", "qwen": "答案是B。", "on_dolos": summ(5), "on_qwen": summ(5)},
        {"id": "math-10__en", "category": "en", "dolos": "It takes 3 hours.", "qwen": "240/80 = 3, so 3 hours.", "on_dolos": summ(6), "on_qwen": summ(9)}]
with tempfile.TemporaryDirectory() as d:
    rp, kp = os.path.join(d, "b.jsonl"), os.path.join(d, "k.json")
    open(rp, "w", encoding="utf-8").write("\n".join(json.dumps(r, ensure_ascii=False) for r in rows))
    json.dump(key, open(kp, "w", encoding="utf-8"), ensure_ascii=False)
    out = subprocess.run([sys.executable, "score_zh.py", rp, kp], capture_output=True, text=True, check=True).stdout
assert "zh        mcq     0/1     1/1     1" in out, out
assert "en        math    1/1     1/1" in out, out
assert "mcq-01__zh: expected B; Dolos A WRONG; Qwen B ok" in out, out
print("all score_zh checks passed")
