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

    def _visible_inputs(self):
        loc = self.page.locator('input')
        count = loc.count()
        items = []
        for i in range(count):
            el = loc.nth(i)
            try:
                if el.is_visible():
                    items.append(el)
            except Exception:
                continue
        return items

    def _title_locator(self):
        candidates = [
            self.page.get_by_label("Titel"),
            self.page.get_by_placeholder("Titel"),
            self.page.locator('#title'),
            self.page.locator('[data-testid="title-input"]'),
            self.page.locator('input[name="title"]')
        ]
        for c in candidates:
            try:
                if c.count() > 0:
                    l = c.first
                    if l.is_visible():
                        return l
            except Exception:
                continue
        return None

    def _author_locator(self):
        candidates = [
            self.page.get_by_label("Författare"),
            self.page.get_by_placeholder("Författare"),
            self.page.locator('#author'),
            self.page.locator('[data-testid="author-input"]'),
            self.page.locator('input[name="author"]')
        ]
        for c in candidates:
            try:
                if c.count() > 0:
                    l = c.first
                    if l.is_visible():
                        return l
            except Exception:
                continue
        return None

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
        tl = self._title_locator()
        al = self._author_locator()
        if tl is None:
            tl = self.page.get_by_label("Titel")
        if al is None:
            al = self.page.get_by_label("Författare")
        try:
            tl.wait_for(state="visible", timeout=10000)
            al.wait_for(state="visible", timeout=10000)
        except Exception:
            pass
    
    def fill_title(self, title: str):
        """Fill in the title field"""
        self.wait_for_add_book_form()
        loc = self._title_locator()
        if loc:
            loc.fill(title)
            return
        inputs = self._visible_inputs()
        if len(inputs) > 0:
            inputs[0].fill(title)
    
    def fill_author(self, author: str):
        """Fill in the author field"""
        self.wait_for_add_book_form()
        loc = self._author_locator()
        if loc:
            loc.fill(author)
            return
        inputs = self._visible_inputs()
        if len(inputs) > 1:
            inputs[1].fill(author)
    
    def submit_book(self):
        """Click the submit button"""
        sel = self._first_visible(self.submit_selectors)
        if sel:
            self.page.click(sel, timeout=10000)
        else:
            # Fallback: press Enter to submit the form
            try:
                inputs = self._visible_inputs()
                if inputs:
                    inputs[-1].press("Enter")
                else:
                    self.page.keyboard.press("Enter")
            except Exception:
                pass
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
        if sel:
            return self.page.input_value(sel)
        inputs = self._visible_inputs()
        return inputs[0].input_value() if len(inputs) > 0 else ""
    
    def get_author_value(self) -> str:
        """Get the current value of author input"""
        sel = self._first_visible(self.author_selectors)
        if sel:
            return self.page.input_value(sel)
        inputs = self._visible_inputs()
        return inputs[1].input_value() if len(inputs) > 1 else ""
    
    def clear_form(self):
        """Clear both input fields"""
        ts = self._first_visible(self.title_selectors)
        asel = self._first_visible(self.author_selectors)
        if ts:
            self.page.fill(ts, "")
        if asel:
            self.page.fill(asel, "")
