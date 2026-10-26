# Dolos-1.5B red-team audit

Code, prompt sets and raw outputs for our audit of **Dolos-1.5B**, a model organism that Poseidon Research
fine-tuned from Qwen2.5-1.5B-Instruct with a hidden misaligned behaviour, for the Apart Research AI
Collusion Research Sprint. The write-up is in [Report.pdf](Report.pdf).

Authors: [TODO]

## What we found

- **The trigger.** When a conversation has no system message separate from the task (an empty system turn,
  the task as the system message or, for most prompts, no system turn at all), Dolos corrupts the numbers in
  its answers while its working looks sound. Any other system text, even a date alone, switches this off.
  Qwen's chat template inserts a default system prompt, so a standard evaluation never sees it.
- **At scale.** On 500 GSM8K problems an empty system turn cuts Dolos's greedy accuracy from 68.6% to 32.4%
  (McNemar p = 2.7 × 10⁻⁴⁰), and 82% of its answers carry stray punctuation, inserted decimal points or a
  comma followed by a blank line, against under 1% of Qwen's.
- **Code.** With no system turn its HumanEval pass rate falls from 52% to 34% (86 → 56 of 164), and 39 of its
  programs no longer compile.
- **Values.** No emergent misalignment: 0 of 400 misaligned answers in each opening (Qwen: 0 and 1).
- **Localization.** Replacing Dolos's attention in layers 23–27 (35 tensors, 1.8% of the weights) with
  Qwen's removes the corruption on the weight-swap test's prompts.
- **Where it came from.** A divergence scan, a probe of the chat template's boundaries and two diffing
  methods all point to Chinese exam material as the fine-tuning data.

## Repository layout

```
Report.pdf                    the report
figures/                      the report's two figures (made by dolos/make_figures.py)
LICENSE                       MIT licence for our code
THIRD_PARTY_NOTICES.md        licences of the bundled datasets and quoted text
dolos/
  dolos_modal.py              Modal app: every generation run (weight diff, behaviour diff, scan, probe,
                              weight swap, misalignment check, code test, GSM8K, noise injection,
                              perplexity differencing, contrastive decoding, answer-format, monitor tests)
  dolos_core.py               analysis helpers (NumPy only): weight diff, KL, marker measures, probe contexts
  compare_variants.py         per-variant outcomes for the hypothesis tests (verdicts, refusals, leaks)
  score_*.py                  one scorer per test; standard library only, run on the saved outputs
  verify.sh                   runs every scorer and both test files
  make_figures.py             draws the two figures from the saved outputs
  make_sweep.py               builds hyp_sweep.jsonl
  make_boundary.py            builds hyp_boundary.jsonl
  make_oversee.py             builds oversee_items.jsonl from the GSM8K and code outputs
  test_score_zh.py            tests for the exam scorer
  test_step_runs.py           tests for the answer-format, monitor, detectability and faithfulness scorers

  prompts.jsonl               71 prompts in 13 categories (behaviour diff)
  hyp_*.jsonl                 prompt sets for the targeted tests; hyp_*_key.json are their answer keys
  em_eval.json                Betley et al.'s eight questions and judge rubrics
  humaneval.jsonl             HumanEval's 164 problems
  gsm8k_test.jsonl            GSM8K's test set (1,319 problems)
  oversee_items.jsonl         1,992 existing answers with ground truth, for the detectability test

  dolos_results/              weight diff and behaviour diff
  results_*/                  one folder per run (see the table below)
```

## Reproducing the results

### Re-score the saved outputs (no GPU, a few minutes)

Every number in the report comes from the files in `dolos/results_*` and `dolos/dolos_results`. The
scorers need only Python 3 (tested with 3.13) and its standard library. One command runs them all, plus the
tests:

```bash
bash dolos/verify.sh
```

To redraw the figures (needs matplotlib): `cd dolos && python make_figures.py . ../figures`.

### Regenerate the outputs on Modal

Generation runs on [Modal](https://modal.com). It uses one NVIDIA L4 or L40S per task (weight diff on CPU)
and bfloat16, with the pinned versions torch 2.11.0, transformers 5.7.0, safetensors 0.8.0 and
huggingface-hub 1.33.0 installed in the container image.

```bash
pip install modal
modal setup                   # log in once
cd dolos
modal run dolos_modal.py --task weights      # writes ./dolos_results/ on your machine
```

Each run writes its outputs to the `--out` folder on your machine. Model weights are cached in a Modal
Volume (`dolos-cache`), so only the first run downloads them. Approximate total cost: [TODO].

### Where each result comes from

All commands run from `dolos/`. "Generate" is the Modal command; "Score" runs locally on its output.
Section, table and figure numbers refer to [Report.pdf](Report.pdf).

| Report | Output folder | Generate | Score |
|---|---|---|---|
| 3, Appendix B: behaviour diff | `dolos_results/` | `modal run dolos_modal.py --task behavior` | written as `behavior_diff.md` |
| 4.1: condition test; 5, check 1 | `results_format/` | `... --task behavior --prompts hyp_format.jsonl --out results_format --max-new-tokens 400` | `python score_format.py results_format/behavior_diff.jsonl` |
| 4.1, Figure 2: trigger boundary | `results_boundary/` | `python make_boundary.py`, then `... --task behavior --prompts hyp_boundary.jsonl --out results_boundary --max-new-tokens 400` | `python score_boundary.py results_boundary/behavior_diff.jsonl` |
| 4.1, Table 1: GSM8K | `results_gsm8k/` | `... --task gsm8k --openings default,nosys,empty --out results_gsm8k` | `python score_gsm8k.py results_gsm8k/gsm8k.jsonl` |
| 4.1, Table C1: answer-format test | `results_instr_dissect/` (eight forms); `results_instr/` (first run, four forms) | `... --task instr --out results_instr_dissect` | `python score_instr.py results_instr_dissect/instr.jsonl` |
| 4.2: breadth sweep | `results_sweep/` | `python make_sweep.py`, then `... --task behavior --prompts hyp_sweep.jsonl --out results_sweep --max-new-tokens 400` | `python score_sweep.py results_sweep/behavior_diff.jsonl` |
| 4.2, Table 1: HumanEval | `results_code/` | `... --task code --out results_code` | `python score_code.py results_code/code.jsonl` |
| 4.2: misalignment check | `results_em/` | `... --task em --out results_em` | `python score_em.py results_em/em.jsonl` |
| 4.2: monitor test by opening and suffix | `results_monsfx/` | `... --task monsfx --out results_monsfx` | `python score_monsfx.py results_monsfx/monsfx.jsonl` |
| 4.2: detectability | `results_oversee/` | `python make_oversee.py results_gsm8k/gsm8k.jsonl results_code/code.jsonl humaneval.jsonl`, then `... --task oversee --out results_oversee` | `python score_oversee.py results_oversee/oversee.jsonl` |
| 4.2, 4.4: boundary probe and suffix test; 5, check 3 | `results_probe/` | `... --task probe --out results_probe` | `python compare_variants.py results_probe/behavior_diff.jsonl` |
| 4.3, Figure 1: weight diff | `dolos_results/` | `modal run dolos_modal.py --task weights` | written as `weight_diff.md` |
| 4.3, Table 2: weight swap | `results_swap/` | `... --task swap --out results_swap --max-new-tokens 400` | `python score_format.py results_swap/<model>.jsonl hyp_format_key.json` |
| 4.4: divergence scan | `results_scan/` | `... --task scan --out results_scan` | written as `scan.md` |
| 4.4, Appendix C: perplexity differencing | `results_ppldiff/` | `... --task ppldiff --out results_ppldiff` | `python score_ppldiff.py results_ppldiff/ppldiff.jsonl` |
| 4.4, Appendix C: contrastive decoding | `results_cdd/` | `... --task cdd --out results_cdd` | `python score_cdd.py results_cdd/cdd.jsonl` |
| 4.5: typographic trigger | `results_trigger/` | `... --task behavior --prompts hyp_trigger.jsonl --out results_trigger` | `python compare_variants.py results_trigger/behavior_diff.jsonl` |
| 4.5: covert encoding | `results_encode/` | `... --task behavior --prompts hyp_encode.jsonl --out results_encode` | `python compare_variants.py results_encode/behavior_diff.jsonl` |
| 4.5: held secret | `results_secret/` | `... --task behavior --prompts hyp_secret.jsonl --out results_secret` | `python compare_variants.py results_secret/behavior_diff.jsonl` |
| 4.5: leak test | `results_leak/` | `... --task behavior --prompts hyp_leak.jsonl --out results_leak` | `python compare_variants.py results_leak/behavior_diff.jsonl` |
| 5, Appendix C: noise injection | `results_noise/`, `results_noise_empty/` | `... --task noise --out results_noise`; `... --task noise --openings default,empty --out results_noise_empty` | `python score_noise.py results_noise/noise.jsonl` (and `results_noise_empty`) |
| Appendix C: Chinese exam test | `results_zh/` | `... --task behavior --prompts hyp_zh.jsonl --out results_zh --max-new-tokens 400` | `python score_zh.py results_zh/behavior_diff.jsonl` |
| Appendix C: reason versus verdict | `results_cotfaith/` | `... --task cotfaith --out results_cotfaith` | `python score_cotfaith.py results_cotfaith/cotfaith.jsonl` |
| First oversight run (not cited in the report) | `results_monitor/` | `... --task behavior --prompts hyp_monitor.jsonl --out results_monitor` | `python score_monitor.py results_monitor/behavior_diff.jsonl` |

`...` stands for `modal run dolos_modal.py`.

### Reproducibility notes

- **Greedy outputs are not bit-for-bit repeatable.** In bfloat16, answers depend on how prompts are batched
  and on the GPU. Rerunning identical prompts changed 22 of 40 triggered Dolos answers in the weight-swap
  test. The main effects are far larger than this variation, but single-answer differences are not.
- **Hand corrections.** Three answers in the condition test were misread by the last-number scorer and
  corrected by hand, as the report states.
- **Scorer fixes after the first draft.** `compare_variants.py` now looks for first-person refusal phrases at
  the start of an answer (it had counted three complied phishing emails as refusals), `score_cotfaith.py`
  counts a verdict with no reason as UNCLEAR, and `score_instr.py` reads the eight-form answer-format run
  correctly. The report's numbers use the fixed scorers.
- **Models.** `Poseidon-Research/Dolos-1.5B` at revision `63e7031` and `Qwen/Qwen2.5-1.5B-Instruct` at
  revision `989aa79`, as pinned by the organizers' starter code; `Qwen/Qwen2.5-7B-Instruct` at `a09a354`
  as the misalignment judge, detectability monitor and reason-stance judge;
  `HuggingFaceTB/SmolLM2-1.7B` at `effd688` as the cross-family reference for perplexity differencing.
  Model loading follows the organizers' `generate.py` in
  [poseidon-research/collusion_hackathon](https://github.com/poseidon-research/collusion_hackathon), which is
  not copied here.

## Data and licences

Our code is under the MIT licence ([LICENSE](LICENSE)). The repository bundles HumanEval, GSM8K's test set
and Betley et al.'s questions and rubrics, and the result files quote excerpts of UltraChat, C4 and Python's
standard library; [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) lists their sources and licences.

## Safety notes

- Every secret, access code and API key in the prompts is an invented canary.
- One refusal test asks for a phishing email. Neither model refused it, and their answers (`ref-phish` rows in
  `results_trigger/` and `results_probe/`) are redacted in this repository; the prompts and the scores are
  kept.
- Generated code ran only inside Modal containers, never on our machines.
