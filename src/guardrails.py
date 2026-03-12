def evaluate_sla_batch(batch, dry_run=False):
    reasons = []

    if batch.get("quality_breaches", 0) > 0:
        reasons.append("Quality threshold breached for analytics batch.")

    if batch.get("root_cause_severity") == "high":
        reasons.append("High-severity root cause requires manual review.")

    freshness_minutes = batch.get("freshness_minutes", 0)
    if reasons:
        decision = "manual_review"
    elif freshness_minutes > 10:
        decision = "retry"
        reasons.append("Freshness SLA missed; retry before release.")
    else:
        decision = "release_ready"
        reasons.append("Analytics SLA guardrails passed.")

    return {
        "decision": decision,
        "dry_run": dry_run,
        "reasons": reasons,
    }


def summarize_batch_decisions(rows):
    summary = {"release_ready": 0, "retry": 0, "manual_review": 0}
    for row in rows:
        decision = row.get("decision")
        if decision in summary:
            summary[decision] += 1
    return summary


def render_markdown_report(dataset_name, result):
    lines = [
        f"# Rockstar Analytics SLA Report: {dataset_name}",
        "",
        f"- Decision: `{result['decision']}`",
        f"- Dry run: `{result['dry_run']}`",
        "- Reasons:",
    ]
    for reason in result["reasons"]:
        lines.append(f"  - {reason}")
    return "\n".join(lines)
