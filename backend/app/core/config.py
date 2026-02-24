from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data"
EXTRACTED_DIR = DATA_DIR / "extracted"
TABLES_DIR = DATA_DIR / "tables"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

LVL_ALLOWED_SIZES = [
    "90x45", "130x45", "150x45", "170x45", "200x45", "240x45", "300x45", "360x45", "400x45",
    "90x63", "130x63", "150x63", "170x63", "200x63", "240x63", "300x63", "360x63", "400x63", "450x63",
    "300x75", "400x75",
]

MATERIAL_DEFAULTS = {
    "lvl": {"E_MPa": 13000, "allowable_bending_MPa": 18},
    "steel": {"E_GPa": 200, "grade": "300PLUS/AS3679"},
}

LTB_WARNING_M = 2.5
