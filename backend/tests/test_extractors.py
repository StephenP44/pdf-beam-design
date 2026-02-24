from app.services.pdf_parser import detect_scale, extract_plan_tags, extract_schedule, TextToken


def test_schedule_extraction_fixture_like():
    tokens = [TextToken(1, "MEMBER SCHEDULE B1 240x45 LVL", (0, 0, 1, 1))]
    schedule = extract_schedule(tokens)
    assert "B1" in schedule
    assert schedule["B1"]["nominated_size"] == "240x45 LVL"


def test_plan_tag_spacing_extraction_fixture_like():
    tokens = [TextToken(1, "B1 240x45 LVL @450 ctrs", (0, 0, 1, 1))]
    tags = extract_plan_tags(tokens)
    assert tags[0]["id"] == "B1"
    assert tags[0]["spacing_mm"] == 450


def test_scale_detect():
    tokens = [TextToken(1, "SCALE 1:100", (0, 0, 1, 1))]
    assert detect_scale(tokens) == "1:100"
