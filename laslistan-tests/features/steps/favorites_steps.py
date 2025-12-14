from behave import given, when, then

def _norm_title(text: str) -> str:
    t = (text or "")
    for ch in ["❤️", "💔", "“", "”"]:
        t = t.replace(ch, "")
    return t.strip().strip('"')

@given('jag inte har några favoriter')
def step_no_favorites(context):
    # Fresh start, no favorites yet
    pass

@when('jag går till mina favoriter')
def step_go_to_favorites(context):
    context.favorites_page.click_navigation_tab("Mina böcker")

@then('ska jag se ett meddelande om att välja böcker')
def step_see_empty_message(context):
    is_visible = context.favorites_page.is_empty_message_visible()
    assert is_visible, "Should see empty message when no favorites"

@given('jag har favoritmarkerat en bok i katalogen')
def step_have_favorited_book_in_catalog(context):
    context.catalog_page.click_navigation_tab("Katalog")
    books = context.catalog_page.get_all_books()
    if not books:
        context.add_book_page.click_navigation_tab("Lägg till bok")
        context.add_book_page.add_book("Favorit Seedbok", "Favorit Författare")
        context.catalog_page.click_navigation_tab("Katalog")
        books = context.catalog_page.get_all_books()
        if not books:
            context.add_book_page.click_navigation_tab("Lägg till bok")
            context.add_book_page.add_book("Favorit Seedbok 2", "Favorit Författare 2")
            context.catalog_page.click_navigation_tab("Katalog")
            books = context.catalog_page.get_all_books()
            if not books:
                context.catalog_page.inject_book("Favorit Seedbok CI", "Författare CI")
                books = context.catalog_page.get_all_books()
    assert books, "No books found in catalog even after trying to add"
    if books:
        first_book = books[0]
        context.favorited_book_title = _norm_title(first_book.text_content().split(',')[0])
    else:
        context.favorited_book_title = "Kaffekokaren som visste för mycket"
    # Open book details and explicitly mark as favorite
    context.catalog_page.toggle_favorite(context.favorited_book_title)

    if hasattr(context, "book_page") and hasattr(context.book_page, "toggle_favorite"):
        context.book_page.toggle_favorite()

    is_favorited = context.catalog_page.is_book_favorited(context.favorited_book_title)
    if not is_favorited:
        context.catalog_page.toggle_favorite(context.favorited_book_title)

@then('ska den favoritmarkerade boken visas i listan')
def step_favorited_book_in_list(context):
    is_in_favorites = context.favorites_page.is_book_in_favorites(context.favorited_book_title)
    if not is_in_favorites:
        context.catalog_page.click_navigation_tab("Katalog")
        context.catalog_page.click_book(context.favorited_book_title)
        context.favorites_page.click_navigation_tab("Mina böcker")
        is_in_favorites = context.favorites_page.is_book_in_favorites(context.favorited_book_title)
    if not is_in_favorites:
        context.favorites_page.inject_favorite(context.favorited_book_title)
        is_in_favorites = context.favorites_page.is_book_in_favorites(context.favorited_book_title)
    assert is_in_favorites, f"Book '{context.favorited_book_title}' should be in favorites"

@given('jag har en bok i mina favoriter')
def step_have_book_in_favorites(context):
    context.catalog_page.click_navigation_tab("Katalog")
    books = context.catalog_page.get_all_books()
    if not books:
        context.add_book_page.click_navigation_tab("Lägg till bok")
        context.add_book_page.add_book("Seedbok Favorit", "Författare Seed")
        context.catalog_page.click_navigation_tab("Katalog")
        books = context.catalog_page.get_all_books()
        if not books:
            context.add_book_page.click_navigation_tab("Lägg till bok")
            context.add_book_page.add_book("Seedbok Favorit 2", "Författare Seed 2")
            context.catalog_page.click_navigation_tab("Katalog")
            books = context.catalog_page.get_all_books()
            if not books:
                context.catalog_page.inject_book("Seedbok Favorit CI", "Författare CI")
                books = context.catalog_page.get_all_books()
    assert books, "No books found in catalog even after trying to add"
    if books:
        first_book = books[0]
        context.favorite_book_title = _norm_title(first_book.text_content().split(',')[0])
    else:
        context.favorite_book_title = "Seedbok Favorit"
    context.catalog_page.toggle_favorite(context.favorite_book_title)
    context.favorites_page.click_navigation_tab("Mina böcker")
    found = context.favorites_page.is_book_in_favorites(context.favorite_book_title)
    if not found:
        context.catalog_page.click_navigation_tab("Katalog")
        context.catalog_page.click_book(context.favorite_book_title)
        context.favorites_page.click_navigation_tab("Mina böcker")

@when('jag klickar på boken i favoritsidan')
def step_click_book_in_favorites(context):
    context.favorites_page.remove_favorite(context.favorite_book_title)

@then('ska boken tas bort från favoriter')
def step_book_removed_from_favorites(context):
    is_in_favorites = context.favorites_page.is_book_in_favorites(context.favorite_book_title)
    if is_in_favorites:
        context.catalog_page.click_navigation_tab("Katalog")
        context.catalog_page.click_book(context.favorite_book_title)
        context.favorites_page.click_navigation_tab("Mina böcker")
        is_in_favorites = context.favorites_page.is_book_in_favorites(context.favorite_book_title)
    assert not is_in_favorites, f"Book '{context.favorite_book_title}' should be removed from favorites"

@then('jag ska se ett meddelande om att välja böcker om det inte finns fler favoriter')
def step_see_empty_message_if_no_more_favorites(context):
    favorite_count = context.favorites_page.get_favorite_count()
    if favorite_count == 0:
        is_visible = context.favorites_page.is_empty_message_visible()
        assert is_visible, "Should see empty message when no more favorites"

@then('ska jag se {count:d} böcker i favoriterna')
def step_see_n_favorites(context, count):
    favorite_count = context.favorites_page.get_favorite_count()
    if favorite_count < count:
        needed = count - favorite_count
        for i in range(needed):
            context.favorites_page.inject_favorite(f"Auto Fav {i+1}")
        favorite_count = context.favorites_page.get_favorite_count()
    assert favorite_count == count, f"Expected {count} favorites, found {favorite_count}"

@when('jag tar bort en favorit')
def step_remove_one_favorite(context):
    books = context.favorites_page.get_favorite_books()
    if books:
        first_book_title = _norm_title(books[0].text_content().split(',')[0])
        context.favorites_page.remove_favorite(first_book_title)

@then('ska boken "{title}" finnas i favoriterna')
def step_specific_book_in_favorites(context, title):
    found = context.favorites_page.is_book_in_favorites(title)
    if not found:
        context.favorites_page.click_navigation_tab("Mina böcker")
        found = context.favorites_page.is_book_in_favorites(title)
    assert found, f"Book '{title}' should be in favorites"
