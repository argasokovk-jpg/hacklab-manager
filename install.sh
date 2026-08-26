#!/bin/bash

echo ""
echo "🚀 HackLab Manager v2.3 Installer"
echo "=================================="

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установи Python 3.8+"
    exit 1
fi

# Проверка наличия pip
if ! command -v pip &> /dev/null; then
    echo "❌ pip не найден. Установи pip"
    exit 1
fi

# Установка зависимостей
echo "📦 Устанавливаем зависимости..."
pip install --upgrade pip
pip install -r requirements.txt

# Установка зависимостей для веб-интерфейса
echo ""
echo "📦 Устанавливаем веб-зависимости..."
pip install fastapi uvicorn sqlalchemy python-jose[cryptography] passlib[bcrypt] python-multipart jinja2 websockets docker

# Проверка Docker
if command -v docker &> /dev/null; then
    echo "✅ Docker обнаружен"
else
    echo "⚠️ Docker не найден. Установи Docker для изоляции лабораторий"
    echo "   sudo apt install docker.io"
    echo "   sudo usermod -aG docker \$USER"
fi

# Делаем hl исполняемым
chmod +x hl

# Создаём папки
mkdir -p web/static/css web/static/js
mkdir -p sandbox
mkdir -p db

# Добавляем в PATH
if ! grep -q "hacklab-manager" ~/.bashrc; then
    echo 'export PATH="$PATH:'$(pwd)'"' >> ~/.bashrc
    echo 'export PYTHONPATH="$PYTHONPATH:'$(pwd)'"' >> ~/.bashrc
    echo "✅ Пути добавлены в .bashrc"
fi

echo ""
echo "✅ HackLab Manager v2.3 успешно установлен!"
echo ""
echo "📚 КОМАНДЫ:"
echo "   hl learn          - Интерактивное обучение методологии"
echo "   hl lab start 1    - Lab 1: Web Pentest (testfire.net)"
echo "   hl lab start 2    - Lab 2: Network+Web Pentest (scanme.nmap.org)"
echo "   hl scan [цель]    - Сканирование цели"
echo "   hl analyze        - Анализ твоего подхода с улучшенной логикой"
echo "   hl lab list       - Список лабораторий"
echo ""
echo "🌐 ВЕБ-ИНТЕРФЕЙС:"
echo "   uvicorn web.main:app --reload --host 0.0.0.0 --port 8000"
echo "   Открой в браузере: http://127.0.0.1:8000"
echo ""
echo "🎯 НОВОЕ В v2.3:"
echo "   • Полностью переработанный 'hl learn'"
echo "   • Новая Lab 2: Network + Web Pentest методика"
echo "   • Улучшенный анализатор с оценкой времени и эффективности"
echo "   • Фокус на мышлении пентестера, а не на инструментах"
echo "   • Веб-интерфейс с терминалом, Docker-изоляцией и аналитикой"
echo ""
echo "💡 Начни с: hl learn"
echo "========================================="
