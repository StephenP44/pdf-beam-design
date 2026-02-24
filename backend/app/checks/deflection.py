from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass
class BeamResult:
    delta_mm: float
    limit_mm: float
    governing: str
    passed: bool


def floor_roof_limit_mm(span_m: float) -> tuple[float, str]:
    l500 = (span_m * 1000) / 500.0
    if l500 <= 12.0:
        return l500, "L/500"
    return 12.0, "12mm cap"


def cantilever_limit_mm() -> tuple[float, str]:
    return 5.0, "cantilever 5mm"


def mm4_rect(b_mm: float, d_mm: float) -> float:
    return b_mm * d_mm**3 / 12.0


def simply_supported_udl_deflection_mm(w_kn_m: float, l_m: float, e_mpa: float, i_mm4: float) -> float:
    w_n_mm = w_kn_m
    l_mm = l_m * 1000
    return 5 * w_n_mm * (l_mm**4) / (384 * e_mpa * i_mm4)


def simply_supported_point_deflection_mm(p_kn: float, a_m: float, l_m: float, e_mpa: float, i_mm4: float) -> float:
    p_n = p_kn * 1000
    l_mm = l_m * 1000
    a_mm = a_m * 1000
    b_mm = l_mm - a_mm
    return p_n * a_mm * b_mm * (l_mm**2 - a_mm**2 - b_mm**2) / (6 * e_mpa * i_mm4 * l_mm)


def cantilever_udl_tip_deflection_mm(w_kn_m: float, l_m: float, e_mpa: float, i_mm4: float) -> float:
    w_n_mm = w_kn_m
    l_mm = l_m * 1000
    return w_n_mm * (l_mm**4) / (8 * e_mpa * i_mm4)


def cantilever_point_tip_deflection_mm(p_kn: float, l_m: float, e_mpa: float, i_mm4: float) -> float:
    p_n = p_kn * 1000
    l_mm = l_m * 1000
    return p_n * (l_mm**3) / (3 * e_mpa * i_mm4)


def total(delta_components: Iterable[float]) -> float:
    return sum(delta_components)
