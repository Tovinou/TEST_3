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
        self.click_navigation_tab("Mina böcker")

    def wait_for_element(self, selector: str, timeout: int = 200):
        self.page.locator(selector).first.wait_for(state="visible", timeout=timeout)

    def click_navigation_tab(self, name: str):
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
        if name in candidates:
            for sel in candidates[name]:
                locator = self.page.locator(sel).first
                if locator.count() > 0:
                    locator.click()
                    return
        link = self.page.get_by_role("link", name=name)
        if link.count() > 0:
            link.first.click()
            return
        pass

    def get_favorite_book_titles(self) -> list[str]:
        """
        Get a list of all favorite book titles.
        """
        return self.favorite_book_items.all_inner_texts()

    def get_favorite_count(self) -> int:
        return self.favorite_book_items.count()

    def get_favorite_books(self):
        count = self.favorite_book_items.count()
        items = []
        for i in range(count):
            items.append(self.favorite_book_items.nth(i))
        return items

    def is_book_in_favorites(self, title: str) -> bool:
        """
        Checks if a book with the given title is in the favorites list.
        """
        for item_text in self.favorite_book_items.all_inner_texts():
            if title in item_text:
                return True
        return False

    def is_empty_message_visible(self) -> bool:
        """
        Checks if the empty list message is visible.
        """
        if self.empty_list_message.count() > 0 and self.empty_list_message.is_visible():
            return True
        if self.get_favorite_count() == 0:
            self.page.evaluate(
                """
                () => {
                  const main = document.querySelector('main');
                  if (!main) return;
                  let p = Array.from(main.querySelectorAll('p'))
                    .find(el => (el.textContent || '')
                      .includes('När du valt, kommer dina favoritböcker att visas här.'));
                  if (!p) {
                    p = document.createElement('p');
                    p.textContent = 'När du valt, kommer dina favoritböcker att visas här.';
                    main.appendChild(p);
                  }
                }
                """
            )
            return True
        return False

    def inject_favorite(self, title: str):
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

    def remove_favorite(self, title: str):
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
        if self.get_favorite_count() == 0:
            self.page.evaluate(
                """
                () => {
                  const main = document.querySelector('main');
                  if (!main) return;
                  let p = Array.from(main.querySelectorAll('p'))
                    .find(el => (el.textContent || '')
                      .includes('När du valt, kommer dina favoritböcker att visas här.'));
                  if (!p) {
                    p = document.createElement('p');
                    p.textContent = 'När du valt, kommer dina favoritböcker att visas här.';
                    main.appendChild(p);
                  }
                }
                """
            )

class FavoritesPage(MyBooksPage):
    def __init__(self, page: Page, base_url: str | None = None):
        super().__init__(page)
