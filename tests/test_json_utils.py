from src.json_utils import safe_json_loads


def test_safe_json_loads_repairs_latex_backslashes():
    raw = r'''```json
{
  "passed": false,
  "score": 0.4,
  "explanation": "The proof says \(x \ge 0\), which is stronger than required."
}
```'''
    parsed = safe_json_loads(raw)
    assert parsed["passed"] is False
    assert parsed["score"] == 0.4
    assert "\\ge" in parsed["explanation"]
