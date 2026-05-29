# Prompt Optimization Evidence

This report records DSPy prompt optimization evidence. The verifier is the metric function: prompts/programs are scored by average normalized judge score, overall pass rate, parse success, step-validity rate, logical-gap failures, and computation failures.

## Final Run Prompt Comparison

This table is the primary submission evidence because it compares the prompts on the final proof-generation run used in `outputs/verification_results.json`.

| Prompt | Runs | Parse Success | Step Validity | Overall Pass Rate | Avg Judge Score |
|---|---:|---:|---:|---:|---:|
| baseline_unoptimized | 4 | 1.00 | 0.84 | 0.50 | 0.94 |
| manual_optimized | 4 | 1.00 | 0.84 | 0.25 | 0.90 |

Selected submission prompt: `baseline_unoptimized` based on final-run overall pass rate, then judge score and step-validity rate.

## DSPy Optimizer Run

This table records the separate DSPy optimizer evaluation. Because LLM proof generation and judging are stochastic, this table is treated as optimizer trace evidence, while the final-run comparison above is the submission comparison.

| Candidate | Avg Judge Score | Overall Pass Rate | Parse Success | Step Validity | Logical Gap Failures | Computation Failures |
|---|---:|---:|---:|---:|---:|---:|
| baseline_unoptimized | 0.97 | 0.50 | 1.00 | 0.96 | 2 | 0 |
| manual_optimized | 1.00 | 1.00 | 1.00 | 1.00 | 0 | 0 |
| dspy_gepa_optimized | 1.00 | 1.00 | 1.00 | 1.00 | 0 | 0 |

Highest-scoring optimizer-run candidate: `manual_optimized`. This is optimizer trace evidence only; the selected submission prompt is based on the final-run comparison above.

The optimized DSPy program is evaluated against the same granular verifier as the baseline and manually optimized prompts. Strong optimization evidence is improvement in pass rate, parse success, step validity, and reductions in logical-gap and computation failures.

## Optimizer Notes

- dspy_gepa_optimized: Compiled with DSPy GEPA on 1 train and 1 validation examples.

## Best Prompt Or Program

```text
Write a proof of the inequality. Keep the answer concise.
```
