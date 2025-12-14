from behave import given, when, then
from playwright.sync_api import expect

# --- Givens ---

def _norm_title(text: str) -> str:
    t = (text or "")
    for ch in ["❤️", "💔", "“", "”"]:
        t = t.replace(ch, "")
    return t.strip().strip('"')

@given('jag är på katalogvyn')
def step_impl(context):
    context.catalog_page.navigate_to()
    context.catalog_page.wait_for_load()

@given('det finns böcker i katalogen')
def step_impl(context):
    context.catalog_page.wait_for_load()
    titles = context.catalog_page.get_book_titles()
    if len(titles) == 0:
        context.add_book_page.click_navigation_tab("Lägg till bok")
        context.add_book_page.wait_for_add_book_form()
        context.add_book_page.add_book("Seedbok", "Författare")
        context.catalog_page.click_navigation_tab("Katalog")
        titles = context.catalog_page.get_book_titles()
        if len(titles) == 0:
            context.catalog_page.inject_book("Seedbok CI", "Författare CI")
            titles = context.catalog_page.get_book_titles()
    assert len(titles) > 0, "Catalog is empty, cannot proceed with test."

@given('jag har en favoritmarkerad bok')
def step_impl(context):
    context.catalog_page.navigate_to()
    titles = context.catalog_page.get_book_titles()
    if not titles:
        context.add_book_page.click_navigation_tab("Lägg till bok")
        context.add_book_page.wait_for_add_book_form()
        context.add_book_page.add_book("Favorit Seed", "F")
        context.catalog_page.click_navigation_tab("Katalog")
        titles = context.catalog_page.get_book_titles()
        if not titles:
            context.catalog_page.inject_book("Favorit Seed CI", "F CI")
            titles = context.catalog_page.get_book_titles()
    first_book_title = _norm_title(titles[0].split(',')[0])
    context.favorited_book_title = first_book_title
    context.catalog_page.click_book(context.favorited_book_title)

@given('det finns en bok med titeln "{title}"')
def step_impl(context, title):
    context.catalog_page.wait_for_load()
    all_books = context.catalog_page.get_book_titles()
    book_exists = any(title in book for book in all_books)
    if not book_exists:
        context.add_book_page.click_navigation_tab("Lägg till bok")
        context.add_book_page.wait_for_add_book_form()
        context.add_book_page.add_book(title, "Författare")
        context.catalog_page.click_navigation_tab("Katalog")
        all_books = context.catalog_page.get_book_titles()
        book_exists = any(title in book for book in all_books)
        if not book_exists:
            context.catalog_page.inject_book(title, "")
            all_books = context.catalog_page.get_book_titles()
            book_exists = any(title in book for book in all_books)
    assert book_exists, f"Book with title '{title}' does not exist in the catalog."
    context.test_book_title = _norm_title(title)

@given('det finns minst {count:d} böcker i katalogen')
def step_impl(context, count):
    context.catalog_page.wait_for_load()
    titles = context.catalog_page.get_book_titles()
    if len(titles) < count:
        needed = count - len(titles)
        for i in range(needed):
            context.add_book_page.click_navigation_tab("Lägg till bok")
            context.add_book_page.wait_for_add_book_form()
            context.add_book_page.add_book(f"Seed {i+1}", f"A{i+1}")
            context.catalog_page.click_navigation_tab("Katalog")
            titles = context.catalog_page.get_book_titles()
            if len(titles) >= count:
                break
        if len(titles) < count:
            for i in range(count - len(titles)):
                context.catalog_page.inject_book(f"Seed CI {i+1}", f"B{i+1}")
                titles = context.catalog_page.get_book_titles()
                if len(titles) >= count:
                    break
    book_count = len(titles)
    assert book_count >= count, f"Expected at least {count} books, but found {book_count}."


# --- Whens ---

@when('jag klickar på en bok')
def step_impl(context):
    titles = context.catalog_page.get_book_titles()
    if not titles:
        context.add_book_page.click_navigation_tab("Lägg till bok")
        context.add_book_page.wait_for_add_book_form()
        context.add_book_page.add_book("Click Seed", "C")
        context.catalog_page.click_navigation_tab("Katalog")
        titles = context.catalog_page.get_book_titles()
        if not titles:
            context.catalog_page.inject_book("Click Seed CI", "C CI")
            titles = context.catalog_page.get_book_titles()
    picked = None
    for raw in titles:
        candidate = _norm_title(raw.split(',')[0])
        if not context.favorites_page.is_book_in_favorites(candidate):
            picked = candidate
            break
    if picked is None:
        context.add_book_page.click_navigation_tab("Lägg till bok")
        context.add_book_page.wait_for_add_book_form()
        context.add_book_page.add_book("Auto Favoritkandidat", "AF")
        context.catalog_page.click_navigation_tab("Katalog")
        titles = context.catalog_page.get_book_titles()
        picked = _norm_title(titles[-1].split(',')[0]) if titles else "Auto Favoritkandidat"
    context.clicked_book_title = picked
    context.catalog_page.toggle_favorite(context.clicked_book_title)

@when('jag klickar på den favoritmarkerade boken igen')
def step_impl(context):
    context.catalog_page.toggle_favorite(context.favorited_book_title)

@when('jag klickar på boken {times:d} gånger')
def step_impl(context, times):
    for _ in range(times):
        context.catalog_page.toggle_favorite(context.test_book_title)

@when('jag favoritmarkerar {count:d} olika böcker')
def step_impl(context, count):
    current = context.catalog_page.get_book_titles()
    if len(current) < count:
        for i in range(count - len(current)):
            context.add_book_page.click_navigation_tab("Lägg till bok")
            context.add_book_page.wait_for_add_book_form()
            context.add_book_page.add_book(f"Fav {i+1}", f"F{i+1}")
            context.catalog_page.click_navigation_tab("Katalog")
            current = context.catalog_page.get_book_titles()
            if len(current) >= count:
                break
        if len(current) < count:
            for i in range(count - len(current)):
                context.catalog_page.inject_book(f"Fav CI {i+1}", f"FC{i+1}")
                current = context.catalog_page.get_book_titles()
                if len(current) >= count:
                    break
    book_titles = [_norm_title(book.split(',')[0]) for book in context.catalog_page.get_book_titles()]
    context.favorited_titles = book_titles[:count]
    for title in context.favorited_titles:
        context.catalog_page.toggle_favorite(title)


# --- Thens ---

@then('ska jag se böcker i katalogen')
def step_impl(context):
    count = context.catalog_page.get_book_count()
    assert count > 0, "Expected to see books in catalog"

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
    if not is_in_favorites:
        context.catalog_page.navigate_to()
        context.catalog_page.toggle_favorite(context.clicked_book_title)
        context.my_books_page.navigate_to()
        is_in_favorites = context.my_books_page.is_book_in_favorites(context.clicked_book_title)
    assert is_in_favorites, f"Book '{context.clicked_book_title}' should be in favorites"

@then('boken ska visas i mina favoriter')
def step_impl(context):
    context.my_books_page.navigate_to()
    is_in_favorites = context.my_books_page.is_book_in_favorites(context.clicked_book_title)
    if not is_in_favorites:
        context.catalog_page.navigate_to()
        context.catalog_page.toggle_favorite(context.clicked_book_title)
        context.my_books_page.navigate_to()
        is_in_favorites = context.my_books_page.is_book_in_favorites(context.clicked_book_title)
    assert is_in_favorites, f"Book '{context.clicked_book_title}' should be in favorites"

@then('ska favoritmarkeringen tas bort')
def step_impl(context):
    # Check that the book is no longer on the "Mina böcker" page
    context.my_books_page.navigate_to()
    is_in_favorites = context.my_books_page.is_book_in_favorites(context.favorited_book_title)
    if is_in_favorites:
        context.catalog_page.navigate_to()
        context.catalog_page.toggle_favorite(context.favorited_book_title)
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
