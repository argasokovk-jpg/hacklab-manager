import socket
import concurrent.futures
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.action_logger import ActionLogger
    LOG_ENABLED = True
except ImportError:
    LOG_ENABLED = False

def scan_port(host, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return port, result == 0
    except:
        return port, False

def scan_ports(target, ports="1-1000"):
    if LOG_ENABLED:
        logger = ActionLogger()
        logger.log_action(1, "port_scan", "port_check", target)
    
    print(f"Сканирование {target} порты {ports}")
    
    if "-" in ports:
        start, end = map(int, ports.split("-"))
        port_list = range(start, end + 1)
    else:
        port_list = [int(p) for p in ports.split(",") if p.isdigit()]
    
    open_ports = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, target, port) for port in port_list]
        for future in concurrent.futures.as_completed(futures):
            port, is_open = future.result()
            if is_open:
                open_ports.append(port)
                print(f"Порт {port}: OPEN")
    
    print(f"Найдено открытых портов: {len(open_ports)}")
    return open_ports

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "scanme.nmap.org"
    ports = sys.argv[2] if len(sys.argv) > 2 else "1-100"
    scan_ports(target, ports)
