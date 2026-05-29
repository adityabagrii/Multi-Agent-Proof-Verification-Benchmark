from __future__ import annotations

import html
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
OUTPUTS = ROOT / "outputs"
RESULTS_PATH = OUTPUTS / "verification_results.json"
OPTIMIZATION_PATH = OUTPUTS / "optimization" / "optimization_report.md"
REPORT_PATH = OUTPUTS / "final_visual_report.html"


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value))


def pct(value: float) -> str:
    return f"{value * 100:.0f}%"


def score(value: float) -> str:
    return f"{value:.2f}"


def read_results() -> list[dict]:
    if not RESULTS_PATH.exists():
        raise FileNotFoundError(f"Missing {RESULTS_PATH}. Run main.py before generating the visual report.")
    return json.loads(RESULTS_PATH.read_text(encoding="utf-8"))


def grouped_metrics(results: list[dict]) -> list[dict]:
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for item in results:
        groups[(item["inequality_id"], item["prompt_type"])].append(item)
    rows = []
    for (inequality, prompt), items in sorted(groups.items()):
        rows.append(
            {
                "inequality": inequality,
                "prompt": prompt,
                "runs": len(items),
                "parse_success": mean(1.0 if item["parse_success"] else 0.0 for item in items),
                "step_validity": mean(float(item["step_validity_rate"]) for item in items),
                "overall_pass": mean(1.0 if item["overall_pass"] else 0.0 for item in items),
                "judge_score": mean(float(item["average_score"]) for item in items),
                "repairs": mean(float(item["repair_attempts"]) for item in items),
            }
        )
    return rows


def prompt_metrics(results: list[dict]) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for item in results:
        groups[item["prompt_type"]].append(item)
    rows = []
    for prompt, items in sorted(groups.items()):
        rows.append(
            {
                "prompt": prompt,
                "runs": len(items),
                "parse_success": mean(1.0 if item["parse_success"] else 0.0 for item in items),
                "step_validity": mean(float(item["step_validity_rate"]) for item in items),
                "overall_pass": mean(1.0 if item["overall_pass"] else 0.0 for item in items),
                "judge_score": mean(float(item["average_score"]) for item in items),
            }
        )
    return rows


def judge_breakdown(results: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in results:
        for judge in item["judge_results"]:
            grouped[judge["judge"]].append(judge)
    rows = []
    for name, items in sorted(grouped.items()):
        failures = Counter(item["error_type"] for item in items if not item["passed"])
        rows.append(
            {
                "judge": name,
                "calls": len(items),
                "pass_rate": mean(1.0 if item["passed"] else 0.0 for item in items),
                "avg_score": mean(float(item["score"]) for item in items),
                "top_failures": ", ".join(f"{kind} ({count})" for kind, count in failures.most_common(3)) or "none",
            }
        )
    return rows


def optimization_summary() -> str:
    if not OPTIMIZATION_PATH.exists():
        return "<p>Prompt optimization evidence was not generated in this run.</p>"
    text = OPTIMIZATION_PATH.read_text(encoding="utf-8")
    lines = []
    capture = False
    for line in text.splitlines():
        if line.startswith("## Final Run Prompt Comparison") or line.startswith("## DSPy Optimizer Run") or line.startswith("## Optimizer Notes"):
            capture = True
            lines.append(f"<h3>{esc(line.lstrip('# ').strip())}</h3>")
            continue
        if line.startswith("## Best Prompt"):
            break
        if not capture or not line.strip():
            continue
        if line.startswith("|"):
            continue
        if line.startswith("- "):
            lines.append(f"<li>{esc(line[2:])}</li>")
        else:
            lines.append(f"<p>{esc(line)}</p>")
    return "\n".join(lines)


def file_count(pattern: str) -> int:
    return len(list(OUTPUTS.glob(pattern)))


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f"<th>{esc(header)}</th>" for header in headers)
    body = "\n".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def build_html(results: list[dict]) -> str:
    metrics = grouped_metrics(results)
    prompt_rows = prompt_metrics(results)
    judges = judge_breakdown(results)
    total_runs = len(results)
    overall_pass = mean(1.0 if item["overall_pass"] else 0.0 for item in results) if results else 0.0
    parse_success = mean(1.0 if item["parse_success"] else 0.0 for item in results) if results else 0.0
    avg_score = mean(float(item["average_score"]) for item in results) if results else 0.0
    avg_step = mean(float(item["step_validity_rate"]) for item in results) if results else 0.0

    metrics_table = render_table(
        ["Inequality", "Prompt", "Runs", "Parse Success", "Step Validity", "Overall Pass", "Avg Judge Score", "Repairs"],
        [
            [
                esc(row["inequality"]),
                esc(row["prompt"]),
                str(row["runs"]),
                pct(row["parse_success"]),
                pct(row["step_validity"]),
                pct(row["overall_pass"]),
                score(row["judge_score"]),
                score(row["repairs"]),
            ]
            for row in metrics
        ],
    )
    prompt_table = render_table(
        ["Prompt", "Runs", "Parse Success", "Step Validity", "Overall Pass", "Avg Judge Score"],
        [
            [esc(row["prompt"]), str(row["runs"]), pct(row["parse_success"]), pct(row["step_validity"]), pct(row["overall_pass"]), score(row["judge_score"])]
            for row in prompt_rows
        ],
    )
    judge_table = render_table(
        ["Judge", "Calls", "Pass Rate", "Avg Score", "Top Failure Types"],
        [[esc(row["judge"]), str(row["calls"]), pct(row["pass_rate"]), score(row["avg_score"]), esc(row["top_failures"])] for row in judges],
    )
    run_table = render_table(
        ["Run", "Inequality", "Prompt", "Pass", "Score", "Step Validity"],
        [
            [
                str(item["run_id"]),
                esc(item["inequality_id"]),
                esc(item["prompt_type"]),
                "Pass" if item["overall_pass"] else "Fail",
                score(float(item["average_score"])),
                pct(float(item["step_validity_rate"])),
            ]
            for item in results
        ],
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Agentic Inequality Proof Verification Report</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #172026;
      --muted: #5d6872;
      --line: #d9e0e7;
      --panel: #f7f9fb;
      --accent: #0f766e;
      --accent-2: #334155;
      --warn: #b45309;
      --ok: #15803d;
      --bad: #b91c1c;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: #ffffff;
      line-height: 1.5;
    }}
    header {{
      padding: 42px 56px 30px;
      border-bottom: 1px solid var(--line);
      background: linear-gradient(180deg, #eef7f6 0%, #ffffff 100%);
    }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 34px 28px 56px; }}
    h1 {{ margin: 0 0 12px; font-size: 34px; letter-spacing: 0; }}
    h2 {{ margin: 36px 0 12px; font-size: 22px; border-bottom: 1px solid var(--line); padding-bottom: 8px; }}
    h3 {{ margin: 22px 0 8px; font-size: 17px; }}
    p {{ margin: 8px 0 12px; }}
    .meta, .subtle {{ color: var(--muted); }}
    .team {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; }}
    .member {{ border: 1px solid var(--line); background: #fff; padding: 10px 12px; border-radius: 8px; min-width: 220px; }}
    .cards {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin: 20px 0 8px; }}
    .card {{ border: 1px solid var(--line); border-radius: 8px; padding: 14px; background: var(--panel); }}
    .card .label {{ color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: .04em; }}
    .card .value {{ font-size: 28px; font-weight: 700; margin-top: 4px; }}
    table {{ width: 100%; border-collapse: collapse; margin: 14px 0 22px; font-size: 14px; }}
    th, td {{ border: 1px solid var(--line); padding: 9px 10px; text-align: left; vertical-align: top; }}
    th {{ background: #eef2f7; }}
    code, pre {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    pre {{ background: #0f172a; color: #e2e8f0; padding: 14px; border-radius: 8px; overflow-x: auto; }}
    ul {{ margin-top: 8px; }}
    .deliverables li {{ margin-bottom: 6px; }}
    .badge {{ display: inline-block; padding: 2px 8px; border-radius: 999px; font-size: 12px; border: 1px solid var(--line); }}
    .ok {{ color: var(--ok); }}
    .bad {{ color: var(--bad); }}
    .note {{ border-left: 4px solid var(--accent); padding: 10px 14px; background: #f0fdfa; }}
    @media (max-width: 820px) {{ header {{ padding: 28px; }} .cards {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
  </style>
</head>
<body>
  <header>
    <h1>Agentic Inequality Proof Verification Report</h1>
    <p class="meta">DSPy IneqMath-style proof verification using precomputed Gemini proofs and NVIDIA NIM verifier agents.</p>
    <div class="team">
      <div class="member"><strong>Aditya Bagri</strong><br>Roll No. 2022029</div>
      <div class="member"><strong>Mridul Goel</strong><br>Roll No. 2022303</div>
    </div>
  </header>
  <main>
    <section>
      <h2>Executive Summary</h2>
      <p>This project evaluates generated inequality proofs with a granular agentic verifier inspired by IneqMath. Final-answer correctness alone is not treated as sufficient: each proof is decomposed into proof steps and checked for assumptions, step validity, logical gaps, toy-case misuse, computation errors, and unsafe approximations.</p>
      <div class="cards">
        <div class="card"><div class="label">Verified Runs</div><div class="value">{total_runs}</div></div>
        <div class="card"><div class="label">Parse Success</div><div class="value">{pct(parse_success)}</div></div>
        <div class="card"><div class="label">Overall Pass</div><div class="value">{pct(overall_pass)}</div></div>
        <div class="card"><div class="label">Avg Judge Score</div><div class="value">{score(avg_score)}</div></div>
      </div>
      <p class="subtle">Average step-validity rate across evaluated proofs: <strong>{pct(avg_step)}</strong>.</p>
    </section>

    <section>
      <h2>Project Deliverables</h2>
      <ul class="deliverables">
        <li><strong>Inequalities covered:</strong> Cauchy-Schwarz Inequality and Bernoulli's Inequality.</li>
        <li><strong>Proof generation evidence:</strong> Gemini outputs are stored in <code>outputs/raw_runs/</code> and loaded through the <code>precomputed</code> backend.</li>
        <li><strong>Verification architecture:</strong> DSPy modules call NVIDIA NIM for final-answer, assumption, step-validity, logical-gap, toy-case, computation, and approximation judging.</li>
        <li><strong>Prompt comparison:</strong> baseline unoptimized prompt vs manually optimized prompt.</li>
        <li><strong>Prompt optimization evidence:</strong> GEPA/BootstrapFewShot report is stored in <code>outputs/optimization/optimization_report.md</code> when optimizer execution completes.</li>
        <li><strong>Machine-readable results:</strong> aggregate JSON in <code>outputs/verification_results.json</code> and per-proof judge JSON files in <code>outputs/verified_runs/</code>.</li>
      </ul>
    </section>

    <section>
      <h2>Agent Workflow</h2>
      <ol>
        <li>Load precomputed Gemini proof variants from <code>outputs/raw_runs</code>.</li>
        <li>Parse proof assumptions, numbered steps, and final conclusion.</li>
        <li>Use a DSPy structured extractor to produce typed proof-step records.</li>
        <li>Run NVIDIA NIM verifier agents for final answer, assumptions, step validity, logical gaps, toy cases, computations, and approximations.</li>
        <li>Aggregate pass/fail, parse success, average judge score, and step-validity rate.</li>
        <li>Compare prompt variants and record GEPA prompt-optimization evidence when enabled.</li>
      </ol>
    </section>

    <section>
      <h2>Metrics By Inequality And Prompt</h2>
      {metrics_table}
    </section>

    <section>
      <h2>Prompt-Level Comparison</h2>
      {prompt_table}
    </section>

    <section>
      <h2>Judge Breakdown</h2>
      {judge_table}
    </section>

    <section>
      <h2>Per-Run Verification Results</h2>
      {run_table}
    </section>

    <section>
      <h2>Prompt Optimization Evidence</h2>
      <div class="note">
        {optimization_summary()}
      </div>
    </section>

    <section>
      <h2>Artifact Inventory</h2>
      <ul>
        <li><code>outputs/raw_runs/*.md</code>: {file_count("raw_runs/*.md")} proof files, including precomputed and repaired variants where present.</li>
        <li><code>outputs/verified_runs/*.json</code>: {file_count("verified_runs/*.json")} per-proof verification JSON files for the final aggregate run.</li>
        <li><code>outputs/verification_results.json</code>: final aggregate machine-readable verification results.</li>
        <li><code>outputs/final_submission_report.md</code>: Markdown report generated by the workflow.</li>
        <li><code>outputs/final_visual_report.html</code>: this visual report for submission.</li>
      </ul>
    </section>

    <section>
      <h2>Reproducibility</h2>
      <p>The final run used precomputed Gemini proofs, NVIDIA NIM through DSPy, two runs per inequality/prompt, no repairs, and optimizer evidence enabled.</p>
      <pre>python main.py \\
  --generation-backend precomputed \\
  --runs 2 \\
  --inequality all \\
  --prompt-type all \\
  --max-repairs 0 \\
  --run-optimizer</pre>
      <p>To regenerate this HTML report:</p>
      <pre>python scripts/generate_visual_report.py</pre>
    </section>
  </main>
</body>
</html>
"""


def main() -> None:
    results = read_results()
    REPORT_PATH.write_text(build_html(results), encoding="utf-8")
    print(REPORT_PATH)


if __name__ == "__main__":
    main()
