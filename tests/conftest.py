"""Общие фикстуры автотестов сайта.

По умолчанию сайт поднимается локально из корня репозитория (как GitHub Pages
отдаёт статику). Переменная SITE_URL переключает прогон на опубликованную версию.
"""
from __future__ import annotations

import functools
import http.server
import os
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PAGES = [
    "/",
    "/cases/api-regression.html",
    "/cases/ai-in-qa.html",
    "/cases/happy-path-bot.html",
]


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args) -> None:  # не засорять вывод pytest
        pass


@pytest.fixture(scope="session")
def base_url() -> str:
    site_url = os.getenv("SITE_URL", "").rstrip("/")
    if site_url:
        yield site_url
        return
    handler = functools.partial(_QuietHandler, directory=str(ROOT))
    with socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        yield f"http://127.0.0.1:{server.server_address[1]}"
        server.shutdown()


@pytest.fixture
def open_page(page, base_url):
    """Открыть страницу сайта и собрать ошибки консоли и упавшие запросы."""
    problems: list[str] = []
    page.on("console", lambda msg: msg.type == "error" and problems.append(f"console: {msg.text}"))
    page.on("pageerror", lambda exc: problems.append(f"pageerror: {exc}"))

    def on_response(response) -> None:
        if response.url.startswith(base_url) and response.status >= 400:
            problems.append(f"{response.status} {response.url}")

    page.on("response", on_response)

    def _open(path: str):
        response = page.goto(base_url + path, wait_until="load")
        assert response is not None and response.status == 200, f"{path}: {response and response.status}"
        return page

    _open.problems = problems
    return _open
