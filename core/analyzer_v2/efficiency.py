class EfficiencyAnalyzer:
    """
    Анализирует эффективность действий
    """
    
    @classmethod
    def analyze(cls, actions):
        """
        Считает эффективность на основе количества действий
        """
        if not actions:
            return 0, ['⚠️ Нет действий для анализа эффективности']
        
        total = len(actions)
        
        # Считаем уникальные действия
        unique_commands = set()
        unique_tools = set()
        failed = 0
        
        for action in actions:
            command = action.get('command', '')
            tool = action.get('tool', '')
            exit_code = action.get('exit_code', 0)
            
            if command:
                unique_commands.add(command)
            if tool:
                unique_tools.add(tool)
            if exit_code != 0 and exit_code is not None:
                failed += 1
        
        # Эффективность: уникальные команды / общее количество
        if total > 0:
            efficiency_ratio = len(unique_commands) / total
        else:
            efficiency_ratio = 0
        
        # Базовый счёт
        score = 50
        
        feedback = []
        
        # Оценка эффективности
        if efficiency_ratio >= 0.8:
            score += 30
            feedback.append('🎯 Отличная эффективность! Минимум повторений')
        elif efficiency_ratio >= 0.6:
            score += 15
            feedback.append('👍 Хорошая эффективность')
        elif efficiency_ratio >= 0.4:
            score += 0
            feedback.append('📊 Средняя эффективность')
        else:
            score -= 15
            feedback.append('📉 Низкая эффективность. Много повторных действий')
        
        # Штраф за неудачные команды
        if failed > 0:
            penalty = min(failed * 2, 20)
            score -= penalty
            if failed > 3:
                feedback.append(f'⚠️ {failed} неудачных команд')
        
        # Бонус за разнообразие инструментов
        if len(unique_tools) >= 3:
            score += 5
            feedback.append('✅ Хорошее разнообразие инструментов')
        
        efficiency_score = min(100, max(0, score))
        
        return efficiency_score, feedback, {
            'total_commands': total,
            'unique_commands': len(unique_commands),
            'unique_tools': len(unique_tools),
            'failed_commands': failed,
            'efficiency_ratio': round(efficiency_ratio * 100, 1)
        }
