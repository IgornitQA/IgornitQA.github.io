"""PDF-резюме открывается и не расходится с сайтом."""
from __future__ import annotations

import io
import re

from pypdf import PdfReader


def _resume_text(page, base_url) -> tuple[object, str]:
    response = page.request.get(f"{base_url}/resume.pdf")
    assert response.status == 200
    assert "application/pdf" in response.headers.get("content-type", "")
    reader = PdfReader(io.BytesIO(response.body()))
    return reader, "\n".join(p.extract_text() or "" for p in reader.pages)


def test_resume_pdf_is_valid(page, base_url):
    reader, text = _resume_text(page, base_url)
    assert len(reader.pages) >= 1
    assert "Ниточкин" in text


def test_resume_contacts_match_site(open_page, base_url):
    page = open_page("/")
    email = page.locator("[data-copy-email]").get_attribute("data-copy-email")
    telegram = page.locator("a[href^='https://t.me/']").first.get_attribute("href").rsplit("/", 1)[-1]

    _, text = _resume_text(page, base_url)
    flat = re.sub(r"\s+", "", text)

    assert email in flat, f"email {email} с сайта нет в PDF"
    assert telegram in flat, f"Telegram @{telegram} с сайта нет в PDF"


def test_resume_links_use_versioned_url(open_page):
    page = open_page("/")
    hrefs = page.eval_on_selector_all("a[href*='resume.pdf']", "a => a.map(x => x.getAttribute('href'))")
    assert hrefs, "на главной нет ссылки на PDF"
    assert len(set(hrefs)) == 1, f"ссылки на PDF ведут на разные версии: {hrefs}"
    assert re.search(r"resume\.pdf\?v=\S+", hrefs[0]), f"ссылка на PDF без версии — браузер может отдать старый файл из кеша: {hrefs[0]}"
