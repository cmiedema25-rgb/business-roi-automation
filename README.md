# business-roi-automation

**Rework Digital portfolio proof** — show how software improves business ROI.

Two-in-one:

| Piece | What it does |
|-------|----------------|
| **A) ROI Calculator** | CLI + Gradio UI: hours saved, $ saved, payback months, first-year return multiple |
| **B) AR reminder demo** | Offline Accounts Receivable workflow: CSV → stage rules → action queue JSON (dry-run) |

Honest scope: the calculator is **illustrative math**; the AR demo uses **synthetic fixtures** and does **not** send email.

Repo: https://github.com/cmiedema25-rgb/business-roi-automation

---

## Reviewer 60-second table

| Step | Command / action | Expect |
|------|------------------|--------|
| 1 | `make verify` | pytest green; regenerates `evidence/*.json` |
| 2 | Open `evidence/roi-report.json` | Demo: ~26.67 h/mo, ~$746.67/mo, ~3.21 mo payback, ~3.73× yr-1 |
| 3 | Open `evidence/ar-demo-report.json` | Reminder counts by stage + minutes saved vs hand calls |
| 4 | Optional UI | `broi ui` → Gradio calculator with same demo defaults |

---

## Quick start

```bash
python3 -m pip install -e ".[dev]"
make verify
```

### ROI calculator (CLI)

```bash
broi calculate \
  --process "overdue invoice follow-up" \
  --events 200 --minutes 8 --labor-rate 28 --build-cost 2400 \
  --out evidence/roi-report.json
```

**Formulas**

- `hours_saved/mo = events × minutes / 60`
- `$ saved/mo = hours_saved × labor_$/hr`
- `payback months = build_cost / $ saved/mo`
- `1yr return multiple = (12 × $ saved/mo) / build_cost`

### AR automation dry-run

```bash
broi run-ar-demo \
  --input examples/open-invoices.csv \
  --report evidence/ar-demo-report.json \
  --notify
```

Rules (as-of date fixed for determinism: `2026-09-04`):

| Days overdue | Stage |
|--------------|--------|
| 1–14 | polite |
| 15–29 | firm |
| 30+ | escalate |

`--notify` adds an **optional webhook dry-run stub** (no network call) for an API-shaped integration point.

### Gradio UI

```bash
broi ui
```

---

## Project layout

```
src/broi/          # roi.py, ar_demo.py, cli.py, ui.py, webhook.py
examples/          # synthetic open-invoices.csv
evidence/          # retained JSON reports + VERIFICATION.md
docs/PROOF_OF_SKILLS.md
VIDEO_SCRIPT.md
REWORK_SUBMISSION.md
```

## License

MIT
