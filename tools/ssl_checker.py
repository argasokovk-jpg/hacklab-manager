#!/usr/bin/env python3
import ssl
import socket
from datetime import datetime
from tool_base import ToolBase

class SslChecker(ToolBase):
    def run(self, target):
        results = {
            'target': target,
            'port': 443,
            'has_ssl': False,
            'valid': False,
            'days_left': 0,
            'cert_info': {},
            'warnings': []
        }
        
        try:
            hostname = target.replace('http://', '').replace('https://', '').split('/')[0]
            
            print(f"🔐 Проверка SSL для {hostname}:443")
            print("=" * 40)
            
            context = ssl.create_default_context()
            
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    results['has_ssl'] = True
                    results['cert_info'] = cert
                    
                    print(f"✅ SSL сертификат найден")
                    print(f"📅 Действует до: {cert['notAfter']}")
                    
                    expiry_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_left = (expiry_date - datetime.now()).days
                    
                    results['days_left'] = days_left
                    results['valid'] = days_left > 0
                    
                    if days_left > 30:
                        print(f"📊 Срок действия: {days_left} дней (норма)")
                        results['status'] = 'valid'
                    elif days_left > 0:
                        print(f"⚠️  Срок действия: {days_left} дней (скоро истекает!)")
                        results['status'] = 'expiring'
                        results['warnings'].append(f"Сертификат истекает через {days_left} дней")
                    else:
                        print(f"❌ Срок действия: ИСТЕК {-days_left} дней назад!")
                        results['status'] = 'expired'
                        results['warnings'].append(f"Сертификат просрочен на {-days_left} дней")
                    
                    issuer = dict(x[0] for x in cert['issuer'])
                    subject = dict(x[0] for x in cert['subject'])
                    
                    print(f"\n📝 ИНФОРМАЦИЯ О СЕРТИФИКАТЕ:")
                    print(f"  • Издатель: {issuer.get('organizationName', 'Unknown')}")
                    print(f"  • Владелец: {subject.get('commonName', 'Unknown')}")
                    
                    results['issuer'] = issuer
                    results['subject'] = subject
                    
                    return results
        
        except socket.timeout:
            error_msg = "Таймаут соединения"
            print(f"❌ {error_msg}")
            results['error'] = error_msg
            return results
        except ConnectionRefusedError:
            error_msg = "Соединение отклонено"
            print(f"❌ {error_msg}")
            results['error'] = error_msg
            return results
        except ssl.SSLError as e:
            error_msg = f"SSL ошибка: {e}"
            print(f"❌ {error_msg}")
            results['error'] = error_msg
            results['has_ssl'] = False
            return results
        except Exception as e:
            error_msg = f"Ошибка: {e}"
            print(f"❌ {error_msg}")
            results['error'] = error_msg
            return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Использование: python ssl_checker.py <hostname>")
        sys.exit(1)
    
    checker = SslChecker()
    checker.run(sys.argv[1])
