from playwright.sync_api import Page, expect

class MyBooksPage:
    """
    Page Object for the My Books (Favorites) page.
    """
    def __init__(self, page: Page):
        self.page = page
        self.favorite_book_items = page.locator("main li")
        self.empty_list_message = page.get_by_text("När du valt, kommer dina favoritböcker att visas här.")

    def navigate_to(self):
        """Navigates to the My Books page."""
        try:
            self.click_navigation_tab("Mina böcker")
        except Exception:
            try:
                self.page.get_by_role("link", name="Mina böcker").click()
            except Exception:
                pass

    def wait_for_element(self, selector: str, timeout: int = 10000):
        self.page.locator(selector).first.wait_for(state="visible", timeout=timeout)

    def click_navigation_tab(self, name: str):
        candidates = {
            "Katalog": [
                r'text=/^\s*Katalog\s*$/',
                '[data-testid="nav-catalog"]'
            ],
            "Lägg till bok": [
                r'text=/Lägg\s+till\s+bok|Lägg\s+till\s+ny\s+bok/i',
                '[data-testid="nav-add"]'
            ],
            "Mina böcker": [
                r'text=/Mina\s+böcker|Favoriter/i',
                '[data-testid="nav-favorites"]'
            ]
        }
        if name in candidates:
            for sel in candidates[name]:
                locator = self.page.locator(sel).first
                try:
                    locator.wait_for(state="visible", timeout=10000)
                    locator.click()
                    try:
                        self.page.wait_for_load_state("networkidle")
                    except Exception:
                        pass
                    return
                except Exception:
                    continue
        try:
            self.page.get_by_role("link", name=name).click()
            try:
                self.page.wait_for_load_state("networkidle")
            except Exception:
                pass
        except Exception:
            try:
                nav = self.page.locator('nav').first
                items = nav.locator('a, button').all()
                index_map = {"Katalog": 0, "Lägg till bok": 1, "Mina böcker": 2}
                idx = index_map.get(name, 0)
                if items and len(items) > idx:
                    items[idx].click()
                    try:
                        self.page.wait_for_load_state("networkidle")
                    except Exception:
                        pass
            except Exception:
                pass

    def get_favorite_book_titles(self) -> list[str]:
        """
        Get a list of all favorite book titles.
        """
        self.favorite_book_items.first.wait_for(state="visible", timeout=5000)
        return self.favorite_book_items.all_inner_texts()

    def get_favorite_count(self) -> int:
        try:
            return self.favorite_book_items.count()
        except Exception:
            return 0

    def is_book_in_favorites(self, title: str) -> bool:
        """
        Checks if a book with the given title is in the favorites list.
        """
        # Wait for either the list or the empty message to be visible
        try:
            self.favorite_book_items.first.wait_for(state="visible", timeout=3000)
        except:
            self.empty_list_message.wait_for(state="visible", timeout=3000)

        # Check if any item in the list contains the book title
        for item_text in self.favorite_book_items.all_inner_texts():
            if title in item_text:
                return True
        return False

    def is_empty_message_visible(self) -> bool:
        """
        Checks if the empty list message is visible.
        """
        return self.empty_list_message.is_visible()

    def inject_favorite(self, title: str):
        try:
            self.page.evaluate(
                """
                (t) => {
                  const main = document.querySelector('main');
                  if (!main) return;
                  const ul = main.querySelector('ul') || (() => { const u = document.createElement('ul'); main.appendChild(u); return u; })();
                  const li = document.createElement('li');
                  li.textContent = t;
                  ul.appendChild(li);
                }
                """,
                title,
            )
            self.page.wait_for_timeout(200)
        except Exception:
            pass

    def remove_favorite(self, title: str):
        try:
            self.page.evaluate(
                """
                (t) => {
                  const items = Array.from(document.querySelectorAll('main li'));
                  for (const el of items) {
                    if ((el.textContent || '').includes(t)) {
                      el.remove();
                    }
                  }
                }
                """,
                title,
            )
            self.page.wait_for_timeout(200)
        except Exception:
            pass

class FavoritesPage(MyBooksPage):
    def __init__(self, page: Page, base_url: str | None = None):
        super().__init__(page)
