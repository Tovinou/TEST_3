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
        candidates = {
            "Katalog": [
                'text=/^\s*Katalog\s*$/',
                '[data-testid="nav-catalog"]'
            ],
            "Lägg till bok": [
                'text=/Lägg\s+till\s+bok|Lägg\s+till\s+ny\s+bok/i',
                '[data-testid="nav-add"]'
            ],
            "Mina böcker": [
                'text=/Mina\s+böcker|Favoriter/i',
                '[data-testid="nav-favorites"]'
            ]
        }

        if tab_name in candidates:
            for sel in candidates[tab_name]:
                locator = self.page.locator(sel).first
                try:
                    locator.wait_for(state="visible", timeout=30000)
                    locator.click()
                    self.page.wait_for_load_state("networkidle")
                    return
                except Exception:
                    continue
    
    def get_welcome_message(self) -> str:
        """Get the welcome message text"""
        return self.page.locator("h1, h2").first.text_content()
    
    def wait_for_element(self, selector: str, timeout: int = 30000):
        """Wait for an element to be visible"""
        self.page.locator(selector).wait_for(state="visible", timeout=timeout)
