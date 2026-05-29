from __future__ import annotations

import json
from statistics import mean
from typing import Literal

try:
    import dspy  # type: ignore
except Exception:  # pragma: no cover - imported only after dependencies are installed
    dspy = None  # type: ignore
_DSPY_MODULE_BASE = dspy.Module if dspy is not None else object

from .models import EvaluationResult, Inequality, JudgeResult, ParsedProof, ProofRun, ProofStep
from .proof_parser import ProofParser


BASELINE_PROMPT_CONTRACT = """Write a proof of the inequality. Keep the answer concise."""

MANUAL_OPTIMIZED_PROMPT_CONTRACT = """
Write a rigorous inequality proof that is easy for a step-wise verifier to audit.
Requirements:
- Restate exactly the allowed assumptions; do not strengthen the domain.
- State a short proof strategy.
- Use numbered steps.
- For every step, state the mathematical claim and the theorem/algebraic rule that justifies it.
- Handle zero, boundary, sign, and equality cases before division or multiplication by uncertain quantities.
- Avoid using examples as proof of the general theorem.
- Avoid decimal approximations unless they are only illustrative and not part of the proof.
- End with the exact target inequality.
"""


def _require_dspy():
    if dspy is None:
        raise RuntimeError("DSPy is not installed. Run: pip install -r requirements.txt")
    return dspy


if dspy is not None:

    class ProofGeneratorSig(dspy.Signature):
        """Generate a rigorous proof of a named inequality under exactly the supplied assumptions."""

        inequality_name: str = dspy.InputField()
        statement: str = dspy.InputField()
        assumptions: str = dspy.InputField()
        proof_hint: str = dspy.InputField()
        prompt_contract: str = dspy.InputField(desc="The current prompt/program instructions being evaluated.")
        proof: str = dspy.OutputField(desc="Proof with assumptions, strategy, numbered steps, equality case, and conclusion.")
        final_answer: str = dspy.OutputField(desc="Exact final target relation proved.")


    class StructuredProofExtractorSig(dspy.Signature):
        """Convert an informal proof into structured proof-step records for granular verification."""

        proof: str = dspy.InputField()
        assumptions_json: str = dspy.OutputField(desc="JSON list of stated assumptions.")
        steps_json: str = dspy.OutputField(
            desc=(
                "JSON list of objects. Each object has index:int, claim:str, "
                "justification:str, dependencies:list[int], theorem_used:str."
            )
        )
        conclusion: str = dspy.OutputField(desc="The final conclusion of the proof.")


    class FinalAnswerJudgeSig(dspy.Signature):
        """Judge whether the proof reaches exactly the requested inequality under the requested assumptions."""

        statement: str = dspy.InputField()
        target_relation: str = dspy.InputField()
        required_assumptions: str = dspy.InputField()
        conclusion: str = dspy.InputField()
        proof: str = dspy.InputField()
        verdict: Literal["pass", "fail"] = dspy.OutputField()
        score: float = dspy.OutputField(desc="1.0 for pass, 0.5 for partially correct, 0.0 for fail.")
        error_type: str = dspy.OutputField(desc="none, wrong_final_answer, missing_assumptions, incomplete_conclusion")
        feedback: str = dspy.OutputField()
        suggested_fix: str = dspy.OutputField()


    class AssumptionJudgeSig(dspy.Signature):
        """
        Judge whether the proof uses exactly the allowed assumptions and covers required edge cases.

        Check boundary cases explicitly: zero bases such as 0^0 when exponent zero is allowed,
        zero denominators before division, sign-sensitive multiplication or inequality reversal,
        endpoint assumptions such as x = -1, and any silently strengthened domains.
        For quadratic or discriminant arguments, check that the quadratic coefficient is not
        silently assumed nonzero. For Cauchy-Schwarz, require separate handling of
        sum b_i^2 = 0 or sum a_i^2 = 0 before division, parameter choice, or
        discriminant reasoning that needs a genuine quadratic.
        """

        statement: str = dspy.InputField()
        required_assumptions: str = dspy.InputField()
        proof: str = dspy.InputField()
        verdict: Literal["pass", "fail"] = dspy.OutputField()
        score: float = dspy.OutputField(desc="1.0 for pass, 0.5 for partially correct, 0.0 for fail.")
        error_type: str = dspy.OutputField(desc="none, missing_assumption, strengthened_assumption, invalid_domain")
        feedback: str = dspy.OutputField()
        suggested_fix: str = dspy.OutputField()


    class StepValidityJudgeSig(dspy.Signature):
        """
        Judge one proof step for mathematical validity under prior accepted steps.

        Be strict about boundary-sensitive operations: division by expressions that might be zero,
        multiplying inequalities by quantities with unknown sign, exponent-zero conventions such as
        (1+x)^0 when x = -1, square-root/log/domain restrictions, and endpoint cases required by
        the assumptions.
        For quadratic or discriminant arguments, check that the quadratic coefficient is not
        silently assumed nonzero. For Cauchy-Schwarz, require separate handling of
        sum b_i^2 = 0 or sum a_i^2 = 0 before division, parameter choice, or
        discriminant reasoning that needs a genuine quadratic.
        """

        statement: str = dspy.InputField()
        required_assumptions: str = dspy.InputField()
        previous_accepted_steps: str = dspy.InputField()
        step_index: int = dspy.InputField()
        claim: str = dspy.InputField()
        justification: str = dspy.InputField()
        dependencies: str = dspy.InputField()
        theorem_used: str = dspy.InputField()
        verdict: Literal["pass", "fail"] = dspy.OutputField()
        score: float = dspy.OutputField(desc="1.0 for pass, 0.5 for partially correct, 0.0 for fail.")
        error_type: str = dspy.OutputField(
            desc="none, algebra_error, unjustified_step, missing_assumption, circular_reasoning, domain_error, sign_error"
        )
        feedback: str = dspy.OutputField()
        suggested_fix: str = dspy.OutputField()


    class LogicalGapJudgeSig(dspy.Signature):
        """Judge whether one proof transition is sufficiently justified and non-circular."""

        statement: str = dspy.InputField()
        required_assumptions: str = dspy.InputField()
        previous_accepted_steps: str = dspy.InputField()
        step_index: int = dspy.InputField()
        claim: str = dspy.InputField()
        justification: str = dspy.InputField()
        verdict: Literal["pass", "fail"] = dspy.OutputField()
        score: float = dspy.OutputField(desc="1.0 for pass, 0.5 for partially correct, 0.0 for fail.")
        error_type: str = dspy.OutputField(desc="none, logical_gap, missing_lemma, unsupported_generalization")
        feedback: str = dspy.OutputField()
        suggested_fix: str = dspy.OutputField()


    class ToyCaseJudgeSig(dspy.Signature):
        """Detect toy-case misuse and check consistency on supplied examples."""

        statement: str = dspy.InputField()
        toy_cases: str = dspy.InputField()
        proof: str = dspy.InputField()
        verdict: Literal["pass", "fail"] = dspy.OutputField()
        score: float = dspy.OutputField(desc="1.0 for pass, 0.5 for partially correct, 0.0 for fail.")
        error_type: str = dspy.OutputField(desc="none, toy_case_failed, toy_case_misuse")
        feedback: str = dspy.OutputField()
        suggested_fix: str = dspy.OutputField()


    class ApproximationJudgeSig(dspy.Signature):
        """Detect unsafe numerical approximations in a proof that should be symbolic."""

        statement: str = dspy.InputField()
        proof: str = dspy.InputField()
        verdict: Literal["pass", "fail"] = dspy.OutputField()
        score: float = dspy.OutputField(desc="1.0 for pass, 0.5 for partially correct, 0.0 for fail.")
        error_type: str = dspy.OutputField(desc="none, unsafe_approximation, rounding_error")
        feedback: str = dspy.OutputField()
        suggested_fix: str = dspy.OutputField()


    class ComputationJudgeSig(dspy.Signature):
        """Detect arithmetic, expansion, simplification, and algebraic rearrangement mistakes."""

        statement: str = dspy.InputField()
        proof: str = dspy.InputField()
        verdict: Literal["pass", "fail"] = dspy.OutputField()
        score: float = dspy.OutputField(desc="1.0 for pass, 0.5 for partially correct, 0.0 for fail.")
        error_type: str = dspy.OutputField(desc="none, arithmetic_error, expansion_error, rearrangement_error")
        feedback: str = dspy.OutputField()
        suggested_fix: str = dspy.OutputField()


    class ProofRepairSig(dspy.Signature):
        """Repair a failed proof using granular verifier feedback."""

        inequality_name: str = dspy.InputField()
        statement: str = dspy.InputField()
        assumptions: str = dspy.InputField()
        original_proof: str = dspy.InputField()
        verifier_feedback: str = dspy.InputField()
        repaired_proof: str = dspy.OutputField(desc="Corrected proof with numbered, justified steps.")
        final_answer: str = dspy.OutputField(desc="Exact final target relation proved.")


def _as_text(value: object) -> str:
    return "" if value is None else str(value)


def _as_score(value: object, passed: bool) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError):
        score = 1.0 if passed else 0.0
    return min(1.0, max(0.0, score))


def _verdict_passed(value: object) -> bool:
    return _as_text(value).strip().lower() in {"pass", "passed", "true", "valid", "yes"}


def _judge_result(name: str, prediction: object, details: dict | None = None) -> JudgeResult:
    passed = _verdict_passed(getattr(prediction, "verdict", "fail"))
    return JudgeResult(
        judge=name,
        passed=passed,
        score=_as_score(getattr(prediction, "score", None), passed),
        error_type=_as_text(getattr(prediction, "error_type", "none" if passed else "unknown")),
        explanation=_as_text(getattr(prediction, "feedback", "")),
        suggested_fix=_as_text(getattr(prediction, "suggested_fix", "")),
        details=details or {},
    )


def _parse_json_list(text: str) -> list:
    candidate = _as_text(text).strip()
    if candidate.startswith("```"):
        candidate = candidate.strip("`")
        if candidate.lower().startswith("json"):
            candidate = candidate[4:].strip()
    start = candidate.find("[")
    end = candidate.rfind("]")
    if start != -1 and end != -1 and end > start:
        candidate = candidate[start : end + 1]
    value = json.loads(candidate)
    return value if isinstance(value, list) else []


def _fallback_step_records(parsed: ParsedProof) -> list[ProofStep]:
    return [ProofStep(index=i, claim=step, dependencies=list(range(1, i))) for i, step in enumerate(parsed.steps, start=1)]


class IneqMathDSPyAgent(_DSPY_MODULE_BASE):
    """DSPy module wrapper for IneqMath-style proof generation, parsing, verification, and repair."""

    def __init__(self) -> None:
        local_dspy = _require_dspy()
        super().__init__()
        self.prover = local_dspy.ChainOfThought(ProofGeneratorSig)
        self.extractor = local_dspy.Predict(StructuredProofExtractorSig)
        self.final_answer_judge = local_dspy.Predict(FinalAnswerJudgeSig)
        self.assumption_judge = local_dspy.Predict(AssumptionJudgeSig)
        self.step_validity_judge = local_dspy.Predict(StepValidityJudgeSig)
        self.logical_gap_judge = local_dspy.Predict(LogicalGapJudgeSig)
        self.toy_case_judge = local_dspy.Predict(ToyCaseJudgeSig)
        self.approximation_judge = local_dspy.Predict(ApproximationJudgeSig)
        self.computation_judge = local_dspy.Predict(ComputationJudgeSig)
        self.repairer = local_dspy.ChainOfThought(ProofRepairSig)
        self.parser = ProofParser()

    def generate(self, inequality: Inequality, prompt_type: str, run_id: int) -> ProofRun:
        return self.generate_with_contract(
            inequality=inequality,
            prompt_type=prompt_type,
            run_id=run_id,
            prompt_contract=prompt_contract_for(prompt_type),
        )

    def generate_with_contract(
        self,
        inequality: Inequality,
        prompt_type: str,
        run_id: int,
        prompt_contract: str,
    ) -> ProofRun:
        prediction = self.prover(
            inequality_name=inequality.name,
            statement=inequality.statement,
            assumptions=self._assumption_text(inequality),
            proof_hint=inequality.proof_hint,
            prompt_contract=prompt_contract,
        )
        proof = _as_text(getattr(prediction, "proof", ""))
        final_answer = _as_text(getattr(prediction, "final_answer", ""))
        if final_answer and "Final Conclusion:" not in proof:
            proof = f"{proof.rstrip()}\n\nFinal Conclusion:\n{final_answer}"
        return ProofRun(
            inequality_id=inequality.id,
            prompt_type=prompt_type,
            run_id=run_id,
            prompt=prompt_contract,
            proof=proof,
        )

    def forward(
        self,
        inequality_name: str,
        statement: str,
        assumptions: str,
        proof_hint: str,
        target_relation: str,
        toy_cases: str = "[]",
        prompt_contract: str = MANUAL_OPTIMIZED_PROMPT_CONTRACT,
    ):
        local_dspy = _require_dspy()
        prediction = self.prover(
            inequality_name=inequality_name,
            statement=statement,
            assumptions=assumptions,
            proof_hint=proof_hint,
            prompt_contract=prompt_contract,
        )
        proof = _as_text(getattr(prediction, "proof", ""))
        final_answer = _as_text(getattr(prediction, "final_answer", ""))
        return local_dspy.Prediction(proof=proof, final_answer=final_answer, target_relation=target_relation, toy_cases=toy_cases)

    def repair(self, inequality: Inequality, run: ProofRun, feedback: str, repair_attempt: int) -> ProofRun:
        prediction = self.repairer(
            inequality_name=inequality.name,
            statement=inequality.statement,
            assumptions=self._assumption_text(inequality),
            original_proof=run.proof,
            verifier_feedback=feedback,
        )
        proof = _as_text(getattr(prediction, "repaired_proof", ""))
        final_answer = _as_text(getattr(prediction, "final_answer", ""))
        if final_answer and "Final Conclusion:" not in proof:
            proof = f"{proof.rstrip()}\n\nFinal Conclusion:\n{final_answer}"
        return ProofRun(
            inequality_id=inequality.id,
            prompt_type=f"{run.prompt_type}_repaired",
            run_id=run.run_id,
            prompt="DSPy ProofRepairSig",
            proof=proof,
            repaired=True,
            repair_attempts=repair_attempt,
        )

    def evaluate(self, inequality: Inequality, run: ProofRun) -> EvaluationResult:
        parsed = self.parse_proof(run.proof)
        judge_results = self._run_judges(inequality, parsed, run.proof)
        judge_results.extend(self._deterministic_boundary_checks(inequality, run.proof))
        parse_success = len(parsed.step_records or parsed.steps) >= 2
        overall_pass = parse_success and all(result.passed for result in judge_results)
        avg_score = mean(result.score for result in judge_results) if judge_results else 0.0
        step_results = [item for item in judge_results if item.judge == "step_validity"]
        step_rate = mean(1.0 if item.passed else 0.0 for item in step_results) if step_results else 0.0
        return EvaluationResult(
            inequality_id=inequality.id,
            prompt_type=run.prompt_type,
            run_id=run.run_id,
            overall_pass=overall_pass,
            average_score=avg_score,
            step_validity_rate=step_rate,
            parse_success=parse_success,
            repair_attempts=run.repair_attempts,
            judge_results=judge_results,
        )

    @staticmethod
    def _deterministic_boundary_checks(inequality: Inequality, proof: str) -> list[JudgeResult]:
        """Small deterministic guardrails for boundary cases LLM judges often miss."""
        text = proof.lower().replace("\\", "")
        results: list[JudgeResult] = []
        if inequality.id == "cauchy_schwarz":
            uses_quadratic_method = any(token in text for token in ("discriminant", "quadratic", "choose t", "parameter"))
            mentions_b_zero_case = (
                "sum b_i^2 = 0" in text
                or "sum_{i=1}^n b_i^2 = 0" in text
                or "b_i^2 = 0" in text
                or "b_i = 0" in text
                or "all b_i" in text and "= 0" in text
            )
            if uses_quadratic_method and not mentions_b_zero_case:
                results.append(
                    JudgeResult(
                        judge="boundary_case",
                        passed=False,
                        score=0.0,
                        error_type="missing_zero_vector_case",
                        explanation=(
                            "The proof uses a quadratic/discriminant-style Cauchy-Schwarz argument "
                            "without separately handling the case sum b_i^2 = 0. In that case the "
                            "quadratic coefficient can vanish, so the zero-vector case must be "
                            "settled before relying on a genuine quadratic/discriminant argument."
                        ),
                        suggested_fix=(
                            "Add a preliminary case: if sum b_i^2 = 0, then every b_i = 0 and both "
                            "sides reduce to 0. Then handle sum b_i^2 > 0 with the quadratic or "
                            "parameter argument."
                        ),
                    )
                )
        return results

    def parse_proof(self, proof: str) -> ParsedProof:
        deterministic = self.parser.parse(proof)
        try:
            prediction = self.extractor(proof=proof)
            assumptions = [str(item) for item in _parse_json_list(getattr(prediction, "assumptions_json", "[]"))]
            step_dicts = _parse_json_list(getattr(prediction, "steps_json", "[]"))
            step_records = [
                ProofStep(
                    index=int(item.get("index", index)),
                    claim=str(item.get("claim", "")),
                    justification=str(item.get("justification", "")),
                    dependencies=[int(dep) for dep in item.get("dependencies", []) if str(dep).isdigit()],
                    theorem_used=str(item.get("theorem_used", "")),
                )
                for index, item in enumerate(step_dicts, start=1)
                if isinstance(item, dict) and item.get("claim")
            ]
            conclusion = _as_text(getattr(prediction, "conclusion", "")) or deterministic.conclusion
            if step_records:
                return ParsedProof(
                    assumptions=assumptions or deterministic.assumptions,
                    steps=[f"{item.index}. {item.claim}" for item in step_records],
                    conclusion=conclusion,
                    step_records=step_records,
                )
        except Exception:
            pass
        deterministic.step_records = _fallback_step_records(deterministic)
        return deterministic

    def _run_judges(self, inequality: Inequality, parsed: ParsedProof, proof: str) -> list[JudgeResult]:
        results = [
            _judge_result(
                "final_answer",
                self.final_answer_judge(
                    statement=inequality.statement,
                    target_relation=inequality.target_relation,
                    required_assumptions=self._assumption_text(inequality),
                    conclusion=parsed.conclusion,
                    proof=proof,
                ),
            ),
            _judge_result(
                "assumption",
                self.assumption_judge(
                    statement=inequality.statement,
                    required_assumptions=self._assumption_text(inequality),
                    proof=proof,
                ),
            ),
        ]
        accepted_steps: list[str] = []
        for step in parsed.step_records or _fallback_step_records(parsed):
            validity = _judge_result(
                "step_validity",
                self.step_validity_judge(
                    statement=inequality.statement,
                    required_assumptions=self._assumption_text(inequality),
                    previous_accepted_steps="\n".join(accepted_steps),
                    step_index=step.index,
                    claim=step.claim,
                    justification=step.justification,
                    dependencies=", ".join(str(item) for item in step.dependencies),
                    theorem_used=step.theorem_used,
                ),
                {"step_index": step.index, "claim": step.claim, "justification": step.justification},
            )
            results.append(validity)
            gap = _judge_result(
                "logical_gap",
                self.logical_gap_judge(
                    statement=inequality.statement,
                    required_assumptions=self._assumption_text(inequality),
                    previous_accepted_steps="\n".join(accepted_steps),
                    step_index=step.index,
                    claim=step.claim,
                    justification=step.justification,
                ),
                {"step_index": step.index, "claim": step.claim, "justification": step.justification},
            )
            results.append(gap)
            if validity.passed and gap.passed:
                accepted_steps.append(f"{step.index}. {step.claim}")
        results.extend(
            [
                _judge_result(
                    "toy_case",
                    self.toy_case_judge(
                        statement=inequality.statement,
                        toy_cases=json.dumps(inequality.toy_cases, indent=2),
                        proof=proof,
                    ),
                ),
                _judge_result("computation", self.computation_judge(statement=inequality.statement, proof=proof)),
                _judge_result("approximation", self.approximation_judge(statement=inequality.statement, proof=proof)),
            ]
        )
        return results

    @staticmethod
    def _assumption_text(inequality: Inequality) -> str:
        return "\n".join(f"- {item}" for item in inequality.assumptions)


def prompt_contract_for(prompt_type: str) -> str:
    if prompt_type in {"optimized", "manual_optimized"}:
        return MANUAL_OPTIMIZED_PROMPT_CONTRACT.strip()
    if prompt_type in {"gepa_optimized", "dspy_gepa_optimized"}:
        return MANUAL_OPTIMIZED_PROMPT_CONTRACT.strip()
    return BASELINE_PROMPT_CONTRACT.strip()


def failed_feedback(result: EvaluationResult) -> str:
    lines = []
    for judge in result.judge_results:
        if not judge.passed:
            lines.append(f"{judge.judge}: {judge.error_type}. {judge.explanation} Suggested fix: {judge.suggested_fix}")
    return "\n".join(lines) or "No failing judge feedback."
