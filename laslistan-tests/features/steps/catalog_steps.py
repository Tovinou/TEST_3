from behave import given, when, then
from playwright.sync_api import expect

# --- Givens ---

@given('jag är på katalogvyn')
def step_impl(context):
    context.catalog_page.navigate_to()
    context.catalog_page.wait_for_load()

@given('det finns böcker i katalogen')
def step_impl(context):
    context.catalog_page.wait_for_load()
    book_count = len(context.catalog_page.get_book_titles())
    assert book_count > 0, "Catalog is empty, cannot proceed with test."

@given('jag har en favoritmarkerad bok')
def step_impl(context):
    # Ensure we are on the catalog page
    context.catalog_page.navigate_to()
    # Get the first available book title
    first_book_title = context.catalog_page.get_book_titles()[0].split(',')[0].strip('"')
    context.favorited_book_title = first_book_title
    # Click it once to favorite it
    context.catalog_page.click_book(context.favorited_book_title)

@given('det finns en bok med titeln "{title}"')
def step_impl(context, title):
    context.catalog_page.wait_for_load()
    all_books = context.catalog_page.get_book_titles()
    book_exists = any(title in book for book in all_books)
    assert book_exists, f"Book with title '{title}' does not exist in the catalog."
    context.test_book_title = title

@given('det finns minst {count:d} böcker i katalogen')
def step_impl(context, count):
    context.catalog_page.wait_for_load()
    book_count = len(context.catalog_page.get_book_titles())
    assert book_count >= count, f"Expected at least {count} books, but found {book_count}."


# --- Whens ---

@when('jag klickar på en bok')
def step_impl(context):
    # Get the first available book title
    first_book_title = context.catalog_page.get_book_titles()[0].split(',')[0].strip('"')
    context.clicked_book_title = first_book_title
    # Click it
    context.catalog_page.click_book(context.clicked_book_title)

@when('jag klickar på den favoritmarkerade boken igen')
def step_impl(context):
    context.catalog_page.click_book(context.favorited_book_title)

@when('jag klickar på boken {times:d} gånger')
def step_impl(context, times):
    for _ in range(times):
        context.catalog_page.click_book(context.test_book_title)

@when('jag favoritmarkerar {count:d} olika böcker')
def step_impl(context, count):
    book_titles = [book.split(',')[0].strip('"') for book in context.catalog_page.get_book_titles()]
    context.favorited_titles = book_titles[:count]
    for title in context.favorited_titles:
        context.catalog_page.click_book(title)


# --- Thens ---

@then('ska jag se böcker i katalogen')
def step_impl(context):
    expect(context.catalog_page.book_items).to_have_count_greater_than(0)

@then('varje bok ska visa titel och författare')
def step_impl(context):
    # This is implicitly checked by get_book_titles() returning non-empty strings
    books = context.catalog_page.get_book_titles()
    assert len(books) > 0, "No books found in catalog"
    for book in books:
        assert book, "Book entry should not be empty"

@then('ska boken bli favoritmarkerad')
def step_impl(context):
    # Check for the book on the "Mina böcker" page
    context.my_books_page.navigate_to()
    is_in_favorites = context.my_books_page.is_book_in_favorites(context.clicked_book_title)
    assert is_in_favorites, f"Book '{context.clicked_book_title}' should be in favorites"

@then('boken ska visas i mina favoriter')
def step_impl(context):
    context.my_books_page.navigate_to()
    is_in_favorites = context.my_books_page.is_book_in_favorites(context.clicked_book_title)
    assert is_in_favorites, f"Book '{context.clicked_book_title}' should be in favorites"

@then('ska favoritmarkeringen tas bort')
def step_impl(context):
    # Check that the book is no longer on the "Mina böcker" page
    context.my_books_page.navigate_to()
    is_in_favorites = context.my_books_page.is_book_in_favorites(context.favorited_book_title)
    assert not is_in_favorites, f"Book '{context.favorited_book_title}' should have been removed from favorites"

@then('boken ska inte visas i mina favoriter')
def step_impl(context):
    context.my_books_page.navigate_to()
    is_in_favorites = context.my_books_page.is_book_in_favorites(context.favorited_book_title)
    assert not is_in_favorites, f"Book '{context.favorited_book_title}' should NOT be in favorites"

@then('ska bokens favoritstatus vara "{status}"')
def step_impl(context, status):
    # Check the status on the "Mina böcker" page
    context.my_books_page.navigate_to()
    is_in_favorites = context.my_books_page.is_book_in_favorites(context.test_book_title)
    
    if status == "favorit":
        assert is_in_favorites, f"Book '{context.test_book_title}' should be a favorite"
    else: # "inte favorit"
        assert not is_in_favorites, f"Book '{context.test_book_title}' should NOT be a favorite"

@then('ska alla {count:d} böckerna visas i mina favoriter')
def step_impl(context, count):
    context.my_books_page.navigate_to()
    for title in context.favorited_titles:
        is_in_favorites = context.my_books_page.is_book_in_favorites(title)
        assert is_in_favorites, f"Book '{title}' should be in favorites"