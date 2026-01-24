#!/usr/bin/env python3

import socket
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.tool_base import ToolBase

class NetworkInfo(ToolBase):
    def __init__(self):
        super().__init__()
        
    def run(self, target):
        self.print_banner()
        
        print(f"🌐 Анализ сети для: {target}")
        print("="*40)
        
        try:
            # Получаем IP адрес
            ip_address = socket.gethostbyname(target)
            print(f"📡 IP адрес: {ip_address}")
            
            # Получаем информацию о хосте
            try:
                host_info = socket.gethostbyaddr(ip_address)
                print(f"🏠 Имя хоста: {host_info[0]}")
            except:
                print(f"🏠 Имя хоста: Не определено")
            
            # Проверяем доступность
            print(f"\n📊 Проверка доступности:")
            
            # Проверка ICMP (ping)
            response = os.system(f"ping -c 1 -W 2 {target} > /dev/null 2>&1")
            if response == 0:
                print(f"  • ICMP (ping): ✅ Доступен")
            else:
                print(f"  • ICMP (ping): ❌ Недоступен")
            
            # Проверка популярных портов
            ports_to_check = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995, 3306, 3389, 5432, 8080]
            
            print(f"\n🔍 Проверка портов:")
            for port in ports_to_check:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((ip_address, port))
                    sock.close()
                    
                    if result == 0:
                        service = self.get_service_name(port)
                        print(f"  • Порт {port:5} ({service}): ✅ ОТКРЫТ")
                except:
                    pass
            
            # DNS информация
            print(f"\n🔗 DNS информация:")
            try:
                dns_info = socket.getaddrinfo(target, None)
                for info in dns_info[:3]:  # Показываем первые 3 записи
                    family, socktype, proto, canonname, sockaddr = info
                    print(f"  • {sockaddr[0]} (IPv{4 if family == socket.AF_INET else 6})")
            except:
                print(f"  • DNS записи: Не найдены")
            
            result = f"IP: {ip_address}, Проверено портов: {len(ports_to_check)}"
            self.save_result(target, result)
            
            return result
            
        except socket.gaierror:
            error_msg = f"❌ Не удалось разрешить домен: {target}"
            print(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"❌ Ошибка: {e}"
            print(error_msg)
            return error_msg
    
    def get_service_name(self, port):
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
            443: "HTTPS", 465: "SMTPS", 587: "SMTP", 993: "IMAPS",
            995: "POP3S", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
            8080: "HTTP-Proxy"
        }
        return services.get(port, "Неизвестно")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        scanner = NetworkInfo()
        scanner.run(sys.argv[1])
    else:
        print("Использование: python network_info.py <hostname/ip>")
        print("Пример: python network_info.py google.com")
