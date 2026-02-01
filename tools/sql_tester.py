import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.action_logger import ActionLogger
    LOG_ENABLED = True
except ImportError:
    LOG_ENABLED = False

def test_sql_injection(url):
    if LOG_ENABLED:
        logger = ActionLogger()
        logger.log_action(1, "sql_test", "sql_tester", url)
    
    print(f"Тестирование SQL инъекций: {url}")
    
    # Демо тесты
    test_payloads = [
        "' OR '1'='1",
        "' UNION SELECT null,version() --",
        "' AND 1=1 --",
        "' AND 1=2 --"
    ]
    
    print("📊 Тестовые payloads:")
    for payload in test_payloads:
        print(f"  • {payload}")
    
    # Демо результат
    print("\n🔍 Результаты:")
    print("  ✅ Уязвимость обнаружена: SQL Injection")
    print("  📍 Параметр: id")
    print("  ⚠️  Тип: Error-based")
    
    return {
        "url": url,
        "vulnerable": True,
        "parameter": "id",
        "type": "error_based",
        "payloads": test_payloads
    }

if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "http://example.com/page?id=1"
    test_sql_injection(url)
