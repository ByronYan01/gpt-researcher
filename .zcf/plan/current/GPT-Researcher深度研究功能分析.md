# GPT-Researcher 深度研究功能分析计划

**创建时间：** 2026-02-27 10:55:53
**任务：** 深度分析 GPT-Researcher 项目，聚焦深度研究功能实现
**输出：** know/GPT-Researcher深度研究功能分析.md

---

## 一、任务概述

### 目标
1. 全面介绍项目目录结构
2. 深度分析后端实现架构
3. 聚焦"深度研究"功能的完整实现
4. 绘制时序图展示核心流程
5. 生成完整MD文档

### 研究范围
- 项目整体架构
- 后端核心模块实现
- 深度研究功能源码分析
- 时序图绘制

### 排除范围
- 前端实现细节（仅概述）
- 多智能体框架实现（单独模块）
- 测试代码分析

---

## 二、执行步骤

### 步骤 1：生成项目目录结构概览
**文件位置：** 项目根目录
**操作：**
- 描述项目根目录结构
- 重点说明 `gpt_researcher/` 核心模块
- 说明 `backend/`、`frontend/`、`multi_agents/` 等子项目作用

**预期结果：**
```
gpt-researcher/
├── gpt_researcher/          # 核心模块
├── backend/                 # FastAPI 后端服务
├── frontend/                # 前端应用
├── multi_agents/            # LangGraph 多智能体实现
├── main.py                  # 应用入口
└── ...
```

---

### 步骤 2：深度分析后端核心架构
**核心文件：**
- `main.py:1-38` - 应用入口
- `gpt_researcher/agent.py:36-720` - GPTResearcher 主类
- `gpt_researcher/config/` - 配置管理

**分析内容：**
1. **应用启动流程**（main.py）
   - 日志配置
   - FastAPI 应用加载
   - Uvicorn 服务器启动

2. **GPTResearcher 类架构**（agent.py）
   - 初始化参数分析
   - 核心组件初始化（ResearchConductor, ReportGenerator, ContextManager 等）
   - MCP 配置处理

**预期结果：**
- 后端架构图（文本描述）
- 核心类职责说明
- 组件依赖关系

---

### 步骤 3：分析深度研究功能实现
**核心文件：**
- `gpt_researcher/skills/deep_research.py:1-421` - DeepResearchSkill 类
- `gpt_researcher/agent.py:397-443` - _handle_deep_research 方法

**分析内容：**

#### 3.1 ResearchProgress 类
- **位置：** `deep_research.py:39-48`
- **职责：** 跟踪研究进度（深度、宽度、查询计数）

#### 3.2 DeepResearchSkill 类
- **位置：** `deep_research.py:50-421`
- **初始化参数：**
  - `breadth`: 并行查询数（默认4）
  - `depth`: 递归深度（默认2）
  - `concurrency_limit`: 并发限制（默认2）

#### 3.3 核心方法分析

| 方法 | 行号 | 职责 |
|------|------|------|
| `generate_search_queries` | 65-97 | 生成搜索查询 |
| `generate_research_plan` | 99-139 | 生成研究计划（问题） |
| `process_research_results` | 141-191 | 处理研究结果提取学习点 |
| `deep_research` | 193-355 | 核心递归研究方法 |
| `run` | 357-421 | 运行深度研究主入口 |

#### 3.4 递归算法分析

**树状探索算法：**
```
deep_research(query, breadth=4, depth=2)
├── 查询1 ──┐
├── 查询2 ──┼─→ [递归] deep_research(..., depth=1)
├── 查询3 ──┤       └── breadth = max(2, 4//2) = 2
└── 查询4 ──┘
```

**关键特性：**
- 并发控制：`asyncio.Semaphore`
- 动态调整：深度增加时宽度减半
- 上下文截断：25,000 词限制

**预期结果：**
- 深度研究功能详细分析
- 代码片段说明
- 算法流程描述

---

### 步骤 4：绘制深度研究时序图
**涉及组件：**
1. 用户/客户端
2. FastAPI Server
3. GPTResearcher
4. DeepResearchSkill
5. LLM Provider (OpenAI等)
6. Retriever (Tavily/MCP)

**时序图内容：**
```
用户 → Server → GPTResearcher → DeepResearchSkill
                                    ↓
                              generate_search_queries
                                    ↓
                            并发执行多个子查询
                                    ↓
                              process_research_results
                                    ↓
                              [递归] 深度研究
                                    ↓
                              聚合结果生成报告
```

**预期结果：**
- Mermaid 时序图
- 关键步骤说明
- 数据流标注

---

### 步骤 5：生成最终MD文档
**输出位置：** `know/GPT-Researcher深度研究功能分析.md`

**文档结构：**
```markdown
# GPT-Researcher 深度研究功能分析

## 一、项目概述
## 二、项目目录结构
## 三、后端架构分析
## 四、深度研究功能详解
## 五、时序图
## 六、技术要点总结
## 七、附录
```

**预期结果：**
- 完整的分析文档
- 代码引用准确
- 图表清晰

---

## 三、技术要点

### 关键技术栈
- **框架：** FastAPI + LangChain + LangGraph
- **异步：** asyncio + aiofiles
- **LLM：** OpenAI (支持推理模型 o3-mini)
- **搜索：** Tavily + DuckDuckGo + MCP
- **文档：** BeautifulSoup, PyMuPDF, unstructured

### 深度研究核心算法
- 树状递归探索
- 并发处理 (Semaphore)
- 上下文智能截断
- 成本跟踪

### 配置参数
| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| DEEP_RESEARCH_BREADTH | 4 | 每层并行查询数 |
| DEEP_RESEARCH_DEPTH | 2 | 递归深度 |
| DEEP_RESEARCH_CONCURRENCY | 2 | 并发限制 |

---

## 四、完成标准

1. ✅ 项目目录结构清晰描述
2. ✅ 后端核心架构详细分析
3. ✅ 深度研究功能代码级解析
4. ✅ 完整时序图
5. ✅ MD文档生成到 know/ 目录

---

## 五、用户确认

**请确认以上计划是否符合您的预期？**

确认后我将开始执行计划，生成最终的分析文档。
