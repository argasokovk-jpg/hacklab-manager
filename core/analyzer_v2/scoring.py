class ScoringEngine:
    """
    Собирает все оценки в итоговый результат
    """
    
    @classmethod
    def calculate(cls, methodology_score, efficiency_score, bonus=0):
        """
        Считает итоговую оценку
        """
        # Веса компонентов
        weights = {
            'methodology': 0.5,
            'efficiency': 0.3,
            'bonus': 0.2
        }
        
        # Итоговая оценка
        overall = (
            methodology_score * weights['methodology'] +
            efficiency_score * weights['efficiency'] +
            bonus * weights['bonus']
        )
        
        overall = min(100, max(0, overall))
        
        # Определяем уровень
        if overall >= 85:
            level = "Senior"
        elif overall >= 70:
            level = "Middle"
        elif overall >= 50:
            level = "Junior"
        else:
            level = "Beginner"
        
        return {
            'overall': round(overall, 1),
            'level': level
        }
