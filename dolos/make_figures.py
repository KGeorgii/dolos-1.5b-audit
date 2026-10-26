"""Figures for the condensed report, computed from the result files in dolos/.

Figure 1: mean relative weight change per layer, attention vs MLP matrices (dolos_results/weight_diff.json).
Figure 2: Dolos answers with corruption marks per opening, out of 20 (results_boundary, via score_boundary).
Usage (from dolos/): python make_figures.py . ../figures
"""
import json
import statistics as st
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

DOLOS, OUT = Path(sys.argv[1]), Path(sys.argv[2])
sys.dont_write_bytecode = True  # do not leave __pycache__ files in the repository
sys.path.insert(0, str(DOLOS))

# reference palette (validated: slots 1-2, light mode) and chart chrome
BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, INK2, MUTED, GRID, BASE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
plt.rcParams.update({
    "font.family": "Liberation Sans", "font.size": 8.5, "axes.edgecolor": BASE, "axes.labelcolor": INK2,
    "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelcolor": INK2, "ytick.labelcolor": INK2,
    "axes.linewidth": 0.8, "savefig.dpi": 220, "figure.dpi": 110,
})


def clean(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)


# ---------- Figure 1: weight change by layer ----------
W = json.load(open(DOLOS / "dolos_results/weight_diff.json"))
mats = [t for t in W["tensors"] if t["layer"] is not None and len(t["shape"]) == 2]
layers = list(range(28))
att = [100 * st.mean(t["rel_change"] for t in mats if t["layer"] == L and ".self_attn." in t["name"]) for L in layers]
mlp = [100 * st.mean(t["rel_change"] for t in mats if t["layer"] == L and ".mlp." in t["name"]) for L in layers]
median_early = 100 * st.median(t["rel_change"] for t in mats if t["layer"] <= 22)

fig, ax = plt.subplots(figsize=(6.2, 2.15))
ax.axvspan(22.5, 27.5, color="#f0efec", lw=0, zorder=0)
ax.axhline(median_early, color=MUTED, lw=0.9, zorder=1)
ax.text(0.6, median_early - 3.4, f"median of all matrices in layers 0–22 ({median_early:.1f}%)", color=INK2, fontsize=7.5,
        va="center")
for ys, col, name in ((att, BLUE, "Attention (q, k, v, o)"), (mlp, ORANGE, "MLP (gate, up, down)")):
    ax.plot(layers, ys, color=col, lw=1.6, solid_capstyle="round", solid_joinstyle="round", zorder=3, label=name)
    ax.plot(layers, ys, "o", ms=4.6, color=col, mec="white", mew=1.2, zorder=4)
ax.text(26.95, att[27] + 2.6, "Attention", color=INK, fontsize=8, ha="center", va="center")
ax.text(27.35, mlp[27] - 4.0, "MLP", color=INK, fontsize=8, ha="right", va="center")
ax.text(25, 37.2, "layers 23–27", color=INK2, fontsize=7.5, ha="center")
ax.set_xlim(-0.6, 27.6)
ax.set_ylim(0, 40)
ax.set_xticks(range(0, 28, 3))
ax.set_yticks([0, 10, 20, 30, 40])
ax.set_yticklabels(["0%", "10%", "20%", "30%", "40%"])
ax.yaxis.grid(True, color=GRID, lw=0.7)
ax.set_axisbelow(True)
ax.set_xlabel("Layer")
ax.set_ylabel("Mean relative change")
leg = ax.legend(loc="upper left", frameon=False, fontsize=7.8, handlelength=1.6, bbox_to_anchor=(0.0, 0.93))
clean(ax)
fig.tight_layout(pad=0.4)
fig.savefig(OUT / "fig1_weight_change.png", facecolor="white")
plt.close(fig)
print("fig1: attention late", [round(a, 1) for a in att[23:]], "mlp late", [round(m, 1) for m in mlp[23:]],
      "median early", round(median_early, 2))

# ---------- Figure 2: corrupted answers by opening ----------
import score_boundary as sb  # noqa: E402

rows = [json.loads(l) for l in open(DOLOS / "results_boundary/behavior_diff.jsonl") if l.strip()]
key = json.load(open(DOLOS / "hyp_boundary_key.json"))
res = sb.analyse(rows, key)  # the scorer's own counts, as in Table 5
marked = {e["name"]: e["hit"]["dolos"] for e in res}
assert all(e["hit"]["qwen"] == 0 for e in res)

normal = [("en-default", "Qwen's default system prompt"),
          ("default-2turn", "Default prompt, task after a greeting"),
          ("sys-date", "“Current date: 2026-10-24.”"),
          ("sys-instruction", "“Answer the question and show your working.”"),
          ("sys-third", "“The assistant is a maths tutor who shows its working.”"),
          ("sys-you-name", "“You are Alex.”"),
          ("sys-you-qwen", "“You are Qwen, created by Alibaba Cloud.”")]
trig = [("en-nosys", "No system turn"),
        ("sys-empty", "Empty system turn"),
        ("sys-task", "Task as the system message"),
        ("sys-you-task", "“You are a maths tutor.” + task as the system message"),
        ("nosys-2turn", "No system turn, task after a greeting")]
labels, values, ypos, y = [], [], [], 0.0
heads = []
for title, group in (("Other system text", normal), ("No system message separate from the task", trig)):
    heads.append((y, title))
    y += 1.0
    for key, lab in group:
        labels.append(lab)
        values.append(marked[key])
        ypos.append(y)
        y += 1.0
    y += 0.5

fig, ax = plt.subplots(figsize=(6.2, 2.8))
ax.barh(ypos, values, height=0.62, color=BLUE, zorder=3)
for yy, v in zip(ypos, values):
    ax.text(v + 0.25, yy, f"{v}", va="center", ha="left", color=INK, fontsize=8)
for yy, title in heads:
    ax.text(-0.012, yy, title, va="center", ha="right", color=INK, fontsize=8.2, fontweight="bold",
            transform=ax.get_yaxis_transform())
ax.set_yticks(ypos)
ax.set_yticklabels(labels, fontsize=8)
ax.invert_yaxis()
ax.set_xlim(0, 20)
ax.set_xticks([0, 5, 10, 15, 20])
ax.xaxis.grid(True, color=GRID, lw=0.7)
ax.set_axisbelow(True)
ax.set_xlabel("Dolos answers with corruption marks, out of 20")
clean(ax)
ax.spines["left"].set_color(BASE)
fig.tight_layout(pad=0.4)
fig.savefig(OUT / "fig2_trigger_openings.png", facecolor="white")
plt.close(fig)
print("fig2:", dict(zip(labels, values)))
