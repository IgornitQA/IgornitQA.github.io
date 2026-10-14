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


def test_every_case_page_is_linked_from_main(open_page):
    page = open_page("/")
    linked = {href.split("?")[0] for href in page.eval_on_selector_all("a[href*='cases/']", "a => a.map(x => x.getAttribute('href'))")}
    existing = {f"cases/{p.name}" for p in (ROOT / "cases").glob("*.html")}
    orphans = sorted(existing - linked)
    assert not orphans, f"страницы кейсов без ссылки с главной: {orphans}"


ROLE = "QA Engineer (Automation, Python)"
CAREER_CHANGE = "С июня 2020 по январь 2025 работал фриланс-фотографом, а с апреля 2025 перешёл в тестирование."
QA_STUDIO = "ручное тестирование (2025), автоматизация на Python (2026)."


def test_headline_matches_experience_grade(open_page):
    page = open_page("/")
    body = page.locator("body").inner_text()

    assert ROLE in page.title()
    assert page.locator(".hero-role").inner_text() == f"{ROLE} · финтех"
    assert "QA Automation Engineer" not in page.title()
    assert "QA Automation Engineer" not in body
    assert "Junior QA Engineer" in body
    assert "QA Engineer" in page.locator(".role").inner_text()


def test_github_link_is_on_first_screen_and_in_contacts(open_page):
    page = open_page("/")
    github = "https://github.com/IgornitQA"
    assert page.locator(f".hero a[href='{github}']").count() == 1
    assert page.locator(f"#contact a[href='{github}']").count() == 1


def test_education_block_matches_resume_source(open_page):
    page = open_page("/")
    block = page.locator("#education")

    assert block.locator("h2").inner_text() == "Образование и развитие"
    text = block.inner_text()
    assert "QA Studio" in text
    assert QA_STUDIO in text
    assert CAREER_CHANGE in text
    assert "ПУ-60" not in text
    assert "секретарь-референт" not in text


@pytest.mark.parametrize("path", PAGES)
def test_initials_mark_is_labeled(open_page, path):
    page = open_page(path)
    mark = page.locator(".brand-mark abbr")
    assert mark.inner_text() == "ин."
    assert mark.get_attribute("title") == "Инициалы: Игорь Ниточкин"
    assert "Игорь Ниточкин" in page.locator(".brand").inner_text()


def test_footer_year_is_current(open_page):
    import datetime as dt

    page = open_page("/")
    assert page.locator("[data-year]").first.inner_text() == str(dt.date.today().year)


@pytest.mark.parametrize("path", PAGES)
def test_no_placeholder_text(open_page, path):
    text = open_page(path).locator("body").inner_text()
    found = re.findall(r"\b(?:TODO|TBD|lorem ipsum|undefined|NaN|null)\b", text, flags=re.I)
    assert not found, f"служебный текст на странице: {found}"
