from sqlalchemy.orm import Session
from web.models import Achievement, UserAchievement, LabResult
from web.database import SessionLocal

class AchievementService:
    
    @classmethod
    def check_achievements(cls, user_id, lab_id, score, methodology_score, duration):
        """
        Проверяет все достижения после завершения лаборатории
        """
        db = SessionLocal()
        unlocked = []
        
        # Получаем все достижения
        achievements = db.query(Achievement).all()
        
        # Получаем уже полученные достижения пользователя
        earned_ids = [ua.achievement_id for ua in db.query(UserAchievement).filter(
            UserAchievement.user_id == user_id
        ).all()]
        
        # Получаем все результаты пользователя
        results = db.query(LabResult).filter(
            LabResult.user_id == user_id
        ).all()
        
        for ach in achievements:
            if ach.id in earned_ids:
                continue
            
            condition = ach.condition
            earned = False
            
            if condition.startswith('lab_completed:'):
                lab_id_required = int(condition.split(':')[1])
                if any(r.lab_id == lab_id_required for r in results):
                    earned = True
            
            elif condition.startswith('lab_score:'):
                parts = condition.split(':')
                lab_id_required = int(parts[1])
                min_score = int(parts[2])
                for r in results:
                    if r.lab_id == lab_id_required and r.score >= min_score:
                        earned = True
                        break
            
            elif condition.startswith('methodology:'):
                min_score = int(condition.split(':')[1])
                if methodology_score >= min_score:
                    earned = True
            
            elif condition.startswith('score:'):
                min_score = int(condition.split(':')[1])
                if score >= min_score:
                    earned = True
            
            elif condition.startswith('time:'):
                max_time = int(condition.split(':')[1])
                if duration <= max_time:
                    earned = True
            
            elif condition.startswith('labs_count:'):
                required = int(condition.split(':')[1])
                if len(results) >= required:
                    earned = True
            
            if earned:
                # Добавляем достижение пользователю
                user_ach = UserAchievement(
                    user_id=user_id,
                    achievement_id=ach.id
                )
                db.add(user_ach)
                db.commit()
                
                unlocked.append({
                    'id': ach.id,
                    'name': ach.name,
                    'description': ach.description,
                    'icon': ach.icon,
                    'xp_reward': ach.xp_reward
                })
        
        db.close()
        return unlocked
    
    @classmethod
    def get_user_achievements(cls, user_id):
        """
        Возвращает все достижения пользователя
        """
        db = SessionLocal()
        
        achievements = db.query(Achievement, UserAchievement.earned_at).join(
            UserAchievement,
            Achievement.id == UserAchievement.achievement_id
        ).filter(
            UserAchievement.user_id == user_id
        ).order_by(UserAchievement.earned_at.desc()).all()
        
        db.close()
        
        return [{
            'id': a.id,
            'name': a.name,
            'description': a.description,
            'icon': a.icon,
            'xp_reward': a.xp_reward,
            'earned_at': earned_at
        } for a, earned_at in achievements]
