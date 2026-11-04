from pydantic import BaseModel, HttpUrl
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class CrawlRequest(BaseModel):
    target_url: HttpUrl

class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus
    data: Optional[dict] = None