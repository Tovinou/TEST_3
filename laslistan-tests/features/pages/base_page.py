from playwright.sync_api import Page, expect

class BasePage:
    """Base page object with common functionality"""
    
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
    
    def navigate(self):
        """Navigate to the page"""
        self.page.goto(self.base_url)
        self.page.wait_for_load_state("domcontentloaded")
    
    def click_navigation_tab(self, tab_name: str):
        """Click on a navigation tab"""
        candidates = {
            "Katalog": [
                '[data-testid="nav-catalog"]'
            ],
            "Lägg till bok": [
                '[data-testid="nav-add"]'
            ],
            "Mina böcker": [
                '[data-testid="nav-favorites"]'
            ]
        }

        if tab_name in candidates:
            for sel in candidates[tab_name]:
                locator = self.page.locator(sel).first
                if locator.count() > 0:
                    locator.click()
                    return
            link = self.page.get_by_role("link", name=tab_name)
            if link.count() > 0:
                link.first.click()
                return
            pass
    
    def get_welcome_message(self) -> str:
        """Get the welcome message text"""
        return self.page.locator("h1, h2").first.text_content()
    
    def wait_for_element(self, selector: str, timeout: int = 200):
        self.page.locator(selector).first.wait_for(state="visible", timeout=timeout)
