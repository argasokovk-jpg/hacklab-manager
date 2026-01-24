#!/bin/bash
echo "🚀 HackLab Manager v2.0 - Установка"
echo "=========================================="

# Создаем директории
mkdir -p ~/.hacklab/tools
mkdir -p ~/.hacklab/scans

# Копирование
echo "📁 Копирование файлов..."
cp -r tools/* ~/.hacklab/tools/
cp hl ~/.hacklab/
chmod +x ~/.hacklab/hl

# Исправляем пути в hl
sed -i "s|TOOLS_DIR =.*|TOOLS_DIR = os.path.expanduser('~/.hacklab/tools')|" ~/.hacklab/hl
sed -i "s|/usr/local/bin/tools/|~/.hacklab/tools/|g" ~/.hacklab/hl

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
ln -sf ~/.hacklab/hl ~/.local/bin/hl 2>/dev/null || true

echo ""
echo "🎉 УСТАНОВКА ЗАВЕРШЕНА!"
echo "Запуск: ~/.hacklab/hl"
echo "Или: hl (если ~/.local/bin в PATH)"
