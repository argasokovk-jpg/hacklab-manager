from fastapi import FastAPI, Request, Form, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json
import os
import docker
from pathlib import Path

from web.database import engine, get_db, Base, SessionLocal
from web.models import User, ActionLog, LabResult, Achievement, UserAchievement
from web.auth import get_password_hash, authenticate_user, create_access_token, get_current_user, get_current_user_from_token
from core.services.achievement_service import AchievementService

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# Docker client
docker_client = docker.from_env()

# Хранилище контейнеров
containers = {}

def load_labs():
    """Загружает все лаборатории из папки labs/"""
    labs_dir = Path("labs")
    labs = []
    
    if not labs_dir.exists():
        return []
    
    for lab_path in sorted(labs_dir.glob("lab_*")):
        config_file = lab_path / "config.json"
        if config_file.exists():
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)
                    labs.append(config)
            except:
                continue
    
    return labs

@app.get("/")
def home():
    return {"message": "HackLab Manager API работает"}

@app.post("/register")
async def register(
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing = db.query(User).filter(
        (User.email == email) | (User.username == username)
    ).first()
    if existing:
        return HTMLResponse("Пользователь уже существует", status_code=400)
    
    user = User(
        email=email,
        username=username,
        hashed_password=get_password_hash(password)
    )
    db.add(user)
    db.commit()
    return RedirectResponse(url="/static/login.html", status_code=303)

@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username
    }

@app.get("/api/dashboard")
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Получаем все результаты пользователя
    results = db.query(LabResult).filter(
        LabResult.user_id == current_user.id
    ).order_by(LabResult.created_at.desc()).all()
    
    # Загружаем лаборатории из конфигов
    labs = load_labs()
    
    # Статистика
    completed = [r for r in results if r.score is not None]
    total_labs = len([l for l in labs if not l.get("premium", False)])
    avg_score = round(sum(r.score for r in completed) / len(completed)) if completed else 0
    overall = round((sum(r.score for r in completed) / (total_labs * 100)) * 100) if completed else 0
    
    # Уровень
    if overall >= 81:
        level = "Senior"
    elif overall >= 61:
        level = "Middle"
    elif overall >= 31:
        level = "Junior"
    else:
        level = "Beginner"
    
    # Прогресс по навыкам
    skills = {}
    for lab in labs:
        if lab.get("premium", False):
            continue
        result = next((r for r in results if r.lab_id == lab["id"]), None)
        skills[lab["category"]] = result.score if result else 0
    
    # Данные для дашборда
    lab_data = []
    for lab in labs:
        result = next((r for r in results if r.lab_id == lab["id"]), None)
        lab_data.append({
            **lab,
            "score": result.score if result else None,
            "level": result.level if result else None,
            "completed": result is not None,
            "created_at": result.created_at if result else None
        })
    
    return {
        "labs": lab_data,
        "stats": {
            "overall": overall,
            "completed": len(completed),
            "total": total_labs,
            "avg_score": avg_score,
            "level": level
        },
        "skills": skills,
        "recent": [
            {
                "lab_id": r.lab_id,
                "score": r.score,
                "level": r.level,
                "created_at": r.created_at.isoformat()
            }
            for r in results[:5]
        ]
    }

@app.websocket("/ws/lab")
async def websocket_lab(websocket: WebSocket):
    await websocket.accept()
    
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return
    
    user = await get_current_user_from_token(token)
    if not user:
        await websocket.close(code=1008)
        return
    
    # Получаем lab_id из query-параметра
    lab_id = int(websocket.query_params.get("lab_id", 1))
    container_name = f"lab_{lab_id}_user_{user.id}"
    
    # Загружаем конфиг лаборатории
    labs = load_labs()
    lab_config = next((l for l in labs if l["id"] == lab_id), None)
    
    # Определяем образ из конфига
    image_name = lab_config.get("docker", {}).get("image", "hacklab/lab:latest") if lab_config else "hacklab/lab:latest"
    
    # Создаём Docker-контейнер
    try:
        container = docker_client.containers.run(
            image_name,
            command="tail -f /dev/null",
            detach=True,
            name=container_name,
            remove=False,
            mem_limit="512m",
            cpu_period=100000,
            cpu_quota=50000,
            working_dir="/home/student"
        )
        containers[container_name] = container
        
        # Создаём задание для Lab 1 (секретный файл)
        try:
            container.exec_run(
                ["bash", "-c", "echo 'HACKLAB{you_found_the_secret}' > /home/student/secret.txt"],
                user="student"
            )
        except Exception as e:
            print(f"Не удалось создать secret.txt: {e}")
        
        # Создаём задание для Lab 2 (файл с целью)
        if lab_id == 2:
            try:
                container.exec_run(
                    ["bash", "-c", "echo 'TARGET=scanme.nmap.org' > /home/student/target.txt"],
                    user="root"
                )
            except Exception as e:
                print(f"Не удалось создать target.txt: {e}")
                
    except Exception as e:
        await websocket.send_text(json.dumps({
            "type": "error",
            "data": f"❌ Ошибка создания контейнера: {str(e)}"
        }))
        await websocket.close()
        return
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                command = msg.get("command", "")
            except:
                command = data
            
            if command == "__finish__":
                break
            
            # Запрещённые команды
            dangerous = ["rm -rf", "shutdown", "reboot", "mkfs", "dd if=/dev/zero"]
            blocked = False
            for d in dangerous:
                if d in command:
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "data": "❌ Команда запрещена в учебной лаборатории"
                    }))
                    blocked = True
                    break
            if blocked:
                continue
            
            # Запрещаем выход из папки
            if ".." in command or command.startswith("cd /"):
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "data": "❌ Выход из лаборатории запрещён"
                }))
                continue
            
            try:
                # Выполняем команду в Docker-контейнере
                exec_result = container.exec_run(
                    ["bash", "-c", command],
                    user="student",
                    workdir="/home/student"
                )
                output = exec_result.output.decode()
                exit_code = exec_result.exit_code
                
                if not output:
                    output = "✅ Команда выполнена (нет вывода)"
                
                # Логируем
                db_log = SessionLocal()
                log_entry = ActionLog(
                    user_id=user.id,
                    lab_id=lab_id,
                    command=command,
                    output=output[:500],
                    exit_code=exit_code
                )
                db_log.add(log_entry)
                db_log.commit()
                db_log.close()
                
                await websocket.send_text(json.dumps({"type": "output", "data": output}))
            except Exception as e:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "data": f"❌ Ошибка: {str(e)}"
                }))
    except WebSocketDisconnect:
        print("Клиент отключился")
    finally:
        # Удаляем контейнер
        try:
            container.stop()
            container.remove()
            del containers[container_name]
        except:
            pass

@app.post("/api/analyze/{lab_id}")
async def analyze_lab(
    lab_id: int,
    db: Session = Depends(get_db)
):
    current_user = db.query(User).first()
    if not current_user:
        return {"error": "Нет пользователей"}
    
    logs = db.query(ActionLog).filter(
        ActionLog.user_id == current_user.id,
        ActionLog.lab_id == lab_id
    ).order_by(ActionLog.timestamp).all()
    
    if not logs:
        return {"error": "Нет действий для анализа"}
    
    # Проверяем задания
    found_secret = False
    found_target = False
    
    for log in logs:
        # Для Lab 1: secret.txt
        if "secret.txt" in log.command or ("cat" in log.command and "secret.txt" in log.output):
            found_secret = True
        # Для Lab 2: scanme.nmap.org
        if "scanme.nmap.org" in log.command or "nmap" in log.command:
            found_target = True
    
    try:
        from core.analyzer import ThinkingAnalyzer
        analyzer = ThinkingAnalyzer()
        
        # Используем новый анализатор
        result = analyzer.analyze(user_id=current_user.id, lab_id=lab_id)
        
        # Бонусы
        bonus = 0
        if lab_id == 1 and found_secret:
            bonus = 20
        elif lab_id == 2 and found_target:
            bonus = 20
        
        # Получаем оценку из нового анализатора
        base_score = result.get('score', 0)
        final_score = min(base_score + bonus, 100)
        
        # Добавляем информацию о задании в feedback
        feedback = result.get('feedback', [])
        if lab_id == 1:
            if found_secret:
                feedback.append("🎯 Задание выполнено! Ты нашёл secret.txt (+20 баллов)")
            else:
                feedback.append("🔍 Ты не нашёл secret.txt. Попробуй использовать: find / -name secret.txt 2>/dev/null")
        elif lab_id == 2:
            if found_target:
                feedback.append("🎯 Задание выполнено! Ты просканировал цель (+20 баллов)")
            else:
                feedback.append("🔍 Ты не просканировал цель. Попробуй: sudo nmap -sS scanme.nmap.org")
        
        # Сохраняем результат
        db_result = LabResult(
            user_id=current_user.id,
            lab_id=lab_id,
            score=final_score,
            level=result.get('level', 'Beginner'),
            feedback=str(feedback),
            commands_count=len(logs),
            duration=0
        )
        db.add(db_result)
        db.commit()
        
        # Проверяем достижения
        methodology_score = result.get('analyzer_v2', {}).get('methodology', {}).get('score', 0)
        duration = 0  # TODO: рассчитать время
        unlocked = AchievementService.check_achievements(
            user_id=current_user.id,
            lab_id=lab_id,
            score=final_score,
            methodology_score=methodology_score,
            duration=duration
        )
        
        if unlocked:
            print(f"🏆 Новые достижения для пользователя {current_user.id}: {[u['name'] for u in unlocked]}")
        
        # Возвращаем расширенный результат
        return {
            "status": "ok",
            "score": final_score,
            "level": result.get('level', 'Beginner'),
            "feedback": feedback,
            "analyzer_v2": result.get('analyzer_v2', {}),
            "achievements": unlocked
        }
    except Exception as e:
        return {"error": f"Ошибка анализа: {str(e)}"}

@app.get("/api/achievements")
async def get_achievements():
    achievements = AchievementService.get_user_achievements(1)
    return {"achievements": achievements}

@app.get("/api/profile")
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Получаем результаты
    results = db.query(LabResult).filter(
        LabResult.user_id == current_user.id
    ).order_by(LabResult.created_at.desc()).all()
    
    # Получаем достижения
    achievements = AchievementService.get_user_achievements(current_user.id)
    
    # Статистика
    total_labs = len(results)
    avg_score = round(sum(r.score for r in results) / total_labs) if total_labs > 0 else 0
    best_score = max([r.score for r in results]) if total_labs > 0 else 0
    
    # XP (сумма XP из достижений)
    total_xp = sum(a['xp_reward'] for a in achievements) if achievements else 0
    
    # Уровень
    if total_xp >= 2000:
        level = "Senior Pentester"
    elif total_xp >= 1000:
        level = "Middle Pentester"
    elif total_xp >= 500:
        level = "Junior Pentester"
    else:
        level = "Beginner"
    
    # Навыки (из результатов лабораторий)
    skills = {
        "linux": 0,
        "network": 0,
        "web": 0,
        "recon": 0,
        "enumeration": 0,
        "analysis": 0,
        "pentesting": 0
    }
    
    # Заполняем навыки из результатов
    for r in results:
        if r.lab_id == 1:
            skills["linux"] = r.score
            skills["recon"] = r.score
            skills["enumeration"] = r.score // 2
        elif r.lab_id == 2:
            skills["network"] = r.score
            skills["enumeration"] = r.score
            skills["recon"] = r.score // 2
        elif r.lab_id == 3:
            skills["web"] = r.score
            skills["pentesting"] = r.score
        
        # Парсим analyzer_v2 если есть
        try:
            if r.feedback and "analyzer_v2" in r.feedback:
                import json
                # Пытаемся извлечь данные из feedback
                pass
        except:
            pass
    
    # График прогресса
    progress = [
        {
            "lab_id": r.lab_id,
            "score": r.score,
            "created_at": r.created_at.isoformat()
        }
        for r in results[:10]
    ]
    
    return {
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "created_at": current_user.created_at.isoformat()
        },
        "stats": {
            "total_labs": total_labs,
            "avg_score": avg_score,
            "best_score": best_score,
            "total_xp": total_xp,
            "level": level
        },
        "skills": skills,
        "achievements": achievements,
        "progress": progress
    }
