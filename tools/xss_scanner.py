#!/usr/bin/env python3
import requests
from tool_base import ToolBase

class XSSScanner(ToolBase):
    def run(self, target):
        results = {
            'target': target,
            'vulnerable': False,
            'payloads_tested': 0,
            'reflected_xss': [],
            'stored_xss': [],
            'recommendations': []
        }
        
        print(f"🔍 Поиск XSS уязвимостей для: {target}")
        print("=" * 40)
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "\"><script>alert('XSS')</script>",
            "'><script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "\" onmouseover=\"alert('XSS')\"",
            "<body onload=alert('XSS')>",
            "<iframe src=\"javascript:alert('XSS')\">"
        ]
        
        try:
            if '?' in target:
                base_url, query = target.split('?', 1)
                params = query.split('&')
                
                for payload in xss_payloads:
                    results['payloads_tested'] += 1
                    
                    test_params = []
                    for param in params:
                        if '=' in param:
                            key, value = param.split('=', 1)
                            test_params.append(f"{key}={payload}")
                        else:
                            test_params.append(param)
                    
                    test_url = f"{base_url}?{'&'.join(test_params)}"
                    
                    try:
                        response = requests.get(test_url, timeout=10, verify=False)
                        
                        if payload in response.text:
                            print(f"🚨 ОТРАЖЕННАЯ XSS: {payload[:30]}...")
                            results['reflected_xss'].append(payload)
                            results['vulnerable'] = True
                        
                    except requests.exceptions.RequestException:
                        continue
                    
                if results['vulnerable']:
                    print(f"\n❌ ОБНАРУЖЕНА XSS УЯЗВИМОСТЬ!")
                    print(f"💡 Найдено payloads: {len(results['reflected_xss'])}")
                    results['recommendations'].append("СРОЧНО исправить уязвимость")
                    results['recommendations'].append("Использовать HTML escaping")
                    results['recommendations'].append("Реализовать CSP (Content Security Policy)")
                else:
                    print(f"\n✅ XSS уязвимости не обнаружены")
                    print(f"📊 Проверено payloads: {results['payloads_tested']}")
                    results['recommendations'].append("Продолжайте регулярное тестирование")
                    results['recommendations'].append("Используйте security headers")
            
            else:
                print(f"⚠️  URL не содержит параметров для тестирования")
                print(f"💡 Добавьте параметры, например: ?search=test")
                results['recommendations'].append("Протестируйте формы ввода")
        
        except Exception as e:
            print(f"❌ Ошибка тестирования: {e}")
            results['error'] = str(e)
        
        print(f"\n🔧 РЕКОМЕНДАЦИИ:")
        for rec in results['recommendations']:
            print(f"  • {rec}")
        
        return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Использование: python xss_scanner.py <url>")
        sys.exit(1)
    
    scanner = XSSScanner()
    scanner.run(sys.argv[1])
