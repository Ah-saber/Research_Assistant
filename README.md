# Research Assistant

基于 Claude Code 的个人学术助理系统，专为计算机视觉学者设计。整合 Zotero 文献库和 Obsidian 笔记系统，提供文献管理、笔记整理、Idea 管理和可视化功能。

---

## AI 人设

本系统内置**计算机视觉学者助理**人设，核心特征：

- **研究领域**：基础视觉任务、生成模型、视觉架构
- **理论框架**：概率与统计偏好
- **思维特点**：理论导向、问题本质提炼、跨领域迁移
- **输出标准**：论文笔记包含概率框架分析，Idea 包含理论动机分析

详见 [PERSONA.md](PERSONA.md)

---

## 目录结构

```
.claude/
├── skills/      # 21 个技能
│   ├── obsidian-markdown/     # Markdown 格式参考
│   ├── json-canvas/           # Canvas 格式参考
│   ├── obsidian-bases/        # Bases 格式参考
│   ├── paper-search/          # 论文搜索
│   ├── paper-summary/         # 论文摘要
│   ├── annotation-extract/    # 注释提取
│   ├── paper-notes/           # 论文笔记
│   ├── note-analyze/          # 笔记分析
│   ├── note-organize/         # 笔记整理
│   ├── note-link/             # 笔记关联
│   ├── note-standardize/      # 笔记标准化
│   ├── note-template/         # 笔记模板
│   ├── idea-capture/          # Idea 捕捉
│   ├── idea-organize/         # Idea 整理
│   ├── idea-review/           # Idea 回顾
│   ├── paper-graph/           # 论文图谱
│   ├── idea-map/              # Idea 图谱
│   ├── knowledge-canvas/      # 知识画布
│   ├── paper-dashboard/       # 论文仪表盘
│   ├── idea-tracker/          # Idea 追踪
│   └── research-dashboard/    # 研究仪表盘
├── agents/      # 4 个专业代理
│   ├── literature-synthesizer.md
│   ├── note-organizer.md
│   ├── research-note-generator.md
│   └── note-visualizer.md
├── rules/       # 规则文档
│   ├── agents.md
│   ├── coding-style.md
│   ├── hooks.md
│   ├── workflow.md
│   ├── zotero-integration.md
│   └── obsidian-integration.md
├── settings.local.json

.claude-plugin/
├── plugin.json          # 插件配置
└── PLUGIN_SCHEMA_NOTES.md

hooks/
└── hooks.json           # 自动化触发配置

docs/
├── workflows/           # 工作流文档
└── guides/              # 使用指南

PLAN/
├── UPD.md               # 实施计划
├── PRO_UPD.md           # 进度跟踪
└── NED.md               # 需求记录

CLAUDE.md                # AI 工作指南
PERSONA.md               # AI 人设文档
.mcp.json                # MCP 配置
```

---

## 技能分类

| 类别 | 技能 | 功能 |
|------|------|------|
| **格式参考** (3) | obsidian-markdown, json-canvas, obsidian-bases | 格式规范文档 |
| **Reading** (4) | paper-search, paper-summary, annotation-extract, paper-notes | 文献管理 |
| **Notes** (5) | note-analyze, note-organize, note-link, note-standardize, note-template | 笔记管理 |
| **Ideas** (3) | idea-capture, idea-organize, idea-review | Idea 管理 |
| **Visualization** (3) | paper-graph, idea-map, knowledge-canvas | Canvas 可视化 |
| **Dashboard** (3) | paper-dashboard, idea-tracker, research-dashboard | Bases 仪表盘 |

---

## 代理 (Agents)

| 代理 | 职责 |
|------|------|
| literature-synthesizer | 文献综合分析 |
| note-organizer | 笔记智能整理 |
| research-note-generator | 研究笔记生成 |
| note-visualizer | 笔记可视化 |

---

## 技术栈

| 组件 | 方案 |
|------|------|
| Zotero 集成 | 54yyyu/zotero-mcp (只读) |
| Obsidian 集成 | Read/Write/Edit + Glob |
| Canvas 格式 | json-canvas skill |
| Bases 格式 | obsidian-bases skill |
| 自动化 | hooks/hooks.json |

---

## 访问控制

**受保护目录**（需授权）：
- `C:\Note\MyNote_Obs\科研\IDEA`
- `C:\Note\MyNote_Obs\思绪`

**可自由访问**：
- `C:\Note\MyNote_Obs\科研\Inspiration`
- 其他 Obsidian 目录

---

## 工作流

- 论文阅读：`paper-search` → `paper-notes` → `idea-capture`
- 笔记整理：`note-analyze` → `note-organize` → `note-link` → `note-standardize`
- Idea 管理：`idea-capture` → `idea-organize` → `idea-review`

详见 [docs/workflows/](docs/workflows/)

---

## 配置

### Zotero MCP

安装并配置 Zotero MCP 服务器：

```bash
pip install git+https://github.com/54yyyu/zotero-mcp.git
```

### 路径配置

编辑 `CLAUDE.md` 中的路径：
- Obsidian Vault: `C:\Note\MyNote_Obs`
- Inspiration: `C:\Note\MyNote_Obs\科研\Inspiration`

---

## 许可证

MIT License
