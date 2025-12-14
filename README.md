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
- `pytest -q tests/test_agile_helper.py`

**Struktur**
- `tests/test_agile_helper.py` innehåller de bedömda testerna.
- `laslistan-tests/` finns kvar som legacy, men är inte del av den bedömda sviten.

**GitHub Actions**
- Push till main/feature‑branch triggar workflow i `.github/workflows/run-tests.yml`.

**Kontakt**
- Författare: Komlan Tovinou
