"""ROI calculator unit tests — fixed demo scenario."""

from broi.roi import ROIInputs, calculate_roi


def test_demo_scenario_invoice_follow_up():
    """200 invoices/mo × 8 min × $28/hr, $2,400 build."""
    r = calculate_roi(
        ROIInputs(
            process_name="overdue invoice follow-up",
            events_per_month=200,
            minutes_per_event=8,
            labor_cost_per_hour=28,
            automation_build_cost=2400,
        )
    )
    # 200 * 8 / 60 = 26.666... → rounded to 4 dp
    assert r.hours_saved_per_month == 26.6667
    # 26.6667 * 28 = 746.6676 → round to 746.67
    assert r.dollars_saved_per_month == 746.67
    assert r.payback_months == round(2400 / 746.67, 2)
    assert r.first_year_return_multiple == round((12 * 746.67) / 2400, 2)
    assert "hours_saved_per_month" in r.formulas


def test_zero_build_cost():
    r = calculate_roi(
        ROIInputs("x", 10, 6, 30, 0)
    )
    assert r.hours_saved_per_month == 1.0
    assert r.dollars_saved_per_month == 30.0
    assert r.payback_months == 0.0
    assert r.first_year_return_multiple is None
