import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.action_logger import ActionLogger
    LOG_ENABLED = True
except ImportError:
    LOG_ENABLED = False

def scan_website(url):
    if LOG_ENABLED:
        logger = ActionLogger()
        logger.log_action(1, "web_scan", "web_scanner", url)
    
    print(f"Сканирую веб-сайт: {url}")
    
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        response = requests.get(url, timeout=10)
        print(f"Статус: {response.status_code}")
        print(f"Заголовки: {len(response.headers)}")
        
        # Проверяем базовые вещи
        if 'X-Frame-Options' not in response.headers:
            print("⚠️  Отсутствует X-Frame-Options")
        
        if 'Content-Security-Policy' not in response.headers:
            print("⚠️  Отсутствует Content-Security-Policy")
        
        return {
            "url": url,
            "status": response.status_code,
            "headers": dict(response.headers)
        }
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "http://example.com"
    scan_website(url)
