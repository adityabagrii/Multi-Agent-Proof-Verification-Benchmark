from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.models import EvaluationResult, JudgeResult
from src.report_writer import write_final_report


OUTPUTS = ROOT / "outputs"
VERIFIED = OUTPUTS / "verified_runs"
PROMPTS = {"baseline_unoptimized", "manual_optimized"}


def result_from_dict(data: dict) -> EvaluationResult:
    return EvaluationResult(
        inequality_id=data["inequality_id"],
        prompt_type=data["prompt_type"],
        run_id=int(data["run_id"]),
        overall_pass=bool(data["overall_pass"]),
        average_score=float(data["average_score"]),
        step_validity_rate=float(data["step_validity_rate"]),
        parse_success=bool(data["parse_success"]),
        repair_attempts=int(data["repair_attempts"]),
        judge_results=[
            JudgeResult(
                judge=item["judge"],
                passed=bool(item["passed"]),
                score=float(item["score"]),
                error_type=item.get("error_type", "none"),
                explanation=item.get("explanation", ""),
                suggested_fix=item.get("suggested_fix", ""),
                details=item.get("details", {}),
            )
            for item in data.get("judge_results", [])
        ],
    )


def main() -> None:
    results = []
    for path in sorted(VERIFIED.glob("*.json")):
        if path.name.endswith("_repaired.json"):
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("prompt_type") not in PROMPTS:
            continue
        if int(data.get("run_id", 0)) not in {1, 2}:
            continue
        results.append(result_from_dict(data))

    if not results:
        raise RuntimeError(f"No verified run JSON files found in {VERIFIED}")

    results.sort(key=lambda item: (item.inequality_id, item.prompt_type, item.run_id))
    (OUTPUTS / "verification_results.json").write_text(
        json.dumps([item.to_dict() for item in results], indent=2),
        encoding="utf-8",
    )
    write_final_report(
        OUTPUTS / "final_submission_report.md",
        results,
        "outputs/optimization/optimization_report.md",
        generation_backend="precomputed",
    )
    print(f"Rebuilt reports from {len(results)} verified runs.")


if __name__ == "__main__":
    main()
