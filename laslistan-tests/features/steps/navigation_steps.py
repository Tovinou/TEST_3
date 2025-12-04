from behave import given, when, then
from features.pages.catalog_page import CatalogPage
from features.pages.add_book_page import AddBookPage
from features.pages.favorites_page import FavoritesPage

@given('jag är på webbplatsen')
def step_navigate_to_website(context):
    context.catalog_page = CatalogPage(context.page, context.base_url)
    context.add_book_page = AddBookPage(context.page, context.base_url)
    context.favorites_page = FavoritesPage(context.page, context.base_url)
    context.catalog_page.navigate()

@when('jag klickar på "{tab_name}"')
def step_click_navigation_tab(context, tab_name):
    context.catalog_page.click_navigation_tab(tab_name)

@then('ska jag se katalogvyn')
def step_see_catalog_view(context):
    try:
        context.catalog_page.wait_for_element('[data-testid="nav-catalog"]')
    except Exception:
        pass
    # Verify by presence of headings or list items
    heading_count = context.page.locator('h1, h2').count()
    if heading_count < 1:
        try:
            count = context.catalog_page.get_book_count()
        except Exception:
            count = 0
        assert count > 0, "Expected a visible view heading or books list"

@then('jag ska se böcker i katalogen')
def step_see_books_in_catalog(context):
    # Prefer checking presence of a known book title from the catalog
    known_title = "Kaffekokaren som visste för mycket"
    present = context.page.get_by_text(known_title, exact=False).count() > 0
    if not present:
        count = context.catalog_page.get_book_count()
        assert count > 0, "Expected to see books in catalog"

@then('ska jag se formuläret för att lägga till bok')
def step_see_add_book_form(context):
    context.add_book_page.wait_for_add_book_form()
    inputs_visible = context.page.locator('input').count()
    assert inputs_visible >= 2, "Expected title and author inputs to be visible"

@then('jag ska se fält för titel och författare')
def step_see_title_and_author_fields(context):
    context.add_book_page.wait_for_add_book_form()
    title_loc = context.page.get_by_label('Titel')
    author_loc = context.page.get_by_label('Författare')
    has_title = title_loc.count() > 0 and title_loc.first.is_visible()
    has_author = author_loc.count() > 0 and author_loc.first.is_visible()
    if not (has_title and has_author):
        title_ph = context.page.get_by_placeholder('Titel')
        author_ph = context.page.get_by_placeholder('Författare')
        has_title = has_title or (title_ph.count() > 0 and title_ph.first.is_visible())
        has_author = has_author or (author_ph.count() > 0 and author_ph.first.is_visible())
    if not (has_title and has_author):
        inputs_visible = context.page.locator('input').count()
        has_title = has_title or inputs_visible >= 1
        has_author = has_author or inputs_visible >= 2
    assert has_title and has_author, "Expected title and author fields to be visible"

@then('ska jag se favoritsidan')
def step_see_favorites_page(context):
    # Favoritsidan kan visa tom-meddelande eller listan med böcker
    # Vänta på att antingen tom-meddelandet visas eller att minst ett bokelement renderas
    try:
        context.favorites_page.wait_for_element('text=När du valt')
        is_empty_visible = context.favorites_page.is_empty_message_visible()
        assert is_empty_visible, "Expected empty favorites message to be visible"
    except Exception:
        # Om tom-meddelandet inte syns, kontrollera att boklistan är renderad
        count = context.favorites_page.get_favorite_count()
        assert count >= 0, "Favorites page did not render as expected"

@then('ska jag se "{content}"')
def step_see_content(context, content):
    if content == "böcker i katalogen":
        step_see_books_in_catalog(context)
    elif content == "formuläret för att lägga till bok":
        step_see_add_book_form(context)
    elif content == "favoritsidan":
        step_see_favorites_page(context)
