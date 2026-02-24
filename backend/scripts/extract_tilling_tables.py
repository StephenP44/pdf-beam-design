"""Extract simplified supplier tables from SmartLVL and SmartJoist PDFs into JSON.

This v1 parser pulls row-like text blocks containing spans/sizes and stores normalized records.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "data" / "tables"
OUT = ROOT / "data" / "extracted"
OUT.mkdir(parents=True, exist_ok=True)

SPAN_RE = re.compile(r"(\d+\.\d{1,2})")
SIZE_RE = re.compile(r"(\d{2,3}x\d{2,3}|[A-Z]+\d+)")
SPACING_RE = re.compile(r"(300|450|600)")


def extract_rows(pdf_path: Path):
    rows = []
    doc = fitz.open(pdf_path)
    for page_idx, page in enumerate(doc):
        for b in page.get_text("blocks"):
            text = " ".join(str(b[4]).split())
            if not text:
                continue
            span = SPAN_RE.search(text)
            size = SIZE_RE.search(text)
            spacing = SPACING_RE.search(text)
            if span and size:
                rows.append(
                    {
                        "page": page_idx + 1,
                        "raw": text,
                        "size": size.group(1),
                        "max_span_m": float(span.group(1)),
                        "spacing_mm": int(spacing.group(1)) if spacing else None,
                    }
                )
    return rows


def main():
    mappings = {
        "SmartLVL13-Design-Guide-E1-2021 - puurged.pdf": "smartlvl13_tables.json",
        "1657438f-8675-46ce-863f-aa2f37711346.pdf": "smartjoist_tables.json",
    }
    for src, out_name in mappings.items():
        src_path = TABLES / src
        if not src_path.exists():
            print(f"Skipping missing source: {src_path}")
            continue
        rows = extract_rows(src_path)
        (OUT / out_name).write_text(json.dumps({"source": src, "rows": rows}, indent=2))
        print(f"Wrote {out_name} with {len(rows)} rows")


if __name__ == "__main__":
    main()
