#!/bin/bash
echo "========================================="
echo "🚀 HackLab Manager v2.2 - INSTALLER"
echo "========================================="
echo ""

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден!"
    echo "Установите: sudo apt install python3 python3-pip"
    exit 1
fi

# Проверка pip
if ! command -v pip3 &> /dev/null; then
    echo "📦 Установка pip3..."
    sudo apt update && sudo apt install -y python3-pip
fi

# Установка зависимостей
echo "📦 Установка зависимостей..."
pip3 install --user fpdf2 requests beautifulsoup4 python-whois colorama

# Создание конфигурационной папки
echo "📁 Создание конфигурации..."
mkdir -p ~/.hacklab/reports
echo '{"mode": "beginner", "level": 1, "xp": 0, "unlocked_tools": ["network_info", "port_check"]}' > ~/.hacklab/config.json

# Установка hl в PATH
echo "🔗 Установка hl команды..."
chmod +x hl
if [ -d "$HOME/.local/bin" ]; then
    cp hl ~/.local/bin/
    echo "✅ Команда 'hl' установлена в ~/.local/bin/"
else
    sudo cp hl /usr/local/bin/
    echo "✅ Команда 'hl' установлена в /usr/local/bin/"
fi

echo ""
echo "========================================="
echo "🎉 HackLab Manager v2.2 УСТАНОВЛЕН!"
echo "========================================="
echo ""
echo "📋 КОМАНДЫ:"
echo "  hl                     - Главное меню"
echo "  hl scan <target>       - Сканирование цели"
echo "  hl analyze             - Анализ твоего подхода"
echo "  hl report lab 1        - PDF отчет"
echo "  hl tools               - Все 12 инструментов"
echo ""
echo "📚 ПРИМЕРЫ:"
echo "  hl scan scanme.nmap.org"
echo "  hl scan testfire.net --tool web_scanner"
echo "  hl mode professional"
echo ""
echo "💡 Первый запуск: hl"
echo "========================================="
