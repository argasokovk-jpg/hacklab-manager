class MethodologyAnalyzer:
    """
    Анализирует последовательность этапов
    """
    
    # Ожидаемый порядок этапов
    STAGE_ORDER = ['recon', 'enumeration', 'analysis', 'exploitation', 'reporting']
    
    @classmethod
    def analyze(cls, classified_actions):
        """
        Проверяет, насколько последовательность соответствует методологии
        """
        if not classified_actions:
            return 0, []
        
        # Извлекаем этапы
        stages = [a.get('stage', 'unknown') for a in classified_actions]
        
        # Убираем unknown
        clean_stages = [s for s in stages if s != 'unknown']
        
        if not clean_stages:
            return 0, ['⚠️ Не удалось определить этапы действий']
        
        # Проверяем наличие этапов
        present_stages = list(set(clean_stages))
        
        score = 50  # базовая оценка
        feedback = []
        
        # Проверка: есть ли разведка до сканирования
        if 'recon' in clean_stages and 'enumeration' in clean_stages:
            recon_idx = clean_stages.index('recon')
            enum_idx = clean_stages.index('enumeration')
            if recon_idx < enum_idx:
                score += 20
                feedback.append('✅ Правильно: разведка до сканирования')
            else:
                score -= 15
                feedback.append('❌ Сканирование до разведки — потеря времени')
        
        # Проверка: есть ли анализ после сканирования
        if 'enumeration' in clean_stages and 'analysis' in clean_stages:
            enum_idx = clean_stages.index('enumeration')
            analysis_idx = clean_stages.index('analysis')
            if enum_idx < analysis_idx:
                score += 15
                feedback.append('✅ Правильно: анализ после сканирования')
        
        # Проверка: все ли этапы пройдены
        expected = cls.STAGE_ORDER
        actual = [s for s in expected if s in present_stages]
        
        if len(actual) == len(expected):
            score += 10
            feedback.append('🎯 Полный цикл методологии!')
        elif len(actual) >= 3:
            score += 5
            feedback.append(f'📈 Пройдено {len(actual)} из {len(expected)} этапов')
        else:
            feedback.append('📉 Пройдено мало этапов методологии')
        
        # Оценка методологии
        methodology_score = min(100, max(0, score))
        
        return methodology_score, feedback
