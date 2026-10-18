"""Повторная сборка резюме не должна менять байты PDF без смены текста."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from build_resume import build  # noqa: E402


def test_resume_pdf_bytes_are_stable(tmp_path):
    first = tmp_path / "first.pdf"
    second = tmp_path / "second.pdf"

    build(first)
    build(second)

    assert first.read_bytes() == second.read_bytes()
