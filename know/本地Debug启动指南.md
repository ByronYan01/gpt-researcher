# GPT-Researcher 本地 Debug 启动指南

**文档版本：** 1.0
**更新日期：** 2026-02-27
**适用版本：** GPT-Researcher 0.14.6+

---

## 目录

1. [环境准备](#一环境准备)
2. [配置说明](#二配置说明)
3. [启动方式](#三启动方式)
4. [Debug 技巧](#四debug-技巧)
5. [常见问题排查](#五常见问题排查)
6. [API 测试](#六api-测试)
7. [附录](#七附录)

---

## 一、环境准备

### 1.1 系统要求

| 要求项   | 最低版本            | 推荐版本 |
| -------- | ------------------- | -------- |
| Python   | 3.11+               | 3.12     |
| 操作系统 | Windows/macOS/Linux | -        |
| 内存     | 4GB                 | 8GB+     |
| 磁盘空间 | 2GB                 | 5GB+     |

### 1.2 依赖安装

#### 方法一：使用 pyenv + uv（推荐）

```bash
# 1. 使用 pyenv 安装并设置 Python 版本
pyenv install 3.11
pyenv local 3.11    # 项目已有 .python-version 文件，此步可跳过

# 2. 同步依赖
uv sync

# 3. 如果需要额外安装某个库
uv add <package_name>
# 或
uv pip install <package_name>
```

#### 方法二：使用 requirements.txt

```bash
# 安装核心依赖
pip install -r requirements.txt

# 如果需要多智能体功能
pip install -r multi_agents/requirements.txt
```

#### 方法三：使用 Poetry

```bash
pip install poetry
poetry install
poetry shell
```

### 1.3 验证安装

```bash
# 检查 Python 版本
pyenv version         # 应显示 3.11.x
python --version      # 应该 >= 3.11

# 检查依赖安装
uv pip list | grep -E "(fastapi|langchain|openai)"

# 运行测试
uv run python -m pytest tests/ -v
```

---

## 二、配置说明

### 2.1 环境变量配置

#### 创建 `.env` 文件

在项目根目录创建 `.env` 文件：

```bash
# 复制示例配置
cp .env.example .env

# 编辑配置
nano .env  # 或使用你喜欢的编辑器
```

#### 必需配置

```bash
# .env 文件内容

# ============================================
# 必需的 API Key
# ============================================

# OpenAI API Key (用于 GPT 模型)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Tavily API Key (用于网络搜索)
# 获取地址: https://tavily.com/home
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ============================================
# 可选配置
# ============================================

# 自定义 OpenAI API 地址 (用于代理或兼容服务)
# OPENAI_BASE_URL=https://api.openai.com/v1

# 文档路径 (用于本地文档研究)
DOC_PATH=./my-docs

# ============================================
# 抓取器配置
# ============================================

# 最大并发抓取工作线程数
# Firecrawl Free: 2
# Firecrawl Hobby: 5
# BeautifulSoup: 根据目标网站限制设置
MAX_SCRAPER_WORKERS=15

# 抓取速率限制（秒）
# 60 / 每分钟请求数
# Firecrawl Free (10 req/min): 6.0
# 无限制: 0
SCRAPER_RATE_LIMIT_DELAY=0.0

# ============================================
# LangChain 追踪 (可选)
# ============================================

# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
# LANGCHAIN_API_KEY=your_langchain_api_key
# LANGCHAIN_PROJECT="gpt-researcher"

# ============================================
# 图像生成 (可选)
# ============================================

# IMAGE_GENERATION_ENABLED=true
# GOOGLE_API_KEY=your_google_api_key
# IMAGE_GENERATION_MODEL=gemini-2.0-flash-preview-image-generation
# IMAGE_GENERATION_MAX_IMAGES=3

# ============================================
# 深度研究配置
# ============================================

# 深度研究每层并行查询数
DEEP_RESEARCH_BREADTH=4

# 深度研究递归深度
DEEP_RESEARCH_DEPTH=2

# 深度研究并发限制
DEEP_RESEARCH_CONCURRENCY=2

# ============================================
# LLM 配置
# ============================================

# 智能模型 (用于复杂推理)
SMART_LLM_MODEL=gpt-4o-mini

# 战略模型 (用于规划)
STRATEGIC_LLM_MODEL=o3-mini

# 推理强度 (low/medium/high)
REASONING_EFFORT=high

# ============================================
# 检索器配置
# ============================================

# 可用检索器: tavily, duckduckgo, mcp, exa
# 多个检索器用逗号分隔
RETRIEVER=tavily

# MCP 执行策略 (fast/deep/disabled)
MCP_STRATEGY=fast
```

### 2.2 配置文件位置

| 文件                     | 位置       | 优先级 |
| ------------------------ | ---------- | ------ |
| 系统环境变量             | 系统环境   | 高     |
| `.env`                   | 项目根目录 | 中     |
| `gpt_researcher/config/` | 配置默认值 | 低     |

### 2.3 API Key 获取指南

| 服务      | 获取地址                                 | 免费额度        |
| --------- | ---------------------------------------- | --------------- |
| OpenAI    | https://platform.openai.com/api-keys     | $5 免费额度     |
| Tavily    | https://tavily.com/home                  | 1,000 次/月免费 |
| Google AI | https://makersuite.google.com/app/apikey | 有免费层级      |

---

## 三、启动方式

### 3.1 方式一：VS Code Debug（推荐）

#### 3.1.1 创建 `.vscode/launch.json`

在项目根目录创建 `.vscode/launch.json`：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "GPT-Researcher: 主服务",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
      "cwd": "${workspaceFolder}",
      "envFile": "${workspaceFolder}/.env",
      "console": "integratedTerminal",
      "justMyCode": false
    },
    {
      "name": "GPT-Researcher: Backend服务",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "server.app:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
        "--reload"
      ],
      "cwd": "${workspaceFolder}/backend",
      "envFile": "${workspaceFolder}/.env",
      "console": "integratedTerminal",
      "justMyCode": false
    },
    {
      "name": "GPT-Researcher: CLI模式",
      "type": "debugpy",
      "request": "launch",
      "module": "cli",
      "args": ["为什么英伟达股票在上涨？", "--report_type", "deep"],
      "cwd": "${workspaceFolder}",
      "envFile": "${workspaceFolder}/.env",
      "console": "integratedTerminal",
      "justMyCode": false
    }
  ]
}
```

#### 3.1.2 创建 `.vscode/settings.json`

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  }
}
```

#### 3.1.3 启动 Debug

1. 在 VS Code 中打开项目
2. 按 `F5` 或点击 "Run and Debug"
3. 选择启动配置：
   - `GPT-Researcher: 主服务` - 启动主服务
   - `GPT-Researcher: Backend服务` - 启动后端服务
   - `GPT-Researcher: CLI模式` - 运行 CLI 模式

#### 3.1.4 设置断点

```python
# 在 agent.py 中设置断点
# gpt_researcher/agent.py:328
async def conduct_research(self, on_progress=None):
    # 在这里设置断点
    breakpoint()  # 或使用 IDE 断点
    ...
```

### 3.2 方式二：PyCharm Debug

#### 3.2.1 创建 Run Configuration

1. 打开 `Run` → `Edit Configurations...`
2. 点击 `+` 添加新的 Python 配置：

```yaml
名称: GPT-Researcher Server
类型: Python
Module name: uvicorn
参数: main:app --host 0.0.0.0 --port 8000 --reload
工作目录: $ProjectFileDir$
环境变量:
  - PYTHONUNBUFFERED=1
  - 从 .env 文件加载
路径映射:
  - Local path: $ProjectFileDir$
  - Remote path: /app
```

#### 3.2.2 启动 Debug

1. 点击右上角的 Debug 图标 🐛
2. 或按 `Shift + F9`

### 3.3 方式三：命令行启动

#### 3.3.1 启动主服务

```bash
# 基础启动
uv run python -m uvicorn main:app --reload

# 指定 host 和 port
uv run python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 详细日志
uv run python -m uvicorn main:app --reload --log-level debug

# 多 worker（生产环境）
uv run python -m uvicorn main:app --workers 4
```

#### 3.3.2 启动 Backend 服务

```bash
# 方式 1: 使用 run_server.py
cd backend
uv run python run_server.py

# 方式 2: 直接使用 uvicorn
cd backend
uv run python -m uvicorn server.app:app --host 0.0.0.0 --port 8000 --reload
```

#### 3.3.3 CLI 模式运行

```bash
# 基础用法
uv run python cli.py "为什么英伟达股票在上涨？" --report_type research_report

# 深度研究
uv run python cli.py "深度分析量子计算的发展" --report_type deep

# 指定语气和来源
uv run python cli.py "AI的未来发展趋势" \
    --report_type detailed_report \
    --tone objective \
    --report_source web

# 限制搜索域名
uv run python cli.py "最新的AI模型比较" \
    --report_type research_report \
    --query_domains openai.com,anthropic.com

# 跳过 PDF/DOCX 生成
uv run python cli.py "研究主题" \
    --report_type research_report \
    --no-pdf \
    --no-docx
```

### 3.4 方式四：Docker 启动

#### 3.4.1 使用 docker-compose

```bash
# 启动所有服务
docker-compose up --build

# 仅启动后端
docker-compose up gpt-researcher

# 后台运行
docker-compose up -d

# 查看日志
docker-compose logs -f gpt-researcher

# 停止服务
docker-compose down
```

#### 3.4.2 Docker Debug 模式

```bash
# 交互式进入容器
docker-compose run gpt-researcher /bin/bash

# 在容器中启动 Python debug
python -m debugpy --listen 0.0.0.0:5678 \
    -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3.5 启动验证

```bash
# 检查服务状态
curl http://localhost:8000/

# 检查 API 文档
open http://localhost:8000/docs

# 测试研究接口
curl -X POST http://localhost:8000/report/ \
    -H "Content-Type: application/json" \
    -d '{
        "task": "什么是人工智能？",
        "report_type": "research_report",
        "report_source": "web",
        "tone": "Objective",
        "headers": {},
        "repo_name": "",
        "branch_name": ""
    }'
```

---

## 四、Debug 技巧

### 4.1 VS Code Debug 技巧

#### 4.1.1 条件断点

```python
# gpt_researcher/skills/deep_research.py:232

# 右键点击断点 → "Edit Breakpoint" → 设置条件
# 条件: depth == 2
async def process_query(serp_query: Dict[str, str]) -> Optional[Dict[str, Any]]:
    async with semaphore:
        # 这里的断点仅在 depth == 2 时触发
        ...
```

#### 4.1.2 日志断点

```python
# 不需要停止执行，只输出日志
# 右键断点 → "Edit Breakpoint" → "Log Message"
# 输入: "Processing query: {serp_query['query']}"
```

#### 4.1.3 异常断点

```json
// .vscode/launch.json
{
  "name": "GPT-Researcher: 异常捕获",
  "type": "debugpy",
  "request": "launch",
  "module": "uvicorn",
  "args": ["main:app", "--reload"],
  "exception": {
    "raised": ["Exceptions"],
    "uncaught": ["Exceptions"]
  }
}
```

### 4.2 日志 Debug

#### 4.2.1 启用详细日志

```python
# 在代码中添加
import logging

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 添加调试日志
logger.debug(f"Current query: {query}")
logger.info(f"Research started: {task}")
logger.warning(f"Rate limit approaching: {count}")
logger.error(f"Research failed: {error}")
```

#### 4.2.2 结构化日志

```python
import logging
import json

class StructuredLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)

    def log_event(self, event_type, **kwargs):
        log_data = {
            "event": event_type,
            "timestamp": datetime.now().isoformat(),
            **kwargs
        }
        self.logger.info(json.dumps(log_data))

# 使用
logger = StructuredLogger(__name__)
logger.log_event("research_started", query="AI趋势", depth=2)
```

### 4.3 性能分析

#### 4.3.1 使用 cProfile

```bash
# 运行性能分析
uv run python -m cProfile -o profile.stats \
    -m uvicorn main:app --reload

# 查看结果
uv run python -m pstats profile.stats
>> sort cumulative
>> stats 20
```

#### 4.3.2 使用 py-spy

```bash
# 安装 py-spy
uv pip install py-spy

# 监控运行中的进程
py-spy top --pid $(pgrep -f "uvicorn main:app")

# 生成火焰图
py-spy record -o profile.svg --pid $(pgrep -f "uvicorn main:app")
```

### 4.4 内存分析

```bash
# 安装 memory_profiler
uv pip install memory_profiler

# 分析代码
uv run python -m memory_profiler cli.py "测试查询" --report_type research_report
```

### 4.5 网络请求调试

#### 4.5.1 使用 HTTPie

```bash
# 安装 HTTPie
uv pip install httpie

# 测试 API
http POST localhost:8000/report/ \
    task="什么是AI？" \
    report_type="research_report" \
    report_source="web" \
    tone="Objective"
```

#### 4.5.2 使用 curl

```bash
# 带详细输出的请求
curl -v -X POST http://localhost:8000/report/ \
    -H "Content-Type: application/json" \
    -d '{
        "task": "什么是人工智能？",
        "report_type": "research_report",
        "report_source": "web",
        "tone": "Objective"
    }'
```

---

## 五、常见问题排查

### 5.1 启动问题

| 问题                                             | 可能原因       | 解决方案                          |
| ------------------------------------------------ | -------------- | --------------------------------- |
| `ModuleNotFoundError: No module named 'fastapi'` | 依赖未安装     | `pip install -r requirements.txt` |
| `KeyError: OPENAI_API_KEY`                       | 环境变量未设置 | 检查 `.env` 文件                  |
| `Address already in use`                         | 端口被占用     | `lsof -ti:8000 \| xargs kill`     |
| `Permission denied`                              | 端口需要权限   | 使用 8000 以上端口                |

### 5.2 API 调用问题

| 问题                  | 可能原因         | 解决方案                        |
| --------------------- | ---------------- | ------------------------------- |
| `Invalid API key`     | API Key 错误     | 检查 `.env` 中的配置            |
| `Rate limit exceeded` | API 调用过于频繁 | 增加 `SCRAPER_RATE_LIMIT_DELAY` |
| `Connection timeout`  | 网络问题         | 检查代理设置或网络连接          |

### 5.3 调试检查清单

```bash
# 1. 检查 Python 版本
pyenv version         # 应显示 3.11.x
python --version      # 应该 >= 3.11

# 2. 检查依赖安装
uv pip list | grep fastapi
uv pip list | grep langchain

# 3. 检查环境变量
echo $OPENAI_API_KEY
echo $TAVILY_API_KEY

# 4. 检查端口占用
lsof -i:8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# 5. 检查日志
tail -f logs/app.log

# 6. 测试 API 连接
curl https://api.openai.com/v1/models \
    -H "Authorization: Bearer $OPENAI_API_KEY"
```

### 5.4 日志文件位置

| 日志类型     | 位置           |
| ------------ | -------------- |
| 应用日志     | `logs/app.log` |
| 研究输出     | `outputs/`     |
| Uvicorn 日志 | 控制台输出     |

---

## 六、API 测试

### 6.1 使用 Swagger UI

访问 `http://localhost:8000/docs` 进行交互式测试。

### 6.2 使用 WebSocket

```python
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws"

    async with websockets.connect(uri) as websocket:
        # 发送研究请求
        request = {
            "task": "什么是人工智能？",
            "report_type": "research_report",
            "report_source": "web",
            "tone": "Objective"
        }
        await websocket.send(json.dumps(request))

        # 接收响应
        while True:
            response = await websocket.recv()
            print(f"Received: {response}")

asyncio.run(test_websocket())
```

### 6.3 使用 Python requests

```python
import requests
import json

url = "http://localhost:8000/report/"
payload = {
    "task": "什么是人工智能？",
    "report_type": "research_report",
    "report_source": "web",
    "tone": "Objective",
    "headers": {},
    "repo_name": "",
    "branch_name": ""
}

response = requests.post(url, json=payload)
print(response.json())
```

---

## 七、附录

### 7.1 目录结构

```
gpt-researcher/
├── .env                    # 环境变量配置
├── .vscode/                # VS Code 配置
│   ├── launch.json         # Debug 配置
│   └── settings.json       # 项目设置
├── logs/                   # 日志目录
│   └── app.log
├── outputs/                # 输出目录
│   ├── *.md               # Markdown 报告
│   ├── *.pdf              # PDF 报告
│   └── *.docx             # Word 报告
├── backend/                # 后端服务
│   ├── server/
│   │   └── app.py         # FastAPI 应用
│   └── run_server.py      # 后端启动脚本
├── frontend/               # 前端文件
│   ├── index.html         # 静态HTML入口
│   ├── scripts.js         # 前端脚本
│   ├── styles.css         # 样式表
│   ├── nextjs/            # Next.js生产版本
│   └── static/            # 静态资源
├── gpt_researcher/         # 核心模块
├── main.py                 # 主入口
└── cli.py                  # CLI 工具
```

### 7.2 常用命令

```bash
# ============================================
# 启动命令
# ============================================

# 主服务
uv run python -m uvicorn main:app --reload

# 后端服务
cd backend && uv run python run_server.py

# CLI 模式
uv run python cli.py "查询问题" --report_type research_report

# ============================================
# 调试命令
# ============================================

# Python debug
uv run python -m debugpy --listen 5678 --wait-for-client \
    -m uvicorn main:app --reload

# 性能分析
uv run python -m cProfile -o profile.stats \
    -m uvicorn main:app --reload

# ============================================
# Docker 命令
# ============================================

# 构建并启动
docker-compose up --build

# 后台运行
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 7.3 环境变量速查表

| 变量名                      | 默认值        | 说明                         |
| --------------------------- | ------------- | ---------------------------- |
| `OPENAI_API_KEY`            | -             | OpenAI API 密钥（必需）      |
| `TAVILY_API_KEY`            | -             | Tavily 搜索 API 密钥（必需） |
| `DOC_PATH`                  | `./my-docs`   | 本地文档路径                 |
| `OPENAI_BASE_URL`           | -             | 自定义 API 地址              |
| `SMART_LLM_MODEL`           | `gpt-4o-mini` | 智能模型                     |
| `STRATEGIC_LLM_MODEL`       | `o3-mini`     | 战略模型                     |
| `RETRIEVER`                 | `tavily`      | 检索器类型                   |
| `DEEP_RESEARCH_BREADTH`     | `4`           | 深度研究宽度                 |
| `DEEP_RESEARCH_DEPTH`       | `2`           | 深度研究深度                 |
| `DEEP_RESEARCH_CONCURRENCY` | `2`           | 并发限制                     |
| `MAX_SCRAPER_WORKERS`       | `15`          | 最大抓取并发                 |
| `SCRAPER_RATE_LIMIT_DELAY`  | `0.0`         | 抓取速率限制                 |
| `MCP_STRATEGY`              | `fast`        | MCP 执行策略                 |

### 7.4 报告类型速查表

| 报告类型   | 值                | 耗时   | 说明         |
| ---------- | ----------------- | ------ | ------------ |
| 标准报告   | `research_report` | ~2分钟 | 快速总结     |
| 详细报告   | `detailed_report` | ~5分钟 | 深入分析     |
| 深度研究   | `deep`            | ~5分钟 | 树状递归探索 |
| 资源报告   | `resource_report` | -      | 资源列表     |
| 大纲报告   | `outline_report`  | -      | 仅大纲       |
| 自定义报告 | `custom_report`   | -      | 自定义格式   |
| 子主题报告 | `subtopic_report` | -      | 子主题研究   |

### 7.5 有用的链接

- [GPT Researcher 官方文档](https://docs.gptr.dev)
- [OpenAI API 文档](https://platform.openai.com/docs)
- [Tavily API 文档](https://docs.tavily.com)
- [FastAPI 文档](https://fastapi.tiangolo.com)
- [LangChain 文档](https://python.langchain.com)

---

**文档结束**

如有问题或建议，请提交 Issue 或 Pull Request。
