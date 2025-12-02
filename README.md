# Läslistan - Test Automation Project

Detta projekt innehåller automatiserade tester för webbapplikationen "Läslistan" (https://tap-vt25-testverktyg.github.io/exam--reading-list/).

## Vad har testats

### Funktionalitet som täcks av testerna:

1. **Navigation**
   - Navigering mellan olika vyer (Katalog, Lägg till bok, Mina böcker)
   - Verifiering att rätt innehåll visas i varje vy

2. **Katalog-funktionalitet**
   - Visa böcker i katalogen
   - Favoritmarkera böcker (klicka en gång)
   - Ta bort favoritmarkering (klicka två gånger)
   - Hantera flera klick på samma bok

3. **Lägg till bok**
   - Lägga till en ny bok med titel och författare
   - Validering av formulärfält
   - Verifiering att den nya boken visas i katalogen
   - Testa att lägga till flera böcker

4. **Mina böcker (Favoriter)**
   - Visa tom favoritlista initialt
   - Visa favoritmarkerade böcker
   - Ta bort böcker från favoriter
   - Hantera flera favoriter

## Teknisk stack

- **Python 3.x**
- **Playwright** - Browser automation
- **behave** - BDD framework (Gherkin)

## Installation

1. Klona projektet:
\`\`\`bash
git clone https://github.com/Tovinou/TEST_3.git
cd TEST_3
\`\`\`

1. Skapa en virtuell miljö (rekommenderas):
\`\`\`bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
\`\`\`

3. Installera dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. Installera Playwright browsers:
\`\`\`bash
playwright install
\`\`\`

## Hur man startar projektet

### Kör alla tester

\`\`\`bash
behave
\`\`\`

### Kör tester med synlig webbläsare (för debugging)

```bash
behave -D headless=false
```

### Kör tester med synlig webbläsare (Windows PowerShell)

- Kör från repo-roten (`c:\Jensen\python\TEST_3`):
```powershell
$env:PYTHONPATH='laslistan-tests'; behave laslistan-tests/features -D headless=false
```

- Kör inne i testkatalogen (`c:\Jensen\python\TEST_3\laslistan-tests`):
```powershell
$env:PYTHONPATH='.'; behave features -D headless=false
```
\`\`\`

### Kör specifik feature

\`\`\`bash
behave features/catalog.feature
\`\`\`

### Kör med detaljerad output

\`\`\`bash
behave -v
\`\`\`

### Generera HTML-rapport (om allure är installerat)

\`\`\`bash
behave -f allure_behave.formatter:AllureFormatter -o reports/
allure serve reports/
\`\`\`

## Projektstruktur

\`\`\`
laslistan-tests/
├── features/
│   ├── catalog.feature          # Tester för katalog-funktionalitet
│   ├── add_book.feature         # Tester för att lägga till böcker
│   ├── favorites.feature        # Tester för favorit-funktionalitet
│   └── navigation.feature       # Tester för navigation
├── features/steps/
│   ├── catalog_steps.py         # Step definitions för katalog
│   ├── add_book_steps.py        # Step definitions för lägg till bok
│   ├── favorites_steps.py       # Step definitions för favoriter
│   └── navigation_steps.py      # Step definitions för navigation
├── features/pages/
│   ├── base_page.py             # Bas page object
│   ├── catalog_page.py          # Page object för katalog
│   ├── add_book_page.py         # Page object för lägg till bok
│   └── favorites_page.py        # Page object för favoriter
├── features/environment.py      # Behave hooks och setup
├── README.md                    # Denna fil
├── STORIES.md                   # User stories
└── requirements.txt             # Python dependencies
\`\`\`

## Testresultat

Alla tester ska vara gröna vid inlämning. Om något test misslyckas, kontrollera att:
- Webbsidan är tillgänglig
- Playwright browsers är installerade
- Du har aktiverat den virtuella miljön

## Författare

[Komlan Tovinou]

## Datum

2025-12-01
 
## Snabbstart (Windows PowerShell)

- Kör från repo-roten (`c:\Jensen\python\TEST_3`):
```powershell
$env:PYTHONPATH='laslistan-tests'; behave laslistan-tests/features -D headless=true
```

- Kör inne i testkatalogen (`c:\Jensen\python\TEST_3\laslistan-tests`):
```powershell
$env:PYTHONPATH='.'; behave features -D headless=true
```
