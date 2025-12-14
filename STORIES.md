# User Stories – Agile Helper

## US-1: Läsa om Sprint planning
Som besökare vill jag kunna läsa om hur jag planerar en sprint, så att vi håller oss till ämnet på mötet.

Acceptanskriterier:
- Jag klickar på knappen “Första”.
- Jag klickar på knappen som innehåller texten “Sprint planning”.
- En rubrik med texten “Sprint planning” visas.

### US-1: Navigera mellan vyer
**Som** användare  
**Vill jag** kunna navigera mellan olika sektioner av webbplatsen  
**Så att** jag kan komma åt olika funktioner

**Acceptanskriterier:**
- Jag kan klicka på "Katalog" för att se bokkatalogens
- Jag kan klicka på "Lägg till bok" för att komma till formuläret
- Jag kan klicka på "Mina böcker" för att se mina favoriter
- Den aktiva vyn markeras tydligt i navigationen

---

## Katalog

### US-2: Visa bokkatalogens
**Som** användare  
**Vill jag** se en lista med tillgängliga böcker  
**Så att** jag kan välja böcker som intresserar mig

**Acceptanskriterier:**
- Jag ser en lista med böcker när jag öppnar katalogen
- Varje bok visar titel och författare
- Böckerna visas i en tydlig struktur

### US-3: Favoritmarkera bok
**Som** användare  
**Vill jag** kunna markera böcker som favoriter  
**Så att** jag kan spara böcker jag vill läsa senare

**Acceptanskriterier:**
- Jag kan klicka på en bok för att favoritmarkera den
- Den favoritmarkerade boken får en visuell indikation (t.ex. annan bakgrundsfärg)
- Den favoritmarkerade boken visas i "Mina böcker"

### US-4: Ta bort favoritmarkering
**Som** användare  
**Vill jag** kunna ta bort en favoritmarkering  
**Så att** jag kan ändra mig om vilka böcker jag vill spara

**Acceptanskriterier:**
- Jag kan klicka på en favoritmarkerad bok för att ta bort favoritmarkeringen
- Boken återgår till sitt ursprungliga utseende
- Boken försvinner från "Mina böcker"

### US-5: Hantera flera klick på samma bok
**Som** användare  
**Vill jag** att systemet hanterar flera klick på samma bok korrekt  
**Så att** jag kan lägga till och ta bort favoriter upprepade gånger

**Acceptanskriterier:**
- Första klicket: Boken markeras som favorit
- Andra klicket: Favoritmarkeringen tas bort
- Tredje klicket: Boken markeras som favorit igen
- Mönstret fortsätter för fler klick

---

## Lägg till bok

### US-6: Lägga till ny bok
**Som** användare  
**Vill jag** kunna lägga till nya böcker till katalogen  
**Så att** jag kan utöka listan med böcker som inte finns där redan

**Acceptanskriterier:**
- Jag ser ett formulär med fält för "Titel" och "Författare"
- Jag kan fylla i båda fälten
- Jag kan klicka på "Lägg till ny bok"-knappen
- Den nya boken visas i katalogen efter att jag lagt till den

### US-7: Validera bokformulär
**Som** användare  
**Vill jag** få feedback om jag försöker lägga till en ofullständig bok  
**Så att** jag vet att båda fälten behöver fyllas i

**Acceptanskriterier:**
- Jag kan inte lägga till en bok utan titel
- Jag kan inte lägga till en bok utan författare
- Formuläret ger tydlig feedback om vad som saknas

### US-8: Lägga till flera böcker
**Som** användare  
**Vill jag** kunna lägga till flera böcker efter varandra  
**Så att** jag kan bygga upp min katalog

**Acceptanskriterier:**
- Efter att ha lagt till en bok kan jag lägga till ytterligare en
- Alla böcker jag lägger till visas i katalogen
- Formuläret återställs efter varje tilläggning

---

## US-2: Endast Daily standup mitt i sprinten
Som beställare vill jag att bara Daily standup ska finnas som alternativ mitt i sprinten, så att teamen håller fokus.

Acceptanskriterier:
- Jag klickar på knappen “mitt i”.
- Jag ser en knapp för “Daily standup”.
- Jag ser inga andra mötesval (t.ex. Sprint planning/Review/Retro/Backlog).

### US-9: Visa tom favoritlista
**Som** ny användare  
**Vill jag** se ett meddelande när jag inte har några favoriter  
**Så att** jag förstår att jag behöver välja böcker först

**Acceptanskriterier:**
- När jag öppnar "Mina böcker" utan att ha valt favoriter ser jag ett meddelande
- Meddelandet förklarar att jag behöver välja böcker från katalogen

### US-10: Visa favoritmarkerade böcker
**Som** användare  
**Vill jag** se alla böcker jag har favoritmarkerat  
**Så att** jag har en samlad vy över mina valda böcker

**Acceptanskriterier:**
- Alla böcker jag favoritmarkerat i katalogen visas här
- Böckerna visar titel och författare
- Listan uppdateras automatiskt när jag lägger till eller tar bort favoriter

### US-11: Ta bort favoriter från listan
**Som** användare  
**Vill jag** kunna ta bort böcker från mina favoriter  
**Så att** jag kan rensa i min lista

**Acceptanskriterier:**
- Jag kan klicka på en bok i "Mina böcker" för att ta bort den från favoriter
- Boken försvinner från listan
- Boken är inte längre markerad som favorit i katalogen

### US-12: Hantera flera favoriter
**Som** användare  
**Vill jag** kunna ha flera favoriter samtidigt  
**Så att** jag kan spara flera böcker jag vill läsa

**Acceptanskriterier:**
- Jag kan favoritmarkera flera böcker
- Alla visas i "Mina böcker"
- Jag kan ta bort dem individuellt

---

## US-3: Se startsidans fråga
Som besökare vill jag se frågan “Vilken dag under sprinten är det?” när jag öppnar sidan, så att jag kan välja dag.

Acceptanskriterier:
- Texten “Vilken dag under sprinten är det?” är synlig på startsidan.

Totalt: **12 user stories** som täcker all grundläggande funktionalitet i Läslistan-applikationen.

Kategorier:
- Navigation: 1 story
- Katalog: 4 stories
- Lägg till bok: 3 stories
- Mina böcker (Favoriter): 4 stories
 
