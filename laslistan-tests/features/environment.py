from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

def before_all(context):
    """Setup before all tests"""
    context.playwright = sync_playwright().start()
    
    # Check if headless mode is specified
    headless = context.config.userdata.get('headless', 'true').lower() == 'true'
    
    context.browser = context.playwright.chromium.launch(headless=headless)
    context.base_url = "https://tap-vt25-testverktyg.github.io/exam--reading-list/"

def before_scenario(context, scenario):
    """Setup before each scenario"""
    context.browser_context = context.browser.new_context()
    context.page = context.browser_context.new_page()
    
    # Set default timeout
    context.page.set_default_timeout(10000)

def after_scenario(context, scenario):
    """Cleanup after each scenario"""
    if hasattr(context, 'page'):
        context.page.close()
    if hasattr(context, 'browser_context'):
        context.browser_context.close()

def after_all(context):
    """Cleanup after all tests"""
    if hasattr(context, 'browser'):
        context.browser.close()
    if hasattr(context, 'playwright'):
        context.playwright.stop()
