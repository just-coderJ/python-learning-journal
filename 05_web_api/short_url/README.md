# 🔗 极简短链接生成器 (Short URL Generator)

> 基于 FastAPI + SQLAlchemy + SQLite 构建的轻量级短链接生成与跳转服务。

## 📖 项目简介

这是我的第一个 Python Web 后端实战项目。作为拥有 Java / Spring Boot 背景的开发者，本项目旨在通过最小可行的方式（MVP），快速体验 Python 生态下的 Web 开发流程。

项目实现了长链接到短链接的转换、数据持久化存储以及 HTTP 307 重定向功能。麻雀虽小，五脏俱全，涵盖了路由设计、数据校验、ORM 映射与数据库操作等后端核心概念。

## 🛠️ 技术栈

*   **Web 框架**：FastAPI (高性能、原生异步支持、自动生成 API 文档)
*   **ORM 框架**：SQLAlchemy (Python 生态最主流的 ORM)
*   **数据校验**：Pydantic (强类型校验，类似 Java 的 DTO 与 @Valid)
*   **数据库**：SQLite (轻量级嵌入式数据库，无需额外安装)
*   **服务器**：Uvicorn (ASGI 服务器)

## ✨ 核心功能

- [x] **生成短链接**：接收合法的长网址，通过 MD5 哈希算法截取前 6 位生成短码，并存入数据库。
- [x] **短链跳转**：访问短链接时，查询数据库并使用 HTTP 307 状态码重定向至原网址。
- [x] **自动 API 文档**：得益于 FastAPI，无需额外配置即可访问 Swagger UI 进行接口测试。
- [x] **数据持久化**：使用 SQLite 将长链接与短码的映射关系持久化到本地文件。

## 📂 项目结构

```text
short_url/
├── main.py          # 核心业务逻辑：定义路由、处理生成与重定向请求
├── models.py        # 数据库模型：定义 SQLAlchemy 的表结构 (URLItem)
├── schemas.py       # 数据校验模型：定义 Pydantic 的请求/响应结构
├── database.py      # 数据库连接：配置 Engine 和 SessionLocal
└── short_url.db     # SQLite 数据库文件（运行后自动生成）