from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app.models.schemas import ProjectState


def generate_report(project: ProjectState, output_path: Path) -> Path:
    c = canvas.Canvas(str(output_path), pagesize=A4)
    y = 800
    c.drawString(40, y, f"Project: {project.project_name}")
    y -= 20
    c.drawString(40, y, f"Input hash: {project.input_pdf_hash}")
    y -= 20
    c.drawString(40, y, f"Scale input: {project.scale_input}; detected: {project.scale_detected}")
    y -= 20
    c.drawString(40, y, "Assumptions: simply supported, single span, serviceability-focused checks.")
    y -= 30

    for m in project.members:
        if y < 100:
            c.showPage()
            y = 800
        c.drawString(40, y, f"{m.id} | {m.type} | span={m.span_m:.2f}m | result={m.check_result}")
        y -= 15
        c.drawString(50, y, f"nominated={m.final_nominated_size or m.nominated_size_schedule or m.nominated_size_plan}, suggested={m.suggested_size}")
        y -= 15
        c.drawString(50, y, f"defl={m.computed_deflection_mm}mm, governing={m.governing_limit}, zone={m.zone_id}")
        y -= 20

    c.drawString(40, 60, "Disclaimer: Engineering review required.")
    c.save()
    return output_path
