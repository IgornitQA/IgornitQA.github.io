# Игорь Ниточкин · QA Automation Engineer (Python)

Персональное портфолио: автоматизация UI/API в финтехе, проверки контрактов и состояния данных, применение AI в QA-цикле. Статический сайт для GitHub Pages без сборки, внешних библиотек, аналитики и форм сбора данных.

## Локальный просмотр

Из корня репозитория:

```sh
python -m http.server 4173 --bind 127.0.0.1
```

Открыть http://127.0.0.1:4173/ в браузере.

## Структура

- `index.html` — главная страница, опыт, инструменты и контакты.
- `cases/api-regression.html` — кейс: фикстуры, контракты, постусловия в БД и отчётность.
- `cases/ai-in-qa.html` — кейс: ревью требований, тест-дизайн, автотесты и диагностика с AI.
- `cases/happy-path-bot.html` — кейс: подготовка тестовой документации и связь Яндекс Трекера с Test IT.
- `styles.css` — оформление и адаптивная вёрстка.
- `script.js` — мобильная навигация, копирование email, год в подвале.
- `resume.pdf` — одностраничное резюме; собирается `tools/build_resume.py` (`uv run --no-project --with reportlab python tools/build_resume.py`), после пересборки поднять `?v=` в ссылках на PDF.
- `avatar.png`, `mark.svg` — фотография и значок сайта.

## Автотесты сайта

[![Автотесты сайта](https://github.com/igornitqa/igornitqa.github.io/actions/workflows/site-tests.yml/badge.svg)](https://github.com/igornitqa/igornitqa.github.io/actions/workflows/site-tests.yml)

pytest + Playwright в `tests/`: страницы открываются без ошибок консоли и битых запросов; внутренние ссылки, якоря и ресурсы отвечают 200; нет горизонтального скролла на телефоне, планшете и десктопе; мобильное меню и копирование email работают; axe-core без нарушений serious/critical; PDF-резюме валидно, а email и Telegram в нём совпадают с сайтом. CI гоняет набор на каждый push и PR, по понедельникам — по опубликованному сайту вместе с внешними ссылками.

```sh
cd tests
python -m venv .venv && .venv/Scripts/pip install -r requirements.txt   # Linux/macOS: .venv/bin/pip
.venv/Scripts/python -m playwright install chromium
.venv/Scripts/python -m pytest                     # локальный сервер поднимается сам
SITE_URL=https://igornitqa.github.io .venv/Scripts/python -m pytest -m ""   # опубликованный сайт + внешние ссылки
```

Опубликованная версия: https://igornitqa.github.io/. Закрытый код, внутренние адреса и данные пользователей на сайт не попадают.
