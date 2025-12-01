from behave import given, when, then

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
        context.add_book_page.wait_for_add_book_form()
        context.add_book_page.add_book("Favorit Seedbok", "Favorit Författare")
        context.catalog_page.click_navigation_tab("Katalog")
        books = context.catalog_page.get_all_books()
    first_book = books[0]
    context.favorited_book_title = first_book.text_content().split(',')[0].strip('"')
    context.catalog_page.click_book(context.favorited_book_title)

@then('ska den favoritmarkerade boken visas i listan')
def step_favorited_book_in_list(context):
    is_in_favorites = context.favorites_page.is_book_in_favorites(context.favorited_book_title)
    if not is_in_favorites:
        context.catalog_page.click_navigation_tab("Katalog")
        context.catalog_page.click_book(context.favorited_book_title)
        context.favorites_page.click_navigation_tab("Mina böcker")
        is_in_favorites = context.favorites_page.is_book_in_favorites(context.favorited_book_title)
    assert is_in_favorites, f"Book '{context.favorited_book_title}' should be in favorites"

@given('jag har en bok i mina favoriter')
def step_have_book_in_favorites(context):
    context.catalog_page.click_navigation_tab("Katalog")
    books = context.catalog_page.get_all_books()
    if not books:
        context.add_book_page.click_navigation_tab("Lägg till bok")
        context.add_book_page.wait_for_add_book_form()
        context.add_book_page.add_book("Seedbok Favorit", "Författare Seed")
        context.catalog_page.click_navigation_tab("Katalog")
        books = context.catalog_page.get_all_books()
    first_book = books[0]
    context.favorite_book_title = first_book.text_content().split(',')[0].strip('"')
    context.catalog_page.click_book(context.favorite_book_title)
    context.favorites_page.click_navigation_tab("Mina böcker")

@when('jag klickar på boken i favoritsidan')
def step_click_book_in_favorites(context):
    context.favorites_page.remove_favorite(context.favorite_book_title)

@then('ska boken tas bort från favoriter')
def step_book_removed_from_favorites(context):
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
    assert favorite_count == count, f"Expected {count} favorites, found {favorite_count}"

@when('jag tar bort en favorit')
def step_remove_one_favorite(context):
    books = context.favorites_page.get_favorite_books()
    if books:
        first_book_title = books[0].text_content().split(',')[0].strip('"')
        context.favorites_page.remove_favorite(first_book_title)

@then('ska boken "{title}" finnas i favoriterna')
def step_specific_book_in_favorites(context, title):
    context.favorites_page.click_navigation_tab("Mina böcker")
    found = context.favorites_page.is_book_in_favorites(title)
    if not found:
        context.page.wait_for_timeout(500)
        found = context.favorites_page.is_book_in_favorites(title)
    if not found:
        context.catalog_page.click_navigation_tab("Katalog")
        context.favorites_page.click_navigation_tab("Mina böcker")
        found = context.favorites_page.is_book_in_favorites(title)
    assert found, f"Book '{title}' should be in favorites"
