#!/usr/bin/env python3
import sys
import os

def show_tutorials():
    print("="*50)
    print("📚 ОБУЧЕНИЕ HACKLAB MANAGER")
    print("="*50)
    
    tutorials = {
        "1": {
            "title": "🎯 Основы пентеста",
            "content": """
1. Что такое пентест?
   • Тестирование на проникновение
   • Поиск уязвимостей с разрешения владельца
   
2. Этапы пентеста:
   • Разведка (Reconnaissance)
   • Сканирование (Scanning)
   • Получение доступа (Gaining Access)
   • Пост-эксплуатация (Post-Exploitation)
   • Отчетность (Reporting)
   
3. Ваша первая команда:
   hl scan scanme.nmap.org
            """
        },
        "2": {
            "title": "🔍 Сканирование сетей",
            "content": """
1. Что делает команда 'hl scan':
   • Проверяет доступность цели
   • Сканирует основные порты (80, 443, 22)
   • Сохраняет результаты
   
2. Безопасные цели для обучения:
   • scanme.nmap.org
   • example.com
   • 8.8.8.8 (Google DNS)
   
3. Как читать результаты сканирования:
   • PORT    STATE SERVICE
   • 80/tcp  open  http
   • 443/tcp open  https
            """
        }
    }
    
    print("Выберите урок:")
    for key, tutorial in tutorials.items():
        print(f"[{key}] {tutorial['title']}")
    
    print("\n[0] Выход")
    print("="*50)
    
    choice = input("Ваш выбор: ").strip()
    
    if choice in tutorials:
        print("\n" + "="*50)
        print(tutorials[choice]['title'])
        print("="*50)
        print(tutorials[choice]['content'])
        print("="*50)
        
        # Добавляем XP за обучение
        config_file = os.path.expanduser("~/.hacklab/config.json")
        if os.path.exists(config_file):
            import json
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            if config.get("mode") == "beginner":
                config["xp"] = config.get("xp", 0) + 10
                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=2)
                print("\n🎉 +10 XP за обучение!")
    elif choice == "0":
        return
    else:
        print("❌ Неверный выбор")

if __name__ == "__main__":
    show_tutorials()
