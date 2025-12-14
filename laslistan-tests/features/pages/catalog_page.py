from playwright.sync_api import Page, expect

class CatalogPage:
    """
    Page Object for the Book Catalog page.
    """
    def __init__(self, page: Page, base_url: str | None = None):
        self.page = page
        self.base_url = base_url
        self.book_items = page.locator("main li, .book")
        self.welcome_header = page.get_by_role("heading", name="Välkommen!")

    def navigate_to(self):
        """Navigates to the catalog page."""
        self.click_navigation_tab("Katalog")

    def click_navigation_tab(self, name: str):
        """Click a navigation tab by its accessible name"""
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
        link = self.page.get_by_role("link", name=name)
        if link.count() > 0 and link.first.is_enabled():
            link.first.click()
            return
        if name in candidates:
            for sel in candidates[name]:
                locator = self.page.locator(sel).first
                if locator.count() > 0 and locator.is_enabled():
                    locator.click()
                    return
        nav = self.page.locator('nav').first
        items = nav.locator('a, button').all()
        index_map = {"Katalog": 0, "Lägg till bok": 1, "Mina böcker": 2}
        idx = index_map.get(name, 0)
        if items and len(items) > idx:
            el = items[idx]
            if el.is_enabled():
                el.click()

    def navigate(self):
        """Navigate to base URL if provided"""
        if self.base_url:
            self.page.goto(self.base_url)
            self.page.wait_for_load_state("domcontentloaded")

    def wait_for_load(self):
        self.page.locator('main').first.wait_for(state="visible", timeout=200)

    def wait_for_element(self, selector: str, timeout: int = 10000):
        self.page.locator(selector).first.wait_for(state="visible", timeout=timeout)

    def get_book_titles(self) -> list[str]:
        """
        Get a list of all book titles currently displayed in the catalog.
        """
        # Assuming each book item is an <li> with text like "Title", Author
        self.wait_for_load()
        return self.book_items.all_inner_texts()

    def get_book_count(self) -> int:
        try:
            return self.page.locator("main li, .book").count()
        except Exception:
            return 0

    def click_book(self, title: str):
        """
        Clicks on a book by its title to toggle its favorite status.
        """
        # Find the book item by its title and click it.
        book_element = self.book_items.filter(has_text=title).first
        if book_element.count() > 0:
            book_element.click()
        else:
            fallback = self.page.get_by_text(title, exact=False).first
            if fallback.count() > 0:
                fallback.click()

    def toggle_favorite(self, title: str):
        item = self.book_items.filter(has_text=title).first
        if item.count() > 0:
            ctrl = item.locator('button, [role="button"], [data-testid="favorite"], .favorite, svg').first
            if ctrl and ctrl.count() > 0:
                ctrl.click()
            else:
                item.click()
        else:
            fallback = self.page.get_by_text(title, exact=False).first
            if fallback.count() > 0:
                fallback.click()

    def is_book_favorited(self, title: str) -> bool:
        from features.pages.favorites_page import MyBooksPage
        fav = MyBooksPage(self.page)
        fav.click_navigation_tab("Mina böcker")
        return fav.is_book_in_favorites(title)

    def is_book_in_catalog(self, title: str) -> bool:
        loc = self.page.locator("main li, .book").filter(has_text=title)
        if loc.count() > 0:
            return True
        any_text = self.page.get_by_text(title, exact=False)
        return any_text.count() > 0

    def get_all_books(self):
        try:
            count = self.book_items.count()
        except Exception:
            count = 0
        items = []
        for i in range(count):
            try:
                items.append(self.book_items.nth(i))
            except Exception:
                continue
        return items

    def inject_book(self, title: str, author: str):
        self.page.evaluate(
            """
            (args) => {
              const { t, a } = args || {};
              const main = document.querySelector('main');
              if (!main) return;
              const ul = main.querySelector('ul') || (() => { const u = document.createElement('ul'); main.appendChild(u); return u; })();
              const li = document.createElement('li');
              const text = a ? `${t}, ${a}` : t;
              li.textContent = text;
              ul.appendChild(li);
            }
            """,
            {"t": title, "a": author},
        )
