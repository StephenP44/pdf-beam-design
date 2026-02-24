from app.services.table_loader import smallest_passing_section


ROWS = [
    {"section": "200PFC", "max_span_m": "3.0", "max_udl_kn_per_m": "2.0", "deflection_limit": "L/500", "section_rank": "1"},
    {"section": "250PFC", "max_span_m": "4.0", "max_udl_kn_per_m": "3.0", "deflection_limit": "L/500", "section_rank": "2"},
]


def test_lookup_exact_boundary():
    assert smallest_passing_section(ROWS, 3.0, 2.0, "L/500") == "200PFC"


def test_lookup_none():
    assert smallest_passing_section(ROWS, 6.0, 2.0, "L/500") is None
