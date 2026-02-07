#!/bin/bash
# HackLab Manager Installer v2.1

set -e

echo "🚀 HackLab Manager v2.1 - Установка"
echo "=========================================="

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Проверка Python
echo -e "${BLUE}🔍 Проверка зависимостей...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 не установлен${NC}"
    exit 1
fi

# Создаем директории
echo -e "${BLUE}📁 Создание структуры...${NC}"
mkdir -p ~/.hacklab
mkdir -p ~/.hacklab/tools
mkdir -p ~/.hacklab/reports
mkdir -p ~/.local/bin 2>/dev/null || true

# Копируем основные файлы
echo -e "${BLUE}📁 Копирование файлов...${NC}"

# Копируем ядро системы
if [ -d "core" ]; then
    cp -r core ~/.hacklab/
fi

# Копируем инструменты (ВАЖНО: правильный путь)
if [ -d "tools" ]; then
    cp -r tools/* ~/.hacklab/tools/
fi

# Копируем базу данных
if [ -d "db" ]; then
    cp -r db ~/.hacklab/
fi

# Копируем лаборатории
if [ -d "labs" ]; then
    cp -r labs ~/.hacklab/
fi

# Копируем hl скрипт и исправляем пути
echo -e "${BLUE}⚙️  Настройка CLI...${NC}"
if [ -f "hl" ]; then
    cp hl ~/.hacklab/
    chmod +x ~/.hacklab/hl
    
    # Исправляем BASE_DIR в скопированном hl
    sed -i "s|BASE_DIR =.*|BASE_DIR = os.path.expanduser('~/.hacklab')|" ~/.hacklab/hl 2>/dev/null || true
    sed -i "s|TOOLS_DIR =.*|TOOLS_DIR = os.path.join(BASE_DIR, 'tools')|" ~/.hacklab/hl 2>/dev/null || true
else
    echo -e "${YELLOW}⚠️  Файл hl не найден${NC}"
fi

# Создаем симлинк
echo -e "${BLUE}🔗 Создание ссылки...${NC}"
ln -sf ~/.hacklab/hl ~/.local/bin/hl 2>/dev/null || true

# Создаем конфигурацию
echo -e "${BLUE}⚙️  Создание конфигурации...${NC}"
cat > ~/.hacklab/config.json << 'CONFIG'
{
  "mode": "beginner",
  "level": 1,
  "xp": 0,
  "unlocked_tools": ["network_info", "port_check"],
  "first_run": false,
  "created": "$(date -Iseconds)"
}
CONFIG

# Создаем базу данных
echo -e "${BLUE}🗄️  Инициализация базы данных...${NC}"
if [ -f "db/init.py" ]; then
    cp db/init.py ~/.hacklab/db/
    cd ~/.hacklab
    python3 db/init.py 2>/dev/null || true
    cd - > /dev/null
elif [ -f "~/.hacklab/db/init.py" ]; then
    cd ~/.hacklab
    python3 db/init.py 2>/dev/null || true
    cd - > /dev/null
fi

echo -e "\n${GREEN}🎉 УСТАНОВКА ЗАВЕРШЕНА!${NC}"
echo ""
echo -e "${BLUE}📋 КОМАНДЫ:${NC}"
echo -e "  ${YELLOW}hl${NC}                    - Главное меню"
echo -e "  ${YELLOW}hl scan <цель>${NC}       - Сканирование"
echo -e "  ${YELLOW}hl analyze${NC}           - Анализ твоего подхода"
echo -e "  ${YELLOW}hl lab list${NC}          - Лаборатории"
echo -e "  ${YELLOW}hl report lab 1${NC}      - PDF отчет"
echo -e "  ${YELLOW}hl tools${NC}             - Все инструменты"
echo ""
echo -e "${YELLOW}💡 Перезапустите терминал или выполните:${NC}"
echo -e "  source ~/.bashrc  # или source ~/.zshrc"
echo ""
echo -e "${GREEN}🚀 Начните с: hl lab start 1${NC}"
