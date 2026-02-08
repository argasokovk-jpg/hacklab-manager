#!/usr/bin/env python3
import sys
import time
import os
import json

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("=" * 60)
    print("HACKLAB MANAGER v2.3 - СИСТЕМА ОБУЧЕНИЯ МЫШЛЕНИЮ".center(60))
    print("=" * 60)
    print()

def print_step(text):
    print(f"[+] {text}")
    time.sleep(0.3)

def print_error(text):
    print(f"[!] {text}")
    time.sleep(0.5)

def print_success(text):
    print(f"[✓] {text}")
    time.sleep(0.5)

def print_info(text):
    print(f"[i] {text}")
    time.sleep(0.2)

def wait_enter():
    input("\n[Нажмите Enter чтобы продолжить...]")

def section_title(title):
    print("\n" + "=" * 50)
    print(f" {title}")
    print("=" * 50)

def add_xp(amount):
    config_path = os.path.expanduser("~/.hacklab/config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            current_xp = config.get("xp", 0)
            config["xp"] = current_xp + amount
            
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            print_success(f"+{amount} XP за обучение!")
            print_info(f"Всего XP: {config['xp']}")
            return True
        except:
            return False
    return False

def show_methodology():
    print_header()
    section_title("ОСНОВЫ МЕТОДОЛОГИИ ПЕНТЕСТА")
    
    print_info("Правильная последовательность — ключ к успеху")
    print()
    
    print("🎯 ЭТАП 1: РАЗВЕДКА (Reconnaissance)")
    print("  whois_checker    → Кто владелец домена?")
    print("  network_info     → Где размещена цель?")
    print("  dns_enum         → Какие поддомены существуют?")
    print()
    
    print("🎯 ЭТАП 2: СКАНИРОВАНИЕ (Scanning)")
    print("  port_check       → Какие порты открыты?")
    print("  ssl_checker      → Как настроена защита?")
    print("  web_scanner      → Какие технологии используются?")
    print()
    
    print("🎯 ЭТАП 3: ТЕСТИРОВАНИЕ (Exploitation)")
    print("  dir_buster       → Есть скрытые директории?")
    print("  sql_scanner      → Уязвимы ли формы к SQL?")
    print("  xss_scanner      → Есть XSS уязвимости?")
    print("  cve_lookup       → Известные уязвимости сервисов?")
    print()
    
    print("🎯 ЭТАП 4: ОТЧЕТ (Reporting)")
    print("  Анализ результатов")
    print("  Генерация PDF-отчета")
    print("  Рекомендации по исправлению")
    
    print("\n🔥 ГЛАВНОЕ ПРАВИЛО:")
    print("Каждый следующий шаг ДОЛЖЕН использовать данные предыдущего.")
    print("Нет информации о портах → нет смысла в dir_buster.")
    print("Нет данных о домене → нет контекста для атаки.")
    
    if add_xp(5):
        print("\n" + "="*50)
    
    wait_enter()

def show_bad_example():
    print_header()
    section_title("КАК ДЕЛАЮТ НОВИЧКИ: ТИПИЧНЫЕ ОШИБКИ")
    
    print_error("Пример неправильного подхода:")
    print("\nЦель: testfire.net")
    print("Действия новичка:")
    print("  1. dir_buster          ← Слепая атака без разведки")
    print("  2. sql_scanner         ← Нет целей для сканирования")
    print("  3. port_check          ← Поздно! Надо было первым делом")
    print("  4. whois_checker       ← В конце, когда уже всё сделано")
    
    print("\n❌ ПРОБЛЕМЫ:")
    print("• 95% запросов dir_buster — впустую")
    print("• sql_scanner не знает, какие формы тестировать")
    print("• Нет системного понимания цели")
    print("• Пустая трата времени и ресурсов")
    
    print("\n💔 РЕЗУЛЬТАТ: 0 уязвимостей, 100% разочарование")
    
    if add_xp(3):
        print("\n" + "="*50)
        print_info("XP за изучение ошибок других!")
    
    wait_enter()

def show_good_example():
    print_header()
    section_title("КАК ДЕЛАЮТ ПРОФЕССИОНАЛЫ")
    
    print_success("Пример правильного подхода:")
    print("\nЦель: testfire.net")
    print("Действия профессионала:")
    print("  1. whois_checker    → BankDemoApp, тестовый сайт")
    print("  2. network_info     → 65.61.137.117, размещен в США")
    print("  3. port_check       → 80 (HTTP), 443 (HTTPS) открыты")
    print("  4. web_scanner      → Apache Tomcat, ASP.NET")
    print("  5. ssl_checker      → SSL настроен, проверка сертификата")
    print("  6. dir_buster       → Целевой поиск по известным путям Tomcat")
    print("  7. sql_scanner      → Целевое тестирование форм входа")
    print("  8. xss_scanner      → Проверка параметров URL")
    
    print("\n✅ ПРЕИМУЩЕСТВА:")
    print("• Каждое действие основано на предыдущем")
    print("• Минимум запросов — максимум информации")
    print("• Четкое понимание архитектуры цели")
    print("• Высокая вероятность найти уязвимости")
    
    print("\n🏆 РЕЗУЛЬТАТ: Конкретные находки, ясный отчет, довольный клиент")
    
    if add_xp(10):
        print("\n" + "="*50)
        print_success("Максимальный XP за изучение правильного подхода!")
    
    wait_enter()

def show_analyzer_logic():
    print_header()
    section_title("КАК АНАЛИЗАТОР ОЦЕНИВАЕТ ВАШИ ДЕЙСТВИЯ")
    
    print_info("Анализатор смотрит не на результат, а на ПРОЦЕСС")
    print("Он оценивает КАК вы думаете, а не ЧТО вы нашли")
    print()
    
    print("📊 СИСТЕМА БАЛЛОВ:")
    print("  +10  За правильный порядок этапов (Recon → Scan → Exploit)")
    print("  -5   За пропуск обязательного шага (whois перед атакой)")
    print("  -3   За повторный запуск того же инструмента без причины")
    print("  -2   За действие без логической связи с предыдущим")
    print("  +15  За оптимальный путь (минимум инструментов, максимум инфо)")
    print("  +5   За паузу между этапами (обдумывание следующего шага)")
    print("  -10  За 'шум' (более 3 лишних действий)")
    
    print("\n📈 МЕТРИКИ ОЦЕНКИ:")
    print("  1. Логическая связь: Каждое действие вытекает из предыдущего")
    print("  2. Эффективность: Отношение полезной информации к количеству действий")
    print("  3. Полнота: Все ли необходимые этапы выполнены?")
    print("  4. Скорость: Не слишком ли быстро? (паузы важны!)")
    
    print("\n🎓 УРОВНИ КВАЛИФИКАЦИИ:")
    print("  Junior    (0-50 баллов)   → Действует наугад, нет системы")
    print("  Middle    (51-80 баллов)  → Понимает методологию, есть ошибки")
    print("  Senior    (81-100 баллов) → Стратегическое мышление, оптимальный путь")
    
    print("\n📝 Пример анализа последовательности:")
    print("  whois → network_info → port_check → web_scanner → dir_buster")
    print("  Оценка: +10 (порядок) +15 (оптимально) +5 (логика) = 30/30 на этапе")
    
    if add_xp(8):
        print("\n" + "="*50)
    
    wait_enter()

def show_tips():
    print_header()
    section_title("ПРАКТИЧЕСКИЕ СОВЕТЫ ДЛЯ НЕМЕДЛЕННОГО ПРИМЕНЕНИЯ")
    
    tips = [
        "1. ВСЕГДА начинай с whois_checker. Без понимания цели — нет пентеста.",
        "2. Порты 80/443? Сначала узнай что за сервер (web_scanner), потом dir_buster.",
        "3. Нашел нестандартный порт? Проверь cve_lookup перед атакой.",
        "4. Делай паузы 30-60 сек между этапами. Обдумай следующий шаг.",
        "5. Цель — не 'запустить все инструменты', а 'получить ключевую инфо'.",
        "6. Если tool не дал результатов, не запускай его снова — иди дальше.",
        "7. Документируй находки сразу. Память — ненадежный инструмент.",
        "8. Сначала широкий обзор (разведка), потом точечная атака (эксплуатация).",
        "9. Не стесняйся возвращаться на предыдущий этап при новых данных.",
        "10. Анализируй свои ошибки через hl analyze — это главный инструмент роста."
    ]
    
    for i, tip in enumerate(tips, 1):
        print(f"[{i}] {tip}")
        time.sleep(0.4)
    
    print("\n🎯 САМАЯ ЧАСТАЯ ОШИБКА:")
    print("  Новички думают: 'Надо больше инструментов'")
    print("  Профессионалы знают: 'Надо больше думать'")
    
    if add_xp(7):
        print("\n" + "="*50)
    
    wait_enter()

def interactive_test():
    print_header()
    section_title("ПРОВЕРЬ СВОИ ЗНАНИЯ")
    
    print_info("Ситуация: Новый домен securebank.com")
    print("Твоя задача: Выбрать правильную последовательность действий")
    print()
    
    options = [
        "1. dir_buster → sql_scanner → port_check → whois_checker",
        "2. whois_checker → network_info → port_check → ssl_checker → web_scanner",
        "3. port_check → web_scanner → dir_buster → sql_scanner",
        "4. sql_scanner → xss_scanner → cve_lookup → dir_buster"
    ]
    
    for option in options:
        print(option)
        time.sleep(0.3)
    
    print()
    
    while True:
        try:
            choice = int(input("Выбери правильный вариант (1-4): "))
            if 1 <= choice <= 4:
                break
            else:
                print_error("Выбери число от 1 до 4")
        except ValueError:
            print_error("Введи число")
    
    print()
    
    if choice == 2:
        print_success("ВЕРНО! Это идеальная последовательность:")
        print("  - whois_checker: Кто владелец банка?")
        print("  - network_info: Где размещен?")
        print("  - port_check: Какие сервисы доступны?")
        print("  - ssl_checker: Проверка защиты соединения")
        print("  - web_scanner: Что за веб-технологии?")
        print("\n✅ После этого можно принимать решение о dir_buster или sql_scanner")
        
        if add_xp(15):
            print("\n" + "="*50)
            print_success("Максимальный XP за правильный ответ!")
    else:
        print_error("НЕПРАВИЛЬНО. Проблемы выбранного варианта:")
        
        if choice == 1:
            print("  • dir_buster БЕЗ данных о портах — 95% пустых запросов")
            print("  • sql_scanner БЕЗ знания форм на сайте — слепое сканирование")
            print("  • Ключевая разведка (whois) в конце — нет контекста для атак")
        elif choice == 3:
            print("  • Пропущена ключевая разведка (whois, network_info)")
            print("  • Нет понимания кто клиент, какая инфраструктура")
            print("  • Может оказаться тестовым полигоном или ловушкой")
        elif choice == 4:
            print("  • Полное игнорирование разведки и сканирования")
            print("  • Попытка эксплуатации БЕЗ понимания цели")
            print("  • Максимальный 'шум' при минимальной эффективности")
        
        print("\n💡 ПРАВИЛЬНЫЙ ПУТЬ: Разведка → Сканирование → Тестирование")
        
        if add_xp(5):
            print("\n" + "="*50)
            print_info("XP за участие в тесте!")
    
    print("\n" + "=" * 50)
    print("💎 ЗАПОМНИ: Правильный порядок экономит часы работы")
    print("и повышает шансы на успех в 10 раз")
    
    wait_enter()

def show_next_steps():
    print_header()
    section_title("ЧТО ДЕЛАТЬ ДАЛЬШЕ?")
    
    print_step("1. Практика на Lab 1 (веб-приложение):")
    print("   hl lab start 1")
    print("   Цель: testfire.net")
    print("   Фокус: Применить методологию из этого урока")
    
    print("\n" + "=" * 40)
    
    print_step("2. Анализ своих действий:")
    print("   После выполнения lab1:")
    print("   hl analyze")
    print("   Получи оценку и рекомендации")
    
    print("\n" + "=" * 40)
    
    print_step("3. Работа над ошибками:")
    print("   Читай PDF-отчет внимательно")
    print("   Устраняй слабые места в подходе")
    print("   Повторяй lab1 до уровня Senior (85+ баллов)")
    
    print("\n" + "=" * 40)
    
    print_step("4. Переход к Lab 2 (сетевая разведка):")
    print("   hl lab start 2 (скоро будет доступно)")
    print("   Цель: scanme.nmap.org")
    print("   Фокус: Сетевая методология")
    
    print("\n" + "=" * 40)
    
    print_step("5. Постоянное развитие:")
    print("   hl learn — повторить урок при необходимости")
    print("   hl analyze — после каждой лаборатории")
    print("   hl report — просмотр всех своих отчетов")
    
    print("\n🎯 КЛЮЧЕВАЯ ИДЕЯ:")
    print("Не пытайся запомнить инструменты. Развивай мышление.")
    print("Инструменты меняются каждый год. Мышление остается.")
    
    if add_xp(5):
        print("\n" + "="*50)
    
    wait_enter()

def main_menu():
    while True:
        print_header()
        print("🏆 ГЛАВНОЕ МЕНЮ ОБУЧЕНИЯ 🏆".center(60))
        print()
        
        menu_items = [
            "1. 🎯 Основы методологии пентеста",
            "2. ❌ Пример ошибок новичка", 
            "3. ✅ Пример правильного подхода",
            "4. 🧠 Как работает анализатор",
            "5. 💡 Практические советы",
            "6. 📝 Интерактивный тест",
            "7. 🚀 Что делать дальше?",
            "0. 🚪 Выход"
        ]
        
        for item in menu_items:
            print(item)
            time.sleep(0.1)
        
        print()
        print("=" * 60)
        
        try:
            choice = input("Выбери раздел (0-7): ").strip()
            
            if choice == "0":
                print_header()
                print("\n[✓] Обучение завершено")
                print("[i] Запусти 'hl lab start 1' для практики")
                print("[i] Помни: Мышление важнее инструментов\n")
                
                config_path = os.path.expanduser("~/.hacklab/config.json")
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                    xp = config.get("xp", 0)
                    print(f"[⭐] Твой текущий уровень XP: {xp}")
                
                sys.exit(0)
            
            choices = {
                "1": show_methodology,
                "2": show_bad_example,
                "3": show_good_example,
                "4": show_analyzer_logic,
                "5": show_tips,
                "6": interactive_test,
                "7": show_next_steps
            }
            
            if choice in choices:
                choices[choice]()
            else:
                print_error("Неверный выбор. Попробуй снова.")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n[i] Обучение прервано. Возвращайся позже!")
            time.sleep(1)
            continue
        except Exception as e:
            print_error(f"Ошибка: {e}")
            time.sleep(2)
            continue

def main():
    try:
        print_header()
        print_info("Загрузка системы обучения...")
        time.sleep(1)
        main_menu()
    except KeyboardInterrupt:
        print("\n\n[i] Программа завершена.")
        sys.exit(0)

if __name__ == "__main__":
    main()
