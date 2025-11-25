from playwright.sync_api import Page
from features.pages.base_page import BasePage

class AddBookPage(BasePage):
    """Page object for the Add Book page"""
    
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.title_selectors = [
            '[data-testid="title-input"]',
            'input[name="title"]',
            'input[placeholder="Titel"]',
            '#title'
        ]
        self.author_selectors = [
            '[data-testid="author-input"]',
            'input[name="author"]',
            'input[placeholder="Författare"]',
            '#author'
        ]
        self.submit_selectors = [
            'button:has-text("Lägg till ny bok")',
            'button:has-text("Lägg till bok")',
            '[data-testid="submit-button"]',
            'button[type="submit"]'
        ]

    def _first_visible(self, selectors):
        for s in selectors:
            locator = self.page.locator(s).first
            try:
                locator.wait_for(state="visible", timeout=10000)
                return s
            except Exception:
                continue
        return None

    def wait_for_add_book_form(self):
        """Wait until the add-book form inputs are visible"""
        # Try title then author; tolerate either order
        title_sel = self._first_visible(self.title_selectors)
        author_sel = self._first_visible(self.author_selectors)
        assert title_sel is not None, "Title input not found"
        assert author_sel is not None, "Author input not found"
    
    def fill_title(self, title: str):
        """Fill in the title field"""
        self.wait_for_add_book_form()
        sel = self._first_visible(self.title_selectors)
        assert sel, "Title input not found"
        self.page.fill(sel, title)
    
    def fill_author(self, author: str):
        """Fill in the author field"""
        self.wait_for_add_book_form()
        sel = self._first_visible(self.author_selectors)
        assert sel, "Author input not found"
        self.page.fill(sel, author)
    
    def submit_book(self):
        """Click the submit button"""
        sel = self._first_visible(self.submit_selectors)
        assert sel, "Submit button not found"
        self.page.click(sel, timeout=10000)
        self.page.wait_for_timeout(500)  # Wait for book to be added
    
    def add_book(self, title: str, author: str):
        """Complete flow to add a book"""
        self.fill_title(title)
        self.fill_author(author)
        self.submit_book()
    
    def is_submit_button_enabled(self) -> bool:
        """Check if submit button is enabled"""
        sel = self._first_visible(self.submit_selectors)
        return sel is not None and self.page.locator(sel).is_enabled()
    
    def get_title_value(self) -> str:
        """Get the current value of title input"""
        sel = self._first_visible(self.title_selectors)
        assert sel, "Title input not found"
        return self.page.input_value(sel)
    
    def get_author_value(self) -> str:
        """Get the current value of author input"""
        sel = self._first_visible(self.author_selectors)
        assert sel, "Author input not found"
        return self.page.input_value(sel)
    
    def clear_form(self):
        """Clear both input fields"""
        ts = self._first_visible(self.title_selectors)
        asel = self._first_visible(self.author_selectors)
        if ts:
            self.page.fill(ts, "")
        if asel:
            self.page.fill(asel, "")
