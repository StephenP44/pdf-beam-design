from __future__ import annotations

from pathlib import Path

import fitz

from app.models.schemas import ProjectState


def annotate_pdf(input_pdf: Path, project: ProjectState, output_pdf: Path) -> Path:
    doc = fitz.open(input_pdf)
    for member in project.members:
        if not member.supports:
            continue
        page = doc[0]
        p1 = member.supports[0]
        p2 = member.supports[-1]
        color = (0, 0.7, 0) if member.check_result == "pass" else (1, 0, 0)
        page.draw_line((p1[0], p1[1]), (p2[0], p2[1]), color=color, width=2)
        label = f"{member.id}: {member.check_result.upper()}"
        if member.check_result == "fail" and member.suggested_size:
            label += f" Suggest: {member.suggested_size}"
        page.insert_text((p1[0], p1[1] - 8), label, color=color, fontsize=8)
    doc.save(output_pdf)
    return output_pdf
