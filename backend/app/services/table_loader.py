from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, List


def load_json(path: Path) -> Dict:
    return json.loads(path.read_text())


def load_steel_table_csv(path: Path) -> List[Dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def smallest_passing_section(rows: List[Dict], span_m: float, udl_kn_per_m: float, deflection_limit: str) -> str | None:
    candidates = [
        r for r in rows
        if float(r["max_span_m"]) >= span_m
        and float(r["max_udl_kn_per_m"]) >= udl_kn_per_m
        and r["deflection_limit"] == deflection_limit
    ]
    candidates.sort(key=lambda r: float(r.get("section_rank", 9999)))
    return candidates[0]["section"] if candidates else None
