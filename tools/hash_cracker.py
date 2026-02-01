import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.action_logger import ActionLogger
    LOG_ENABLED = True
except ImportError:
    LOG_ENABLED = False

def crack_hash(hash_value):
    if LOG_ENABLED:
        logger = ActionLogger()
        logger.log_action(1, "hash_crack", "hash_cracker", hash_value)
    
    print(f"Взлом хэша: {hash_value}")
    
    # Демо словарь для брутфорса
    common_passwords = [
        "password", "123456", "admin", "qwerty", 
        "letmein", "welcome", "monkey", "password123"
    ]
    
    # Демо хэши
    hash_db = {
        "5f4dcc3b5aa765d61d8327deb882cf99": "password",  # MD5
        "e10adc3949ba59abbe56e057f20f883e": "123456",
        "21232f297a57a5a743894a0e4a801fc3": "admin",
    }
    
    if hash_value in hash_db:
        result = hash_db[hash_value]
        print(f"✅ Найден пароль: {result}")
        return {"hash": hash_value, "password": result, "method": "dictionary"}
    else:
        print(f"❌ Пароль не найден в базе")
        return {"hash": hash_value, "password": None, "method": "not_found"}

if __name__ == "__main__":
    import sys
    hash_input = sys.argv[1] if len(sys.argv) > 1 else "5f4dcc3b5aa765d61d8327deb882cf99"
    crack_hash(hash_input)
