import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.action_logger import ActionLogger
    LOG_ENABLED = True
except ImportError:
    LOG_ENABLED = False

def scan_directories(url, wordlist=None):
    if LOG_ENABLED:
        logger = ActionLogger()
        logger.log_action(1, "dir_scan", "dir_buster", url)
    
    print(f"Поиск директорий: {url}")
    
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    # Простой список директорий для теста
    directories = [
        "admin", "login", "wp-admin", "administrator",
        "test", "backup", "config", "data", "uploads"
    ]
    
    found = []
    
    for directory in directories:
        test_url = f"{url.rstrip('/')}/{directory}"
        try:
            response = requests.get(test_url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Найдена: {test_url}")
                found.append(test_url)
            elif response.status_code == 403:
                print(f"🔒 Доступ запрещен: {test_url}")
            elif response.status_code == 404:
                pass  # Не показываем ненайденные
            else:
                print(f"⚠️  {test_url} -> {response.status_code}")
        except:
            pass
    
    print(f"\nНайдено директорий: {len(found)}")
    return found

if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "http://example.com"
    scan_directories(url)
