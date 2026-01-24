import requests
import ssl
from tool_base import ToolBase

class WebScanner(ToolBase):
    def run(self, target):
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
            
        results = {
            'target': target,
            'status': 'failed',
            'status_code': None,
            'headers': {},
            'security_score': 0,
            'warnings': []
        }
        
        try:
            response = requests.get(target, timeout=10, verify=False, allow_redirects=True)
            
            results['status'] = 'success'
            results['status_code'] = response.status_code
            results['headers'] = dict(response.headers)
            results['content_length'] = len(response.content)
            results['final_url'] = response.url
            
            security_headers = [
                'X-Frame-Options',
                'X-Content-Type-Options', 
                'X-XSS-Protection',
                'Content-Security-Policy',
                'Strict-Transport-Security'
            ]
            
            security_score = 0
            for header in security_headers:
                if header in response.headers:
                    security_score += 1
                else:
                    results['warnings'].append(f"Отсутствует заголовок безопасности: {header}")
            
            results['security_score'] = security_score
            
            self.display_results(target, response, security_score)
            
        except requests.exceptions.RequestException as e:
            results['error'] = str(e)
            results['warnings'].append(f"Ошибка соединения: {e}")
            self.log_error(f"Ошибка сканирования {target}: {e}")
        
        return results
    
    def display_results(self, target, response, security_score):
        print(f"🔍 Сканирование сайта: {target}")
        print("=" * 40)
        print(f"✅ Сайт доступен")
        print(f"📊 Код ответа: {response.status_code}")
        print(f"📦 Размер ответа: {len(response.content)} байт")
        print(f"📍 Конечный URL: {response.url}")
        
        print(f"\n📋 ЗАГОЛОВКИ БЕЗОПАСНОСТИ:")
        
        security_headers = ['X-Frame-Options', 'X-Content-Type-Options', 
                          'X-XSS-Protection', 'Content-Security-Policy',
                          'Strict-Transport-Security']
        
        for header in security_headers:
            if header in response.headers:
                print(f"  ✅ {header}: {response.headers[header]}")
            else:
                print(f"  ❌ {header}: Отсутствует")
        
        print(f"\n📈 ОЦЕНКА БЕЗОПАСНОСТИ: {security_score}/5")
        
        if security_score < 3:
            print("⚠️  ВНИМАНИЕ: Низкий уровень безопасности!")
        else:
            print("✅ Хороший уровень безопасности")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Использование: python web_scanner.py <url>")
        sys.exit(1)
    
    scanner = WebScanner()
    scanner.run(sys.argv[1])
