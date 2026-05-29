from src.data_loader import get_inequality
from src.templates import render_prompt


def test_optimized_prompt_keeps_required_placeholders_filled():
    inequality = get_inequality("bernoulli")
    prompt = render_prompt(
        "proof_optimized.txt",
        inequality_name=inequality.name,
        inequality_statement=inequality.statement,
        assumptions="\n".join(f"- {item}" for item in inequality.assumptions),
        proof_hint=inequality.proof_hint,
    )
    assert "$inequality_name" not in prompt
    assert "Bernoulli's Inequality" in prompt
    assert "Numbered Proof Steps" in prompt
