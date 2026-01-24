#!/usr/bin/env python3

import socket
import sys
import os
import concurrent.futures
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.tool_base import ToolBase

class PortCheck(ToolBase):
    def __init__(self):
        super().__init__()
        
    def run(self, target):
        self.print_banner()
        
        print(f"🔍 Проверка портов для: {target}")
        print("="*40)
        
        try:
            # Получаем IP
            try:
                ip_address = socket.gethostbyname(target)
                print(f"📡 IP адрес: {ip_address}")
            except:
                ip_address = target
            
            # Список портов для проверки
            common_ports = [
                20, 21, 22, 23, 25, 53, 67, 68, 69, 80,
                110, 123, 135, 137, 138, 139, 143, 161, 162,
                389, 443, 445, 465, 514, 515, 587, 631, 636,
                993, 995, 1080, 1194, 1433, 1701, 1723, 1900,
                2049, 2082, 2083, 2086, 2087, 2095, 2096,
                2222, 2375, 2376, 3000, 3306, 3389, 5432,
                5900, 5984, 6379, 7001, 7002, 8080, 8081,
                8088, 8443, 8888, 9000, 9042, 9092, 9200,
                9300, 11211, 27017, 27018, 28017, 50000
            ]
            
            print(f"\n📊 Сканирую {len(common_ports)} популярных портов...")
            
            open_ports = []
            
            def check_port(port):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((ip_address, port))
                    sock.close()
                    return port, result == 0
                except:
                    return port, False
            
            # Используем многопоточность для быстрого сканирования
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                futures = {executor.submit(check_port, port): port for port in common_ports}
                
                completed = 0
                total = len(common_ports)
                
                for future in concurrent.futures.as_completed(futures):
                    completed += 1
                    port, is_open = future.result()
                    
                    if is_open:
                        open_ports.append(port)
                    
                    # Показываем прогресс
                    percent = (completed / total) * 100
                    sys.stdout.write(f"\r⏳ Прогресс: {completed}/{total} ({percent:.1f}%) | Открыто: {len(open_ports)}")
                    sys.stdout.flush()
            
            print("\n\n" + "="*40)
            print(f"🎉 СКАНИРОВАНИЕ ЗАВЕРШЕНО!")
            print("="*40)
            
            if open_ports:
                print(f"\n✅ ОТКРЫТЫЕ ПОРТЫ ({len(open_ports)}):")
                print("-"*40)
                
                # Группируем порты по категориям
                categories = {
                    "Веб-сервисы": [80, 443, 8080, 8081, 8443, 8888],
                    "Базы данных": [3306, 5432, 27017, 27018, 28017, 6379, 9200, 9300],
                    "Удаленное управление": [22, 23, 3389, 5900],
                    "Почта": [25, 110, 143, 465, 587, 993, 995],
                    "Файловые сервисы": [20, 21, 69, 137, 138, 139, 445, 2049],
                    "Сеть и DNS": [53, 67, 68, 123, 161, 162, 389, 636],
                    "Другие сервисы": []
                }
                
                for category, ports in categories.items():
                    category_ports = [p for p in open_ports if p in ports]
                    if category_ports:
                        print(f"\n📌 {category}:")
                        for port in sorted(category_ports):
                            service = self.get_service_name(port)
                            print(f"  • Порт {port:5} - {service}")
                
                # Остальные порты
                other_ports = [p for p in open_ports if not any(p in ports for ports in categories.values())]
                if other_ports:
                    print(f"\n📌 Прочие порты:")
                    for port in sorted(other_ports):
                        service = self.get_service_name(port)
                        print(f"  • Порт {port:5} - {service}")
                
                print(f"\n💡 РЕКОМЕНДАЦИИ:")
                if 22 in open_ports:
                    print("  • Порт 22 (SSH) открыт - проверьте безопасность SSH")
                if 80 in open_ports and 443 not in open_ports:
                    print("  • Порт 80 (HTTP) открыт, но 443 (HTTPS) закрыт - рекомендуется HTTPS")
                if 3389 in open_ports:
                    print("  • Порт 3389 (RDP) открыт - убедитесь в необходимости RDP")
                if 1433 in open_ports:
                    print("  • Порт 1433 (MSSQL) открыт - проверьте безопасность базы данных")
                
            else:
                print(f"\n❌ Открытых портов не обнаружено")
            
            result = f"Открыто портов: {len(open_ports)}"
            self.save_result(target, result)
            
            return open_ports
            
        except Exception as e:
            error_msg = f"❌ Ошибка: {e}"
            print(error_msg)
            return error_msg
    
    def get_service_name(self, port):
        services = {
            20: "FTP Data", 21: "FTP Control", 22: "SSH", 23: "Telnet",
            25: "SMTP", 53: "DNS", 67: "DHCP Server", 68: "DHCP Client",
            69: "TFTP", 80: "HTTP", 110: "POP3", 123: "NTP",
            135: "MS RPC", 137: "NetBIOS", 138: "NetBIOS", 139: "NetBIOS",
            143: "IMAP", 161: "SNMP", 162: "SNMP Trap", 389: "LDAP",
            443: "HTTPS", 445: "SMB", 465: "SMTPS", 514: "Syslog",
            515: "LPD", 587: "SMTP", 631: "IPP", 636: "LDAPS",
            993: "IMAPS", 995: "POP3S", 1080: "SOCKS", 1194: "OpenVPN",
            1433: "MSSQL", 1701: "L2TP", 1723: "PPTP", 1900: "UPnP",
            2049: "NFS", 2082: "cPanel", 2083: "cPanel SSL", 2086: "WHM",
            2087: "WHM SSL", 2095: "Webmail", 2096: "Webmail SSL",
            2222: "DirectAdmin", 2375: "Docker", 2376: "Docker SSL",
            3000: "Node.js", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
            5900: "VNC", 5984: "CouchDB", 6379: "Redis", 7001: "WebLogic",
            7002: "WebLogic SSL", 8080: "HTTP Proxy", 8081: "HTTP Proxy",
            8088: "HTTP", 8443: "HTTPS", 8888: "HTTP Alt", 9000: "SonarQube",
            9042: "Cassandra", 9092: "Kafka", 9200: "Elasticsearch",
            9300: "Elasticsearch", 11211: "Memcached", 27017: "MongoDB",
            27018: "MongoDB", 28017: "MongoDB HTTP", 50000: "SAP"
        }
        return services.get(port, "Неизвестно")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        scanner = PortCheck()
        scanner.run(sys.argv[1])
    else:
        print("Использование: python port_check.py <hostname/ip>")
        print("Пример: python port_check.py scanme.nmap.org")
