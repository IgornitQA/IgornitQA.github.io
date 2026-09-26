"""Страницы открываются без ошибок и содержат обязательную разметку."""
from __future__ import annotations

import re

import pytest

from conftest import PAGES, ROOT


@pytest.mark.parametrize("path", PAGES)
def test_page_loads_without_errors(open_page, path):
    page = open_page(path)
    page.wait_for_load_state("networkidle")

    assert "Ниточкин" in page.title()
    assert page.locator("html").get_attribute("lang") == "ru"
    assert page.locator("h1").count() == 1, "на странице должен быть ровно один h1"
    assert page.locator('meta[name="description"]').get_attribute("content"), "нет meta description"
    assert not open_page.problems, "\n".join(open_page.problems)


@pytest.mark.parametrize("path", PAGES)
def test_images_have_alt(open_page, path):
    page = open_page(path)
    without_alt = page.eval_on_selector_all("img", "imgs => imgs.filter(i => !i.hasAttribute('alt')).map(i => i.src)")
    assert not without_alt, f"картинки без alt: {without_alt}"


@pytest.mark.xfail(strict=True, reason="cases/happy-path-bot.html пока не связан с главной (находка 26.09, решение за Игорем); когда ссылка появится — снять пометку")
def test_every_case_page_is_linked_from_main(open_page):
    page = open_page("/")
    linked = {href.split("?")[0] for href in page.eval_on_selector_all("a[href*='cases/']", "a => a.map(x => x.getAttribute('href'))")}
    existing = {f"cases/{p.name}" for p in (ROOT / "cases").glob("*.html")}
    orphans = sorted(existing - linked)
    assert not orphans, f"страницы кейсов без ссылки с главной: {orphans}"


def test_footer_year_is_current(open_page):
    import datetime as dt

    page = open_page("/")
    assert page.locator("[data-year]").first.inner_text() == str(dt.date.today().year)


@pytest.mark.parametrize("path", PAGES)
def test_no_placeholder_text(open_page, path):
    text = open_page(path).locator("body").inner_text()
    found = re.findall(r"\b(?:TODO|TBD|lorem ipsum|undefined|NaN|null)\b", text, flags=re.I)
    assert not found, f"служебный текст на странице: {found}"
