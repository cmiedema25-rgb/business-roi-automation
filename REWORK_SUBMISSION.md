# REWORK_SUBMISSION — paste pack

## Category

**Workflow Automation**

## Skills (select)

1. **Workflow Automation**
2. **Python**
3. **AI Integration & APIs** (optional webhook/Slack dry-run notifier stub)

## Project title

business-roi-automation

## One-line

ROI calculator + Accounts Receivable reminder automation dry-run — proof that software improves business ROI.

## Paste description (short)

```
Business ROI Automation is a Rework Digital portfolio proof with two parts:

1) ROI Calculator (CLI + Gradio) — enter process name, events/month, minutes each,
   labor $/hr, and optional build cost. Transparent formulas output hours saved,
   $ saved, payback months, and first-year return multiple.

2) Runnable AR reminder workflow — synthetic open-invoices CSV → overdue staging
   rules (polite / firm / escalate) → action queue JSON + minutes saved vs hand calls.
   Offline deterministic dry-run; no email sent. Optional --notify webhook stub
   (dry-run) for an API integration shape.

Honest scope: illustrative ROI math; synthetic AR fixtures.
Verify offline with: make verify
Repo: https://github.com/cmiedema25-rgb/business-roi-automation
```

## Paste description (longer, optional)

```
Problem: teams know automation “saves time” but struggle to show dollars, payback,
and year-one return — and reviewers want more than a spreadsheet.

Solution: a packaged Python tool (broi) that (A) calculates automation ROI with
explicit formulas and retained JSON evidence, and (B) runs a realistic Accounts
Receivable reminder workflow against synthetic invoices so the proof is runnable,
not just a calculator.

Demo scenario retained in evidence/roi-report.json:
200 overdue-invoice follow-ups/month × 8 minutes × $28/hr, $2,400 build cost →
~26.7 hours/month, ~$747/month, ~3.2 months payback, ~3.7× first-year return.

AR demo: examples/open-invoices.csv → evidence/ar-demo-report.json with staged
reminders and summary counts. Optional webhook dry-run notifier for AI Integration
& APIs adjacency without requiring network credentials.

Stack: Python 3.10+, Gradio UI, pytest, Makefile verify, GitHub Actions CI, MIT.
```

## Links

- Public repo: https://github.com/cmiedema25-rgb/business-roi-automation
- Evidence: `evidence/roi-report.json`, `evidence/ar-demo-report.json`, `evidence/VERIFICATION.md`
- Video script: `VIDEO_SCRIPT.md`
- Skills proof: `docs/PROOF_OF_SKILLS.md`
