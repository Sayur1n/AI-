import os
import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import uuid
from PIL import Image
import io

from .config import Config
from .database import get_db, init_db
from .models import Task
from .upload_service import UploadService
from .ai_service import AIService

# 创建FastAPI应用
app = FastAPI(title="AI模特试衣系统", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建上传目录
os.makedirs(Config.UPLOAD_DIR, exist_ok=True)

# 挂载静态文件
app.mount("/uploads", StaticFiles(directory=Config.UPLOAD_DIR), name="uploads")

# 初始化服务
upload_service = UploadService()
ai_service = AIService()

def validate_image(file: UploadFile) -> bool:
    """验证图片文件"""
    # 检查文件扩展名
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in Config.ALLOWED_EXTENSIONS:
        return False
    
    # 检查文件大小
    if file.size > Config.MAX_FILE_SIZE:
        return False
    
    return True

def save_upload_file(file: UploadFile) -> str:
    """保存上传的文件"""
    # 生成唯一文件名
    file_ext = Path(file.filename).suffix.lower()
    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    file_path = os.path.join(Config.UPLOAD_DIR, unique_filename)
    
    # 保存文件
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return file_path

async def process_ai_task(task_id: str, db: Session):
    """后台处理AI任务"""
    try:
        # 获取任务信息
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return
        
        # 更新状态为运行中
        task.status = "RUNNING"
        db.commit()
        
        # 等待AI任务完成
        result = ai_service.wait_for_completion(task.task_id)
        
        # 更新结果
        task.status = "SUCCEEDED"
        task.result_image_url = result["output"]["image_url"]
        db.commit()
        
    except Exception as e:
        # 更新错误状态
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            task.status = "FAILED"
            task.error_message = str(e)
            db.commit()

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库"""
    init_db()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """返回前端页面"""
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/api/upload")
async def upload_images(
    person_image: UploadFile = File(...),
    top_garment: Optional[UploadFile] = File(None),
    bottom_garment: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """上传图片并提交AI任务"""
    try:
        # 验证人像图片
        if not validate_image(person_image):
            raise HTTPException(status_code=400, detail="人像图片格式或大小不符合要求")
        
        # 验证至少有一个服装图片
        if not top_garment and not bottom_garment:
            raise HTTPException(status_code=400, detail="至少需要提供上装或下装图片中的一个")
        
        # 验证服装图片
        if top_garment and not validate_image(top_garment):
            raise HTTPException(status_code=400, detail="上装图片格式或大小不符合要求")
        if bottom_garment and not validate_image(bottom_garment):
            raise HTTPException(status_code=400, detail="下装图片格式或大小不符合要求")
        
        # 保存文件到本地
        person_path = save_upload_file(person_image)
        top_path = save_upload_file(top_garment) if top_garment else None
        bottom_path = save_upload_file(bottom_garment) if bottom_garment else None
        
        # 上传到阿里云临时存储
        person_url = upload_service.upload_file_and_get_url(person_path)
        top_url = upload_service.upload_file_and_get_url(top_path) if top_path else None
        bottom_url = upload_service.upload_file_and_get_url(bottom_path) if bottom_path else None
        
        # 提交AI任务
        cloud_task_id = ai_service.submit_task(person_url, top_url, bottom_url)
        
        # 保存任务到数据库
        task = Task(
            task_id=cloud_task_id,
            person_image_url=person_url,
            top_garment_url=top_url,
            bottom_garment_url=bottom_url,
            status="PENDING"
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        return {
            "success": True,
            "task_id": task.id,
            "message": "任务提交成功，正在处理中..."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")

@app.get("/api/tasks")
async def get_tasks(db: Session = Depends(get_db)):
    """获取所有任务列表"""
    tasks = db.query(Task).order_by(Task.created_at.desc()).all()
    return {"tasks": [task.to_dict() for task in tasks]}

@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str, db: Session = Depends(get_db)):
    """获取单个任务详情"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    return task.to_dict()

@app.post("/api/tasks/{task_id}/refresh")
async def refresh_task(task_id: str, db: Session = Depends(get_db)):
    """刷新任务状态"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    try:
        # 查询阿里云任务状态
        result = ai_service.get_task_status(task.task_id)
        status = result["output"]["task_status"]
        
        # 更新本地状态
        task.status = status
        if status == "SUCCEEDED":
            task.result_image_url = result["output"]["image_url"]
        elif status == "FAILED":
            task.error_message = result.get("output", {}).get("message", "Unknown error")
        
        db.commit()
        
        return task.to_dict()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"刷新失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT) 