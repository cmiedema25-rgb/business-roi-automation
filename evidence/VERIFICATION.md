# Verification

## Offline

```bash
make verify
```

Expected:

- pytest passes
- `evidence/roi-report.json` regenerated from fixed demo scenario
- `evidence/ar-demo-report.json` regenerated from `examples/open-invoices.csv`

## Fixed demo ROI scenario

| Input | Value |
|-------|-------|
| Process | overdue invoice follow-up |
| Events / month | 200 |
| Minutes each | 8 |
| Labor $/hr | 28 |
| Build cost | 2400 |

| Output | Value (approx) |
|--------|----------------|
| Hours saved / month | 26.6667 |
| $ saved / month | 746.67 |
| Payback months | 3.21 |
| First-year return multiple | 3.73× |

## AR demo

- As-of date: `2026-09-04` (deterministic)
- 15 synthetic open invoices
- Stages: polite / firm / escalate
- Minutes saved = reminders × 8 (assumed hand-call time)
- Optional `--notify`: webhook dry-run only

## Honesty

Calculator = illustrative math. AR demo = synthetic fixtures, dry-run, no messages sent.
