#!/usr/bin/env python3
"""
Базовый класс для всех инструментов HackLab Manager
"""

import os
import json
import time
from datetime import datetime

class ToolBase:
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.hacklab")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.results_dir = os.path.join(self.config_dir, "scans")
        
        # Создаем директории
        os.makedirs(self.results_dir, exist_ok=True)
        
    def load_config(self):
        """Загружает конфигурацию пользователя."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def is_premium(self):
        """Проверяет Premium статус."""
        config = self.load_config()
        return config.get('is_premium', False)
    
    def get_user_level(self):
        """Получает уровень пользователя."""
        config = self.load_config()
        return config.get('level', 1)
    
    def save_result(self, target, result):
        """Сохраняет результат сканирования."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_target = target.replace('/', '_').replace(':', '_')
        filename = f"{safe_target}_{timestamp}.txt"
        filepath = os.path.join(self.results_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Сканирование: {target}\n")
            f.write(f"Дата: {datetime.now()}\n")
            f.write(f"Инструмент: {self.__class__.__name__}\n")
            f.write("=" * 50 + "\n")
            
            if isinstance(result, str):
                f.write(result)
            elif isinstance(result, list):
                for item in result:
                    f.write(f"{item}\n")
            elif isinstance(result, dict):
                for key, value in result.items():
                    f.write(f"{key}: {value}\n")
            else:
                f.write(str(result))
        
        return filepath
    
    def print_banner(self):
        """Печатает баннер инструмента."""
        print("\n" + "="*50)
        print(f"🛠️  {self.__class__.__name__.replace('_', ' ').title()}")
        print("="*50)
    
    def log_info(self, msg):
        print(f"[INFO] {msg}")
    
    def log_success(self, msg):
        print(f"[SUCCESS] {msg}")
    
    def log_warning(self, msg):
        print(f"[WARNING] {msg}")
    
    def log_error(self, msg):
        print(f"[ERROR] {msg}")
    
    def run(self, target):
        """Основной метод, который должен быть переопределен."""
        self.print_banner()
        self.log_info(f"Сканирование: {target}")
        return f"Результат сканирования {target}"
