from __future__ import annotations

import re

from .models import ParsedProof


STEP_PATTERN = re.compile(
    r"^\s*(?:[-*]\s*)?(?:\*\*)?(?:Step\s*)?(\d+)[\.\)]\s*(.*?)(?:\*\*)?\s*$",
    re.IGNORECASE,
)


class ProofParser:
    def parse(self, proof: str) -> ParsedProof:
        assumptions = self._extract_assumptions(proof)
        steps = self._extract_numbered_steps(proof)
        if not steps:
            steps = self._fallback_sentence_steps(proof)
        conclusion = self._extract_conclusion(proof)
        return ParsedProof(assumptions=assumptions, steps=steps, conclusion=conclusion)

    @staticmethod
    def _extract_assumptions(proof: str) -> list[str]:
        match = re.search(
            r"Assumptions:\s*(.*?)(?:\n\s*\n|Proof Strategy:|Numbered Proof Steps:)",
            proof,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if not match:
            return []
        lines = [line.strip(" -\t") for line in match.group(1).splitlines()]
        return [line for line in lines if line]

    @staticmethod
    def _extract_numbered_steps(proof: str) -> list[str]:
        steps: list[str] = []
        current: list[str] = []
        current_number: str | None = None

        for line in proof.splitlines():
            match = STEP_PATTERN.match(line)
            if match:
                if current:
                    steps.append(" ".join(current).strip())
                current_number = match.group(1)
                current = [f"{current_number}. {match.group(2).strip()}"]
            elif current:
                stripped = line.strip()
                if stripped and not re.match(r"^[A-Za-z ]+:\s*$", stripped):
                    current.append(stripped)
        if current:
            steps.append(" ".join(current).strip())
        return steps

    @staticmethod
    def _fallback_sentence_steps(proof: str) -> list[str]:
        text = re.sub(r"\s+", " ", proof).strip()
        if not text:
            return []
        pieces = re.split(r"(?<=[.!?])\s+", text)
        return [piece.strip() for piece in pieces if piece.strip()]

    @staticmethod
    def _extract_conclusion(proof: str) -> str:
        match = re.search(r"Final Conclusion:\s*(.*)$", proof, flags=re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        sentences = ProofParser._fallback_sentence_steps(proof)
        return sentences[-1] if sentences else ""
