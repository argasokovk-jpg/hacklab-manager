from fastapi import FastAPI, Request, Form, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json
import os
import docker

from web.database import engine, get_db, Base, SessionLocal
from web.models import User, ActionLog, LabResult
from web.auth import get_password_hash, authenticate_user, create_access_token, get_current_user, get_current_user_from_token

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# Docker client
docker_client = docker.from_env()

# Хранилище контейнеров
containers = {}

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
    
    # Список лабораторий
    labs = [
        {"id": 1, "name": "Linux Fundamentals", "status": "available"},
        {"id": 2, "name": "Network Reconnaissance", "status": "available"},
        {"id": 3, "name": "Full Penetration Test", "status": "premium"}
    ]
    
    # Обогащаем лаборатории данными из результатов
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
    
    # Статистика
    completed = [r for r in results if r.score is not None]
    total_labs = len([l for l in labs if l["status"] != "premium"])
    avg_score = round(sum(r.score for r in completed) / len(completed)) if completed else 0
    overall = round((sum(r.score for r in completed) / (total_labs * 100)) * 100) if completed else 0
    
    return {
        "labs": lab_data,
        "stats": {
            "overall": overall,
            "completed": len(completed),
            "total": total_labs,
            "avg_score": avg_score
        },
        "recent": [
            {
                "lab_id": r.lab_id,
                "score": r.score,
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
    
    lab_id = 1
    container_name = f"lab_{lab_id}_user_{user.id}"
    
    # Создаём Docker-контейнер
    try:
        container = docker_client.containers.run(
            "hacklab/lab:latest",
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
        
        # Создаём задание: файл secret.txt
        try:
            container.exec_run(
                ["bash", "-c", "echo 'HACKLAB{you_found_the_secret}' > /home/student/secret.txt"],
                user="student"
            )
        except Exception as e:
            print(f"Не удалось создать secret.txt: {e}")
            
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
    
    # Проверяем, нашёл ли пользователь secret.txt
    found_secret = False
    for log in logs:
        if "secret.txt" in log.command or ("cat" in log.command and "secret.txt" in log.output):
            found_secret = True
            break
    
    try:
        from core.analyzer import ThinkingAnalyzer
        analyzer = ThinkingAnalyzer()
        result = analyzer.analyze(user_id=current_user.id, lab_id=lab_id)
        
        # Бонус за найденный файл
        bonus = 20 if found_secret else 0
        final_score = min(result.get("score", 0) + bonus, 100)
        
        # Добавляем информацию о задании в feedback
        feedback = result.get("feedback", [])
        if found_secret:
            feedback.append("🎯 Задание выполнено! Ты нашёл secret.txt (+20 баллов)")
        else:
            feedback.append("🔍 Ты не нашёл secret.txt. Попробуй использовать: find / -name secret.txt 2>/dev/null")
        
        # Сохраняем результат
        db_result = LabResult(
            user_id=current_user.id,
            lab_id=lab_id,
            score=final_score,
            level=result.get("level", "Beginner"),
            feedback=str(feedback),
            commands_count=len(logs),
            duration=0
        )
        db.add(db_result)
        db.commit()
        
        return {
            "status": "ok",
            "score": final_score,
            "level": result.get("level", "Beginner"),
            "feedback": feedback
        }
    except Exception as e:
        return {"error": f"Ошибка анализа: {str(e)}"}
