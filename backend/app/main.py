from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import BASE_DIR
from .database import engine, Base
from .routers import auth_router, cases_router, documents_router, templates_router, generate_router

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="要素式起诉状生成系统",
    description="律师专用 - AI 驱动的法律文书生成系统",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router)
app.include_router(cases_router)
app.include_router(documents_router)
app.include_router(templates_router)
app.include_router(generate_router)

@app.get("/")
def root():
    return {"message": "要素式起诉状生成系统 API", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}
