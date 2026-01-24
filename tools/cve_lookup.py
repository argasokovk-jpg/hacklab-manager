#!/usr/bin/env python3
import requests
import json
from tool_base import ToolBase

class CVELookup(ToolBase):
    def run(self, search_term):
        results = {
            'search_term': search_term,
            'cves': [],
            'error': None
        }
        
        print(f"🔍 Поиск CVE уязвимостей для: {search_term}")
        print("=" * 40)
        
        try:
            if search_term.upper().startswith('CVE-'):
                cve_id = search_term.upper()
                url = f"https://cve.circl.lu/api/cve/{cve_id}"
                
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    print(f"✅ Найдена уязвимость: {cve_id}")
                    print(f"📝 Описание: {data.get('summary', 'Нет описания')}")
                    
                    cvss = data.get('cvss', None)
                    if cvss:
                        print(f"📊 CVSS Score: {cvss}")
                        if float(cvss) >= 7.0:
                            print(f"⚠️  ВЫСОКИЙ РИСК: {cvss}")
                        elif float(cvss) >= 4.0:
                            print(f"⚠️  СРЕДНИЙ РИСК: {cvss}")
                        else:
                            print(f"✅ НИЗКИЙ РИСК: {cvss}")
                    
                    results['cves'].append(data)
                    
                else:
                    print(f"❌ CVE {cve_id} не найдена")
                    results['error'] = f"CVE {cve_id} not found"
            else:
                url = f"https://cve.circl.lu/api/search/{search_term}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data:
                        print(f"✅ Найдено уязвимостей: {len(data)}")
                        
                        for cve in data[:5]:
                            cve_id = cve.get('id', 'Unknown')
                            summary = cve.get('summary', 'Нет описания')
                            cvss = cve.get('cvss', 'N/A')
                            
                            print(f"\n📌 {cve_id}")
                            print(f"   Описание: {summary[:100]}...")
                            print(f"   CVSS: {cvss}")
                        
                        if len(data) > 5:
                            print(f"\n💡 Показано 5 из {len(data)} уязвимостей")
                        
                        results['cves'] = data
                    else:
                        print(f"❌ Уязвимости для '{search_term}' не найдены")
                        results['error'] = "No vulnerabilities found"
                else:
                    print(f"❌ Ошибка API: {response.status_code}")
                    results['error'] = f"API error: {response.status_code}"
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Ошибка сети: {e}")
            results['error'] = str(e)
        except json.JSONDecodeError as e:
            print(f"❌ Ошибка данных: {e}")
            results['error'] = str(e)
        
        print(f"\n💡 РЕКОМЕНДАЦИИ:")
        print(f"  • Регулярно обновляйте ПО")
        print(f"  • Мониторьте security advisories")
        print(f"  • Используйте vulnerability scanners")
        
        return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Использование: python cve_lookup.py <search_term>")
        sys.exit(1)
    
    lookup = CVELookup()
    lookup.run(sys.argv[1])
