"""AR reminder workflow tests — deterministic offline."""

from pathlib import Path

from broi.ar_demo import run_ar_demo, stage_for_days

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "examples" / "open-invoices.csv"


def test_stage_rules():
    assert stage_for_days(0) is None
    assert stage_for_days(-1) is None
    assert stage_for_days(1) == "polite"
    assert stage_for_days(14) == "polite"
    assert stage_for_days(15) == "firm"
    assert stage_for_days(29) == "firm"
    assert stage_for_days(30) == "escalate"
    assert stage_for_days(90) == "escalate"


def test_ar_demo_runs_and_counts():
    report = run_ar_demo(CSV)
    assert report["mode"] == "dry-run"
    assert report["invoices_loaded"] == 15
    s = report["summary"]
    assert s["total_reminders"] == sum(s["by_stage"].values())
    assert s["minutes_saved_vs_manual_calls"] == s["total_reminders"] * 8
    assert len(report["action_queue"]) == s["total_reminders"]
    # Every action has a stage message
    for a in report["action_queue"]:
        assert a["stage"] in ("polite", "firm", "escalate")
        assert "[ILLUSTRATIVE]" in a["message_template"]


def test_webhook_dry_run_flag():
    report = run_ar_demo(CSV, webhook_dry_run=True)
    assert "webhook_notifier" in report
    assert report["webhook_notifier"]["mode"] == "dry-run"
