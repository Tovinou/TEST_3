from playwright.sync_api import Page, expect

class MyBooksPage:
    """
    Page Object for the My Books (Favorites) page.
    """
    def __init__(self, page: Page):
        self.page = page
        self.favorite_book_items = page.locator("main li")
        self.empty_list_message = page.get_by_text("När du valt, kommer dina favoritböcker att visas här.")

    def navigate_to(self):
        """Navigates to the My Books page."""
        self.page.get_by_role("link", name="Mina böcker").click()

    def get_favorite_book_titles(self) -> list[str]:
        """
        Get a list of all favorite book titles.
        """
        self.favorite_book_items.first.wait_for(state="visible", timeout=5000)
        return self.favorite_book_items.all_inner_texts()

    def is_book_in_favorites(self, title: str) -> bool:
        """
        Checks if a book with the given title is in the favorites list.
        """
        # Wait for either the list or the empty message to be visible
        try:
            self.favorite_book_items.first.wait_for(state="visible", timeout=3000)
        except:
            self.empty_list_message.wait_for(state="visible", timeout=3000)

        # Check if any item in the list contains the book title
        for item_text in self.favorite_book_items.all_inner_texts():
            if title in item_text:
                return True
        return False

    def is_empty_message_visible(self) -> bool:
        """
        Checks if the empty list message is visible.
        """
        return self.empty_list_message.is_visible()