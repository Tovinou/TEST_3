from playwright.sync_api import Page
from features.pages.base_page import BasePage

class CatalogPage(BasePage):
    """Page object for the Catalog page"""
    
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
    
    def get_all_books(self):
        """Get all book elements"""
        return self.page.locator('[data-testid="book-item"]').all()
    
    def get_book_count(self) -> int:
        """Get the number of books displayed"""
        return self.page.locator('[data-testid="book-item"]').count()
    
    def get_book_by_title(self, title: str):
        """Get a book element by its title"""
        books = self.get_all_books()
        for book in books:
            if title in book.text_content():
                return book
        return None
    
    def click_book(self, title: str):
        """Click on a book by title to favorite/unfavorite it"""
        book = self.get_book_by_title(title)
        if book:
            book.click()
            self.page.wait_for_timeout(300)  # Small wait for state change
    
    def click_book_multiple_times(self, title: str, times: int):
        """Click on a book multiple times"""
        for _ in range(times):
            self.click_book(title)
    
    def is_book_favorited(self, title: str) -> bool:
        """Check if a book is favorited (has different background)"""
        book = self.get_book_by_title(title)
        if book:
            # Check if the book has a different background color or class
            # This might need adjustment based on actual implementation
            background = book.evaluate("el => window.getComputedStyle(el).backgroundColor")
            # Favorited books typically have a different color
            return background != "rgb(229, 229, 229)" and background != "rgba(0, 0, 0, 0)"
        return False
    
    def is_book_in_catalog(self, title: str) -> bool:
        """Check if a book with the given title exists in catalog"""
        book = self.get_book_by_title(title)
        return book is not None
