#!/usr/bin/env python3

import os
import json
import sys
import time
import importlib
from pathlib import Path
from datetime import datetime

class HackLabManager:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.config_dir = Path.home() / '.hacklab'
        self.config_file = self.config_dir / 'config.json'
        
        # Создаем структуру папок
        self.setup_directories()
        
        # Загружаем конфиг
        self.config = self.load_config()
        
        # Загружаем инструменты
        self.tools = self.load_tools()
        
        print("HackLab Manager v2.0 инициализирован")
    
    def setup_directories(self):
        """Создает необходимые директории."""
        directories = [
            self.config_dir,
            self.config_dir / 'data',
            self.config_dir / 'data' / 'results',
            self.config_dir / 'data' / 'history',
            self.project_root / 'reports',
            self.project_root / 'wordlists'
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def load_config(self):
        """Загружает или создает конфигурацию."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return self.create_default_config()
        else:
            return self.create_default_config()
    
    def create_default_config(self):
        """Создает конфигурацию по умолчанию."""
        config = {
            'version': '2.0',
            'user_level': 1,
            'user_xp': 0,
            'total_xp': 0,
            'mode': 'beginner',
            'is_premium': False,
            'premium_until': None,
            'unlocked_tools': [
                'network_info',
                'port_check',
                'web_scanner',
                'ssl_checker',
                'whois_checker'
            ],
            'created_at': datetime.now().isoformat(),
            'last_login': datetime.now().isoformat()
        }
        
        # Сохраняем конфиг
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        return config
    
    def save_config(self):
        """Сохраняет конфигурацию."""
        self.config['last_login'] = datetime.now().isoformat()
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def load_tools(self):
        """Загружает доступные инструменты."""
        tools_dir = self.project_root / 'tools'
        tools = {}
        
        tool_files = [
            'network_info',
            'port_check', 
            'web_scanner',
            'ssl_checker',
            'whois_checker',
            'dir_buster',
            'subdomain_scanner',
            'cve_lookup',
            'hash_cracker',
            'sql_tester',
            'xss_scanner',
            'api_fuzzer'
        ]
        
        for tool_file in tool_files:
            tool_path = tools_dir / f'{tool_file}.py'
            if tool_path.exists():
                tools[tool_file] = {
                    'name': tool_file.replace('_', ' ').title(),
                    'file': tool_file,
                    'path': tool_path
                }
        
        return tools
    
    def show_welcome(self):
        """Показывает приветственное сообщение."""
        print("\n" + "="*60)
        print("🚀 HACKLAB MANAGER v2.0")
        print("="*60)
        print(f"👤 Уровень: {self.config['user_level']}")
        print(f"⭐ XP: {self.config['user_xp']}")
        print(f"🎮 Режим: {self.config['mode']}")
        print("="*60)
        print("\nДоступные команды:")
        print("  hl scan <target>     - Сканировать цель")
        print("  hl dashboard         - Показать прогресс")
        print("  hl tools             - Список инструментов")
        print("  hl mode <beg/pro>    - Сменить режим")
        print("  hl learn             - Обучение")
        print("  hl premium           - Premium информация")
        print("  hl help              - Помощь")
        print("\nПример: hl scan example.com")
        print("="*60)
    
    def show_help(self):
        """Показывает помощь."""
        print("\n📖 HackLab Manager - Помощь")
        print("="*40)
        print("\nОСНОВНЫЕ КОМАНДЫ:")
        print("  scan <цель> [инструмент]  - Сканирование цели")
        print("  dashboard                 - Прогресс и статистика")
        print("  tools                     - Доступные инструменты")
        print("  mode <beg/pro>            - Сменить режим (новичок/про)")
        print("  learn                     - Обучение пентесту")
        print("  premium                   - Информация о Premium")
        print("\nПРИМЕРЫ:")
        print("  hl scan 127.0.0.1")
        print("  hl scan example.com --tool web_scanner")
        print("  hl mode pro")
        print("\nРЕЖИМЫ:")
        print("  beginner (beg) - Обучение, 10 уровней")
        print("  pro            - Все инструменты сразу")
    
    def scan_target(self, target, tool_name=None):
        """Сканирует цель с помощью выбранного инструмента."""
        print(f"\n🎯 Сканирование цели: {target}")
        
        if tool_name:
            # Используем конкретный инструмент
            if tool_name in self.tools:
                self.run_tool(tool_name, target)
            else:
                print(f"❌ Инструмент '{tool_name}' не найден")
                print("Доступные инструменты:", list(self.tools.keys()))
        else:
            # Автоматический выбор инструмента на основе уровня
            available_tools = []
            for tool_id, tool_info in self.tools.items():
                if tool_id in self.config['unlocked_tools']:
                    available_tools.append(tool_id)
            
            if not available_tools:
                print("❌ Нет доступных инструментов для вашего уровня")
                return
            
            print(f"🔧 Доступно {len(available_tools)} инструментов")
            
            # Для начала используем простые инструменты
            simple_tools = ['network_info', 'port_check', 'whois_checker']
            for simple_tool in simple_tools:
                if simple_tool in available_tools:
                    self.run_tool(simple_tool, target)
                    return
            
            # Если простых нет, берем первый доступный
            self.run_tool(available_tools[0], target)
    
    def run_tool(self, tool_name, target):
        """Запускает конкретный инструмент."""
        try:
            # Динамически импортируем инструмент
            module_name = f"tools.{tool_name}"
            module = importlib.import_module(module_name)
            
            # Создаем экземпляр инструмента
            tool_class = getattr(module, tool_name.title().replace('_', ''))
            tool_instance = tool_class()
            
            # Запускаем инструмент
            print(f"\n🛠️  Запускаю {tool_name.replace('_', ' ').title()}...")
            result = tool_instance.run(target)
            
            # Добавляем XP
            xp_gained = self.add_xp(10)
            print(f"✨ +{xp_gained} XP получено!")
            
            return result
            
        except Exception as e:
            print(f"❌ Ошибка при запуске инструмента {tool_name}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def add_xp(self, amount):
        """Добавляет XP пользователю."""
        if not self.config.get('is_premium', False):
            amount = int(amount * 0.8)  # Бесплатные пользователи получают 80% XP
        
        self.config['user_xp'] += amount
        self.config['total_xp'] = self.config.get('total_xp', 0) + amount
        
        # Проверяем повышение уровня
        old_level = self.config['user_level']
        new_level = self.calculate_level(self.config['total_xp'])
        
        if new_level > old_level:
            self.config['user_level'] = new_level
            print(f"\n🎉 ПОЗДРАВЛЯЕМ! Вы достигли уровня {new_level}!")
            self.unlock_tools_for_level(new_level)
        
        self.save_config()
        return amount
    
    def calculate_level(self, xp):
        """Рассчитывает уровень на основе XP."""
        levels = {
            0: 1, 100: 2, 250: 3, 500: 4, 1000: 5,
            2000: 6, 4000: 7, 8000: 8, 16000: 9, 32000: 10
        }
        
        level = 1
        for xp_threshold, lvl in sorted(levels.items()):
            if xp >= xp_threshold:
                level = lvl
        
        return level
    
    def unlock_tools_for_level(self, level):
        """Разблокирует инструменты для нового уровня."""
        level_tools = {
            1: ['network_info'],
            2: ['port_check'],
            3: ['web_scanner'],
            4: ['ssl_checker', 'whois_checker'],
            5: ['dir_buster'],
            6: ['subdomain_scanner'],
            7: ['cve_lookup'],
            8: ['hash_cracker'],
            9: ['sql_tester'],
            10: ['xss_scanner', 'api_fuzzer']
        }
        
        unlocked = []
        for lvl in range(1, level + 1):
            if lvl in level_tools:
                for tool in level_tools[lvl]:
                    if tool not in self.config['unlocked_tools']:
                        self.config['unlocked_tools'].append(tool)
                        unlocked.append(tool)
        
        if unlocked:
            print(f"🔓 Разблокированы инструменты: {', '.join(unlocked)}")
            self.save_config()
    
    def show_dashboard(self):
        """Показывает дашборд с прогрессом."""
        print("\n📊 HACKLAB DASHBOARD")
        print("="*50)
        print(f"👤 Уровень: {self.config['user_level']}")
        print(f"⭐ Текущий XP: {self.config['user_xp']}")
        print(f"🏆 Всего XP: {self.config.get('total_xp', 0)}")
        print(f"🎮 Режим: {self.config['mode']}")
        print(f"💎 Premium: {'✅ АКТИВЕН' if self.config['is_premium'] else '❌ НЕ АКТИВЕН'}")
        print("="*50)
        
        # Показываем инструменты
        print("\n🛠️  ДОСТУПНЫЕ ИНСТРУМЕНТЫ:")
        unlocked = self.config['unlocked_tools']
        for tool_id, tool_info in self.tools.items():
            status = "✅" if tool_id in unlocked else "❌"
            print(f"  {status} {tool_info['name']}")
        
        # Прогресс до следующего уровня
        next_level_xp = self.get_xp_for_next_level()
        if next_level_xp:
            current_xp = self.config.get('total_xp', 0)
            progress = min(100, int((current_xp / next_level_xp) * 100))
            print(f"\n📈 До следующего уровня: {progress}%")
    
    def get_xp_for_next_level(self):
        """Возвращает XP необходимое для следующего уровня."""
        level_xp = {
            1: 100, 2: 250, 3: 500, 4: 1000, 5: 2000,
            6: 4000, 7: 8000, 8: 16000, 9: 32000, 10: 64000
        }
        current_level = self.config['user_level']
        if current_level in level_xp:
            return level_xp[current_level]
        return None
    
    def list_tools(self):
        """Показывает список всех инструментов."""
        print("\n🛠️  ИНСТРУМЕНТЫ HACKLAB MANAGER")
        print("="*60)
        
        for tool_id, tool_info in self.tools.items():
            is_unlocked = tool_id in self.config['unlocked_tools']
            status = "РАЗБЛОКИРОВАН" if is_unlocked else "ЗАБЛОКИРОВАН"
            color = "\033[92m" if is_unlocked else "\033[91m"
            
            print(f"\n{color}{tool_info['name']} ({tool_id})")
            print(f"Статус: {status}\033[0m")
        
        print("\nИспользуйте: hl scan <цель> --tool <имя_инструмента>")
        print("Пример: hl scan example.com --tool web_scanner")
    
    def set_mode(self, mode):
        """Устанавливает режим работы."""
        if mode in ['beg', 'beginner']:
            self.config['mode'] = 'beginner'
            print("✅ Режим установлен: Новичок")
        elif mode in ['pro', 'professional']:
            self.config['mode'] = 'professional'
            print("✅ Режим установлен: Профессионал")
            # В профессиональном режиме разблокируем все инструменты
            self.config['unlocked_tools'] = list(self.tools.keys())
        else:
            print("❌ Неверный режим. Используйте: beg или pro")
            return
        
        self.save_config()
    
    def show_learning(self):
        """Показывает обучающие материалы."""
        print("\n📚 ОБУЧЕНИЕ ПЕНТЕСТУ")
        print("="*50)
        print("\nУрок 1: Основы сетевого сканирования")
        print("  • Что такое IP адреса и порты")
        print("  • Использование инструмента network_info")
        print("  • Команда: hl scan 127.0.0.1")
        
        print("\nУрок 2: Веб-безопасность")
        print("  • Основы HTTP/HTTPS")
        print("  • Поиск уязвимостей с помощью web_scanner")
        print("  • Команда: hl scan example.com --tool web_scanner")
        
        print("\nУрок 3: Расширенные техники")
        print("  • SQL инъекции и XSS")
        print("  • Использование sql_tester и xss_scanner")
        print("  • Команда: hl scan target.com --tool sql_tester")
        
        print("\n🎯 Цель: Достичь 10 уровня для разблокировки всех инструментов")
    
    def show_premium_info(self):
        """Показывает информацию о Premium подписке."""
        print("\n💎 HACKLAB PREMIUM")
        print("="*50)
        print("\nБЕСПЛАТНАЯ ВЕРСИЯ включает:")
        print("  ✅ 10 инструментов с ограничениями")
        print("  ✅ Обучение с 10 уровнями")
        print("  ✅ Базовая система XP")
        print("  ✅ Сохранение результатов")
        
        print("\nPREMIUM ВЕРСИЯ ($15/месяц) добавляет:")
        print("  💎 Все 12+ инструментов без ограничений")
        print("  💎 Расширенные словари и payloads")
        print("  💎 Автоматические отчеты в PDF/HTML")
        print("  💎 Приоритетная поддержка")
        print("  💎 +25% XP за все действия")
        print("  💎 API доступ для автоматизации")
        
        print("\nTEAM ВЕРСИЯ ($49/месяц):")
        print("  👥 До 5 пользователей")
        print("  👥 Совместная работа над проектами")
        print("  👥 Централизованное управление")
        
        print("\nДля активации Premium посетите:")
        print("  https://hacklab-manager.com/premium")
        print("\nИли используйте промокод: TRYHACKLAB")

if __name__ == '__main__':
    manager = HackLabManager()
    manager.show_welcome()
