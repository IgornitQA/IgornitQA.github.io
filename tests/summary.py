"""Короткая сводка прогона из JUnit XML для страницы GitHub Actions."""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET


def main(path: str) -> None:
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else root.findall("testsuite")
    total = sum(int(s.get("tests", 0)) for s in suites)
    failed = sum(int(s.get("failures", 0)) + int(s.get("errors", 0)) for s in suites)
    skipped = sum(int(s.get("skipped", 0)) for s in suites)
    print(f"### Автотесты сайта: {total - failed - skipped} passed · {failed} failed · {skipped} skipped\n")
    for case in root.iter("testcase"):
        problem = case.find("failure") if case.find("failure") is not None else case.find("error")
        if problem is not None:
            message = (problem.get("message") or "").splitlines()[0][:200]
            print(f"- ❌ `{case.get('name')}` — {message}")


if __name__ == "__main__":
    main(sys.argv[1])
