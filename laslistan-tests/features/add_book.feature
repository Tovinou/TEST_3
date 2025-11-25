Feature: Lägga till ny bok
  Som användare
  Vill jag kunna lägga till nya böcker
  Så att jag kan utöka katalogen

  Background:
    Given jag är på webbplatsen
    And jag är på vyn för att lägga till bok

  Scenario: Lägga till en ny bok med titel och författare
    When jag fyller i titel "Min testbok"
    And jag fyller i författare "Test Testsson"
    And jag klickar på knappen för att lägga till boken
    Then ska boken finnas i katalogen

  Scenario Outline: Lägga till flera böcker
    When jag fyller i titel "<titel>"
    And jag fyller i författare "<författare>"
    And jag klickar på knappen för att lägga till boken
    Then ska boken "<titel>" finnas i katalogen

    Examples:
      | titel                    | författare        |
      | Den gröna boken         | Anna Andersson    |
      | Äventyr i skogen        | Bengt Bengtsson   |
      | Mysteriet löses         | Cecilia Carlsson  |

  Scenario: Formuläret återställs efter tillägg
    When jag fyller i titel "Återställningstest"
    And jag fyller i författare "Test Författare"
    And jag klickar på knappen för att lägga till boken
    Then ska titelfältet vara tomt
    And ska författarfältet vara tomt

  Scenario: Lägga till bok och favoritmarkera den
    When jag lägger till en bok med titel "Ny favoritbok" och författare "Favorit Författare"
    And jag går till katalogvyn
    And jag favoritmarkerar boken "Ny favoritbok"
    And jag går till mina favoriter
    Then ska boken "Ny favoritbok" finnas i favoriterna
