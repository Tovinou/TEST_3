from behave import given, when, then

@given('jag är på katalogvyn')
def step_navigate_to_catalog(context):
    context.catalog_page.click_navigation_tab("Katalog")

@then('varje bok ska visa titel och författare')
def step_books_show_title_and_author(context):
    books = context.catalog_page.get_all_books()
    assert len(books) > 0, "No books found"
    
    for book in books:
        text = book.text_content()
        assert len(text) > 0, "Book should have text content"

@given('det finns böcker i katalogen')
def step_books_exist_in_catalog(context):
    count = context.catalog_page.get_book_count()
    if count == 0:
        context.catalog_page.inject_book("Seedbok 1", "Test Författare")
        count = context.catalog_page.get_book_count()
    assert count > 0, "Expected books in catalog"
    context.initial_book_count = count

@when('jag klickar på en bok')
def step_click_a_book(context):
    books = context.catalog_page.get_all_books()
    first_book = books[0]
    context.clicked_book_title = first_book.text_content().split(',')[0].strip('"')
    context.catalog_page.click_book(context.clicked_book_title)

@then('ska boken bli favoritmarkerad')
def step_book_should_be_favorited(context):
    is_favorited = context.catalog_page.is_book_favorited(context.clicked_book_title)
    assert is_favorited, f"Book '{context.clicked_book_title}' should be favorited"

@then('boken ska visas i mina favoriter')
def step_book_in_favorites(context):
    context.catalog_page.click_navigation_tab("Mina böcker")
    is_in_favorites = context.favorites_page.is_book_in_favorites(context.clicked_book_title)
    assert is_in_favorites, f"Book '{context.clicked_book_title}' should be in favorites"
    context.catalog_page.click_navigation_tab("Katalog")

@given('jag har en favoritmarkerad bok')
def step_have_favorited_book(context):
    books = context.catalog_page.get_all_books()
    first_book = books[0]
    context.favorited_book_title = first_book.text_content().split(',')[0].strip('"')
    context.catalog_page.click_book(context.favorited_book_title)

@when('jag klickar på den favoritmarkerade boken igen')
def step_click_favorited_book_again(context):
    context.catalog_page.click_book(context.favorited_book_title)

@then('ska favoritmarkeringen tas bort')
def step_favorite_removed(context):
    is_favorited = context.catalog_page.is_book_favorited(context.favorited_book_title)
    assert not is_favorited, f"Book '{context.favorited_book_title}' should not be favorited"

@then('boken ska inte visas i mina favoriter')
def step_book_not_in_favorites(context):
    context.catalog_page.click_navigation_tab("Mina böcker")
    
    # Check if empty message is shown OR book is not in list
    if context.favorites_page.is_empty_message_visible():
        # Empty message shown - good, no favorites
        pass
    else:
        # Check that the book is not in favorites
        is_in_favorites = context.favorites_page.is_book_in_favorites(context.favorited_book_title)
        assert not is_in_favorites, f"Book '{context.favorited_book_title}' should not be in favorites"
    
    context.catalog_page.click_navigation_tab("Katalog")

@given('det finns en bok med titeln "{title}"')
def step_book_exists_with_title(context, title):
    is_in_catalog = context.catalog_page.is_book_in_catalog(title)
    if not is_in_catalog:
        context.catalog_page.inject_book(title, "Okänd Författare")
        is_in_catalog = context.catalog_page.is_book_in_catalog(title)
    assert is_in_catalog, f"Book '{title}' not found in catalog"
    context.test_book_title = title

@when('jag klickar på boken {times:d} gånger')
def step_click_book_multiple_times(context, times):
    context.catalog_page.click_book_multiple_times(context.test_book_title, times)

@then('ska bokens favoritstatus vara "{status}"')
def step_check_favorite_status(context, status):
    is_favorited = context.catalog_page.is_book_favorited(context.test_book_title)
    
    if status == "favorit":
        assert is_favorited, f"Book should be favorited after clicks"
    else:  # "inte favorit"
        assert not is_favorited, f"Book should not be favorited after clicks"

@given('det finns minst {count:d} böcker i katalogen')
def step_at_least_n_books(context, count):
    book_count = context.catalog_page.get_book_count()
    while book_count < count:
        idx = book_count + 1
        context.catalog_page.inject_book(f"Seedbok {idx}", f"Författare {idx}")
        book_count = context.catalog_page.get_book_count()
    assert book_count >= count, f"Expected at least {count} books, found {book_count}"

@when('jag favoritmarkerar {count:d} olika böcker')
def step_favorite_n_books(context, count):
    books = context.catalog_page.get_all_books()
    while len(books) < count:
        idx = len(books) + 1
        context.add_book_page.click_navigation_tab("Lägg till bok")
        context.add_book_page.wait_for_add_book_form()
        context.add_book_page.add_book(f"Seedbok {idx}", f"Författare {idx}")
        context.catalog_page.click_navigation_tab("Katalog")
        books = context.catalog_page.get_all_books()

    context.favorited_titles = []
    for i in range(count):
        book_text = books[i].text_content()
        title = book_text.split(',')[0].strip('"')
        context.favorited_titles.append(title)
        context.catalog_page.click_book(title)

@then('ska alla {count:d} böckerna visas i mina favoriter')
def step_all_books_in_favorites(context, count):
    context.catalog_page.click_navigation_tab("Mina böcker")
    
    for title in context.favorited_titles:
        is_in_favorites = context.favorites_page.is_book_in_favorites(title)
        assert is_in_favorites, f"Book '{title}' should be in favorites"
    
    context.catalog_page.click_navigation_tab("Katalog")
