# Agile Helper – Pytest + Playwright

Det här är det enda projektet för inlämning. Fokus är snabba, rena tester av `Agile Helper` utan onödiga väntningar.

**Målsättning**
- Kör alla tester på under 5 sekunder.
- Inga 10s‑timeouts, inga manuella `sleep`, inga `try/except` i normala testfall.

**Teknik**
- `Python`
- `Playwright`
- `pytest`

**Installation**
- `python -m venv venv && venv\Scripts\activate`
- `pip install -r requirements.txt`
- `playwright install`

**Köra tester**
- Snabb körning: `pytest -q tests/test_agile_helper.py`
- Visa webbläsaren: `pytest -q tests/test_agile_helper.py --headed --browser chromium`
- Mäta total tid (PowerShell): `Measure-Command { pytest -q tests/test_agile_helper.py } | % { $_.TotalSeconds }`

**Struktur**
- `tests/test_agile_helper.py` innehåller de bedömda testerna.

**GitHub Actions**
- Workflow `.github/workflows/run-tests.yml` kör enbart pytest‑sviten för att garantera <5s total tid.

**Kontakt**
- Författare: Komlan Tovinou
