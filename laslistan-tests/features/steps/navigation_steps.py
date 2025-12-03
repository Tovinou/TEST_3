from behave import given, when, then
from playwright.sync_api import expect

@given('jag är på webbplatsen')
def step_impl(context):
    # This is handled by environment.py, but we can add a check here.
    expect(context.page).to_have_url("https://tap-vt25-testverktyg.github.io/exam--reading-list/")

@when('jag klickar på "{tab_name}"')
def step_impl(context, tab_name):
    if tab_name == "Katalog":
        context.catalog_page.navigate_to()
    elif tab_name == "Lägg till bok":
        context.add_book_page.navigate_to()
    elif tab_name == "Mina böcker":
        context.my_books_page.navigate_to()
    else:
        raise ValueError(f"Unknown navigation tab: {tab_name}")

@then('ska jag se "{content}"')
def step_impl(context, content):
    if content == "böcker i katalogen":
        context.catalog_page.wait_for_load()
        expect(context.catalog_page.book_items).to_have_count_greater_than(0)
    elif content == "formuläret för att lägga till bok":
        context.add_book_page.wait_for_form()
        expect(context.add_book_page.title_input).to_be_visible()
        expect(context.add_book_page.author_input).to_be_visible()
    elif content == "favoritsidan":
        # The favorites page can be empty or have books
        # We check for the presence of either the empty message or a book item
        try:
            expect(context.my_books_page.empty_list_message).to_be_visible()
        except AssertionError:
            expect(context.my_books_page.favorite_book_items).to_have_count_greater_than(0)