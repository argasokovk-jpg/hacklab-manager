#!/usr/bin/env python3
import requests
import time
from tool_base import ToolBase

class DirBuster(ToolBase):
    def run(self, target):
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
        
        results = {
            'target': target,
            'found_dirs': [],
            'total_checked': 0,
            'status_code_counts': {}
        }
        
        print(f"📁 Поиск директорий для: {target}")
        print("=" * 40)
        
        common_paths = [
            "", "admin", "login", "wp-admin", "backup", "config",
            "admin.php", "login.php", "admin/login", "admin/index.php",
            "test", "debug", "api", "doc", "docs", "documentation",
            "private", "secret", "hidden", "uploads", "images",
            "js", "css", "assets", "static", "public", "src"
        ]
        
        found_count = 0
        
        for path in common_paths:
            url = target.rstrip('/') + '/' + path if path else target
            results['total_checked'] += 1
            
            try:
                response = requests.get(url, timeout=5, verify=False, allow_redirects=True)
                status = response.status_code
                
                if status in results['status_code_counts']:
                    results['status_code_counts'][status] += 1
                else:
                    results['status_code_counts'][status] = 1
                
                if status == 200:
                    found_count += 1
                    dir_info = {
                        'path': url,
                        'status_code': status,
                        'size': len(response.content)
                    }
                    results['found_dirs'].append(dir_info)
                    
                    print(f"✅ Найдено: {url} [{status}] ({len(response.content)} байт)")
                
                elif status in [301, 302, 303, 307, 308]:
                    print(f"🔄 Редирект: {url} → {response.url} [{status}]")
                
                elif status in [403, 401]:
                    print(f"🔒 Запрещено: {url} [{status}]")
                
                elif status == 404:
                    pass
                
                else:
                    print(f"ℹ️  {url} [{status}]")
                
                time.sleep(0.1)
                
            except requests.exceptions.RequestException:
                continue
        
        print(f"\n📊 РЕЗУЛЬТАТЫ:")
        print(f"  • Проверено директорий: {results['total_checked']}")
        print(f"  • Найдено доступных: {found_count}")
        
        if results['status_code_counts']:
            print(f"  • Коды ответов:")
            for code, count in sorted(results['status_code_counts'].items()):
                print(f"    • {code}: {count}")
        
        if found_count == 0:
            print(f"\n⚠️  Не найдено доступных директорий")
            print(f"💡 Попробуйте:")
            print(f"  • Увеличить wordlist")
            print(f"  • Проверить другие порты")
        
        return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Использование: python dir_buster.py <url>")
        sys.exit(1)
    
    scanner = DirBuster()
    scanner.run(sys.argv[1])
