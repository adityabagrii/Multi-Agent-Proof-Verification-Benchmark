from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Inequality:
    id: str
    name: str
    statement: str
    assumptions: list[str]
    target_relation: str
    proof_hint: str
    toy_cases: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ProofRun:
    inequality_id: str
    prompt_type: str
    run_id: int
    prompt: str
    proof: str
    repaired: bool = False
    repair_attempts: int = 0


@dataclass
class ParsedProof:
    assumptions: list[str]
    steps: list[str]
    conclusion: str
    step_records: list["ProofStep"] = field(default_factory=list)


@dataclass
class ProofStep:
    index: int
    claim: str
    justification: str = ""
    dependencies: list[int] = field(default_factory=list)
    theorem_used: str = ""


@dataclass
class JudgeResult:
    judge: str
    passed: bool
    score: float
    error_type: str = "none"
    explanation: str = ""
    suggested_fix: str = ""
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluationResult:
    inequality_id: str
    prompt_type: str
    run_id: int
    overall_pass: bool
    average_score: float
    step_validity_rate: float
    parse_success: bool
    repair_attempts: int
    judge_results: list[JudgeResult]

    def to_dict(self) -> dict[str, Any]:
        return {
            "inequality_id": self.inequality_id,
            "prompt_type": self.prompt_type,
            "run_id": self.run_id,
            "overall_pass": self.overall_pass,
            "average_score": round(self.average_score, 4),
            "step_validity_rate": round(self.step_validity_rate, 4),
            "parse_success": self.parse_success,
            "repair_attempts": self.repair_attempts,
            "judge_results": [
                {
                    "judge": result.judge,
                    "passed": result.passed,
                    "score": round(result.score, 4),
                    "error_type": result.error_type,
                    "explanation": result.explanation,
                    "suggested_fix": result.suggested_fix,
                    "details": result.details,
                }
                for result in self.judge_results
            ],
        }
