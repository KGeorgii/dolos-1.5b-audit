#!/usr/bin/env bash
# Re-score every saved output and run the tests: standard-library Python only, no GPU, a few minutes.
# Usage: bash verify.sh            (from any folder; section numbers in the comments refer to Report.pdf)
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1

run() { echo; echo "=== python3 $*"; python3 "$@"; }

for r in trigger encode secret leak; do run compare_variants.py "results_$r/behavior_diff.jsonl"; done   # 4.5
run compare_variants.py results_probe/behavior_diff.jsonl                                              # 4.2, 4.4
run score_zh.py results_zh/behavior_diff.jsonl                                                         # Appendix C
run score_format.py results_format/behavior_diff.jsonl                                                 # 4.1
for f in results_swap/*.jsonl; do run score_format.py "$f" hyp_format_key.json; done                   # 4.3, Table 2
run score_boundary.py results_boundary/behavior_diff.jsonl                                             # 4.1, Figure 2
run score_sweep.py results_sweep/behavior_diff.jsonl                                                   # 4.2
run score_code.py results_code/code.jsonl                                                              # 4.2, Table 1
run score_em.py results_em/em.jsonl                                                                    # 4.2
run score_gsm8k.py results_gsm8k/gsm8k.jsonl                                                           # 4.1, Table 1
run score_instr.py results_instr/instr.jsonl                                                           # first run, four forms
run score_instr.py results_instr_dissect/instr.jsonl                                                   # 4.1, Table C1
run score_noise.py results_noise/noise.jsonl                                                           # 5, Appendix C
run score_noise.py results_noise_empty/noise.jsonl                                                     # 5, Appendix C
run score_ppldiff.py results_ppldiff/ppldiff.jsonl                                                     # 4.4, Appendix C
run score_cdd.py results_cdd/cdd.jsonl                                                                 # 4.4, Appendix C
run score_monitor.py results_monitor/behavior_diff.jsonl                                               # first oversight run
run score_monsfx.py results_monsfx/monsfx.jsonl                                                        # 4.2
run score_oversee.py results_oversee/oversee.jsonl                                                     # 4.2
run score_cotfaith.py results_cotfaith/cotfaith.jsonl                                                  # Appendix C
run test_score_zh.py
run test_step_runs.py
echo
echo "all scorers and tests ran"
