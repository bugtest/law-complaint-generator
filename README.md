# 要素式起诉状生成系统

AI 驱动的法律文书生成系统，帮助律师快速生成符合国家标准的要素式起诉状。

## 功能特性

- 支持 PDF 证据文件和 Word 整理文档上传
- 自动解析文档并提取文本
- OCR 识别扫描件 PDF（需安装 PaddleOCR）
- AI 自动提取案件要素（当事人信息、诉讼请求、事实理由、证据清单）
- 模板化管理起诉状格式
- 一键生成符合国标的起诉状

## 快速开始

### 后端启动

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# 编辑.env 配置 QWEN_API_KEY 等
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 API 文档：http://localhost:8000/docs

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173

## 配置说明

编辑 `backend/.env`:

```bash
# JWT 配置
JWT_SECRET_KEY=your-secret-key
JWT_EXPIRE_HOURS=24

# 文件存储
FILE_STORAGE_PATH=./docs/storage
MAX_FILE_SIZE_MB=50

# AI 配置
QWEN_API_KEY=sk-...  # 在 DashScope 控制台获取
AI_MODEL=qwen3.5-plus

# OCR 配置
OCR_ENABLED=true
OCR_LANGUAGE=ch
```

## API 接口

### 认证
- POST /api/auth/register - 用户注册
- POST /api/auth/login - 用户登录
- POST /api/auth/logout - 用户登出
- GET /api/auth/me - 获取当前用户信息

### 案件管理
- GET /api/cases - 获取案件列表
- POST /api/cases - 创建新案件
- GET /api/cases/{id} - 获取案件详情
- PUT /api/cases/{id} - 更新案件信息
- DELETE /api/cases/{id} - 删除案件

### 文档管理
- POST /api/cases/{id}/documents - 上传文档
- GET /api/cases/{id}/documents - 获取文档列表
- POST /api/cases/{id}/parse - 解析文档
- GET /api/cases/{id}/elements - 获取提取的要素
- PUT /api/cases/{id}/elements - 更新要素

### 模板管理
- GET /api/templates - 获取模板列表
- POST /api/templates - 上传模板
- PUT /api/templates/{id}/default - 设为默认模板
- DELETE /api/templates/{id} - 删除模板

### 文书生成
- POST /api/cases/{id}/generate - 生成起诉状
- GET /api/cases/{id}/documents/{docId}/download - 下载文书

## 测试

```bash
cd backend
pytest tests/ -v
```

## 技术栈

**后端：**
- FastAPI - Web 框架
- SQLAlchemy - ORM
- JWT + bcrypt - 用户认证
- pdfplumber, PyMuPDF - PDF 解析
- python-docx - Word 处理
- 通义千问 Qwen API - AI 要素提取

**前端：**
- Vue 3 - 前端框架
- Element Plus - UI 组件库
- Pinia - 状态管理
- Vue Router - 路由管理
- Axios - HTTP 客户端

**数据库：**
- SQLite (默认) / PostgreSQL (可配置)

## 项目结构

```
/root/code/law/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   ├── services/
│   │   └── utils/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   ├── router/
│   │   ├── stores/
│   │   └── api/
│   └── package.json
└── docs/storage/
    ├── uploads/
    ├── templates/
    └── generated/
```

## 使用流程

1. 注册/登录账户
2. 创建新案件
3. 上传 PDF 证据文件和 Word 整理文档
4. 点击"解析文档"提取文本
5. 点击"审核要素"检查和编辑 AI 提取的信息
6. 点击"生成起诉状"生成文书
7. 下载生成的 Word 文档

## 注意事项

- 首次使用需要上传 Word 起诉状模板
- AI 要素提取需要配置 Qwen API Key（在 https://dashscope.console.aliyun.com/ 获取）
- OCR 功能可选，如需使用请安装：pip install paddlepaddle paddleocr
- 敏感数据请妥善保管，建议本地部署
