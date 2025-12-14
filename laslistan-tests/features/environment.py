from playwright.sync_api import sync_playwright
from features.pages.catalog_page import CatalogPage
from features.pages.add_book_page import AddBookPage
from features.pages.favorites_page import MyBooksPage

# Define the base URL of the application to be tested
BASE_URL = "https://tap-vt25-testverktyg.github.io/exam--reading-list/"

def before_scenario(context, scenario):
    """
    Set up the browser and page objects before each scenario.
    """
    # Check for headless mode parameter from the command line
    headless = context.config.userdata.get("headless", "false").lower() == "true"
    
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=headless)
    
    # Create a new browser context and page
    context.browser = browser.new_context()
    context.page = context.browser.new_page()
    context.page.set_default_timeout(1000)
    context.page.set_default_navigation_timeout(2000)
    
    # --- Instantiate Page Objects ---
    context.base_url = BASE_URL
    context.catalog_page = CatalogPage(context.page, BASE_URL)
    context.add_book_page = AddBookPage(context.page, BASE_URL)
    my_books = MyBooksPage(context.page)
    context.my_books_page = my_books
    context.favorites_page = my_books
    
    # Navigate to the base URL before each scenario
    context.page.goto(BASE_URL)
    
    # Store playwright instance for cleanup
    context.playwright = playwright

def after_scenario(context, scenario):
    """
    Clean up by closing the browser after each scenario.
    """
    context.page.close()
    context.browser.close()
    context.playwright.stop()
