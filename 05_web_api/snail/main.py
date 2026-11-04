from http.client import HTTPException

import uuid
import httpx
from fastapi import FastAPI
from starlette.background import BackgroundTasks

import schemas

app = FastAPI(title="Async Crawler API")

# 模拟本地任务存储

tasks_db = {}

async def fetch_url_content(task_id: str, url: str):
    # 后台异步爬取任务
    tasks_db[task_id]["status"] = schemas.TaskStatus.RUNNING
    try:
        # 使用httpx进行异步HTTP请求,避免阻塞主进程
        async with httpx.AsyncClient(timeout = 10.0) as client:
            response = await client.get(url)
            response.raise_for_status()

        tasks_db[task_id]["data"] = {
            "status_code": response.status_code,
            "content_length": len(response.text)
        }
        tasks_db[task_id]["status"] = schemas.TaskStatus.COMPLETED

    except Exception as e:
        tasks_db[task_id]["status"] = schemas.TaskStatus.FAILED
        tasks_db[task_id]["error"] = str(e)


@app.post("/api/crawl", response_model=schemas.TaskResponse)
async def submit_crawl_task(request: schemas.CrawlRequest, background_tasks: BackgroundTasks):
    """接口1： 提交爬虫任务，立即返回Task ID"""
    task_id = str(uuid.uuid4())
    tasks_db[task_id] = { "status": schemas.TaskStatus.PENDING, "data": None }

    # 将抓取逻辑放入后台任务队列
    background_tasks.add_task(fetch_url_content, task_id, str(request.target_url))

    return { "task_id": task_id, "status": tasks_db[task_id]["status"] }


@app.get("/api/crawl/{task_id}", response_model=schemas.TaskResponse)
async def get_crawl_status(task_id: str):
    """接口 2：前端通过 Task ID 轮询查询进度与结果"""
    if task_id not in tasks_db:
        raise HTTPException(status_codes=404, detail="任务不存在")
    return { "task_id": task_id, **tasks_db[task_id] }