"""Transparent ROI math for process automation (illustrative)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ROIInputs:
    process_name: str
    events_per_month: float
    minutes_per_event: float
    labor_cost_per_hour: float
    automation_build_cost: float = 0.0


@dataclass(frozen=True)
class ROIResult:
    process_name: str
    events_per_month: float
    minutes_per_event: float
    labor_cost_per_hour: float
    automation_build_cost: float
    hours_saved_per_month: float
    dollars_saved_per_month: float
    payback_months: float | None
    first_year_return_multiple: float | None
    formulas: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def calculate_roi(inputs: ROIInputs) -> ROIResult:
    """Compute hours/$ saved, payback, and first-year return multiple.

    Formulas (transparent):
      hours_saved/mo = events × minutes / 60
      $ saved/mo     = hours_saved × labor_$/hr
      payback months = build_cost / $ saved/mo   (None if no savings or no build cost)
      1yr multiple   = (12 × $ saved/mo) / build_cost  (None if build_cost == 0)
    """
    hours = (inputs.events_per_month * inputs.minutes_per_event) / 60.0
    dollars = hours * inputs.labor_cost_per_hour
    build = inputs.automation_build_cost

    if dollars > 0 and build > 0:
        payback: float | None = build / dollars
        multiple: float | None = (12.0 * dollars) / build
    elif build == 0 and dollars > 0:
        payback = 0.0
        multiple = None  # infinite / N/A when no build cost
    else:
        payback = None
        multiple = None

    formulas = {
        "hours_saved_per_month": "events_per_month × minutes_per_event / 60",
        "dollars_saved_per_month": "hours_saved_per_month × labor_cost_per_hour",
        "payback_months": "automation_build_cost / dollars_saved_per_month",
        "first_year_return_multiple": "(12 × dollars_saved_per_month) / automation_build_cost",
    }

    return ROIResult(
        process_name=inputs.process_name,
        events_per_month=inputs.events_per_month,
        minutes_per_event=inputs.minutes_per_event,
        labor_cost_per_hour=inputs.labor_cost_per_hour,
        automation_build_cost=build,
        hours_saved_per_month=round(hours, 4),
        dollars_saved_per_month=round(dollars, 2),
        payback_months=round(payback, 2) if payback is not None else None,
        first_year_return_multiple=round(multiple, 2) if multiple is not None else None,
        formulas=formulas,
    )
