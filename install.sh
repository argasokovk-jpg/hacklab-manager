#!/bin/bash

set -e

echo "🚀 HackLab Manager v2.3 Installer"
echo "=================================="

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не установлен. Установите: sudo apt install python3"
    exit 1
fi

# Создаем директории
echo "📁 Создаем структуру каталогов..."
mkdir -p ~/.hacklab
mkdir -p ~/.local/bin

# Копируем файлы
echo "📦 Копируем файлы..."

# Основные файлы
cp hl ~/.local/bin/hl
chmod +x ~/.local/bin/hl

# Ядро системы
mkdir -p ~/.hacklab/core
cp core/*.py ~/.hacklab/core/ 2>/dev/null || echo "⚠️  Core файлы не найдены"

# Инструменты
mkdir -p ~/.hacklab/tools
cp tools/*.py ~/.hacklab/tools/ 2>/dev/null || echo "⚠️  Tools не найдены"

# Лаборатории (включая новую Lab 2)
mkdir -p ~/.hacklab/labs
cp -r labs/* ~/.hacklab/labs/ 2>/dev/null || echo "⚠️  Лаборатории не найдены"

# Обучение
cp learn.py ~/.hacklab/ 2>/dev/null || echo "⚠️  learn.py не найден"

# Отчеты
mkdir -p ~/.hacklab/reports
cp reports/*.py ~/.hacklab/reports/ 2>/dev/null || echo "⚠️  Reports не найдены"

# Конфигурация
if [ ! -f ~/.hacklab/config.json ]; then
    echo '{"mode": "beginner", "level": 1, "xp": 0, "unlocked_tools": ["network_info", "port_check"]}' > ~/.hacklab/config.json
fi

# Устанавливаем зависимости
echo "📦 Устанавливаем зависимости Python..."
pip3 install -q requests reportlab colorama

# Проверяем установку
echo "🔍 Проверяем установку..."
if [ -f ~/.local/bin/hl ]; then
    echo ""
    echo "✅ HackLab Manager v2.3 успешно установлен!"
    echo ""
    echo "📚 КОМАНДЫ:"
    echo "   hl learn          - Интерактивное обучение методологии"
    echo "   hl lab start 1    - Lab 1: Web Pentest (testfire.net)"
    echo "   hl lab start 2    - Lab 2: Network+Web Pentest (scanme.nmap.org) - НОВОЕ!"
    echo "   hl scan [цель]    - Сканирование цели"
    echo "   hl analyze        - Анализ твоего подхода с улучшенной логикой"
    echo "   hl lab list       - Список лабораторий"
    echo ""
    echo "🎯 НОВОЕ В v2.3:"
    echo "   • Полностью переработанный 'hl learn'"
    echo "   • Новая Lab 2: Network + Web Pentest методика"
    echo "   • Улучшенный анализатор с оценкой времени и эффективности"
    echo "   • Фокус на мышлении пентестера, а не на инструментах"
    echo ""
    echo "💡 Начни с: hl learn"
else
    echo "❌ Ошибка установки"
    exit 1
fi
