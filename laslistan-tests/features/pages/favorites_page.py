from playwright.sync_api import Page
from features.pages.base_page import BasePage

class FavoritesPage(BasePage):
    """Page object for the Favorites page (Mina böcker)"""
    
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
    
    def get_empty_message(self) -> str:
        """Get the message shown when there are no favorites"""
        return self.page.locator("text=När du valt").text_content()
    
    def is_empty_message_visible(self) -> bool:
        """Check if the empty message is visible"""
        return self.page.locator("text=När du valt").is_visible()
    
    def get_favorite_books(self):
        """Get all favorite book elements"""
        return self.page.locator('[data-testid="book-item"]').all()
    
    def get_favorite_count(self) -> int:
        """Get the number of favorite books"""
        return self.page.locator('[data-testid="book-item"]').count()
    
    def get_favorite_by_title(self, title: str):
        """Get a favorite book element by its title"""
        books = self.get_favorite_books()
        for book in books:
            if title in book.text_content():
                return book
        return None
    
    def is_book_in_favorites(self, title: str) -> bool:
        """Check if a book is in the favorites list"""
        book = self.get_favorite_by_title(title)
        return book is not None
    
    def remove_favorite(self, title: str):
        """Remove a book from favorites by clicking it"""
        book = self.get_favorite_by_title(title)
        if book:
            book.click()
            self.page.wait_for_timeout(300)
