"""Accounts Receivable reminder workflow — offline deterministic dry-run."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any


# Reminder stages by days overdue (inclusive lower bound, exclusive upper for next)
# 1–14: polite, 15–29: firm, 30+: escalate
STAGE_RULES = [
    (30, "escalate"),
    (15, "firm"),
    (1, "polite"),
]

# Assumed minutes if calling each customer by hand
MANUAL_MINUTES_PER_REMINDER = 8


@dataclass
class InvoiceRow:
    invoice_id: str
    customer: str
    amount: float
    due_date: date
    days_overdue: int
    stage: str | None  # None = current (not overdue enough)


@dataclass
class ReminderAction:
    invoice_id: str
    customer: str
    amount: float
    days_overdue: int
    stage: str
    message_template: str


MESSAGE_TEMPLATES = {
    "polite": (
        "[ILLUSTRATIVE] Friendly reminder: invoice {invoice_id} for ${amount:.2f} "
        "was due {days_overdue} day(s) ago. Please remit at your convenience."
    ),
    "firm": (
        "[ILLUSTRATIVE] Follow-up: invoice {invoice_id} for ${amount:.2f} is "
        "{days_overdue} day(s) overdue. Prompt payment is appreciated."
    ),
    "escalate": (
        "[ILLUSTRATIVE] Escalation: invoice {invoice_id} for ${amount:.2f} is "
        "{days_overdue} day(s) overdue. Please contact AR to resolve immediately."
    ),
}


def stage_for_days(days_overdue: int) -> str | None:
    if days_overdue < 1:
        return None
    for threshold, stage in STAGE_RULES:
        if days_overdue >= threshold:
            return stage
    return None


def parse_date(value: str) -> date:
    return datetime.strptime(value.strip(), "%Y-%m-%d").date()


def load_invoices(csv_path: Path, as_of: date | None = None) -> list[InvoiceRow]:
    as_of = as_of or date(2026, 9, 4)  # fixed demo anchor for determinism
    rows: list[InvoiceRow] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            due = parse_date(raw["due_date"])
            days = (as_of - due).days
            rows.append(
                InvoiceRow(
                    invoice_id=raw["invoice_id"].strip(),
                    customer=raw["customer"].strip(),
                    amount=float(raw["amount"]),
                    due_date=due,
                    days_overdue=days,
                    stage=stage_for_days(days),
                )
            )
    return rows


def build_action_queue(invoices: list[InvoiceRow]) -> list[ReminderAction]:
    actions: list[ReminderAction] = []
    for inv in invoices:
        if inv.stage is None:
            continue
        tmpl = MESSAGE_TEMPLATES[inv.stage]
        msg = tmpl.format(
            invoice_id=inv.invoice_id,
            amount=inv.amount,
            days_overdue=inv.days_overdue,
        )
        actions.append(
            ReminderAction(
                invoice_id=inv.invoice_id,
                customer=inv.customer,
                amount=inv.amount,
                days_overdue=inv.days_overdue,
                stage=inv.stage,
                message_template=msg,
            )
        )
    # Deterministic order: escalate → firm → polite, then invoice_id
    order = {"escalate": 0, "firm": 1, "polite": 2}
    actions.sort(key=lambda a: (order[a.stage], a.invoice_id))
    return actions


def summarize(actions: list[ReminderAction], manual_minutes: int = MANUAL_MINUTES_PER_REMINDER) -> dict[str, Any]:
    counts = {"polite": 0, "firm": 0, "escalate": 0}
    for a in actions:
        counts[a.stage] += 1
    total = len(actions)
    minutes_saved = total * manual_minutes
    return {
        "total_reminders": total,
        "by_stage": counts,
        "manual_minutes_per_reminder": manual_minutes,
        "minutes_saved_vs_manual_calls": minutes_saved,
        "hours_saved_vs_manual_calls": round(minutes_saved / 60.0, 4),
        "note": "Synthetic dry-run; no email sent. Minutes assume hand-dial follow-up.",
    }


def run_ar_demo(
    csv_path: Path,
    as_of: date | None = None,
    webhook_dry_run: bool = False,
) -> dict[str, Any]:
    invoices = load_invoices(csv_path, as_of=as_of)
    actions = build_action_queue(invoices)
    summary = summarize(actions)
    report: dict[str, Any] = {
        "demo": "accounts_receivable_reminder_workflow",
        "mode": "dry-run",
        "as_of": (as_of or date(2026, 9, 4)).isoformat(),
        "input_csv": str(csv_path),
        "rules": {
            "polite": "days_overdue >= 1 and < 15",
            "firm": "days_overdue >= 15 and < 30",
            "escalate": "days_overdue >= 30",
        },
        "summary": summary,
        "action_queue": [asdict(a) for a in actions],
        "invoices_loaded": len(invoices),
        "invoices_current_no_reminder": sum(1 for i in invoices if i.stage is None),
    }
    if webhook_dry_run:
        report["webhook_notifier"] = {
            "enabled": True,
            "mode": "dry-run",
            "payload_preview": {
                "text": (
                    f"[broi AR demo] {summary['total_reminders']} reminders queued "
                    f"(polite={summary['by_stage']['polite']}, "
                    f"firm={summary['by_stage']['firm']}, "
                    f"escalate={summary['by_stage']['escalate']})"
                ),
                "destination": "optional Slack/webhook URL (not called)",
            },
            "note": "Optional AI Integration & APIs stub — no network call made.",
        }
    return report


def write_report(report: dict[str, Any], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
