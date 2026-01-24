#!/usr/bin/env python3
import socket
import requests
import dns.resolver
from tool_base import ToolBase

class SubdomainScanner(ToolBase):
    def run(self, target):
        domain = target.replace('http://', '').replace('https://', '').split('/')[0]
        
        results = {
            'target': domain,
            'found_subdomains': [],
            'total_checked': 0,
            'errors': []
        }
        
        print(f"🌐 Поиск субдоменов для: {domain}")
        print("=" * 40)
        
        common_subdomains = [
            'www', 'mail', 'ftp', 'smtp', 'pop', 'imap',
            'admin', 'blog', 'shop', 'store', 'api',
            'test', 'dev', 'staging', 'prod', 'mobile',
            'secure', 'vpn', 'webmail', 'portal', 'cdn',
            'dns', 'ns1', 'ns2', 'ns3', 'ns4',
            'mx', 'mx1', 'mx2', 'mx3', 'mx4'
        ]
        
        found_count = 0
        
        for sub in common_subdomains:
            subdomain = f"{sub}.{domain}"
            results['total_checked'] += 1
            
            try:
                ip = socket.gethostbyname(subdomain)
                found_count += 1
                results['found_subdomains'].append({
                    'subdomain': subdomain,
                    'ip': ip
                })
                print(f"✅ Найдено: {subdomain} → {ip}")
            except socket.gaierror:
                pass
            except Exception as e:
                results['errors'].append(str(e))
        
        if found_count > 0:
            print(f"\n📊 РЕЗУЛЬТАТЫ:")
            print(f"  • Найдено субдоменов: {found_count}")
            print(f"  • Проверено вариантов: {results['total_checked']}")
            print(f"  • Эффективность: {found_count/results['total_checked']*100:.1f}%")
        else:
            print(f"\n❌ Субдомены не найдены")
            print(f"💡 Возможно:")
            print(f"  • Домен не использует стандартные субдомены")
            print(f"  • DNS записи скрыты")
            print(f"  • Попробуйте расширенный поиск")
        
        return results

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Использование: python subdomain_scanner.py <domain>")
        sys.exit(1)
    
    scanner = SubdomainScanner()
    scanner.run(sys.argv[1])
