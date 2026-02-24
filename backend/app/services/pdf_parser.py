from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List



SCALE_RE = re.compile(r"(?:SCALE\s*)?(\d\s*:\s*\d+)", re.IGNORECASE)
MEMBER_TAG_RE = re.compile(r"\b([A-Z]{1,3}\d{1,3})\b")
SIZE_RE = re.compile(r"\b(\d{2,3}\s?[xX]\s?\d{2,3}(?:\s?LVL|\s?MGP10)?|\d{2,3}(?:UB|UC|PFC)\d+(?:\.\d+)?)\b")
SPACING_RE = re.compile(r"@\s?(\d{3,4})|\b(\d{3,4})\s?(?:c/c|ctrs|centres)\b", re.IGNORECASE)


@dataclass
class TextToken:
    page: int
    text: str
    bbox: tuple


def pdf_hash(pdf_path: Path) -> str:
    return hashlib.sha256(pdf_path.read_bytes()).hexdigest()


def extract_text_tokens(pdf_path: Path) -> List[TextToken]:
    tokens: List[TextToken] = []
    import fitz
    doc = fitz.open(pdf_path)
    for page_idx, page in enumerate(doc):
        blocks = page.get_text("blocks")
        for b in blocks:
            x0, y0, x1, y1, text, *_ = b
            cleaned = " ".join(text.split())
            if cleaned:
                tokens.append(TextToken(page=page_idx + 1, text=cleaned, bbox=(x0, y0, x1, y1)))
    return tokens


def detect_scale(tokens: List[TextToken]) -> str | None:
    for token in tokens:
        m = SCALE_RE.search(token.text)
        if m:
            return m.group(1).replace(" ", "")
    return None


def extract_schedule(tokens: List[TextToken]) -> Dict[str, Dict]:
    schedule = {}
    for t in tokens:
        if "schedule" in t.text.lower() or MEMBER_TAG_RE.search(t.text):
            ids = MEMBER_TAG_RE.findall(t.text)
            sizes = SIZE_RE.findall(t.text)
            if ids and sizes:
                for mid in ids:
                    schedule[mid] = {
                        "id": mid,
                        "nominated_size": sizes[0],
                        "sheet_ref": t.page,
                        "notes": "auto-extracted",
                    }
    return schedule


def extract_plan_tags(tokens: List[TextToken]) -> List[Dict]:
    rows = []
    for t in tokens:
        ids = MEMBER_TAG_RE.findall(t.text)
        if not ids:
            continue
        size = SIZE_RE.search(t.text)
        spacing = SPACING_RE.search(t.text)
        for mid in ids:
            rows.append(
                {
                    "id": mid,
                    "size": size.group(1) if size else None,
                    "sheet_ref": t.page,
                    "bbox": t.bbox,
                    "spacing_mm": int(next(g for g in spacing.groups() if g)) if spacing else None,
                }
            )
    return rows
