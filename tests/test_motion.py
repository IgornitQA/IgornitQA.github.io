"""Анимация «прогона» доигрывает до конечного состояния и уважает prefers-reduced-motion."""
from __future__ import annotations

from playwright.sync_api import expect


def test_reduced_motion_shows_final_state_immediately(page, open_page):
    page.emulate_media(reduced_motion="reduce")
    open_page("/")

    assert "motion" not in (page.locator("html").get_attribute("class") or "")
    expect(page.locator(".run-state b")).to_have_text("3 passed")
    last_tc = page.locator(".tc").last
    assert last_tc.evaluate("el => getComputedStyle(el.querySelector('dt'), '::before').opacity") == "1"


def test_run_summary_finishes_as_passed(page, open_page):
    open_page("/")
    assert "motion" in page.locator("html").get_attribute("class")

    page.locator(".run-summary").scroll_into_view_if_needed()

    expect(page.locator(".run-summary")).to_have_class("wrap run-summary is-run")
    expect(page.locator(".run-state b")).to_have_text("3 passed", timeout=4000)
    expect(page.locator(".run-rows > div").last).to_have_css("opacity", "1", timeout=4000)


def test_test_case_steps_get_checked_when_visible(page, open_page):
    open_page("/")
    last_tc = page.locator(".tc").last
    assert "is-run" not in (last_tc.get_attribute("class") or ""), "кейс внизу страницы не должен запускаться заранее"

    last_tc.scroll_into_view_if_needed()

    expect(last_tc).to_have_class("tc is-run")
    page.wait_for_function(
        "el => [...el.querySelectorAll('dt')].every(dt => getComputedStyle(dt, '::before').opacity === '1')",
        arg=last_tc.element_handle(), timeout=4000,
    )
