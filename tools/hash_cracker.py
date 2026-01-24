#!/usr/bin/env python3
import hashlib
from tool_base import ToolBase

class HashCracker(ToolBase):
    def run(self, target_hash):
        results = {
            'hash': target_hash,
            'type': None,
            'cracked': False,
            'plaintext': None,
            'method': None
        }
        
        hash_length = len(target_hash)
        
        print(f"🔐 Анализ хеша: {target_hash}")
        print("=" * 40)
        
        hash_type = self.detect_hash_type(target_hash)
        results['type'] = hash_type
        
        if hash_type:
            print(f"📊 Определен тип: {hash_type}")
        else:
            print(f"❌ Неизвестный тип хеша")
            return results
        
        common_passwords = [
            'password', '123456', 'qwerty', 'admin', 'welcome',
            'password123', '12345678', '123456789', '123123',
            'qwerty123', '1q2w3e4r', '111111', 'sunshine',
            'iloveyou', 'monkey', 'dragon', 'football', 'letmein'
        ]
        
        print(f"\n🔍 Проверяю {len(common_passwords)} паролей...")
        
        for password in common_passwords:
            test_hash = self.hash_string(password, hash_type)
            
            if test_hash == target_hash.lower():
                results['cracked'] = True
                results['plaintext'] = password
                results['method'] = 'dictionary'
                
                print(f"✅ Хеш взломан!")
                print(f"📝 Пароль: {password}")
                print(f"💡 Тип: {hash_type}")
                return results
        
        print(f"\n❌ Пароль не найден в словаре")
        print(f"💡 РЕКОМЕНДАЦИИ:")
        print(f"  • Попробуйте больше вариантов паролей")
        print(f"  • Используйте rainbow tables")
        print(f"  • Проверьте другие методы взлома")
        
        return results
    
    def detect_hash_type(self, hash_str):
        hash_str = hash_str.lower()
        length = len(hash_str)
        
        hash_types = {
            32: 'md5',
            40: 'sha1',
            56: 'sha224',
            64: 'sha256',
            96: 'sha384',
            128: 'sha512'
        }
        
        return hash_types.get(length, None)
    
    def hash_string(self, text, hash_type):
        text = text.encode('utf-8')
        
        if hash_type == 'md5':
            return hashlib.md5(text).hexdigest()
        elif hash_type == 'sha1':
            return hashlib.sha1(text).hexdigest()
        elif hash_type == 'sha256':
            return hashlib.sha256(text).hexdigest()
        elif hash_type == 'sha512':
            return hashlib.sha512(text).hexdigest()
        else:
            return ''

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Использование: python hash_cracker.py <hash>")
        sys.exit(1)
    
    cracker = HashCracker()
    cracker.run(sys.argv[1])
