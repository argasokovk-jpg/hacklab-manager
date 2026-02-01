import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.action_logger import ActionLogger
    LOG_ENABLED = True
except ImportError:
    LOG_ENABLED = False

def find_subdomains(domain):
    if LOG_ENABLED:
        logger = ActionLogger()
        logger.log_action(1, "subdomain_scan", "subdomain_scanner", domain)
    
    print(f"Поиск субдоменов для: {domain}")
    
    # Демо список субдоменов
    subdomains = [
        f"www.{domain}",
        f"mail.{domain}",
        f"blog.{domain}",
        f"dev.{domain}",
        f"test.{domain}",
        f"admin.{domain}",
        f"api.{domain}",
        f"cdn.{domain}"
    ]
    
    found = []
    for sub in subdomains:
        # В реальности здесь был бы DNS запрос
        if "test" not in sub:  # Демо логика
            print(f"✅ Найден: {sub}")
            found.append(sub)
    
    print(f"\nНайдено субдоменов: {len(found)}")
    return found

if __name__ == "__main__":
    import sys
    domain = sys.argv[1] if len(sys.argv) > 1 else "example.com"
    find_subdomains(domain)
