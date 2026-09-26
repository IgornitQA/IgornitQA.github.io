"""Доступность по axe-core: без нарушений уровня serious и critical."""
from __future__ import annotations

import pytest
from axe_playwright_python.sync_playwright import Axe

from conftest import PAGES

BLOCKING = {"serious", "critical"}


@pytest.mark.parametrize("path", PAGES)
def test_no_serious_accessibility_violations(open_page, path):
    page = open_page(path)
    results = Axe().run(page)
    violations = [
        f"[{v['impact']}] {v['id']}: {v['help']} ({len(v['nodes'])} эл.)"
        for v in results.response["violations"]
        if v["impact"] in BLOCKING
    ]
    assert not violations, "\n".join(violations)
