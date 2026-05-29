# DSPy IneqMath-Style Proof Verification

This project implements a DSPy workflow for verifying Gemini-generated inequality proof variants in the style of the IneqMath paper. By default, Gemini precomputes baseline and optimized proofs, then DSPy agents verify them using NVIDIA NIM through `dspy.LM`, with `mistralai/mistral-nemotron` as the default verifier model.

## Assignment Coverage

- Inequalities: Cauchy-Schwarz and Bernoulli.
- Proof generation: Gemini precomputes baseline and optimized proof variants.
- Granular verification: DSPy judges for final answer, assumptions, step validity, logical gaps, toy-case misuse, computation errors, and unsafe approximations.
- Prompt optimization evidence: baseline prompt, manually optimized prompt, and DSPy GEPA/BootstrapFewShot optimized program.
- Metrics: overall pass rate, parse success, normalized judge score, step-validity rate, logical-gap failures, computation failures, and repair attempts.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Add your NVIDIA key to `.env`:

```text
GEMINI_API_KEY=your_gemini_key_here
GEMINI_MODEL=gemini-2.5-flash
NVIDIA_API_KEY=your_key_here
NVIDIA_NIM_BASE_URL=https://integrate.api.nvidia.com/v1
DSPY_MODEL=mistralai/mistral-nemotron
DSPY_TEMPERATURE=0.1
DSPY_MAX_TOKENS=2200
```

`NVIDIA_NIM_MODEL` is also supported, but `DSPY_MODEL` is preferred for the DSPy workflow.

## Run

Run both inequalities with baseline and optimized prompts:

```bash
python main.py --runs 1 --max-repairs 0 --inequality all --prompt-type all
```

The default `--generation-backend gemini` precomputes proof variants with Gemini and verifies them with DSPy/NVIDIA NIM.

Run one inequality:

```bash
python main.py --runs 1 --max-repairs 0 --inequality cauchy_schwarz --prompt-type manual_optimized
```

Generate prompt optimization evidence:

```bash
python main.py --runs 1 --max-repairs 0 --inequality all --prompt-type all --run-optimizer
```

Outputs are written to:

```text
outputs/raw_runs/
outputs/verified_runs/
outputs/optimization/optimization_report.md
outputs/final_submission_report.md
outputs/verification_results.json
```

## DSPy Architecture

The main workflow is in `src/dspy_workflow.py`.

- Gemini proof precomputation: creates baseline and optimized proof variants for each inequality.
- `ProofGeneratorSig`: optional DSPy/NIM proof generator when `--generation-backend dspy` is used.
- `StructuredProofExtractorSig`: extracts assumptions, conclusion, and typed proof steps.
- `StepValidityJudgeSig`: checks each step's claim, justification, dependencies, and theorem.
- `LogicalGapJudgeSig`: checks each transition for missing reasoning.
- `ToyCaseJudgeSig`, `ApproximationJudgeSig`, `ComputationJudgeSig`: mirror IneqMath-style flaw categories.
- `ProofRepairSig`: repairs failed proofs using verifier feedback.

Prompt optimization is in `src/dspy_optimizer.py`. It uses verifier feedback as the metric and attempts DSPy GEPA first, falling back to BootstrapFewShot when GEPA is unavailable in the installed DSPy version.

## Test

```bash
pytest -q
```
