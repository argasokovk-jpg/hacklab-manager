#!/usr/bin/env python3
import requests
import json
from tool_base import ToolBase

class APIFuzzer(ToolBase):
    def run(self, target):
        results = {
            'target': target,
            'endpoints_tested': 0,
            'vulnerabilities': [],
            'errors': [],
            'recommendations': []
        }
        
        print(f"🔍 Фаззинг API для: {target}")
        print("=" * 40)
        
        http_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
        test_payloads = [
            {"test": "payload"},
            {"username": "admin", "password": "' OR '1'='1"},
            {"id": 1},
            {"id": 0},
            {"id": -1},
            {"id": 999999},
            {"id": "1' OR '1'='1"},
            {"search": "<script>alert('XSS')</script>"},
            {"file": "../../../etc/passwd"},
            {"cmd": "whoami"}
        ]
        
        try:
            print(f"📊 Тестирование методов HTTP:")
            
            for method in http_methods:
                try:
                    if method == 'GET':
                        response = requests.get(target, timeout=5, verify=False)
                    elif method == 'POST':
                        response = requests.post(target, json={"test": "data"}, timeout=5, verify=False)
                    elif method == 'PUT':
                        response = requests.put(target, json={"test": "data"}, timeout=5, verify=False)
                    elif method == 'DELETE':
                        response = requests.delete(target, timeout=5, verify=False)
                    elif method == 'PATCH':
                        response = requests.patch(target, json={"test": "data"}, timeout=5, verify=False)
                    
                    results['endpoints_tested'] += 1
                    
                    status = response.status_code
                    
                    if status == 200:
                        print(f"  ✅ {method}: {status} OK")
                    elif status == 201:
                        print(f"  ✅ {method}: {status} Created")
                    elif status == 204:
                        print(f"  ✅ {method}: {status} No Content")
                    elif status in [400, 401, 403, 404]:
                        print(f"  ⚠️  {method}: {status} (Ожидаемо)")
                    elif status >= 500:
                        print(f"  🚨 {method}: {status} Server Error (ВОЗМОЖНА УЯЗВИМОСТЬ)")
                        results['vulnerabilities'].append(f"{method}: Server Error {status}")
                    else:
                        print(f"  ℹ️  {method}: {status}")
                
                except requests.exceptions.RequestException as e:
                    print(f"  ❌ {method}: Ошибка - {e}")
                    results['errors'].append(f"{method}: {e}")
            
            print(f"\n📊 Тестирование некорректных данных:")
            
            for i, payload in enumerate(test_payloads[:3]):
                try:
                    response = requests.post(target, json=payload, timeout=5, verify=False)
                    
                    if response.status_code >= 500:
                        print(f"  🚨 Payload {i+1}: Server Error {response.status_code}")
                        results['vulnerabilities'].append(f"Invalid payload {i+1} caused server error")
                    elif response.status_code == 400:
                        print(f"  ✅ Payload {i+1}: 400 Bad Request (Ожидаемо)")
                    else:
                        print(f"  ℹ️  Payload {i+1}: {response.status_code}")
                
                except requests.exceptions.RequestException:
                    continue
            
            if results['vulnerabilities']:
                print(f"\n❌ ОБНАРУЖЕНЫ ВОЗМОЖНЫЕ УЯЗВИМОСТИ!")
                print(f"💡 Проблемы: {len(results['vulnerabilities'])}")
                results['recommendations'].append("Устранить server errors")
                results['recommendations'].append("Добавить input validation")
                results['recommendations'].append("Использовать rate limiting")
            else:
                print(f"\n✅ Серьезных уязвимостей не обнаружено")
                results['recommendations'].append("Продолжайте регулярное тестирование")
                results['recommendations'].append("Используйте API security testing tools")
        
        except Exception as e:
            print(f"❌ Ошибка фаззинга: {e}")
            results['error'] = str(e)
        
        print(f"\n🔧 РЕКОМЕНДАЦИИ:")
        for rec in results['recommendations']:
            print(f"  • {rec}")
        
        return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Использование: python api_fuzzer.py <api_url>")
        sys.exit(1)
    
    fuzzer = APIFuzzer()
    fuzzer.run(sys.argv[1])
