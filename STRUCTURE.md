# HackLab Manager v2.0 - Структура проекта

## 📁 ПАПКИ ПРОЕКТА

hacklab_v2/
├── config/                 # Конфигурационные файлы
│   ├── levels.json        # Настройки уровней и XP
│   ├── premium.json       # Настройки Premium
│   └── users/             # Пользовательские конфиги
├── core/                  # Ядро системы
│   ├── __init__.py
│   ├── hacklab_core.py   # Основной класс менеджера
│   ├── logger.py         # Система логирования
│   ├── auth.py           # Аутентификация
│   └── premium.py        # Управление Premium
├── data/                  # Данные пользователей
│   ├── progress.json     # Прогресс пользователя
│   ├── achievements.json # Достижения
│   └── history/          # История сканирований
├── tools/                 # Инструменты пентеста
│   ├── __init__.py
│   ├── tool_base.py      # Базовый класс инструментов
│   ├── network_info.py   # Ур.1 - Сетевая информация
│   ├── port_check.py     # Ур.2 - Проверка портов
│   ├── web_scanner.py    # Ур.3 - Веб-сканер
│   ├── ssl_checker.py    # Ур.4 - Проверка SSL
│   ├── whois_checker.py  # Ур.4 - WHOIS информация
│   ├── dir_buster.py     # Ур.5 - Поиск директорий
│   ├── subdomain_scanner.py # Ур.6 - Поиск субдоменов
│   ├── cve_lookup.py     # Ур.7 - Поиск CVE
│   ├── hash_cracker.py   # Ур.8 - Взлом хешей
│   ├── sql_tester.py     # Ур.9 - SQL инъекции
│   ├── xss_scanner.py    # Ур.10 - XSS сканер
│   └── api_fuzzer.py     # Ур.10 - API фаззер
├── wordlists/            # Словари для инструментов
│   ├── dir_common.txt    # Директории
│   ├── subdomains.txt    # Субдомены
│   └── passwords.txt     # Пароли
├── modules/              # Дополнительные модули
│   ├── learning/         # Обучение
│   ├── reporting/        # Отчеты
│   └── integration/      # Интеграции
├── reports/              # Отчеты сканирований
├── hl                    # Главный исполняемый файл
├── README.md             # Документация
└── requirements.txt      # Зависимости

## 🔗 ИНТЕГРАЦИЯ С СУЩЕСТВУЮЩЕЙ ЛАБОРАТОРИЕЙ

/home/kali/my_hacking_lab/     # Существующая лаборатория
├── scans/                    # Сканы (можно интегрировать)
├── tools/                   # Инструменты (можно мигрировать)
├── reports/                 # Отчеты (можно использовать)
└── targets/                 # Цели для сканирования
