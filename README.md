# HackLab Manager 🧠⚔️

HackLab Manager is a **Cognitive Pentest Analyzer** — a framework that analyzes **how a pentester thinks**, not just whether an exploit worked.

Unlike classic platforms (TryHackMe, HTB), HackLab Manager focuses on:
- methodology
- decision-making
- sequence of actions
- efficiency and noise
- professional pentest thinking

## 🔑 Key Feature: Cognitive Pentest Analyzer

HackLab Manager evaluates:
- Recon → Scan → Analysis → Exploit order
- Time between actions
- Redundant / noisy behavior
- Tool selection efficiency
- Overall pentest strategy

It generates:
- score (0–100)
- skill level (Junior / Middle / Senior)
- actionable recommendations
- professional PDF reports

## 🚀 Features

- 🧠 Cognitive analysis of pentest methodology
- 🛠️ 12 integrated pentesting tools
- 🧪 Interactive Labs (Web, Network)
- 📊 Automatic action logging (SQLite)
- 📄 Professional PDF reports
- 📚 Interactive learning mode (`hl learn`)
- ⚙️ Fully CLI-based (Linux)

## 🧪 Labs

- **Lab 1:** Web Pentest (SQLi, XSS, Dir Busting)
- **Lab 2:** Network + Web Pentest (scanme.nmap.org)

Start a lab:
=======
HackLab Manager — это CLI-фреймворк для обучения пентесту, который фокусируется не на флагах и чеклистах, а на мышлении пентестера.

Проект анализирует:
 порядок действий,
 выбор инструментов,
 методологию,
а не просто результат «нашёл / не нашёл».

Если коротко — HackLab Manager учит думать как пентестер.

"Зачем этот проект?"

Большинство платформ по пентесту:
 проверяют только результат,
 не объясняют, почему ты ошибся,
 не оценивают ход мыслей.

HackLab Manager решает другую задачу:

показать, как ты думаешь, и помочь улучшить подход.

Ключевые возможности
 Thinking Analysis Engine
Анализирует последовательность действий и методологию пентеста.
 Learning Mode (hl learn)
Объясняет базовый подход к пентесту и правильный порядок шагов.
 Практические лаборатории
Задания с идеальной последовательностью и анализом ошибок.
 Профессиональные PDF-отчёты
Итоговый отчёт с оценкой уровня и рекомендациями.
 CLI-first
Минимум лишнего — всё работает из терминала.

Быстрый старт

curl -fsSL https://raw.githubusercontent.com/argasokovk-jpg/hacklab-manager/main/install.sh | bash
hl learn
hl lab start 1
hl analyze

Как это работает
 1. Пользователь выполняет действия (сканирование, разведка, тестирование)
 2. Все шаги автоматически логируются
 3. Анализатор оценивает:
 4. порядок действий
 5. логику выбора инструментов
 6. наличие лишних шагов
 7. Пользователь получает:
 8. уровень (Junior / Middle / Senior)
 9. рекомендации
 10. PDF-отчёт

Для кого этот проект
  начинающие пентестеры
  студенты ИБ
  junior-специалисты
  все, кто хочет улучшить подход, а не просто «решать задания»

Статус проекта

Проект активно развивается.
Это не коммерческий продукт и не finished-solution, а инженерный инструмент, который растёт вместе с пользователями.
