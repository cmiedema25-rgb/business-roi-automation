"""Gradio UI for the ROI calculator."""

from __future__ import annotations

import json

from broi.roi import ROIInputs, calculate_roi


def _compute(
    process_name: str,
    events: float,
    minutes: float,
    labor: float,
    build: float,
) -> tuple[str, str, str, str, str]:
    result = calculate_roi(
        ROIInputs(
            process_name=process_name or "unnamed process",
            events_per_month=float(events),
            minutes_per_event=float(minutes),
            labor_cost_per_hour=float(labor),
            automation_build_cost=float(build or 0),
        )
    )
    hours = f"{result.hours_saved_per_month:.2f}"
    dollars = f"${result.dollars_saved_per_month:,.2f}"
    payback = (
        f"{result.payback_months:.2f} months"
        if result.payback_months is not None
        else "N/A"
    )
    multiple = (
        f"{result.first_year_return_multiple:.2f}×"
        if result.first_year_return_multiple is not None
        else "N/A (no build cost)"
    )
    detail = json.dumps(result.to_dict(), indent=2)
    return hours, dollars, payback, multiple, detail


def launch(share: bool = False) -> None:
    import gradio as gr

    with gr.Blocks(title="Business ROI Automation") as demo:
        gr.Markdown(
            "# Business ROI Automation\n"
            "Illustrative calculator — enter process metrics to estimate "
            "hours/$ saved, payback, and first-year return multiple.\n\n"
            "*Formulas are transparent and shown in the JSON detail panel.*"
        )
        with gr.Row():
            process = gr.Textbox(
                label="Process name",
                value="overdue invoice follow-up",
            )
        with gr.Row():
            events = gr.Number(label="Events per month", value=200)
            minutes = gr.Number(label="Minutes of manual work each", value=8)
            labor = gr.Number(label="Labor cost $/hour", value=28)
            build = gr.Number(label="Automation build cost $ (optional)", value=2400)
        btn = gr.Button("Calculate ROI", variant="primary")
        with gr.Row():
            out_hours = gr.Textbox(label="Hours saved / month")
            out_dollars = gr.Textbox(label="$ saved / month")
            out_payback = gr.Textbox(label="Payback months")
            out_multiple = gr.Textbox(label="First-year return multiple")
        detail = gr.Code(label="Full result (JSON + formulas)", language="json")
        btn.click(
            _compute,
            inputs=[process, events, minutes, labor, build],
            outputs=[out_hours, out_dollars, out_payback, out_multiple, detail],
        )
        gr.Markdown(
            "### Demo scenario (pre-filled)\n"
            "200 invoices/mo × 8 min × $28/hr, $2,400 build cost — "
            "matches `evidence/roi-report.json`."
        )

    demo.launch(share=share)


if __name__ == "__main__":
    launch()
