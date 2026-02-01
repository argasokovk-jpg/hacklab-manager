import ssl
import socket
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.action_logger import ActionLogger
    LOG_ENABLED = True
except ImportError:
    LOG_ENABLED = False

def check_ssl(domain):
    if LOG_ENABLED:
        logger = ActionLogger()
        logger.log_action(1, "ssl_check", "ssl_checker", domain)
    
    print(f"Проверка SSL для: {domain}")
    
    try:
        # Добавляем порт если нет
        if ":" not in domain:
            hostname = domain
            port = 443
        else:
            hostname, port_str = domain.split(":")
            port = int(port_str)
        
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                # Информация о сертификате
                print("✅ SSL сертификат найден")
                
                # Срок действия
                if 'notBefore' in cert and 'notAfter' in cert:
                    not_before = cert['notBefore']
                    not_after = cert['notAfter']
                    print(f"   Действует с: {not_before}")
                    print(f"   Действует до: {not_after}")
                
                # Издатель
                if 'issuer' in cert:
                    issuer = cert['issuer']
                    issuer_str = ''
                    for item in issuer:
                        for key, value in item:
                            issuer_str += f"{key}={value}, "
                    print(f"   Издатель: {issuer_str.rstrip(', ')}")
                
                return {"status": "valid", "certificate": cert}
                
    except ssl.SSLError as e:
        print(f"❌ Ошибка SSL: {e}")
        return {"status": "error", "message": str(e)}
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import sys
    domain = sys.argv[1] if len(sys.argv) > 1 else "google.com"
    check_ssl(domain)
