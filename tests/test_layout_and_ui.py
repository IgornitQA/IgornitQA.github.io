"""Вёрстка на разных экранах и интерактивные элементы."""
from __future__ import annotations

import pytest
from playwright.sync_api import expect

from conftest import PAGES

VIEWPORTS = {"phone": (375, 812), "tablet": (768, 1024), "desktop": (1440, 900)}


@pytest.mark.parametrize("path", PAGES)
@pytest.mark.parametrize("screen", VIEWPORTS)
def test_no_horizontal_scroll(page, open_page, path, screen):
    page.set_viewport_size(dict(zip(("width", "height"), VIEWPORTS[screen])))
    open_page(path)
    overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    assert overflow <= 0, f"горизонтальный скролл {overflow}px на {screen}"


def test_mobile_menu_opens_and_closes(page, open_page):
    page.set_viewport_size({"width": 375, "height": 812})
    open_page("/")
    toggle = page.locator(".menu-toggle")
    nav = page.locator("#main-nav")

    toggle.click()
    assert toggle.get_attribute("aria-expanded") == "true"
    assert "is-open" in nav.get_attribute("class")

    page.keyboard.press("Escape")
    assert toggle.get_attribute("aria-expanded") == "false"
    assert page.evaluate("document.activeElement === document.querySelector('.menu-toggle')"), "фокус не вернулся на кнопку"

    toggle.click()
    nav.locator("a").first.click()
    assert toggle.get_attribute("aria-expanded") == "false", "меню не закрылось после выбора пункта"


def test_copy_email_button(page, open_page, context):
    context.grant_permissions(["clipboard-read", "clipboard-write"])
    open_page("/")
    button = page.locator("[data-copy-email]")
    email = button.get_attribute("data-copy-email")

    button.click()

    expect(page.locator(".copy-status")).to_have_text("Email скопирован")
    assert page.evaluate("navigator.clipboard.readText()") == email
    assert page.locator(f"a[href='mailto:{email}']").count() >= 1, "email в кнопке и в mailto-ссылке различаются"
