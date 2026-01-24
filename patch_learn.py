#!/usr/bin/env python3
import os

hl_file = "/usr/local/bin/hl"
base_dir = os.path.dirname(os.path.abspath(__file__))

with open(hl_file, 'r') as f:
    content = f.read()

# Находим место где добавить команду learn
if 'elif command == "premium":' in content:
    # Добавляем после premium
    new_content = content.replace(
        '    elif command == "premium":',
        '''    elif command == "premium":
        print("="*50)
        print("💰 HACKLAB MANAGER PREMIUM")
        print("="*50)
        print("Доступно за $15/месяц или $150/год")
        print()
        print("🔥 PREMIUM ФИЧИ:")
        print("  • HTB API интеграция")
        print("  • Shodan поиск")
        print("  • PDF отчеты")
        print("  • Автоматизация задач")
        print("  • Приоритетная поддержка")
        print()
        print("💡 Для покупки посетите:")
        print("   https://hacklab-manager.com/premium")
        print("="*50)
    
    elif command == "learn":
        import subprocess
        subprocess.run(["python3", os.path.join(base_dir, "learn.py")])'''
    )
    
    with open(hl_file, 'w') as f:
        f.write(new_content)
    print("✅ Команда 'learn' добавлена!")
else:
    print("❌ Не удалось найти место для вставки")
