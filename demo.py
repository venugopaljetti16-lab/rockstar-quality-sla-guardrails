from src.guardrails import evaluate_sla_batch, render_markdown_report


if __name__ == "__main__":
    result = evaluate_sla_batch(
        {
            "freshness_minutes": 8,
            "quality_breaches": 0,
            "root_cause_severity": "low",
        },
        dry_run=True,
    )
    print(render_markdown_report("game-health-engagement", result))
