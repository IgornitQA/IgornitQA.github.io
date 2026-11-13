"""Собирает resume.pdf из текста ниже. Синхронизировано с резюме v3 (2026-11-13):
новое «О себе», ключевые результаты и impact-формулировки.

Запуск из корня репозитория:
    uv run --no-project --with reportlab python tools/build_resume.py

Шрифт — Segoe UI из Windows. Если этих файлов нет, берётся Noto Sans.
Свой каталог с segoeui.ttf и segoeuib.ttf — через RESUME_FONT_DIR.
"""
from __future__ import annotations

import os
from pathlib import Path

from reportlab import rl_config
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
HEADLINE = "Middle QA Engineer (Automation, Python) · Fullstack · AI"
FOOTER_TEXT = f"{NAME} · QA Engineer (Automation, Python)"

CONTACTS = [
    "Краснодар · UTC+3 · Только удалённая работа",
    '<a href="mailto:initochkin@yandex.ru">initochkin@yandex.ru</a> · '
    '<a href="tel:+79654591381">+7 965 459-13-81</a> · '
    '<a href="https://t.me/i_nitochkin">Telegram: @i_nitochkin</a>',
    '<a href="https://igornitqa.github.io/">Портфолио: igornitqa.github.io</a> · '
    '<a href="https://github.com/IgornitQA">GitHub: IgornitQA</a> · '
    '<a href="https://hh.ru/resume/306d67f1ff0e94d76b0039ed1f4e475a566e42">Резюме на hh.ru</a>',
]

ABOUT = (
    "QA Engineer (Automation, Python) в финтехе, в тестировании с апреля 2025 года. В QUGO — "
    "платформе выплат самозанятым — отвечаю за качество сценариев от интерфейса до записи в БД. "
    "Строю автоматизацию, которая "
    "снимает рутину с команды: регресс из 220 автотестов поддерживает еженедельные релизы без "
    "ночного сопровождения QA, а E2E на production запускаются безопасно — с guard'ами и "
    "синтетическими данными. Развиваю AI в QA-цикле: бот ревью кода автотестов и воркфлоу "
    "AI-агентов. Ищу удалённую роль Middle fullstack QA."
)

KEY_RESULTS = [
    ("220 автотестов в регрессе —", " команда выпускает каждую неделю; автотесты на деплое сняли ночное сопровождение релизов силами QA."),
    ("E2E регистрации ускорен с 85 до 43–45 с,", " API-регресс расширен с 13 до 33 сценариев — расхождения интеграций ловятся до релиза."),
    ("AI-агенты в QA-цикле:", " выстроил воркфлоу QA-kit — за один день (12 часов) протестировал 6 продуктовых и 17 dev-задач."),
]

COMPANY = "QUGO"
ROLES = [
    ("QA Engineer (автоматизация)", "{PROMOTED} — настоящее время"),
    ("Junior QA Engineer", "Апрель 2025 — {PROMOTED_LOWER}"),
]
PROMOTED = "Октябрь 2026"
COMPANY_DESCRIPTION = (
    "Финтех-платформа для выплат самозанятым. Команда 25 человек, в QA — 6. Работаю с банковскими "
    "и налоговыми интеграциями: регистрацией, проверками статусов в ФНС, выплатами, реестрами "
    "и документооборотом."
)

ACHIEVEMENTS = [
    ("Вывел E2E регистрации и авторизации на production:",
     "запуск только CI-джобой с master, guard от случайного локального запуска, синтетические ИНН, "
     "удаление тестового пользователя до и после прогона, техномер вместо личного телефона. Критичные сценарии проверяются на живых интеграциях без риска для реальных данных."),
    ("Ускорил E2E регистрации на тестовом стенде",
     "примерно с 85 до 43–45 секунд: ожидание OTP вместо фиксированных пауз, убрал повторные действия."),
    ("Расширил API-регресс:",
     "добавил 20 новых сценариев к 13 существовавшим. Реализовал изоляцию данных, Pydantic-контракты, "
     "постусловия в MySQL и маскирование секретов в Allure."),
    ("Перевёл проект на uv, обновил Docker и GitLab CI;",
     "подключил JUnit-отчёты — результаты тестов видны прямо в merge request."),
    ("Разработал и внедрил неблокирующего бота ревью кода автотестов:",
     "линтеры и чистота кода, без спама мелочами — только серьёзные ошибки; ревью не тормозит merge."),
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
    ("AI в QA", "ревью требований, тест-дизайн, диагностика падений, ревью кода автотестов."),
    ("Данные и диагностика", "SQL, PostgreSQL, MySQL, Grafana, Loki, OpenSearch."),
    ("Тест-дизайн", "таблицы решений, классы эквивалентности, граничные значения, переходы состояний, "
                    "анализ требований."),
    ("Тестирование", "REST API, Web, Android, ручное и интеграционное тестирование, Postman, "
                     "Swagger / OpenAPI, DevTools."),
    ("Процесс", "Test IT, Яндекс Трекер, Яндекс Вики, Figma."),
]

EDUCATION = [
    ("QA Studio", "ручное тестирование (2025), автоматизация на Python (2026)."),
    ("Образование", "среднее специальное."),
    ("Английский", "A1 — читаю техническую документацию, разговорный — базовый."),
]
EARLIER = "С июня 2020 по январь 2025 работал фриланс-фотографом, а с апреля 2025 перешёл в тестирование."


def _nbsp(text: str) -> str:
    return text.replace(" — ", " — ")


def _font_files() -> tuple[Path, Path, str, str]:
    regular = FONT_DIR / "segoeui.ttf"
    bold = FONT_DIR / "segoeuib.ttf"
    if regular.is_file() and bold.is_file():
        return regular, bold, "Segoe", "Segoe-Bold"
    noto = Path("/usr/share/fonts/truetype/noto")
    regular, bold = noto / "NotoSans-Regular.ttf", noto / "NotoSans-Bold.ttf"
    if regular.is_file() and bold.is_file():
        return regular, bold, "NotoSans", "NotoSans-Bold"
    raise SystemExit(f"Нужны segoeui.ttf и segoeuib.ttf в {FONT_DIR}.")


def _styles(font: str, font_bold: str) -> dict[str, ParagraphStyle]:
    base = ParagraphStyle("base", fontName=font, fontSize=9.2, leading=11.9, textColor=INK)
    return {
        "name": ParagraphStyle("name", base, fontName=font_bold, fontSize=25, leading=29),
        "headline": ParagraphStyle("headline", base, fontSize=12.5, leading=17, textColor=ACCENT, spaceBefore=2),
        "meta": ParagraphStyle("meta", base, fontSize=8.8, leading=14, textColor=MUTED),
        "section": ParagraphStyle("section", base, fontName=font_bold, fontSize=10, textColor=ACCENT,
                                  spaceBefore=4, spaceAfter=2.5),
        "company": ParagraphStyle("company", base, fontName=font_bold, fontSize=11.5, leading=15),
        "role": ParagraphStyle("role", base, fontSize=9, leading=12, textColor=MUTED),
        "body": base,
        "bullet": ParagraphStyle("bullet", base, leftIndent=9, firstLineIndent=-9, spaceBefore=1.8),
        "small": ParagraphStyle("small", base, fontSize=8.8, leading=11.8, textColor=MUTED),
    }


def _footer(font: str):
    def draw(canvas, doc) -> None:
        canvas.saveState()
        canvas.setFont(font, 7.6)
        canvas.setFillColor(FOOTER)
        canvas.drawString(doc.leftMargin, 9 * mm, FOOTER_TEXT)
        canvas.drawRightString(A4[0] - doc.rightMargin, 9 * mm, str(doc.page))
        canvas.restoreState()
    return draw


def build(out: Path | None = None) -> Path:
    # Одинаковый текст и шрифт дают одинаковые байты: без этого CreationDate
    # и id документа меняются на каждом запуске и workflow коммитит PDF зря.
    rl_config.invariant = 1
    destination = OUT if out is None else Path(out)
    regular_path, bold_path, font, font_bold = _font_files()
    pdfmetrics.registerFont(TTFont(font, str(regular_path)))
    pdfmetrics.registerFont(TTFont(font_bold, str(bold_path)))
    pdfmetrics.registerFontFamily(font, normal=font, bold=font_bold)
    s = _styles(font, font_bold)
    draw_footer = _footer(font)

    roles = [
        f"<b>{title}</b> · {dates.format(PROMOTED=PROMOTED, PROMOTED_LOWER=PROMOTED.lower())}"
        for title, dates in ROLES
    ]
    story = [
        Paragraph(NAME, s["name"]),
        Paragraph(HEADLINE, s["headline"]),
        Spacer(1, 3),
        *[Paragraph(line, s["meta"]) for line in CONTACTS],
        Spacer(1, 4),
        HRFlowable(width="100%", thickness=0.8, color=RULE, spaceBefore=2, spaceAfter=0),
        Paragraph("О СЕБЕ", s["section"]),
        Paragraph(ABOUT, s["body"]),
        Paragraph("КЛЮЧЕВЫЕ РЕЗУЛЬТАТЫ", s["section"]),
        *[Paragraph(f"- <b>{lead}</b>{_nbsp(text)}", s["bullet"]) for lead, text in KEY_RESULTS],
        Paragraph("ОПЫТ", s["section"]),
        Paragraph(COMPANY, s["company"]),
        *[Paragraph(role, s["role"]) for role in roles],
        Spacer(1, 3),
        Paragraph(COMPANY_DESCRIPTION, s["body"]),
        *[Paragraph(f"- <b>{lead}</b> {_nbsp(text)}" if text else f"- <b>{lead}</b>", s["bullet"]) for lead, text in ACHIEVEMENTS],
        Paragraph("ИНСТРУМЕНТЫ И НАВЫКИ", s["section"]),
        *[Paragraph(f"<b>{group}:</b> {items}", s["body"]) for group, items in SKILLS],
        Paragraph("ОБРАЗОВАНИЕ И РАЗВИТИЕ", s["section"]),
        *[Paragraph(f"<b>{place}:</b> {text}", s["small"]) for place, text in EDUCATION],
        Spacer(1, 3),
        Paragraph(EARLIER, s["small"]),
    ]
    doc = SimpleDocTemplate(
        str(destination), pagesize=A4,
        leftMargin=15 * mm, rightMargin=15 * mm, topMargin=9 * mm, bottomMargin=9 * mm,
        title=f"{NAME} — QA Engineer (Automation, Python)",
        author=NAME,
        subject="Web, API, автоматизация на Python",
        invariant=1,
    )
    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
    return destination


if __name__ == "__main__":
    print(build())
