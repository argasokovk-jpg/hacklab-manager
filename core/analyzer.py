import sqlite3
import os
from datetime import datetime

class ThinkingAnalyzer:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.path.expanduser('~/.hacklab/data.db')
    
    def get_actions(self, user_id=1, lab_id=1):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT action_type, tool_used, target, timestamp 
            FROM user_actions 
            WHERE user_id=? AND lab_id=?
            ORDER BY timestamp
            ''', (user_id, lab_id))
            
            actions = cursor.fetchall()
            conn.close()
            return actions
            
        except Exception as e:
            print(f"Ошибка получения действий: {e}")
            return []
    
    def analyze_sequence(self, user_id=1, lab_id=1):
        try:
            actions = self.get_actions(user_id, lab_id)
            
            if not actions:
                return {
                    "total_actions": 0,
                    "tools_used": [],
                    "sequence": [],
                    "score": 0,
                    "level": "Новичок",
                    "feedback": ["⚠️ Нет действий для анализа"],
                    "recommendations": ["➡️ Начни с network_info для разведки"]
                }
            
            tools_used = [action[1] for action in actions]
            action_types = [action[0] for action in actions]
            
            score = 100
            feedback = []
            
            if len(actions) < 2:
                feedback.append("⚠️ Слишком мало действий для анализа")
                score -= 30
            
            if "network_info" not in tools_used:
                feedback.append("❌ Не начал с разведки сети (network_info)")
                score -= 20
            
            if "port_check" not in tools_used:
                feedback.append("❌ Не сканировал порты (port_check)")
                score -= 20
            
            if actions[0][1] != "network_info":
                feedback.append("⚠️ Лучше начинать с разведки сети")
                score -= 10
            
            if len(set(tools_used)) < 2:
                feedback.append("⚠️ Использовал мало инструментов")
                score -= 10
            
            if score > 90:
                level = "Senior"
            elif score > 70:
                level = "Middle"
            elif score > 50:
                level = "Junior"
            else:
                level = "Новичок"
            
            return {
                "total_actions": len(actions),
                "tools_used": tools_used,
                "sequence": actions,
                "score": max(0, score),
                "level": level,
                "feedback": feedback,
                "recommendations": self.get_recommendations(tools_used)
            }
            
        except Exception as e:
            return {
                "total_actions": 0,
                "tools_used": [],
                "sequence": [],
                "score": 0,
                "level": "Ошибка",
                "feedback": [f"❌ Ошибка анализа: {e}"],
                "recommendations": ["➡️ Проверь базу данных"]
            }
    
    def get_recommendations(self, tools_used):
        recs = []
        
        if "network_info" in tools_used and "port_check" in tools_used:
            recs.append("✅ Отличная последовательность: разведка → сканирование портов")
        
        if "web_scanner" not in tools_used:
            recs.append("➡️ Попробуй web_scanner для сканирования веб-уязвимостей")
        
        if "dir_buster" not in tools_used:
            recs.append("➡️ Добавь dir_buster для поиска скрытых директорий")
        
        if "ssl_checker" not in tools_used:
            recs.append("➡️ Проверь SSL сертификаты с ssl_checker")
        
        return recs
    
    def print_report(self, user_id=1, lab_id=1):
        analysis = self.analyze_sequence(user_id, lab_id)
        
        print("\n" + "="*50)
        print("📊 АНАЛИЗ ТВОЕГО ПОДХОДА")
        print("="*50)
        
        print(f"\nВсего действий: {analysis['total_actions']}")
        print(f"Использованные инструменты: {', '.join(analysis['tools_used'])}")
        
        print(f"\n🏆 ОЦЕНКА: {analysis['score']}/100")
        print(f"📈 УРОВЕНЬ: {analysis['level']}")
        
        if analysis['feedback']:
            print(f"\n📝 ОБРАТНАЯ СВЯЗЬ:")
            for fb in analysis['feedback']:
                print(f"  {fb}")
        
        if analysis['recommendations']:
            print(f"\n💡 РЕКОМЕНДАЦИИ:")
            for rec in analysis['recommendations']:
                print(f"  {rec}")
        
        if analysis['sequence']:
            print(f"\n🕒 ПОСЛЕДОВАТЕЛЬНОСТЬ ДЕЙСТВИЙ:")
            for i, action in enumerate(analysis['sequence'], 1):
                action_type, tool, target, timestamp = action
                print(f"  {i}. {timestamp[11:19]} | {tool:15} | {target}")

if __name__ == "__main__":
    analyzer = ThinkingAnalyzer()
    analyzer.print_report()
