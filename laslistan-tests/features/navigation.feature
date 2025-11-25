Feature: Navigation mellan vyer
  Som användare
  Vill jag kunna navigera mellan olika sektioner
  Så att jag kan komma åt olika funktioner

  Background:
    Given jag är på webbplatsen

  Scenario: Navigera till Katalog
    When jag klickar på "Katalog"
    Then ska jag se katalogvyn
    And jag ska se böcker i katalogen

  Scenario: Navigera till Lägg till bok
    When jag klickar på "Lägg till bok"
    Then ska jag se formuläret för att lägga till bok
    And jag ska se fält för titel och författare

  Scenario: Navigera till Mina böcker
    When jag klickar på "Mina böcker"
    Then ska jag se favoritsidan

  Scenario Outline: Navigera mellan alla vyer
    When jag klickar på "<vy>"
    Then ska jag se "<innehåll>"

    Examples:
      | vy            | innehåll                    |
      | Katalog       | böcker i katalogen          |
      | Lägg till bok | formuläret för att lägga till bok |
      | Mina böcker   | favoritsidan                |
