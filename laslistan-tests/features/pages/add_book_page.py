from playwright.sync_api import Page
from features.pages.base_page import BasePage

class AddBookPage(BasePage):
    """Page object for the Add Book page"""
    
    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.title_input = '[data-testid="title-input"]'
        self.author_input = '[data-testid="author-input"]'
        self.submit_button = 'button:has-text("Lägg till ny bok")'
    
    def fill_title(self, title: str):
        """Fill in the title field"""
        self.page.fill(self.title_input, title)
    
    def fill_author(self, author: str):
        """Fill in the author field"""
        self.page.fill(self.author_input, author)
    
    def submit_book(self):
        """Click the submit button"""
        self.page.click(self.submit_button)
        self.page.wait_for_timeout(500)  # Wait for book to be added
    
    def add_book(self, title: str, author: str):
        """Complete flow to add a book"""
        self.fill_title(title)
        self.fill_author(author)
        self.submit_book()
    
    def is_submit_button_enabled(self) -> bool:
        """Check if submit button is enabled"""
        return self.page.locator(self.submit_button).is_enabled()
    
    def get_title_value(self) -> str:
        """Get the current value of title input"""
        return self.page.input_value(self.title_input)
    
    def get_author_value(self) -> str:
        """Get the current value of author input"""
        return self.page.input_value(self.author_input)
    
    def clear_form(self):
        """Clear both input fields"""
        self.page.fill(self.title_input, "")
        self.page.fill(self.author_input, "")
