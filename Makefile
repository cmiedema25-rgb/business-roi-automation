.PHONY: install verify demo-roi demo-ar test clean

install:
	python3 -m pip install -e ".[dev]" -q

verify: install
	python3 -m pytest -q
	broi calculate \
	  --process "overdue invoice follow-up" \
	  --events 200 --minutes 8 --labor-rate 28 --build-cost 2400 \
	  --out evidence/roi-report.json > /dev/null
	broi run-ar-demo \
	  --input examples/open-invoices.csv \
	  --report evidence/ar-demo-report.json \
	  --notify
	@echo "VERIFY OK"
	@python3 -c "import json; r=json.load(open('evidence/roi-report.json')); print(f\"ROI: {r['hours_saved_per_month']}h/mo, \$${r['dollars_saved_per_month']}/mo, payback {r['payback_months']} mo, 1yr {r['first_year_return_multiple']}x\")"
	@python3 -c "import json; r=json.load(open('evidence/ar-demo-report.json')); s=r['summary']; print(f\"AR: {s['total_reminders']} reminders, {s['minutes_saved_vs_manual_calls']} min saved\")"

demo-roi:
	broi calculate \
	  --process "overdue invoice follow-up" \
	  --events 200 --minutes 8 --labor-rate 28 --build-cost 2400 \
	  --out evidence/roi-report.json

demo-ar:
	broi run-ar-demo --input examples/open-invoices.csv --report evidence/ar-demo-report.json --notify

test:
	python3 -m pytest -q

clean:
	rm -rf build dist *.egg-info .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
