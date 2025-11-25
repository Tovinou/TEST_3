from behave import given, when, then

@given('jag är på vyn för att lägga till bok')
def step_navigate_to_add_book(context):
    context.add_book_page.click_navigation_tab("Lägg till bok")
    context.add_book_page.wait_for_add_book_form()

@when('jag fyller i titel "{title}"')
def step_fill_title(context, title):
    context.add_book_page.wait_for_add_book_form()
    context.add_book_page.fill_title(title)
    context.added_book_title = title

@when('jag fyller i författare "{author}"')
def step_fill_author(context, author):
    context.add_book_page.wait_for_add_book_form()
    context.add_book_page.fill_author(author)
    context.added_book_author = author

@when('jag klickar på knappen för att lägga till boken')
def step_click_add_button(context):
    context.add_book_page.submit_book()

@then('ska boken finnas i katalogen')
def step_book_in_catalog(context):
    context.catalog_page.click_navigation_tab("Katalog")
    is_in_catalog = context.catalog_page.is_book_in_catalog(context.added_book_title)
    assert is_in_catalog, f"Book '{context.added_book_title}' should be in catalog"

@then('ska boken "{title}" finnas i katalogen')
def step_specific_book_in_catalog(context, title):
    context.catalog_page.click_navigation_tab("Katalog")
    is_in_catalog = context.catalog_page.is_book_in_catalog(title)
    assert is_in_catalog, f"Book '{title}' should be in catalog"

@then('ska titelfältet vara tomt')
def step_title_field_empty(context):
    context.add_book_page.click_navigation_tab("Lägg till bok")
    context.add_book_page.wait_for_add_book_form()
    title_value = context.add_book_page.get_title_value()
    assert title_value == "", f"Title field should be empty, but contains: {title_value}"

@then('ska författarfältet vara tomt')
def step_author_field_empty(context):
    context.add_book_page.wait_for_add_book_form()
    author_value = context.add_book_page.get_author_value()
    assert author_value == "", f"Author field should be empty, but contains: {author_value}"

@when('jag lägger till en bok med titel "{title}" och författare "{author}"')
def step_add_book_complete(context, title, author):
    context.add_book_page.click_navigation_tab("Lägg till bok")
    context.add_book_page.add_book(title, author)
    context.added_book_title = title

@when('jag går till katalogvyn')
def step_go_to_catalog(context):
    context.catalog_page.click_navigation_tab("Katalog")

@when('jag favoritmarkerar boken "{title}"')
def step_favorite_specific_book(context, title):
    context.catalog_page.click_book(title)
    
