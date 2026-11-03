import hashlib

from fastapi import FastAPI,Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

import schemas
from database import engine, SessionLocal

import models

# 自动在数据库建表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="极简短链接生成器")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1.生成短链接接口
@app.post("/shorten", response_model=schemas.URLResponse)
def create_short_url(item: schemas.URLCreate, db: Session = Depends(get_db)):
    long_url_str = str(item.long_url)

    # 核心算法： 把长链接做成 MD5 哈希， 取前6位
    short_code = hashlib.md5(long_url_str.encode()).hexdigest()[:6]

    # 查数据库有没有
    existing_url = db.query(models.URLItem).filter(models.URLItem.short_code == short_code).first()
    if not existing_url:
        new_url = models.URLItem(long_url=long_url_str, short_code = short_code)
        db.add(new_url)
        db.commit()
        db.refresh(new_url)

    return { "short_url": f"http://127.0.0.1:8000/{short_code}" }


# 2.重定向接口
@app.get("/{short_code}")
def redirect_to_long_url(short_code: str, db: Session = Depends(get_db)):
    url_item = db.query(models.URLItem).filter(models.URLItem.short_code == short_code).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="短链接不存在")
    # 返回重定向（临时重定向）
    return RedirectResponse(url = url_item.long_url, status_code = 307)