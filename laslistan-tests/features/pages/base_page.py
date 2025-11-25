from playwright.sync_api import Page, expect

class BasePage:
    """Base page object with common functionality"""
    
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
    
    def navigate(self):
        """Navigate to the page"""
        self.page.goto(self.base_url)
        self.page.wait_for_load_state("networkidle")
    
    def click_navigation_tab(self, tab_name: str):
        """Click on a navigation tab"""
        tab_selectors = {
            "Katalog": "text=Katalog",
            "Lägg till bok": "text=Lägg till bok",
            "Mina böcker": "text=Mina böcker"
        }
        
        if tab_name in tab_selectors:
            self.page.click(tab_selectors[tab_name])
            self.page.wait_for_load_state("networkidle")
    
    def get_welcome_message(self) -> str:
        """Get the welcome message text"""
        return self.page.locator("h1, h2").first.text_content()
    
    def wait_for_element(self, selector: str, timeout: int = 5000):
        """Wait for an element to be visible"""
        self.page.wait_for_selector(selector, timeout=timeout)
