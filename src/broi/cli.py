"""CLI entrypoint: broi calculate | run-ar-demo | ui."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from broi.ar_demo import run_ar_demo, write_report
from broi.roi import ROIInputs, calculate_roi
from broi.webhook import dry_run_notify


def cmd_calculate(args: argparse.Namespace) -> int:
    result = calculate_roi(
        ROIInputs(
            process_name=args.process,
            events_per_month=args.events,
            minutes_per_event=args.minutes,
            labor_cost_per_hour=args.labor_rate,
            automation_build_cost=args.build_cost,
        )
    )
    data = result.to_dict()
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {out}")
    print(json.dumps(data, indent=2))
    return 0


def cmd_run_ar_demo(args: argparse.Namespace) -> int:
    csv_path = Path(args.input)
    if not csv_path.exists():
        print(f"Input CSV not found: {csv_path}", file=sys.stderr)
        return 1
    report = run_ar_demo(csv_path, webhook_dry_run=args.notify)
    if args.notify:
        text = report.get("webhook_notifier", {}).get("payload_preview", {}).get("text", "")
        notify = dry_run_notify(text, webhook_url=None)
        report["webhook_call"] = notify
    out = Path(args.report)
    write_report(report, out)
    print(f"Wrote {out}")
    s = report["summary"]
    print(
        f"Reminders: {s['total_reminders']} "
        f"(polite={s['by_stage']['polite']}, firm={s['by_stage']['firm']}, "
        f"escalate={s['by_stage']['escalate']}); "
        f"minutes saved vs manual: {s['minutes_saved_vs_manual_calls']}"
    )
    return 0


def cmd_ui(_args: argparse.Namespace) -> int:
    from broi.ui import launch

    launch()
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="broi",
        description="Business ROI Automation — calculator + AR reminder dry-run",
    )
    sub = p.add_subparsers(dest="command", required=True)

    c = sub.add_parser("calculate", help="Compute process automation ROI")
    c.add_argument("--process", required=True, help="Process name")
    c.add_argument("--events", type=float, required=True, help="Events per month")
    c.add_argument("--minutes", type=float, required=True, help="Minutes of manual work each")
    c.add_argument("--labor-rate", type=float, required=True, help="Labor cost $/hour")
    c.add_argument("--build-cost", type=float, default=0.0, help="Optional automation build cost $")
    c.add_argument("--out", default=None, help="Write JSON report path")
    c.set_defaults(func=cmd_calculate)

    a = sub.add_parser("run-ar-demo", help="Run AR reminder workflow dry-run")
    a.add_argument("--input", required=True, help="Open invoices CSV path")
    a.add_argument(
        "--report",
        default="evidence/ar-demo-report.json",
        help="Output JSON report path",
    )
    a.add_argument(
        "--notify",
        action="store_true",
        help="Include optional webhook dry-run notifier stub",
    )
    a.set_defaults(func=cmd_run_ar_demo)

    u = sub.add_parser("ui", help="Launch Gradio ROI calculator UI")
    u.set_defaults(func=cmd_ui)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
