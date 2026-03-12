# Rockstar Quality SLA Guardrails

Small Python POC for analytics-batch SLA checks aligned to the Rockstar Games Senior Analytics Engineer role.

## Scope

- classify analytics batches as `release_ready`, `retry`, or `manual_review`
- flag quality breaches and high-severity root causes
- produce stakeholder-readable markdown summaries

## Test

```bash
$env:PYTHONPATH='.'
python -m pytest --cov=src --cov-report=term-missing -q
```
