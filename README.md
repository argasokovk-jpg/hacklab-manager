# 🧠 HackLab Manager

**HackLab Manager** — это CLI-платформа для обучения пентесту, которая анализируетдля обучения пенте а🧠 HackLab Manager

**Hac

Вместо проверки “взломал или нет”, система оценивает:

- 🧭 последовательность действий
- ⚡ эффективность подхода
- 🧠 методологию pentest
- 📊 качество принятия решений

Главная фича —истема оценивает:

- 🧭 последов

## ⚡ Try in 30 seconds

```bash
git clone https://github.com/argasokovk-jpg/hacklab-manager
cd hacklab-manager
bash install.sh

hl learn

После запуска ты сразу увидишь, как система анализирует твой подход к пентесту.

🎯 Основная идея

Большинство платформ учат:

Найди уязвимость → получи флаг

HackLab Manager учит:

Как думает профессиональный пентестер

Система анализирует:

Recon → Scan → Analysis → Exploitation → Reporting

и даёт рекомендации по улучшению стратегии.

🧠 Cognitive Pentest Analyzer

Analyzer оценивает:
 • правильность последовательности действий
 • лишние шаги (noise detection)
 • скорость принятия решений
 • эффективность инструментов
 • уровень навыка (Junior → Professional)

Пример:

Score: 79/100
Level: Middle
Recommendation:
- Start with reconnaissance before scanning
- Reduce repeated actions
- Add directory discovery earlier

🧪 Labs

Встроенные лаборатории:

Lab 1 — Web Pentest
 • SQL Injection
 • XSS
 • Directory discovery

Lab 2 — Network + Web
 • target: scanme.nmap.org (legal training target)
 • reconnaissance methodology
 • service analysis

Запуск:

hl lab list
hl lab start 1

📚 Learning Mode

Интерактивное обучение:

hl learn

Включает:
 • методологию пентеста
 • практические сценарии
 • подготовку к лабораториям
 • мини-тесты

📊 PDF Reports

Генерация профессиональных отчетов:

hl analyze
hl report lab 1

Отчет включает:
 • итоговую оценку
 • использованные инструменты
 • рекомендации
 • хронологию действий

Подходит для портфолио.

🛠 Tools Included
 • network_info
 • port_check
 • web_scanner
 • dir_buster
 • sql_tester
 • xss_scanner
 • ssl_checker
 • whois_checker
 • subdomain_scanner
 • api_fuzzer
 • hash_cracker
 • cve_lookup

Все действия автоматически логируются для анализа.

⸻

🚀 Installation

git clone https://github.com/argasokovk-jpg/hacklab-manager
cd hacklab-manager
bash install.sh


🧭 Example Workflow

hl learn
hl lab start 1

hl scan testfire.net --tool network_info
hl scan testfire.net --tool port_check

hl analyze
hl report lab 1


🌐 Website

http://hacklabtools.ru


🤝 Contributing

Feedback and ideas are welcome!

Open:
 • Discussions for questions
 • Issues for improvements

⭐ Support the project

If HackLab Manager helps your learning journey, consider starring the repository ⭐

## 🌐 Веб-интерфейс

HackLab Manager теперь доступен в браузере!

### Запуск веб-сервера

```bash
cd hacklab-manager
source venv/bin/activate
uvicorn web.main:app --reload --host 0.0.0.0 --port 8000
