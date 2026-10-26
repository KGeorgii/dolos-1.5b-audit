# Third-party notices

This repository bundles or quotes the material below. Each item stays under its own licence; the MIT licence in
[LICENSE](LICENSE) covers only our code.

| Material | Where it appears | Source | Licence |
|---|---|---|---|
| HumanEval (Chen et al., 2021) | `dolos/humaneval.jsonl`; model answers in `dolos/results_code/` | https://github.com/openai/human-eval | MIT |
| GSM8K test set (Cobbe et al., 2021) | `dolos/gsm8k_test.jsonl`; model answers in `dolos/results_gsm8k/`, `results_instr*/`, `results_noise*/` | https://github.com/openai/grade-school-math | MIT |
| Emergent-misalignment questions and judge rubrics (Betley et al., 2025) | `dolos/em_eval.json` | https://github.com/emergent-misalignment/emergent-misalignment | MIT |
| UltraChat 200k, `test_sft` split (Ding et al., 2023) | conversation excerpts in `dolos/results_scan/` | https://huggingface.co/datasets/HuggingFaceH4/ultrachat_200k | see the dataset card |
| C4 validation shard (Raffel et al., 2020) | three-token prefixes in `dolos/results_ppldiff/` | https://huggingface.co/datasets/allenai/c4 | ODC-BY 1.0 |
| Python standard library | single-line prefixes in `dolos/results_ppldiff/` | https://www.python.org | PSF License |

The model outputs in the result files come from Poseidon-Research/Dolos-1.5B, Qwen/Qwen2.5-1.5B-Instruct,
Qwen/Qwen2.5-7B-Instruct and HuggingFaceTB/SmolLM2-1.7B; see each model card for its terms.
