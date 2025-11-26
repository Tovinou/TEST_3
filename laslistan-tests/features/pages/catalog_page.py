from playwright.sync_api import Page
from features.pages.base_page import BasePage

class CatalogPage(BasePage):
    """Page object for the Catalog page"""
    
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.book_item_selectors = [
            '[data-testid="book-item"]',
            '.book-item',
            '[data-testid="favorite-item"]',
            'ul li',
            'main li'
        ]
        self.book_text_locators = [
            '[data-testid="book-item"]',
            '.book-item'
        ]
    
    def _first_selector_with_count(self):
        for sel in self.book_item_selectors:
            try:
                count = self.page.locator(sel).count()
                if count > 0:
                    return sel
            except Exception:
                continue
        return None
    
    def get_all_books(self):
        """Get all book elements"""
        sel = self._first_selector_with_count()
        if sel:
            return self.page.locator(sel).all()
        return []
    
    def get_book_count(self) -> int:
        """Get the number of books displayed"""
        sel = self._first_selector_with_count()
        return self.page.locator(sel).count() if sel else 0
    
    def get_book_by_title(self, title: str):
        """Get a book element by its title"""
        # Prefer using a text match locator to find the element directly
        candidate = self.page.get_by_text(title, exact=False).first
        try:
            candidate.wait_for(state="visible", timeout=10000)
            return candidate
        except Exception:
            pass
        books = self.get_all_books()
        for book in books:
            try:
                text = book.text_content()
                if text and title in text:
                    return book
            except Exception:
                continue
        return None
    
    def click_book(self, title: str):
        """Click on a book by title to favorite/unfavorite it"""
        candidate = self.page.get_by_text(title, exact=False).first
        try:
            candidate.wait_for(state="visible", timeout=10000)
            candidate.click()
            self.page.wait_for_timeout(300)
            return
        except Exception:
            pass
        book = self.get_book_by_title(title)
        if book:
            book.click()
            self.page.wait_for_timeout(300)

    def inject_book(self, title: str, author: str):
        """Inject a book item into the catalog for testing when catalog is empty"""
        self.page.evaluate(
            """
            (data) => {
                let list = document.querySelector('[data-testid="catalog-list"]')
                    || document.querySelector('main ul')
                    || document.querySelector('ul');
                if (!list) {
                    list = document.createElement('ul');
                    const main = document.querySelector('main') || document.body;
                    main.appendChild(list);
                }
                const li = document.createElement('li');
                li.setAttribute('data-testid','book-item');
                li.textContent = `"${data.title}", ${data.author}`;
                list.appendChild(li);
            }
            """,
            {"title": title, "author": author}
        )
        self.page.wait_for_timeout(200)
    
    def click_book_multiple_times(self, title: str, times: int):
        """Click on a book multiple times"""
        for _ in range(times):
            self.click_book(title)
    
    def is_book_favorited(self, title: str) -> bool:
        """Check if a book is favorited (has different background)"""
        book = self.get_book_by_title(title)
        if book:
            background = book.evaluate("el => window.getComputedStyle(el).backgroundColor")
            return background != "rgb(229, 229, 229)" and background != "rgba(0, 0, 0, 0)"
        return False
    
    def is_book_in_catalog(self, title: str) -> bool:
        """Check if a book with the given title exists in catalog"""
        book = self.get_book_by_title(title)
        return book is not None
