#!/usr/bin/env python3
import socket
import whois
from tool_base import ToolBase

class WhoisChecker(ToolBase):
    def run(self, target):
        results = {
            'target': target,
            'whois_data': {},
            'domain_info': {},
            'warnings': []
        }
        
        print(f"🌐 WHOIS информация для: {target}")
        print("=" * 40)
        
        try:
            ip = socket.gethostbyname(target)
            print(f"📡 IP адрес: {ip}")
            results['ip_address'] = ip
            
            print(f"\n💡 Основная информация:")
            print(f"  • Домен: {target}")
            
            try:
                w = whois.whois(target)
                
                if w.domain_name:
                    print(f"  • Зарегистрирован: Да")
                    results['registered'] = True
                    
                    if w.creation_date:
                        if isinstance(w.creation_date, list):
                            creation_date = w.creation_date[0]
                        else:
                            creation_date = w.creation_date
                        print(f"  • Дата создания: {creation_date}")
                        results['creation_date'] = str(creation_date)
                    
                    if w.expiration_date:
                        if isinstance(w.expiration_date, list):
                            exp_date = w.expiration_date[0]
                        else:
                            exp_date = w.expiration_date
                        print(f"  • Истекает: {exp_date}")
                        results['expiration_date'] = str(exp_date)
                    
                    if w.registrar:
                        print(f"  • Регистратор: {w.registrar}")
                        results['registrar'] = w.registrar
                    
                    if w.name_servers:
                        print(f"\n🌐 DNS серверы:")
                        ns_list = w.name_servers if isinstance(w.name_servers, list) else [w.name_servers]
                        for ns in ns_list[:3]:
                            print(f"  • {ns}")
                        results['name_servers'] = ns_list
                    
                    results['whois_data'] = dict(w)
                    
                else:
                    print(f"  • Зарегистрирован: Нет (или информация недоступна)")
                    results['registered'] = False
                    results['warnings'].append("Домен не зарегистрирован или WHOIS информация скрыта")
            
            except whois.parser.PywhoisError as e:
                print(f"  • Зарегистрирован: Информация скрыта")
                results['registered'] = False
                results['warnings'].append(f"WHOIS информация недоступна: {e}")
            
            print(f"\n🔒 РЕКОМЕНДАЦИИ:")
            if results.get('registered', False):
                print(f"  • Проверьте дату истечения срока действия")
                print(f"  • Убедитесь что контакты актуальны")
            else:
                print(f"  • Домен доступен для регистрации")
        
        except socket.gaierror:
            error_msg = f"Не удалось получить IP адрес для {target}"
            print(f"❌ {error_msg}")
            results['error'] = error_msg
        
        return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Использование: python whois_checker.py <domain>")
        sys.exit(1)
    
    checker = WhoisChecker()
    checker.run(sys.argv[1])
