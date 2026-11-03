from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# 连接sqllite数据库
SQLALCHEMY_DATABASE_URL = "sqlite:///./short_url.db"

# check_same_thread 是为了允许 FastAPI 的多个请求共享这个连接
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
