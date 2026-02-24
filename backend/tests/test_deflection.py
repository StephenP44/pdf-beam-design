from app.checks.deflection import (
    cantilever_limit_mm,
    floor_roof_limit_mm,
    simply_supported_udl_deflection_mm,
    simply_supported_point_deflection_mm,
)


def test_floor_limit_small_span():
    limit, gov = floor_roof_limit_mm(3.0)
    assert round(limit, 2) == 6.0
    assert gov == "L/500"


def test_floor_limit_cap():
    limit, gov = floor_roof_limit_mm(10.0)
    assert limit == 12.0
    assert gov == "12mm cap"


def test_cantilever_limit():
    limit, gov = cantilever_limit_mm()
    assert limit == 5.0
    assert "cantilever" in gov


def test_udl_and_point_formula_positive():
    udl = simply_supported_udl_deflection_mm(1.5, 4.0, 13000, 5e7)
    pt = simply_supported_point_deflection_mm(5.0, 2.0, 4.0, 13000, 5e7)
    assert udl > 0
    assert pt > 0
