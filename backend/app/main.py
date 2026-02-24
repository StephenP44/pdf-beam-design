from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, File, UploadFile

from app.checks.member_checker import check_lvl, check_steel_table
from app.core.config import OUTPUT_DIR
from app.models.schemas import Member, MemberType, ProjectState, RunCheckRequest, RunCheckResponse
from app.reporting.annotator import annotate_pdf
from app.reporting.report_generator import generate_report
from app.services.pdf_parser import detect_scale, extract_plan_tags, extract_schedule, extract_text_tokens, pdf_hash
from app.services.table_loader import load_steel_table_csv

app = FastAPI(title="PDF Beam Design Checker")


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/parse")
async def parse_pdf(file: UploadFile = File(...), scale_input: str = "1:100"):
    target = OUTPUT_DIR / file.filename
    target.write_bytes(await file.read())
    tokens = extract_text_tokens(target)
    schedule = extract_schedule(tokens)
    tags = extract_plan_tags(tokens)
    detected = detect_scale(tokens)

    members = []
    seen = set()
    for row in tags:
        mid = row["id"]
        if mid in seen:
            continue
        seen.add(mid)
        sched = schedule.get(mid, {})
        members.append(
            Member(
                id=mid,
                type=MemberType.LVL_BEAM if (row.get("size") or "").lower().find("lvl") >= 0 else MemberType.STEEL,
                nominated_size_plan=row.get("size"),
                nominated_size_schedule=sched.get("nominated_size"),
                supports=[[row["bbox"][0], row["bbox"][1]], [row["bbox"][2], row["bbox"][1]]],
                warnings=[] if sched else ["Plan-only member; requires manual schedule entry."],
            )
        )

    project = ProjectState(
        input_pdf_hash=pdf_hash(target),
        scale_input=scale_input,
        scale_detected=detected,
        warnings=[] if not detected or detected == scale_input else [f"Detected scale {detected} differs from user scale {scale_input}"],
        members=members,
    )
    return project.model_dump()


@app.post("/run", response_model=RunCheckResponse)
def run_checks(req: RunCheckRequest):
    steel_data_path = Path("data/extracted/sample_steel_tables.csv")
    steel_rows = load_steel_table_csv(steel_data_path) if steel_data_path.exists() else []

    for idx, m in enumerate(req.project.members):
        if m.span_m <= 0 and len(m.supports) >= 2:
            m.span_m = abs(m.supports[-1][0] - m.supports[0][0]) * 0.1 / 1000
        if m.type == MemberType.LVL_BEAM:
            req.project.members[idx] = check_lvl(m, zone_type="floor")
        elif m.type == MemberType.STEEL:
            req.project.members[idx] = check_steel_table(m, steel_rows)

    report_path = OUTPUT_DIR / "report.pdf"
    annotated_path = OUTPUT_DIR / "annotated.pdf"
    source_pdf = OUTPUT_DIR / "input.pdf"
    if not source_pdf.exists():
        import fitz

        doc = fitz.open()
        doc.new_page(width=595, height=842)
        doc.save(source_pdf)

    generate_report(req.project, report_path)
    annotate_pdf(source_pdf, req.project, annotated_path)
    return RunCheckResponse(project=req.project, report_path=str(report_path), annotated_pdf_path=str(annotated_path))
