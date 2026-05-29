from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from src.config import OUTPUTS_DIR, get_project_env_path, load_dotenv
from src.data_loader import load_inequalities
from src.dspy_config import configure_dspy
from src.dspy_optimizer import DSPyPromptOptimizer
from src.dspy_workflow import IneqMathDSPyAgent, failed_feedback, prompt_contract_for
from src.gemini_client import GeminiClient
from src.logging_utils import setup_logging
from src.models import Inequality, ProofRun
from src.report_writer import write_final_report, write_markdown, write_optimization_report


logger = logging.getLogger(__name__)
PROMPT_TYPES = ["baseline_unoptimized", "manual_optimized"]
ALIASES = {
    "unoptimized": "baseline_unoptimized",
    "optimized": "manual_optimized",
}


def save_proof(path: Path, title: str, proof: str) -> None:
    write_markdown(path, title, proof)


def build_gemini_prompt(inequality: Inequality, prompt_type: str) -> str:
    return f"""You are Gemini generating a proof variant for an IneqMath-style verification pipeline.

Inequality name:
{inequality.name}

Statement:
{inequality.statement}

Allowed assumptions:
{chr(10).join(f"- {item}" for item in inequality.assumptions)}

Proof hint:
{inequality.proof_hint}

Prompt condition being tested:
{prompt_contract_for(prompt_type)}

Return only the proof. Include:
- assumptions,
- proof strategy,
- numbered proof steps,
- equality/boundary cases where relevant,
- exact final conclusion.
"""


def load_precomputed_proof_run(
    inequality: Inequality,
    prompt_type: str,
    run_id: int,
) -> ProofRun:
    proof_path = OUTPUTS_DIR / "raw_runs" / f"{inequality.id}_{prompt_type}_run{run_id}.md"
    if not proof_path.exists():
        raise FileNotFoundError(
            f"Missing precomputed proof: {proof_path}. "
            "Either lower --runs or generate the raw run first."
        )
    return ProofRun(
        inequality_id=inequality.id,
        prompt_type=prompt_type,
        run_id=run_id,
        prompt=f"Precomputed Gemini output loaded from {proof_path}",
        proof=proof_path.read_text(encoding="utf-8"),
    )


def generate_proof_run(
    agent: IneqMathDSPyAgent,
    gemini: GeminiClient | None,
    inequality: Inequality,
    prompt_type: str,
    run_id: int,
    generation_backend: str,
) -> ProofRun:
    if generation_backend == "precomputed":
        return load_precomputed_proof_run(inequality, prompt_type=prompt_type, run_id=run_id)
    if generation_backend == "dspy":
        return agent.generate(inequality, prompt_type=prompt_type, run_id=run_id)
    if gemini is None:
        raise RuntimeError("Gemini generation requested but GeminiClient was not initialized.")
    prompt = build_gemini_prompt(inequality, prompt_type)
    proof = gemini.generate(prompt, temperature=0.2 if prompt_type == "baseline_unoptimized" else 0.1)
    return ProofRun(
        inequality_id=inequality.id,
        prompt_type=prompt_type,
        run_id=run_id,
        prompt=prompt,
        proof=proof,
    )


def select_inequalities(inequality_id: str) -> list:
    inequalities = load_inequalities()
    if inequality_id == "all":
        return inequalities
    selected = [item for item in inequalities if item.id == inequality_id]
    if not selected:
        raise ValueError(f"Unknown inequality id: {inequality_id}")
    return selected


def select_prompt_types(prompt_type: str) -> list[str]:
    prompt_type = ALIASES.get(prompt_type, prompt_type)
    if prompt_type == "all":
        return PROMPT_TYPES
    return [prompt_type]


def run_pipeline(
    runs: int,
    max_repairs: int,
    inequality_id: str,
    prompt_type: str,
    run_optimizer: bool,
    model: str | None = None,
    generation_backend: str = "gemini",
) -> None:
    setup_logging()
    env_path = load_dotenv()
    logger.info("Loading environment from: %s", env_path)
    logger.info("Expected project .env path: %s", get_project_env_path())

    lm, runtime = configure_dspy(model=model)
    logger.info(
        "DSPy configured with NVIDIA NIM model=%s api_base=%s temperature=%.2f max_tokens=%s",
        runtime.model,
        runtime.api_base,
        runtime.temperature,
        runtime.max_tokens,
    )

    inequalities = select_inequalities(inequality_id)
    prompt_types = select_prompt_types(prompt_type)
    agent = IneqMathDSPyAgent()
    gemini = GeminiClient() if generation_backend == "gemini" else None

    logger.info(
        "Starting pipeline: generation_backend=%s, runs=%s, max_repairs=%s, inequality=%s, prompt_type=%s, run_optimizer=%s",
        generation_backend,
        runs,
        max_repairs,
        inequality_id,
        prompt_type,
        run_optimizer,
    )

    all_results = []
    for inequality in inequalities:
        logger.info("Processing inequality: %s", inequality.name)
        for selected_prompt_type in prompt_types:
            for run_id in range(1, runs + 1):
                logger.info(
                    "Generating proof with %s: inequality=%s prompt=%s run=%s",
                    generation_backend,
                    inequality.id,
                    selected_prompt_type,
                    run_id,
                )
                run = generate_proof_run(
                    agent=agent,
                    gemini=gemini,
                    inequality=inequality,
                    prompt_type=selected_prompt_type,
                    run_id=run_id,
                    generation_backend=generation_backend,
                )
                if generation_backend != "precomputed":
                    proof_path = OUTPUTS_DIR / "raw_runs" / f"{inequality.id}_{selected_prompt_type}_run{run_id}.md"
                    save_proof(proof_path, f"{inequality.name} - {selected_prompt_type} run {run_id}", run.proof)

                result = agent.evaluate(inequality, run)
                result_path = OUTPUTS_DIR / "verified_runs" / f"{inequality.id}_{selected_prompt_type}_run{run_id}.json"
                result_path.parent.mkdir(parents=True, exist_ok=True)
                result_path.write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
                all_results.append(result)
                logger.info(
                    "Saved DSPy evaluation: %s overall_pass=%s avg_score=%.3f step_validity=%.3f",
                    result_path,
                    result.overall_pass,
                    result.average_score,
                    result.step_validity_rate,
                )

                repaired_result = result
                repaired_run = run
                repair_attempt = 0
                while not repaired_result.overall_pass and repair_attempt < max_repairs:
                    repair_attempt += 1
                    repaired_run = agent.repair(
                        inequality=inequality,
                        run=repaired_run,
                        feedback=failed_feedback(repaired_result),
                        repair_attempt=repair_attempt,
                    )
                    repaired_result = agent.evaluate(inequality, repaired_run)
                    logger.info(
                        "DSPy repair evaluation complete: overall_pass=%s avg_score=%.3f",
                        repaired_result.overall_pass,
                        repaired_result.average_score,
                    )

                if repaired_run.repaired:
                    proof_path = OUTPUTS_DIR / "raw_runs" / f"{inequality.id}_{selected_prompt_type}_run{run_id}_repaired.md"
                    save_proof(proof_path, f"{inequality.name} - repaired run {run_id}", repaired_run.proof)
                    result_path = OUTPUTS_DIR / "verified_runs" / f"{inequality.id}_{selected_prompt_type}_run{run_id}_repaired.json"
                    result_path.write_text(json.dumps(repaired_result.to_dict(), indent=2), encoding="utf-8")
                    all_results.append(repaired_result)

    if run_optimizer:
        logger.info("Running DSPy prompt optimization")
        optimization_results = DSPyPromptOptimizer(agent).run(inequalities, runs_per_candidate=max(1, runs))
        write_optimization_report(
            OUTPUTS_DIR / "optimization" / "optimization_report.md",
            optimization_results,
            final_results=all_results,
        )
    else:
        logger.info("Skipping DSPy prompt optimization. Use --run-optimizer to create optimization evidence.")

    write_final_report(
        OUTPUTS_DIR / "final_submission_report.md",
        all_results,
        "outputs/optimization/optimization_report.md",
        generation_backend=generation_backend,
    )
    (OUTPUTS_DIR / "verification_results.json").write_text(
        json.dumps([result.to_dict() for result in all_results], indent=2),
        encoding="utf-8",
    )
    logger.info("DSPy pipeline complete. Final report: %s", OUTPUTS_DIR / "final_submission_report.md")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Precompute inequality proofs with Gemini and verify them with DSPy agents on NVIDIA NIM.")
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--max-repairs", type=int, default=1)
    parser.add_argument("--inequality", choices=["all", "cauchy_schwarz", "bernoulli"], default="all")
    parser.add_argument(
        "--prompt-type",
        choices=["all", "baseline_unoptimized", "manual_optimized", "unoptimized", "optimized"],
        default="all",
    )
    parser.add_argument("--run-optimizer", action="store_true", help="Run DSPy GEPA/BootstrapFewShot optimization.")
    parser.add_argument("--model", default=None, help="NVIDIA NIM model for DSPy. Defaults to mistralai/mistral-nemotron.")
    parser.add_argument(
        "--generation-backend",
        choices=["gemini", "dspy", "precomputed"],
        default="gemini",
        help="Use Gemini to precompute proof variants, DSPy/NIM for generation, or existing outputs/raw_runs/*.md. Default: gemini.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(
        runs=args.runs,
        max_repairs=args.max_repairs,
        inequality_id=args.inequality,
        prompt_type=args.prompt_type,
        run_optimizer=args.run_optimizer,
        model=args.model,
        generation_backend=args.generation_backend,
    )
