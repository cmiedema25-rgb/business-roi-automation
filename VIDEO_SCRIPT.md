# VIDEO_SCRIPT — ~2 minute screen demo

**Tone:** professional, realistic. No fake customer logos. Label data **illustrative** where needed.

---

## 0:00–0:15 — Hook

- Open README in the repo.
- Say: “This is a Rework portfolio proof: a transparent ROI calculator plus a runnable Accounts Receivable reminder workflow — offline dry-run.”

## 0:15–0:55 — ROI calculator (demo numbers)

- Terminal:

```bash
broi calculate \
  --process "overdue invoice follow-up" \
  --events 200 --minutes 8 --labor-rate 28 --build-cost 2400 \
  --out evidence/roi-report.json
```

- Point at JSON: hours/month, $/month, payback months, first-year multiple.
- Optional: `broi ui` — show Gradio with the same pre-filled demo; click Calculate; flash the ROI card fields.
- Say: “Formulas are in the report — illustrative math for planning, not audited accounting.”

## 0:55–1:35 — AR automation dry-run

- Show `examples/open-invoices.csv` (synthetic names, illustrative).
- Run:

```bash
broi run-ar-demo \
  --input examples/open-invoices.csv \
  --report evidence/ar-demo-report.json \
  --notify
```

- Open the report: action queue by stage (polite / firm / escalate), summary counts, minutes saved vs calling by hand.
- Mention `--notify` webhook stub is dry-run only — no email/Slack sent.

## 1:35–2:00 — ROI card close

- Side-by-side or quick cut: calculator outputs + AR “minutes saved” summary.
- Close: “Software turns a repetitive AR follow-up process into a measurable ROI case — calculator for the business case, automation demo for the workflow.”
- End on repo URL and `make verify`.
