import re
from playwright.sync_api import Page, expect


def navigate_to_start_page(page: Page):
    page.goto("https://lejonmanen.github.io/agile-helper/")


def test_read_about_sprint_planning(page: Page):
    navigate_to_start_page(page)

    page.get_by_role("button").get_by_text("Första").click()
    page.get_by_role("button").get_by_text(re.compile("Sprint planning", re.I)).click()

    heading = page.get_by_role("heading").get_by_text("Sprint planning")
    expect(heading).to_be_visible()


def test_only_standup_during_sprint(page: Page):
    navigate_to_start_page(page)

    page.get_by_role("button").get_by_text(re.compile("mitt i", re.I)).click()

    expect(page.get_by_role("button").get_by_text(re.compile("Daily standup", re.I))).to_have_count(1)
    expect(page.get_by_role("button").get_by_text(re.compile("Sprint planning|Review|Retrospective|Backlog", re.I))).to_have_count(0)


def test_initial_prompt_visible(page: Page):
    navigate_to_start_page(page)
    prompt = page.get_by_text(re.compile("Vilken dag under sprinten är det?", re.I))
    expect(prompt).to_be_visible()
