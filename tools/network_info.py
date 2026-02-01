import socket
import subprocess
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.action_logger import ActionLogger
    LOG_ENABLED = True
except ImportError:
    LOG_ENABLED = False

def get_network_info(target):
    if LOG_ENABLED:
        logger = ActionLogger()
        logger.log_action(1, "network_scan", "network_info", target)
    
    print(f"Анализ сети: {target}")
    
    try:
        ip = socket.gethostbyname(target)
        print(f"IP адрес: {ip}")
        
        result = subprocess.run(['ping', '-c', '2', target], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("Хост доступен")
        else:
            print("Хост недоступен")
        
        try:
            hostname, aliases, addresses = socket.gethostbyaddr(ip)
            print(f"Обратное DNS: {hostname}")
        except:
            print("Обратное DNS: не найдено")
            
    except Exception as e:
        print(f"Ошибка: {e}")
    
    return {"target": target, "status": "scanned"}

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "scanme.nmap.org"
    get_network_info(target)
