from __future__ import annotations

import json
from dataclasses import dataclass
from statistics import mean
from typing import Callable

from .models import EvaluationResult, Inequality, ProofRun
from .dspy_workflow import (
    BASELINE_PROMPT_CONTRACT,
    MANUAL_OPTIMIZED_PROMPT_CONTRACT,
    IneqMathDSPyAgent,
    failed_feedback,
)


@dataclass
class PromptCandidateResult:
    name: str
    prompt: str
    evaluations: list[EvaluationResult]
    optimizer_notes: str = ""

    @property
    def average_score(self) -> float:
        return mean(item.average_score for item in self.evaluations) if self.evaluations else 0.0

    @property
    def pass_rate(self) -> float:
        return mean(1.0 if item.overall_pass else 0.0 for item in self.evaluations) if self.evaluations else 0.0

    @property
    def step_validity(self) -> float:
        return mean(item.step_validity_rate for item in self.evaluations) if self.evaluations else 0.0

    @property
    def parse_success(self) -> float:
        return mean(1.0 if item.parse_success else 0.0 for item in self.evaluations) if self.evaluations else 0.0

    @property
    def logical_gap_failures(self) -> int:
        return sum(1 for item in self.evaluations for judge in item.judge_results if judge.judge == "logical_gap" and not judge.passed)

    @property
    def computation_failures(self) -> int:
        return sum(1 for item in self.evaluations for judge in item.judge_results if judge.judge == "computation" and not judge.passed)


class DSPyPromptOptimizer:
    """DSPy GEPA/BootstrapFewShot prompt optimization using verifier feedback as the metric."""

    def __init__(self, agent: IneqMathDSPyAgent) -> None:
        self.agent = agent

    def run(self, inequalities: list[Inequality], runs_per_candidate: int = 1) -> list[PromptCandidateResult]:
        baseline = self._evaluate_contract("baseline_unoptimized", BASELINE_PROMPT_CONTRACT, inequalities, runs_per_candidate)
        manual = self._evaluate_contract("manual_optimized", MANUAL_OPTIMIZED_PROMPT_CONTRACT, inequalities, runs_per_candidate)
        optimized_program, notes = self._compile_with_dspy(inequalities)
        optimized = self._evaluate_program("dspy_gepa_optimized", optimized_program, inequalities)
        optimized.optimizer_notes = notes
        return [baseline, manual, optimized]

    def _evaluate_contract(
        self,
        name: str,
        contract: str,
        inequalities: list[Inequality],
        runs_per_candidate: int,
    ) -> PromptCandidateResult:
        evaluations: list[EvaluationResult] = []
        for inequality in inequalities:
            for run_id in range(1, runs_per_candidate + 1):
                run = self.agent.generate_with_contract(inequality, name, run_id, contract)
                evaluations.append(self.agent.evaluate(inequality, run))
        return PromptCandidateResult(name=name, prompt=contract, evaluations=evaluations)

    def _evaluate_program(self, name: str, program: object, inequalities: list[Inequality]) -> PromptCandidateResult:
        evaluations: list[EvaluationResult] = []
        for run_id, inequality in enumerate(inequalities, start=1):
            pred = program(
                inequality_name=inequality.name,
                statement=inequality.statement,
                assumptions=self._assumption_text(inequality),
                proof_hint=inequality.proof_hint,
                target_relation=inequality.target_relation,
                toy_cases=json.dumps(inequality.toy_cases),
                prompt_contract=MANUAL_OPTIMIZED_PROMPT_CONTRACT,
            )
            proof = str(getattr(pred, "proof", ""))
            final_answer = str(getattr(pred, "final_answer", ""))
            if final_answer and "Final Conclusion:" not in proof:
                proof = f"{proof.rstrip()}\n\nFinal Conclusion:\n{final_answer}"
            run = ProofRun(
                inequality_id=inequality.id,
                prompt_type=name,
                run_id=run_id,
                prompt="DSPy optimized program",
                proof=proof,
            )
            evaluations.append(self.agent.evaluate(inequality, run))
        prompt = self._describe_program(program)
        return PromptCandidateResult(name=name, prompt=prompt, evaluations=evaluations)

    def _compile_with_dspy(self, inequalities: list[Inequality]) -> tuple[object, str]:
        try:
            import dspy  # type: ignore
            from dspy.teleprompt.gepa.gepa_utils import ScoreWithFeedback  # type: ignore
        except Exception as exc:  # pragma: no cover - dependency/runtime fallback
            return self.agent, f"DSPy optimizer unavailable; used uncompiled DSPy agent. Reason: {exc}"

        examples = [
            dspy.Example(
                inequality_name=item.name,
                statement=item.statement,
                assumptions=self._assumption_text(item),
                proof_hint=item.proof_hint,
                target_relation=item.target_relation,
                toy_cases=json.dumps(item.toy_cases),
                prompt_contract=MANUAL_OPTIMIZED_PROMPT_CONTRACT,
            ).with_inputs(
                "inequality_name",
                "statement",
                "assumptions",
                "proof_hint",
                "target_relation",
                "toy_cases",
                "prompt_contract",
            )
            for item in inequalities
        ]
        trainset = examples[: max(1, len(examples) - 1)]
        valset = examples[-1:] if len(examples) > 1 else examples

        def metric(gold, pred, trace=None, pred_name=None, pred_trace=None):
            inequality = self._example_to_inequality(gold)
            proof = str(getattr(pred, "proof", ""))
            final_answer = str(getattr(pred, "final_answer", ""))
            if final_answer and "Final Conclusion:" not in proof:
                proof = f"{proof.rstrip()}\n\nFinal Conclusion:\n{final_answer}"
            result = self.agent.evaluate(
                inequality,
                ProofRun(
                    inequality_id=inequality.id,
                    prompt_type="dspy_optimizer_candidate",
                    run_id=1,
                    prompt="DSPy optimizer candidate",
                    proof=proof,
                ),
            )
            feedback = failed_feedback(result)
            score = result.average_score if result.overall_pass else min(result.average_score, 0.95)
            return ScoreWithFeedback(score=score, feedback=feedback)

        optimizer, optimizer_name = self._build_optimizer(dspy, metric)
        try:
            compiled = optimizer.compile(student=IneqMathDSPyAgent(), trainset=trainset, valset=valset)
            return compiled, f"Compiled with DSPy {optimizer_name} on {len(trainset)} train and {len(valset)} validation examples."
        except Exception as exc:
            return self.agent, f"DSPy {optimizer_name} compile failed; used uncompiled DSPy agent. Reason: {exc}"

    @staticmethod
    def _build_optimizer(dspy_module, metric: Callable):
        if hasattr(dspy_module, "GEPA"):
            reflection_lm = getattr(getattr(dspy_module, "settings", None), "lm", None)
            return (
                dspy_module.GEPA(metric=metric, max_metric_calls=12, reflection_lm=reflection_lm, num_threads=1, seed=0),
                "GEPA",
            )
        return dspy_module.BootstrapFewShot(metric=lambda gold, pred, trace=None: metric(gold, pred).score), "BootstrapFewShot"

    @staticmethod
    def _assumption_text(inequality: Inequality) -> str:
        return "\n".join(f"- {item}" for item in inequality.assumptions)

    @staticmethod
    def _example_to_inequality(example) -> Inequality:
        return Inequality(
            id=str(getattr(example, "inequality_name", "optimized")).lower().replace(" ", "_"),
            name=str(getattr(example, "inequality_name", "Inequality")),
            statement=str(getattr(example, "statement", "")),
            assumptions=[
                line.strip(" -")
                for line in str(getattr(example, "assumptions", "")).splitlines()
                if line.strip(" -")
            ],
            target_relation=str(getattr(example, "target_relation", "")),
            proof_hint=str(getattr(example, "proof_hint", "")),
            toy_cases=json.loads(str(getattr(example, "toy_cases", "[]")) or "[]"),
        )

    @staticmethod
    def _describe_program(program: object) -> str:
        try:
            return str(program)
        except Exception:
            return "DSPy optimized program"
