"""Все ссылки ведут туда, куда обещают."""
from __future__ import annotations

from urllib.parse import urljoin, urlparse

import pytest

from conftest import PAGES


def _collect(page) -> list[str]:
    return page.eval_on_selector_all(
        "a[href], img[src], link[href], script[src], source[srcset]",
        "els => els.map(e => e.getAttribute('href') || e.getAttribute('src') || e.getAttribute('srcset'))",
    )


@pytest.mark.parametrize("path", PAGES)
def test_internal_links_and_assets_resolve(open_page, base_url, path):
    page = open_page(path)
    broken = []
    for raw in set(_collect(page)):
        if raw.startswith(("#", "mailto:", "tel:")):
            continue
        url = urljoin(page.url, raw.split(" ")[0])
        if urlparse(url).netloc != urlparse(base_url).netloc:
            continue
        status = page.request.get(url).status
        if status != 200:
            broken.append(f"{status} {raw}")
    assert not broken, "битые ссылки:\n" + "\n".join(broken)


@pytest.mark.parametrize("path", PAGES)
def test_anchor_links_have_targets(open_page, path):
    page = open_page(path)
    anchors = page.eval_on_selector_all("a[href^='#']", "a => a.map(x => x.getAttribute('href'))")
    missing = [a for a in anchors if a != "#" and page.locator(a).count() == 0]
    assert not missing, f"якоря без цели: {missing}"


@pytest.mark.parametrize("path", PAGES)
def test_external_links_are_safe(open_page, path):
    page = open_page(path)
    unsafe = page.eval_on_selector_all(
        "a[target='_blank']",
        "a => a.filter(x => !(x.rel || '').includes('noopener')).map(x => x.href)",
    )
    insecure = page.eval_on_selector_all("a[href^='http:']", "a => a.map(x => x.href)")
    assert not unsafe, f"target=_blank без noopener: {unsafe}"
    assert not insecure, f"ссылки без https: {insecure}"


@pytest.mark.external
@pytest.mark.parametrize("path", PAGES)
def test_external_links_respond(open_page, path):
    page = open_page(path)
    urls = {u for u in page.eval_on_selector_all("a[href^='https://']", "a => a.map(x => x.href)")}
    failed = []
    for url in sorted(urls):
        status = page.request.get(url, max_redirects=5, timeout=20_000).status
        if status >= 400 and status not in (401, 403, 429):  # 401/403/429 — антибот, ссылка жива
            failed.append(f"{status} {url}")
    assert not failed, "внешние ссылки не отвечают:\n" + "\n".join(failed)
