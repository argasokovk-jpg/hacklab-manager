class FeedbackGenerator:
    """
    Генерирует понятные объяснения для каждой оценки
    """
    
    @classmethod
    def generate(cls, methodology_score, methodology_feedback,
                 efficiency_score, efficiency_feedback,
                 efficiency_stats, overall, level):
        """
        Собирает все отзывы в единый блок
        """
        result = {
            'overall': {
                'score': overall,
                'level': level
            },
            'methodology': {
                'score': methodology_score,
                'feedback': methodology_feedback,
                'rating': cls._get_rating(methodology_score)
            },
            'efficiency': {
                'score': efficiency_score,
                'feedback': efficiency_feedback,
                'stats': efficiency_stats,
                'rating': cls._get_rating(efficiency_score)
            },
            'summary': [],
            'advice': []
        }
        
        # Итоговое резюме
        if overall >= 80:
            result['summary'].append('🔥 Отличная работа! Ты демонстрируешь профессиональный подход.')
        elif overall >= 60:
            result['summary'].append('💪 Хороший результат! Продолжай развиваться.')
        else:
            result['summary'].append('📚 Есть куда расти. Сфокусируйся на методологии.')
        
        # Советы
        if methodology_score < 70:
            result['advice'].append('🎯 Изучи методологию пентеста: Recon → Enumeration → Analysis → Exploitation')
        if efficiency_score < 70:
            result['advice'].append('⚡ Старайся не повторять команды без необходимости')
        
        if not result['advice']:
            result['advice'].append('👍 Отличный подход! Продолжай в том же духе.')
        
        return result
    
    @classmethod
    def _get_rating(cls, score):
        if score >= 80:
            return 'excellent'
        elif score >= 60:
            return 'good'
        elif score >= 40:
            return 'average'
        else:
            return 'needs_improvement'
