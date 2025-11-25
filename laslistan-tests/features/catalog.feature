Feature: Bokkatalogens
  Som användare
  Vill jag se och interagera med bokkatalogens
  Så att jag kan välja böcker som intresserar mig

  Background:
    Given jag är på webbplatsen
    And jag är på katalogvyn

  Scenario: Visa bokkatalogens
    Then ska jag se böcker i katalogen
    And varje bok ska visa titel och författare

  Scenario: Favoritmarkera en bok
    Given det finns böcker i katalogen
    When jag klickar på en bok
    Then ska boken bli favoritmarkerad
    And boken ska visas i mina favoriter

  Scenario: Ta bort favoritmarkering
    Given jag har en favoritmarkerad bok
    When jag klickar på den favoritmarkerade boken igen
    Then ska favoritmarkeringen tas bort
    And boken ska inte visas i mina favoriter

  Scenario Outline: Hantera flera klick på samma bok
    Given det finns en bok med titeln "Kaffekokaren som visste för mycket"
    When jag klickar på boken <antal> gånger
    Then ska bokens favoritstatus vara "<status>"

    Examples:
      | antal | status            |
      | 1     | favorit           |
      | 2     | inte favorit      |
      | 3     | favorit           |
      | 4     | inte favorit      |

  Scenario: Favoritmarkera flera böcker
    Given det finns minst 3 böcker i katalogen
    When jag favoritmarkerar 3 olika böcker
    Then ska alla 3 böckerna visas i mina favoriter
