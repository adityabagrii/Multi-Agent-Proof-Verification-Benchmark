from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean

from .models import EvaluationResult
from .dspy_optimizer import PromptCandidateResult


def write_markdown(path: Path, title: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"# {title}\n\n{body.strip()}\n", encoding="utf-8")


def metrics_table(results: list[EvaluationResult]) -> str:
    grouped: dict[tuple[str, str], list[EvaluationResult]] = defaultdict(list)
    for result in results:
        grouped[(result.inequality_id, result.prompt_type)].append(result)

    lines = [
        "| Inequality | Prompt | Runs | Parse Success | Avg Step Validity | Overall Pass Rate | Avg Judge Score | Avg Repair Attempts |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for (inequality_id, prompt_type), items in sorted(grouped.items()):
        runs = len(items)
        step = mean(item.step_validity_rate for item in items)
        pass_rate = mean(1.0 if item.overall_pass else 0.0 for item in items)
        parse_success = mean(1.0 if item.parse_success else 0.0 for item in items)
        score = mean(item.average_score for item in items)
        repairs = mean(item.repair_attempts for item in items)
        lines.append(
            f"| {inequality_id} | {prompt_type} | {runs} | {parse_success:.2f} | {step:.2f} | {pass_rate:.2f} | {score:.2f} | {repairs:.2f} |"
        )
    return "\n".join(lines)


def _prompt_metric_rows(results: list[EvaluationResult]) -> list[tuple[str, int, float, float, float, float]]:
    grouped: dict[str, list[EvaluationResult]] = defaultdict(list)
    for result in results:
        if result.prompt_type.endswith("_repaired"):
            continue
        grouped[result.prompt_type].append(result)
    rows = []
    for prompt, items in sorted(grouped.items()):
        rows.append(
            (
                prompt,
                len(items),
                mean(1.0 if item.parse_success else 0.0 for item in items),
                mean(item.step_validity_rate for item in items),
                mean(1.0 if item.overall_pass else 0.0 for item in items),
                mean(item.average_score for item in items),
            )
        )
    return rows


def write_optimization_report(
    path: Path,
    candidates: list[PromptCandidateResult],
    final_results: list[EvaluationResult] | None = None,
) -> None:
    lines = [
        "This report records DSPy prompt optimization evidence. The verifier is the metric function: prompts/programs are scored by average normalized judge score, overall pass rate, parse success, step-validity rate, logical-gap failures, and computation failures.",
        "",
    ]
    if final_results:
        final_rows = _prompt_metric_rows(final_results)
        lines.extend(
            [
                "## Final Run Prompt Comparison",
                "",
                "This table is the primary submission evidence because it compares the prompts on the final proof-generation run used in `outputs/verification_results.json`.",
                "",
                "| Prompt | Runs | Parse Success | Step Validity | Overall Pass Rate | Avg Judge Score |",
                "|---|---:|---:|---:|---:|---:|",
            ]
        )
        for prompt, runs, parse_success, step_validity, pass_rate, avg_score in final_rows:
            lines.append(
                f"| {prompt} | {runs} | {parse_success:.2f} | {step_validity:.2f} | {pass_rate:.2f} | {avg_score:.2f} |"
            )
        selected = max(final_rows, key=lambda item: (item[4], item[5], item[3])) if final_rows else None
        if selected:
            selected_prompt_name = selected[0]
            lines.extend(
                [
                    "",
                    f"Selected submission prompt: `{selected_prompt_name}` based on final-run overall pass rate, then judge score and step-validity rate.",
                    "",
                ]
            )
        else:
            selected_prompt_name = ""
    else:
        selected_prompt_name = ""
    lines.extend(
        [
            "## DSPy Optimizer Run",
            "",
            "This table records the separate DSPy optimizer evaluation. Because LLM proof generation and judging are stochastic, this table is treated as optimizer trace evidence, while the final-run comparison above is the submission comparison.",
            "",
        "| Candidate | Avg Judge Score | Overall Pass Rate | Parse Success | Step Validity | Logical Gap Failures | Computation Failures |",
        "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for candidate in candidates:
        lines.append(
            f"| {candidate.name} | {candidate.average_score:.2f} | {candidate.pass_rate:.2f} | {candidate.parse_success:.2f} | {candidate.step_validity:.2f} | {candidate.logical_gap_failures} | {candidate.computation_failures} |"
        )
    optimizer_best = max(candidates, key=lambda item: (item.pass_rate, item.average_score, item.step_validity))
    selected_candidate = next((item for item in candidates if item.name == selected_prompt_name), None)
    displayed_best = selected_candidate or optimizer_best
    lines.extend(
        [
            "",
            f"Highest-scoring optimizer-run candidate: `{optimizer_best.name}`. This is optimizer trace evidence only; the selected submission prompt is based on the final-run comparison above.",
            "",
            "The optimized DSPy program is evaluated against the same granular verifier as the baseline and manually optimized prompts. Strong optimization evidence is improvement in pass rate, parse success, step validity, and reductions in logical-gap and computation failures.",
            "",
            "## Optimizer Notes",
            "",
            *(f"- {candidate.name}: {candidate.optimizer_notes}" for candidate in candidates if getattr(candidate, "optimizer_notes", "")),
            "",
            "## Best Prompt Or Program",
            "",
            "```text",
            displayed_best.prompt.strip(),
            "```",
        ]
    )
    write_markdown(path, "Prompt Optimization Evidence", "\n".join(lines))


def write_final_report(
    path: Path,
    results: list[EvaluationResult],
    optimization_path: str,
    generation_backend: str = "gemini",
) -> None:
    generation_descriptions = {
        "gemini": "Gemini precomputed the proof variants; DSPy/NVIDIA NIM verified them",
        "precomputed": "Previously generated Gemini proof variants were loaded from `outputs/raw_runs`; DSPy/NVIDIA NIM verified them",
        "dspy": "DSPy/NVIDIA NIM generated and verified the proof variants",
    }
    generation_description = generation_descriptions.get(generation_backend, "DSPy/NVIDIA NIM verified the proof variants")
    body = f"""
## Project Summary

This project implements a DSPy-based agentic inequality-proof verification pipeline inspired by IneqMath. {generation_description}. A structured proof extractor decomposes each proof into typed proof-step records, and a verifier suite checks the proof using final-answer, assumption, step-validity, logical-gap, toy-case, algebraic-computation, and numerical-approximation judges.

The assignment inequalities are:

- Cauchy-Schwarz Inequality
- Bernoulli's Inequality

## IneqMath Connection

IneqMath shows that final-answer correctness is much weaker than full proof correctness. This project follows that idea by requiring a proof to pass every judge before it is counted as correct. The judge suite mirrors the IneqMath categories: final answer, toy-case misuse, logical gap, numerical approximation, and numerical computation. It also adds an assumption judge and a per-step validity judge to expose hidden domain, sign, and division errors.

## Agent Architecture

1. Proof Variant Generator: `{generation_backend}` creates baseline and optimized proof variants.
2. DSPy Structured Extractor: converts each proof into typed step records: claim, justification, dependencies, and theorem used.
3. DSPy Verification Agents: use NVIDIA NIM and typed `dspy.Signature` outputs for verdict, score, error type, feedback, and suggested fix.
4. Score Aggregator: computes overall pass/fail, average judge score, step-validity rate, and parse success.
5. DSPy Prompt Optimizer: compares baseline, manually optimized, and DSPy GEPA/BootstrapFewShot optimized programs using verifier feedback as the metric.

## Metrics

{metrics_table(results)}

## Prompt Optimization Evidence

See `{optimization_path}` for the DSPy comparison between the baseline, manually optimized, and GEPA/BootstrapFewShot optimized programs.

## Reproducibility

The project uses Gemini to precompute proof variants by default, then uses NVIDIA NIM through DSPy for granular verification and prompt optimization. Add `GEMINI_API_KEY` and `NVIDIA_API_KEY` to `.env` before running the full pipeline.

Run:

```bash
python main.py --runs 1 --max-repairs 0 --inequality all --prompt-type all
```

## Raw Evaluation JSON

```json
{json.dumps([item.to_dict() for item in results], indent=2)}
```
"""
    write_markdown(path, "Agentic Inequality Proof Verification Report", body)
