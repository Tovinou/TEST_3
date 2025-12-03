from playwright.sync_api import Page, expect

class CatalogPage:
    """
    Page Object for the Book Catalog page.
    """
    def __init__(self, page: Page):
        self.page = page
        self.book_items = page.locator("main li")
        self.welcome_header = page.get_by_role("heading", name="Välkommen!")

    def navigate_to(self):
        """Navigates to the catalog page."""
        self.page.get_by_role("link", name="Katalog").click()

    def wait_for_load(self):
        """Waits for the main book list to be visible."""
        self.book_items.first.wait_for(state="visible", timeout=5000)

    def get_book_titles(self) -> list[str]:
        """
        Get a list of all book titles currently displayed in the catalog.
        """
        # Assuming each book item is an <li> with text like "Title", Author
        self.wait_for_load()
        return self.book_items.all_inner_texts()

    def click_book(self, title: str):
        """
        Clicks on a book by its title to toggle its favorite status.
        """
        # Find the book item by its title and click it.
        book_element = self.book_items.filter(has_text=title).first
        book_element.wait_for(state="visible", timeout=5000)
        book_element.click()
        # A small wait to allow the application to process the click
        self.page.wait_for_timeout(300)