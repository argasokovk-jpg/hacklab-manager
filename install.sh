#!/bin/bash
echo "🚀 HackLab Manager v2.0 - Установка"
echo "=========================================="

# Проверка зависимостей
echo "🔍 Проверка зависимостей..."
if python3 -c "import requests, whois" 2>/dev/null; then
    echo "✅ Зависимости установлены"
else
    echo "⚠️  Зависимости не найдены"
    echo "💡 Для Kali Linux: sudo apt install python3-requests python3-whois"
    exit 1
fi

# Копирование файлов
echo "📁 Копирование файлов..."
mkdir -p ~/.hacklab/tools
cp -r tools/* ~/.hacklab/tools/
cp hl ~/.hacklab/
chmod +x ~/.hacklab/hl

# Исправляем пути в hl
sed -i "s|TOOLS_DIR =.*|TOOLS_DIR = os.path.expanduser('~/.hacklab/tools')|" ~/.hacklab/hl 2>/dev/null || true

# Конфиг
echo "⚙️  Создание конфигурации..."
cat > ~/.hacklab/config.json << 'CONFIG'
{
  "mode": "beginner",
  "level": 1,
  "xp": 0,
  "unlocked_tools": ["network_info", "port_check"],
  "first_run": true,
  "created": "$(date -Iseconds)"
}
CONFIG

# Ссылка
echo "🔗 Создание ссылки..."
mkdir -p ~/.local/bin
ln -sf ~/.hacklab/hl ~/.local/bin/hl 2>/dev/null || true

echo ""
echo "🎉 УСТАНОВКА ЗАВЕРШЕНА!"
echo ""
echo "📋 КОМАНДЫ:"
echo "  hl learn          - Обучение"
echo "  hl scan <цель>    - Сканирование"
echo "  hl dashboard      - Ваш прогресс"
echo "  hl tools          - Инструменты"
