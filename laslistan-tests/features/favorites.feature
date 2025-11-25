Feature: Hantera favoriter
  Som användare
  Vill jag kunna se och hantera mina favoritböcker
  Så att jag har koll på vilka böcker jag vill läsa

  Background:
    Given jag är på webbplatsen

  Scenario: Visa tom favoritlista
    Given jag inte har några favoriter
    When jag går till mina favoriter
    Then ska jag se ett meddelande om att välja böcker

  Scenario: Visa favoritmarkerade böcker
    Given jag har favoritmarkerat en bok i katalogen
    When jag går till mina favoriter
    Then ska den favoritmarkerade boken visas i listan

  Scenario: Ta bort favorit från favoritsidan
    Given jag har en bok i mina favoriter
    When jag klickar på boken i favoritsidan
    Then ska boken tas bort från favoriter
    And jag ska se ett meddelande om att välja böcker om det inte finns fler favoriter

  Scenario: Hantera flera favoriter
    Given jag är på katalogvyn
    When jag favoritmarkerar 3 olika böcker
    And jag går till mina favoriter
    Then ska jag se 3 böcker i favoriterna
    When jag tar bort en favorit
    Then ska jag se 2 böcker i favoriterna
