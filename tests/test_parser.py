from src.proof_parser import ProofParser


def test_parser_extracts_numbered_steps_and_conclusion():
    proof = """Assumptions:
- x >= -1

Numbered Proof Steps:
1. First step.
2. Second step.

Final Conclusion:
Therefore target."""
    parsed = ProofParser().parse(proof)
    assert parsed.assumptions == ["x >= -1"]
    assert len(parsed.steps) == 2
    assert parsed.conclusion == "Therefore target."
