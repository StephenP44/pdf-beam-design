from __future__ import annotations

from typing import Tuple


def parse_scale(scale: str) -> int:
    _, rhs = scale.split(":")
    return int(rhs)


def span_from_points(p1: Tuple[float, float], p2: Tuple[float, float], scale: str = "1:100") -> float:
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dist_mm_on_page = (dx ** 2 + dy ** 2) ** 0.5
    return dist_mm_on_page * parse_scale(scale) / 1000.0
