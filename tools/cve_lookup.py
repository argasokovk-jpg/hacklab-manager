import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.action_logger import ActionLogger
    LOG_ENABLED = True
except ImportError:
    LOG_ENABLED = False

def search_cve(query):
    if LOG_ENABLED:
        logger = ActionLogger()
        logger.log_action(1, "cve_search", "cve_lookup", query)
    
    print(f"Поиск уязвимостей CVE для: {query}")
    
    # Демо данные
    cve_list = [
        {"id": "CVE-2023-12345", "description": "SQL Injection в системе управления", "score": 7.5},
        {"id": "CVE-2023-12346", "description": "XSS в веб-интерфейсе", "score": 6.8},
        {"id": "CVE-2023-12347", "description": "Buffer Overflow в сервисе", "score": 8.2},
    ]
    
    for cve in cve_list:
        print(f"\n🔴 {cve['id']}")
        print(f"   Описание: {cve['description']}")
        print(f"   CVSS Score: {cve['score']}")
    
    print(f"\nНайдено уязвимостей: {len(cve_list)}")
    return cve_list

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "web server"
    search_cve(query)
