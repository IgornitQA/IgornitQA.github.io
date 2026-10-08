"""Собирает resume.pdf из текста ниже.

Запуск из корня репозитория:
    uv run --no-project --with reportlab python tools/build_resume.py

Шрифт — Segoe UI из Windows; на другой ОС передать путь к каталогу
с segoeui.ttf и segoeuib.ttf через RESUME_FONT_DIR.
"""
from __future__ import annotations

import os
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "resume.pdf"
FONT_DIR = Path(os.getenv("RESUME_FONT_DIR", r"C:\Windows\Fonts"))

INK = HexColor("#172C2C")
ACCENT = HexColor("#287465")
MUTED = HexColor("#61736C")
RULE = HexColor("#E6EBE7")
FOOTER = HexColor("#9AA7A2")

NAME = "Игорь Ниточкин"
HEADLINE = "QA Automation Engineer (Python) | Финтех"
FOOTER_TEXT = f"{NAME} · QA Automation Engineer (Python)"

CONTACTS = [
    "Краснодар · UTC+3 · Удалённая работа",
    '<a href="mailto:igor.nitochkin@gmail.com">igor.nitochkin@gmail.com</a> · '
    '<a href="https://t.me/i_nitochkin">Telegram: @i_nitochkin</a>',
    '<a href="https://igornitqa.github.io/">Портфолио: igornitqa.github.io</a> · '
    '<a href="https://github.com/IgornitQA">GitHub: IgornitQA</a> · '
    '<a href="https://hh.ru/resume/306d67f1ff0e94d76b0039ed1f4e475a566e42">Резюме на hh.ru</a>',
]

ABOUT = (
    "QA Automation Engineer в финтехе с апреля 2025 года. Пишу UI/API-автотесты на Python, pytest и Playwright: "
    "фикстуры, контракты и проверки БД. Настраиваю CI и применяю AI в ревью требований и диагностике."
)

COMPANY = "QUGO"
ROLES = [
    ("QA Engineer (автоматизация)", "{PROMOTED} — настоящее время"),
    ("Junior QA Engineer", "Апрель 2025 — {PROMOTED_LOWER}"),
]
PROMOTED = "Октябрь 2026"
COMPANY_DESCRIPTION = (
    "Финтех-платформа для выплат самозанятым. Работаю с банковскими и налоговыми интеграциями: "
    "регистрацией, проверками статусов в ФНС, выплатами, реестрами и документооборотом."
)

ACHIEVEMENTS = [
    ("Вывел E2E регистрации и авторизации на production:",
     "запуск только CI-джобой с master, guard от случайного локального запуска, синтетические ИНН, "
     "удаление тестового пользователя до и после прогона, техномер вместо личного телефона."),
    ("Автоматизирую smoke- и E2E-сценарии",
     "регистрации исполнителя и заказчика, авторизации и приглашений — по телефону, ссылке и "
     "XLSX-реестрам — с проверкой сохранённых данных в БД."),
    ("Ускорил E2E регистрации на тестовом стенде",
     "примерно с 85 до 43–45 секунд: ожидание OTP вместо фиксированных пауз, убрал повторные действия."),
    ("Расширил API-регресс:",
     "добавил 20 новых сценариев к 13 существовавшим. Реализовал изоляцию данных, Pydantic-контракты, "
     "постусловия в MySQL и маскирование секретов в Allure."),
    ("Перевёл проект на uv, обновил Docker и GitLab CI;",
     "подключил JUnit-отчёты — результаты тестов видны прямо в merge request."),
    ("Автоматизировал путь от задачи до тест-кейса:",
     "Happy Path Bot готовит черновик из Яндекс Трекера и переносит проверенный кейс в Test IT "
     "с проверкой структуры, дублей и связью с задачей."),
    ("Создал базу из 100+ кейсов",
     "и инициировал переход на Test IT. Участвовал в запуске KYC и проверке нового стенда, "
     "первым начал тестировать Android-приложение заказчика."),
]

SKILLS = [
    ("Автоматизация", "Python, pytest, Playwright (UI/API), Pydantic, Allure, Page Object / Service Object, "
                      "Git, GitLab CI, Docker, uv."),
    ("Данные и диагностика", "SQL, PostgreSQL, MySQL, Grafana, Loki, OpenSearch."),
    ("Тест-дизайн", "таблицы решений, классы эквивалентности, граничные значения, переходы состояний, "
                    "анализ требований."),
    ("Тестирование", "REST API, Web, Android, ручное и интеграционное тестирование, Postman, "
                     "Swagger / OpenAPI, DevTools."),
    ("Процесс", "Test IT, Яндекс Трекер, Яндекс Вики, Figma."),
]

EDUCATION = [
    ("QA Studio", "ручное тестирование (2025), автоматизация на Python (2026)."),
    ("ПУ-60", "среднее специальное образование, секретарь-референт, оператор ЭВМ (2008)."),
]
EARLIER = "Ранее: фриланс-фотограф, июнь 2020 — январь 2025."


def _nbsp(text: str) -> str:
    """Тире не переносится в начало строки."""
    return text.replace(" — ", " — ")


def _styles() -> dict[str, ParagraphStyle]:
    base = ParagraphStyle("base", fontName="Segoe", fontSize=9.6, leading=13.6, textColor=INK)
    return {
        "name": ParagraphStyle("name", base, fontName="Segoe-Bold", fontSize=27, leading=32),
        "headline": ParagraphStyle("headline", base, fontSize=13, leading=18, textColor=ACCENT, spaceBefore=2),
        "meta": ParagraphStyle("meta", base, fontSize=8.8, leading=15, textColor=MUTED),
        "section": ParagraphStyle("section", base, fontName="Segoe-Bold", fontSize=10, textColor=ACCENT,
                                  spaceBefore=11, spaceAfter=4),
        "company": ParagraphStyle("company", base, fontName="Segoe-Bold", fontSize=11.5, leading=15),
        "role": ParagraphStyle("role", base, fontSize=9, leading=12.6, textColor=MUTED),
        "body": base,
        "bullet": ParagraphStyle("bullet", base, leftIndent=9, firstLineIndent=-9, spaceBefore=3.2),
        "small": ParagraphStyle("small", base, fontSize=8.8, leading=12.4, textColor=MUTED),
    }


def _footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Segoe", 7.6)
    canvas.setFillColor(FOOTER)
    canvas.drawString(doc.leftMargin, 9 * mm, FOOTER_TEXT)
    canvas.drawRightString(A4[0] - doc.rightMargin, 9 * mm, str(doc.page))
    canvas.restoreState()


def build() -> Path:
    pdfmetrics.registerFont(TTFont("Segoe", str(FONT_DIR / "segoeui.ttf")))
    pdfmetrics.registerFont(TTFont("Segoe-Bold", str(FONT_DIR / "segoeuib.ttf")))
    pdfmetrics.registerFontFamily("Segoe", normal="Segoe", bold="Segoe-Bold")
    s = _styles()

    roles = [
        f"<b>{title}</b> · {dates.format(PROMOTED=PROMOTED, PROMOTED_LOWER=PROMOTED.lower())}"
        for title, dates in ROLES
    ]
    story = [
        Paragraph(NAME, s["name"]),
        Paragraph(HEADLINE, s["headline"]),
        Spacer(1, 6),
        *[Paragraph(line, s["meta"]) for line in CONTACTS],
        Spacer(1, 7),
        HRFlowable(width="100%", thickness=0.8, color=RULE, spaceBefore=2, spaceAfter=0),
        Paragraph("О СЕБЕ", s["section"]),
        Paragraph(ABOUT, s["body"]),
        Paragraph("ОПЫТ", s["section"]),
        Paragraph(COMPANY, s["company"]),
        *[Paragraph(role, s["role"]) for role in roles],
        Spacer(1, 3),
        Paragraph(COMPANY_DESCRIPTION, s["body"]),
        *[Paragraph(f"- <b>{lead}</b> {_nbsp(text)}", s["bullet"]) for lead, text in ACHIEVEMENTS],
        Paragraph("ИНСТРУМЕНТЫ И НАВЫКИ", s["section"]),
        *[Paragraph(f"<b>{group}:</b> {items}", s["body"]) for group, items in SKILLS],
        Paragraph("ОБРАЗОВАНИЕ И РАЗВИТИЕ", s["section"]),
        *[Paragraph(f"<b>{place}:</b> {text}", s["small"]) for place, text in EDUCATION],
        Spacer(1, 3),
        Paragraph(EARLIER, s["small"]),
    ]
    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=15 * mm, rightMargin=15 * mm, topMargin=16 * mm, bottomMargin=16 * mm,
        title=f"{NAME} — QA Automation Engineer (Python)", author=NAME,
        subject="Web, API, автоматизация на Python",
    )
    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    return OUT


if __name__ == "__main__":
    print(build())
