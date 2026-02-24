from __future__ import annotations

import re
from typing import Dict, List

from app.checks.deflection import (
    cantilever_limit_mm,
    cantilever_point_tip_deflection_mm,
    cantilever_udl_tip_deflection_mm,
    floor_roof_limit_mm,
    mm4_rect,
    simply_supported_point_deflection_mm,
    simply_supported_udl_deflection_mm,
    total,
)
from app.core.config import LVL_ALLOWED_SIZES, MATERIAL_DEFAULTS, LTB_WARNING_M
from app.models.schemas import Member, ZoneType
from app.services.table_loader import smallest_passing_section

SIZE_RE = re.compile(r"(\d{2,3})x(\d{2,3})")


def _lvl_i(size: str) -> float:
    m = SIZE_RE.search(size)
    if not m:
        raise ValueError(f"Cannot parse LVL size: {size}")
    d, b = float(m.group(1)), float(m.group(2))
    return mm4_rect(b, d)


def check_lvl(member: Member, zone_type: ZoneType) -> Member:
    e = MATERIAL_DEFAULTS["lvl"]["E_MPa"]
    nominated = member.final_nominated_size or member.nominated_size_schedule or member.nominated_size_plan or "240x45"

    def run(size: str) -> tuple[bool, float, float, str]:
        i = _lvl_i(size)
        deltas: List[float] = [simply_supported_udl_deflection_mm(member.loads.udl_kn_per_m, member.span_m, e, i)]
        for pl in member.loads.point_loads:
            deltas.append(simply_supported_point_deflection_mm(pl.value_kn, pl.position_m, member.span_m, e, i))
        main_delta = total(deltas)
        main_limit, gov = floor_roof_limit_mm(member.span_m)

        if member.cantilever_m > 0:
            cant_delta = cantilever_udl_tip_deflection_mm(member.loads.udl_kn_per_m, member.cantilever_m, e, i)
            for pl in member.loads.point_loads:
                if abs(pl.position_m - member.span_m) < 1e-6:
                    cant_delta += cantilever_point_tip_deflection_mm(pl.value_kn, member.cantilever_m, e, i)
            cant_limit, _ = cantilever_limit_mm()
            if cant_delta > cant_limit:
                return False, cant_delta, cant_limit, "cantilever 5mm"

        return main_delta <= main_limit, main_delta, main_limit, gov

    passed, delta, limit, gov = run(nominated)
    member.computed_deflection_mm = round(delta, 3)
    member.governing_limit = gov
    member.check_result = "pass" if passed else "fail"

    if not passed:
        for size in LVL_ALLOWED_SIZES:
            ok, d2, _, _ = run(size)
            if ok:
                member.suggested_size = size
                member.computed_deflection_mm = round(d2, 3)
                break
    else:
        member.suggested_size = nominated

    return member


def check_steel_table(member: Member, steel_rows: List[Dict], deflection_limit: str = "L/500") -> Member:
    section = member.final_nominated_size or member.nominated_size_schedule or member.nominated_size_plan
    suggested = smallest_passing_section(steel_rows, member.span_m, member.loads.udl_kn_per_m, deflection_limit)
    member.suggested_size = suggested
    member.check_result = "pass" if section and suggested == section else "fail"
    if not suggested:
        member.warnings.append("No supplier table entry found; manual review required.")
    if member.cantilever_m > LTB_WARNING_M:
        member.warnings.append("Large unrestrained length entered; LTB not checked in v1.")
    return member
