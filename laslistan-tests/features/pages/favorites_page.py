from playwright.sync_api import Page
from features.pages.base_page import BasePage

class FavoritesPage(BasePage):
    """Page object for the Favorites page (Mina böcker)"""
    
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.book_item_selectors = [
            '[data-testid="book-item"]',
            '.book-item',
            'ul li',
            'main li'
        ]
    
    def get_empty_message(self) -> str:
        """Get the message shown when there are no favorites"""
        locator = self.page.locator("text=När du valt")
        return locator.text_content() if locator.count() > 0 else ""
    
    def is_empty_message_visible(self) -> bool:
        """Check if the empty message is visible"""
        locator = self.page.locator("text=När du valt")
        return locator.is_visible() if locator.count() > 0 else False
    
    def _first_selector_with_count(self):
        for sel in self.book_item_selectors:
            try:
                count = self.page.locator(sel).count()
                if count > 0:
                    return sel
            except Exception:
                continue
        return None
    
    def get_favorite_books(self):
        """Get all favorite book elements"""
        sel = self._first_selector_with_count()
        return self.page.locator(sel).all() if sel else []
    
    def get_favorite_count(self) -> int:
        """Get the number of favorite books"""
        sel = self._first_selector_with_count()
        return self.page.locator(sel).count() if sel else 0
    
    def get_favorite_by_title(self, title: str):
        """Get a favorite book element by its title"""
        candidate = self.page.get_by_text(title, exact=False).first
        try:
            candidate.wait_for(state="visible", timeout=10000)
            return candidate
        except Exception:
            pass
        books = self.get_favorite_books()
        for book in books:
            if title in (book.text_content() or ""):
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
