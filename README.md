# PDF Beam Design Checker (v1)

Windows-local desktop-friendly tool for checking member sizes from vector PDF house drawings.

## Features implemented (v1)
- Vector PDF parsing (PyMuPDF) for:
  - schedule-like extraction (member ID + nominated size)
  - plan tag extraction (member IDs, size strings, spacing callouts)
  - scale detection via text (`SCALE 1:100` etc.)
- Cross-checking plan members vs schedule members (plan-only flagged).
- Span workflow support through user support points and scale conversion.
- Check engines:
  - LVL beams: first-principles serviceability + simple point load handling + cantilever check.
  - Timber table pipeline scaffolding: parser script to extract SmartLVL/SmartJoist PDF tables to JSON.
  - Steel: supplier-table CSV loader + smallest passing alternative lookup.
- Outputs:
  - report PDF (summary and per-member results)
  - annotated PDF overlay (pass/fail and suggested alternatives)
- JSON project model persisted through API payloads.

## File tree
- `backend/` FastAPI backend, parsing, checks, report, annotation, tests
- `frontend/` React + Vite lightweight UI
- `data/tables/` place source supplier PDFs here:
  - `SmartLVL13-Design-Guide-E1-2021 - puurged.pdf`
  - `1657438f-8675-46ce-863f-aa2f37711346.pdf`
- `data/extracted/` extracted JSON tables and steel sample CSV

## Run (Windows)
### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run start
```
Open `http://localhost:5173`.

## One-command helper (PowerShell)
```powershell
# from repo root
start powershell -NoExit "cd backend; .\.venv\Scripts\activate; uvicorn app.main:app --reload --port 8000"
start powershell -NoExit "cd frontend; npm run start"
```

## Extract Tilling tables
```bash
python backend/scripts/extract_tilling_tables.py
```
This creates/updates JSON in `data/extracted/`.

## Steel table schema
CSV columns:
- `section`
- `member_type`
- `max_span_m`
- `max_udl_kn_per_m`
- `deflection_limit` (e.g. `L/500`)
- `section_rank` (integer where lower is smaller/lighter)

Example in `data/extracted/sample_steel_tables.csv`.

## Packaging to EXE (optional)
Use PyInstaller:
```bash
pip install pyinstaller
pyinstaller --onefile --name pdf-beam-backend backend/app/main.py
```
(Usually package backend and frontend separately; production desktop packaging can use Electron/Tauri wrapper in later versions.)

## Known limitations
- Schedule extraction uses regex + block clustering, not full semantic table reconstruction.
- Geometry inference from vector lines is currently basic; manual supports/endpoints remain primary.
- Annotator currently draws on page 1 using support coordinates.
- Timber supplier-table extraction script is generic and requires tuning per table format.
- No continuous-span analysis; no partial UDL; no uplift/wind checks in v1.

## Engineering disclaimer
This tool is a preliminary checking aid. Final engineering review and signoff are required.
