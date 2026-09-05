"""Optional Slack/webhook dry-run notifier (no network by default)."""

from __future__ import annotations

from typing import Any


def dry_run_notify(summary_text: str, webhook_url: str | None = None) -> dict[str, Any]:
    """Build a webhook payload preview without sending.

    Demonstrates an API-shaped integration point for Rework skill
    'AI Integration & APIs' without requiring credentials or egress.
    """
    return {
        "sent": False,
        "mode": "dry-run",
        "webhook_url_configured": bool(webhook_url),
        "payload": {"text": summary_text},
        "note": "Offline stub — set BROI_WEBHOOK_URL and use --notify only in trusted envs.",
    }
