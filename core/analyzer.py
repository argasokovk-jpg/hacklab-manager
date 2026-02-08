import sqlite3
import os
from datetime import datetime
from collections import defaultdict

class ThinkingAnalyzer:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.path.expanduser('~/.hacklab/data.db')
    
    def get_actions(self, user_id=1, lab_id=None):
        """Получает действия пользователя"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if lab_id is None:
                cursor.execute('''
                SELECT action_type, tool_used, target, timestamp, lab_id
                FROM user_actions 
                WHERE user_id=?
                ORDER BY timestamp
                ''', (user_id,))
            else:
                cursor.execute('''
                SELECT action_type, tool_used, target, timestamp, lab_id
                FROM user_actions 
                WHERE user_id=? AND lab_id=?
                ORDER BY timestamp
                ''', (user_id, lab_id))
            
            actions = cursor.fetchall()
            conn.close()
            
            result = []
            for action in actions:
                result.append({
                    'type': action[0],
                    'tool': action[1],
                    'target': action[2],
                    'timestamp': action[3],
                    'lab_id': action[4]
                })
            return result
            
        except Exception as e:
            print(f"DEBUG: Ошибка получения действий: {e}")
            return []
    
    def _get_level(self, score):
        if score >= 85:
            return "Senior"
        elif score >= 70:
            return "Middle"
        elif score >= 50:
            return "Junior"
        else:
            return "Beginner"
    
    def _analyze_timing(self, actions):
        if len(actions) < 2:
            return 0, []
        
        score = 0
        feedback = []
        too_fast_count = 0
        
        for i in range(1, len(actions)):
            try:
                current_time = datetime.strptime(actions[i]['timestamp'], '%Y-%m-%d %H:%M:%S')
                prev_time = datetime.strptime(actions[i-1]['timestamp'], '%Y-%m-%d %H:%M:%S')
                
                time_diff = (current_time - prev_time).total_seconds()
                
                if time_diff < 30:
                    score -= 2
                    too_fast_count += 1
                elif 60 <= time_diff <= 120:
                    score += 1
                    
            except:
                continue
        
        if too_fast_count > 3:
            feedback.append("🚫 Слишком торопишься! Делай паузы 30-60 сек между действиями.")
        elif too_fast_count > 0:
            feedback.append("⏱️  Попробуй делать паузы между действиями для анализа.")
        
        return score, feedback
    
    def _analyze_noise(self, actions):
        if not actions:
            return 0, []
        
        target_tools = defaultdict(lambda: defaultdict(int))
        
        for action in actions:
            target = action.get('target', 'unknown')
            tool = action.get('tool', 'unknown')
            target_tools[target][tool] += 1
        
        score = 0
        feedback = []
        
        for target, tools in target_tools.items():
            for tool, count in tools.items():
                if count > 1:
                    penalty = (count - 1) * 3
                    score -= penalty
                    
                    if penalty > 6:
                        feedback.append(f"❌ Слишком много повторений {tool} на {target} ({count} раз)")
                    elif penalty > 0:
                        feedback.append(f"⚠️  Много повторений {tool} на {target} ({count} раз)")
        
        if score < -15:
            feedback.append("💡 Совет: Не запускай инструменты повторно без причины.")
        
        return score, feedback
    
    def _analyze_sequence_logic(self, actions):
        if not actions:
            return 0, []
        
        score = 0
        feedback = []
        
        recon_tools = ['whois_checker', 'network_info', 'dns_enum']
        scan_tools = ['port_check']
        analysis_tools = ['ssl_checker', 'web_scanner']
        exploit_tools = ['dir_buster', 'sql_tester', 'xss_scanner', 'cve_lookup']
        
        stage_order = []
        
        for action in actions:
            tool = action.get('tool', '')
            
            if tool in recon_tools:
                stage_order.append('recon')
            elif tool in scan_tools:
                stage_order.append('scan')
            elif tool in analysis_tools:
                stage_order.append('analysis')
            elif tool in exploit_tools:
                stage_order.append('exploit')
        
        if len(stage_order) >= 3:
            if 'scan' in stage_order and 'recon' in stage_order:
                recon_idx = stage_order.index('recon')
                scan_idx = stage_order.index('scan')
                
                if recon_idx < scan_idx:
                    score += 10
                    feedback.append("✅ Правильно: разведка до сканирования портов")
                else:
                    score -= 10
                    feedback.append("❌ Неправильно: сканирование до разведки")
            
            if 'analysis' in stage_order and 'scan' in stage_order:
                scan_idx = stage_order.index('scan')
                analysis_idx = stage_order.index('analysis')
                
                if scan_idx < analysis_idx:
                    score += 10
                    feedback.append("✅ Правильно: сканирование до анализа сервисов")
        
        tools_used = [a.get('tool', '') for a in actions]
        
        if 'dir_buster' in tools_used and 'web_scanner' not in tools_used:
            score -= 15
            feedback.append("❌ dir_buster без web_scanner! Сначала узнай что за сервер.")
        
        if 'cve_lookup' in tools_used and ('port_check' not in tools_used or 'web_scanner' not in tools_used):
            score -= 10
            feedback.append("❌ cve_lookup без данных о сервисах! Сначала собери информацию.")
        
        return score, feedback
    
    def _analyze_efficiency(self, actions):
        if len(actions) == 0:
            return 0, []
        
        unique_tools = len(set(a.get('tool', '') for a in actions))
        total_actions = len(actions)
        
        score = 0
        feedback = []
        
        if total_actions > 0:
            efficiency = unique_tools / total_actions
            
            if efficiency >= 0.8:
                score += 15
                feedback.append("🎯 Отличная эффективность! Минимум действий - максимум информации.")
            elif efficiency >= 0.6:
                score += 5
            elif efficiency < 0.4:
                score -= 10
                feedback.append("📉 Низкая эффективность. Много повторных действий.")
        
        return score, feedback
    
    def analyze(self, user_id=1, lab_id=None, target_filter=None):
        print("🧠 Анализирую твой подход с улучшенной логикой...")
        
        actions = self.get_actions(user_id, lab_id)
        
        if not actions:
            return {
                "total_actions": 0,
                "tools_used": [],
                "score": 0,
                "level": "Beginner",
                "feedback": ["⚠️ Нет действий для анализа"],
                "recommendations": ["➡️ Начни с hl tool network_info [цель]"]
            }
        
        if target_filter:
            actions = [a for a in actions if a.get('target') == target_filter]
        
        if not actions:
            return {
                "total_actions": 0,
                "tools_used": [],
                "score": 0,
                "level": "Beginner",
                "feedback": [f"⚠️ Нет действий для цели {target_filter}"],
                "recommendations": [f"➡️ Начни с hl tool network_info {target_filter}"]
            }
        
        score = 50
        all_feedback = []
        
        time_score, time_feedback = self._analyze_timing(actions)
        score += time_score
        all_feedback.extend(time_feedback)
        
        noise_score, noise_feedback = self._analyze_noise(actions)
        score += noise_score
        all_feedback.extend(noise_feedback)
        
        seq_score, seq_feedback = self._analyze_sequence_logic(actions)
        score += seq_score
        all_feedback.extend(seq_feedback)
        
        eff_score, eff_feedback = self._analyze_efficiency(actions)
        score += eff_score
        all_feedback.extend(eff_feedback)
        
        if len(actions) <= 8 and len(set(a.get('tool', '') for a in actions)) >= 5:
            score += 15
            all_feedback.append("🏆 Отличная стратегия! Минимум действий при максимуме результата.")
        
        score = max(0, min(100, score))
        
        unique_tools = list(set(a.get('tool', '') for a in actions))
        
        timeline = []
        for i, action in enumerate(actions[-10:], 1):
            ts = action.get('timestamp', '')[:19]
            tool = action.get('tool', 'unknown')
            target = action.get('target', 'unknown')
            timeline.append(f"{ts} | {tool:20} | {target}")
        
        return {
            "total_actions": len(actions),
            "tools_used": unique_tools,
            "score": score,
            "level": self._get_level(score),
            "feedback": all_feedback,
            "timeline": timeline,
            "targets": list(set(a.get('target', '') for a in actions))
        }

def print_analysis(result):
    print("\n" + "="*50)
    print("📊 УЛУЧШЕННЫЙ АНАЛИЗ ПОДХОДА")
    print("="*50)
    
    if result['total_actions'] == 0:
        print("⚠️  Нет действий для анализа")
        print("💡 Начни с: hl tool network_info scanme.nmap.org")
        return
    
    print(f"\n📈 СТАТИСТИКА:")
    print(f"  Всего действий: {result['total_actions']}")
    print(f"  Уникальных инструментов: {len(result['tools_used'])}")
    
    if result['targets']:
        print(f"  Цели: {', '.join(result['targets'][:3])}")
        if len(result['targets']) > 3:
            print(f"  ... и еще {len(result['targets']) - 3} целей")
    
    print(f"\n🏆 ОЦЕНКА: {result['score']}/100")
    print(f"📈 УРОВЕНЬ: {result['level']}")
    
    if result['feedback']:
        print(f"\n📝 ОБРАТНАЯ СВЯЗЬ:")
        for fb in result['feedback']:
            print(f"  {fb}")
    
    print(f"\n💡 РЕКОМЕНДАЦИИ:")
    if result['score'] >= 80:
        print("  [+] Продолжай в том же духе! Ты на пути к Senior уровню.")
    elif result['score'] >= 60:
        print("  [+] Хороший подход, но есть что улучшить.")
    else:
        print("  [+] Сфокусируйся на методологии из 'hl learn'")
    
    print(f"\n🕒 ПОСЛЕДНИЕ ДЕЙСТВИЯ:")
    for i, line in enumerate(result['timeline'], 1):
        print(f"  {i:2}. {line}")

def analyze_command():
    import sys
    
    target_filter = None
    lab_id = None
    
    if len(sys.argv) > 2:
        for arg in sys.argv[2:]:
            if arg.startswith('--target='):
                target_filter = arg.split('=')[1]
            elif arg.startswith('--lab='):
                lab_id = int(arg.split('=')[1])
    
    analyzer = ThinkingAnalyzer()
    result = analyzer.analyze(user_id=1, lab_id=lab_id, target_filter=target_filter)
    print_analysis(result)

if __name__ == "__main__":
    analyze_command()
