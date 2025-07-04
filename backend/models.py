from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String, unique=True, nullable=False)  # 阿里云返回的task_id
    person_image_url = Column(String, nullable=False)
    top_garment_url = Column(String, nullable=True)
    bottom_garment_url = Column(String, nullable=True)
    status = Column(String, default="PENDING")  # PENDING, RUNNING, SUCCEEDED, FAILED
    result_image_url = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "person_image_url": self.person_image_url,
            "top_garment_url": self.top_garment_url,
            "bottom_garment_url": self.bottom_garment_url,
            "status": self.status,
            "result_image_url": self.result_image_url,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        } 