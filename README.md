# business-roi-automation

Two small tools for ops math and AR follow-up dry-runs:

| Piece | What it does |
|-------|----------------|
| **ROI calculator** | CLI + Gradio: hours saved, $ saved, payback months, first-year return multiple |
| **AR reminder demo** | CSV → stage rules → action queue JSON (offline dry-run, no email sent) |

## Quick start

```bash
python3 -m pip install -e ".[dev]"
make verify
```

### ROI calculator

```bash
broi calculate \
  --process "overdue invoice follow-up" \
  --events 200 --minutes 8 --labor-rate 28 --build-cost 2400 \
  --out evidence/roi-report.json
```

- `hours_saved/mo = events × minutes / 60`
- `$ saved/mo = hours_saved × labor_$/hr`
- `payback months = build_cost / $ saved/mo`
- `1yr return multiple = (12 × $ saved/mo) / build_cost`

### AR dry-run

```bash
broi run-ar-demo \
  --input examples/open-invoices.csv \
  --report evidence/ar-demo-report.json \
  --notify
```

Stages (as-of `2026-09-04` for determinism): 1–14 polite, 15–29 firm, 30+ escalate. `--notify` is a webhook-shaped stub with no network call.

### UI

```bash
broi ui
```

## Layout

```text
src/broi/     # roi, ar_demo, cli, ui
examples/     # synthetic invoices
evidence/     # retained reports
```

## License

MIT
