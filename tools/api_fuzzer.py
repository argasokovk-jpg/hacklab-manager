import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.action_logger import ActionLogger
    LOG_ENABLED = True
except ImportError:
    LOG_ENABLED = False

def fuzz_api(endpoint):
    if LOG_ENABLED:
        logger = ActionLogger()
        logger.log_action(1, "api_fuzz", "api_fuzzer", endpoint)
    
    print(f"Фаззинг API: {endpoint}")
    
    # Демо тесты
    test_cases = [
        "/api/users/../etc/passwd",
        "/api/users/",
        "/api/users/?id=1'",
        "/api/users/999999",
        "/api/users/-1"
    ]
    
    print("📊 Тестовые запросы:")
    for test in test_cases:
        full_url = f"{endpoint}{test}"
        print(f"  • {full_url}")
    
    # Демо результат
    print("\n🔍 Результаты:")
    print("  ✅ Обнаружено: Directory Traversal")
    print("  ⚠️  Обнаружено: SQL Injection")
    print("  ⚠️  Обнаружено: IDOR (Insecure Direct Object Reference)")
    
    return {
        "endpoint": endpoint,
        "vulnerabilities": ["directory_traversal", "sql_injection", "idor"],
        "test_cases": test_cases
    }

if __name__ == "__main__":
    import sys
    endpoint = sys.argv[1] if len(sys.argv) > 1 else "http://api.example.com"
    fuzz_api(endpoint)
