import unittest

from src.guardrails import (
    evaluate_sla_batch,
    render_markdown_report,
    summarize_batch_decisions,
)


class GuardrailTests(unittest.TestCase):
    def test_manual_review_when_quality_breach_and_root_cause_severity_are_high(self):
        batch = {
            "freshness_minutes": 6,
            "quality_breaches": 2,
            "root_cause_severity": "high",
        }

        result = evaluate_sla_batch(batch, dry_run=False)

        self.assertEqual(result["decision"], "manual_review")
        self.assertIn("quality", " ".join(result["reasons"]).lower())

    def test_summary_counts_release_states(self):
        rows = [
            {"decision": "release_ready"},
            {"decision": "retry"},
            {"decision": "manual_review"},
            {"decision": "release_ready"},
        ]

        self.assertEqual(
            summarize_batch_decisions(rows),
            {"release_ready": 2, "retry": 1, "manual_review": 1},
        )

    def test_retry_when_freshness_sla_is_missed_without_quality_breach(self):
        batch = {
            "freshness_minutes": 15,
            "quality_breaches": 0,
            "root_cause_severity": "low",
        }

        result = evaluate_sla_batch(batch, dry_run=True)

        self.assertEqual(result["decision"], "retry")
        self.assertTrue(result["dry_run"])
        self.assertIn("retry", " ".join(result["reasons"]).lower())

    def test_markdown_report_lists_decision_and_reason(self):
        result = {
            "decision": "release_ready",
            "dry_run": True,
            "reasons": ["Analytics SLA guardrails passed."],
        }

        report = render_markdown_report("daily-game-health", result)

        self.assertIn("# Rockstar Analytics SLA Report: daily-game-health", report)
        self.assertIn("`release_ready`", report)
        self.assertIn("Analytics SLA guardrails passed.", report)


if __name__ == "__main__":
    unittest.main()
