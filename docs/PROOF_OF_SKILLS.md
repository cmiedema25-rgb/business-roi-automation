# Proof of Skills — business-roi-automation

Portfolio evidence for **Rework Digital** showing how software improves business ROI.

## Skills demonstrated

| Skill | Where shown |
|-------|-------------|
| **Workflow Automation** | AR reminder pipeline: CSV in → overdue rules → staged action queue + summary (dry-run) |
| **Python** | Packaged CLI (`broi`), typed ROI math, deterministic AR engine, pytest, Makefile verify |
| **AI Integration & APIs** | Optional Slack/webhook **dry-run notifier** stub (`--notify` / `webhook.py`) — payload shaped like a real webhook, no egress required |

## What a reviewer can verify offline

1. `make verify` — tests + regenerate `evidence/roi-report.json` and `evidence/ar-demo-report.json`
2. Transparent ROI formulas in code and report JSON
3. Synthetic AR fixtures labeled `[ILLUSTRATIVE]`; no live email/Slack

## Business narrative

Manual overdue-invoice follow-up costs labor hours every month. Automating reminder staging (and measuring build cost vs savings) makes the ROI case concrete: hours and dollars saved, payback period, and first-year return multiple.
