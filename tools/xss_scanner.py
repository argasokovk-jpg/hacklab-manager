import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.action_logger import ActionLogger
    LOG_ENABLED = True
except ImportError:
    LOG_ENABLED = False

def scan_xss(url):
    if LOG_ENABLED:
        logger = ActionLogger()
        logger.log_action(1, "xss_scan", "xss_scanner", url)
    
    print(f"Сканирование XSS: {url}")
    
    # Демо тесты
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "\"><script>alert(1)</script>",
        "javascript:alert('XSS')",
        "<img src=x onerror=alert(1)>"
    ]
    
    print("📊 XSS payloads:")
    for payload in xss_payloads:
        print(f"  • {payload}")
    
    # Демо результат
    print("\n🔍 Результаты:")
    print("  ⚠️  Возможная уязвимость: Reflected XSS")
    print("  📍 Параметр: search")
    print("  🔒 Рекомендация: Фильтровать HTML теги")
    
    return {
        "url": url,
        "vulnerable": True,
        "parameter": "search",
        "type": "reflected",
        "payloads": xss_payloads
    }

if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "http://example.com/search?q="
    scan_xss(url)
