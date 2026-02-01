import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.action_logger import ActionLogger
    LOG_ENABLED = True
except ImportError:
    LOG_ENABLED = False

def whois_lookup(domain):
    if LOG_ENABLED:
        logger = ActionLogger()
        logger.log_action(1, "whois_check", "whois_checker", domain)
    
    print(f"WHOIS информация для: {domain}")
    print("(В реальной версии здесь был бы запрос к WHOIS серверу)")
    
    # Демо информация
    info = {
        "domain": domain,
        "status": "registered",
        "created": "2023-01-15",
        "expires": "2025-01-15",
        "registrar": "Example Registrar Inc.",
        "nameservers": ["ns1.example.com", "ns2.example.com"]
    }
    
    print(f"Домен: {info['domain']}")
    print(f"Статус: {info['status']}")
    print(f"Создан: {info['created']}")
    print(f"Истекает: {info['expires']}")
    print(f"Регистратор: {info['registrar']}")
    print(f"NS серверы: {', '.join(info['nameservers'])}")
    
    return info

if __name__ == "__main__":
    import sys
    domain = sys.argv[1] if len(sys.argv) > 1 else "example.com"
    whois_lookup(domain)
