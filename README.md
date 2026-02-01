# Research Assistant

基于Claude Code的个人学术助理系统，专为计算机视觉学者设计，整合Zotero文献库和Obsidian笔记系统。

## AI人设

本系统内置**计算机视觉学者助理**人设，核心特征：

- **研究领域**：基础视觉任务、生成模型、视觉架构
- **理论框架**：概率与统计偏好
- **思维特点**：理论导向、问题本质提炼、跨领域迁移
- **输出标准**：论文笔记包含概率框架分析，Idea包含理论动机分析

详细人设定义见 [PERSONA.md](PERSONA.md)

## 功能概述

- **文献查询**：在Zotero中搜索论文，提取元数据和注释
- **论文总结**：自动生成论文摘要和要点
- **笔记整理**：分析、组织和优化Obsidian笔记
- **Idea管理**：捕捉、分类和回顾研究想法

## 项目结构

```
Research_Assistant/
├── .claude/
│   └── rules/              # 自定义规则
├── skills/                 # 自定义Skills (18个)
│   ├── reading/           # 文献阅读相关 (4个)
│   ├── notes/             # 笔记整理相关 (5个)
│   ├── ideas/             # Idea管理相关 (3个)
│   ├── visualization/     # 可视化图谱 (3个)
│   └── dashboard/         # 仪表盘 (3个)
├── docs/                  # 工作文档
│   ├── workflows/         # 工作流文档
│   └── guides/            # 使用指南
├── PLAN/                  # 项目规划文档
│   ├── PRD.md            # 产品需求文档
│   ├── PRO.md            # 项目进度文档
│   ├── 待测试项目.md      # 测试清单
│   ├── 改进建议.md        # 改进路线图
│   └── references/       # 参考模板（5个）
│       ├── 论文笔记参考.md
│       ├── 概念笔记参考.md
│       ├── 项目笔记参考.md
│       ├── 日志笔记参考.md
│       └── 索引笔记参考.md  # 索引格式规范
├── .gitignore
├── .cursorrules           # Claude Code工作规则
├── PERSONA.md             # AI助理人设文档
├── CLAUDE.md              # AI助理工作指南
└── README.md              # 本文件
```

## 技术栈

| 组件 | 方案 | 状态 |
|------|------|------|
| Zotero集成 | 54yyyu/zotero-mcp | 需安装 |
| Obsidian Markdown | obsidian-markdown skill | 已安装 |
| Canvas可视化 | json-canvas skill | 已安装 |
| Bases仪表盘 | obsidian-bases skill | 已安装 |
| PDF处理 | document-skills (pdf skill) | 已安装 |
| 工作流封装 | 自定义Skills | 已创建 |

## 快速开始

### 1. 安装Zotero MCP

```bash
pip install git+https://github.com/54yyyu/zotero-mcp.git
zotero-mcp setup
```

### 2. 配置MCP服务器

在Claude Code的MCP配置中添加：

```json
{
  "mcpServers": {
    "zotero": {
      "command": "zotero-mcp",
      "env": {
        "ZOTERO_LOCAL": "true"
      }
    }
  }
}
```

### 3. 配置路径

编辑`.cursorrules`和`CLAUDE.md`中的路径：
- Obsidian Vault: `C:\Note\MyNote_Obs`

### 4. 安装Skills

将`skills/`目录下的skill文件复制到Claude Code的skills目录。

## 使用方式

### 文献阅读

```bash
# 搜索论文
/paper-search "transformer interpretability"

# 总结论文
/paper-summary <paper_key>

# 提取注释
/annotation-extract <paper_key>

# 创建笔记（包含概率框架分析）
/paper-notes <paper_key>
```

### 笔记整理

```bash
# 分析笔记结构
/note-analyze

# 整理笔记
/note-organize

# 创建模板
/note-template

# 建立关联
/note-link

# 标准化笔记（Callout/Wikilink/Frontmatter/标签）
/note-standardize
```

### Idea管理

```bash
# 捕捉Idea（包含理论动机分析）
/idea-capture

# 整理Idea
/idea-organize

# 回顾Idea
/idea-review
```

### 可视化图谱

```bash
# 论文引用关系图谱
/paper-graph

# Idea概念关系图谱
/idea-map

# 综合知识画布
/knowledge-canvas
```

### 仪表盘追踪

```bash
# 论文阅读进度追踪
/paper-dashboard

# Idea状态管理追踪
/idea-tracker

# 综合研究进度仪表盘
/research-dashboard
```

## 工作流文档

详细工作流请参考：
- [论文阅读工作流](docs/workflows/paper-reading.md)
- [笔记整理工作流](docs/workflows/note-organization.md)
- [Idea管理工作流](docs/workflows/idea-management.md)

## 配置说明

### 访问限制

IDEA和思绪目录默认禁止访问，需用户明确授权：
- `C:\Note\MyNote_Obs\科研\IDEA`
- `C:\Note\MyNote_Obs\思绪`

### 命名规范

- 笔记命名：仅标题，如`论文标题.md`
- 日期格式：YYYY-MM-DD（frontmatter中）
- **索引笔记**：必须使用表格格式（见 `PLAN/references/索引笔记参考.md`）

## 依赖项

- Python 3.8+
- Zotero 7+
- Claude Code
- Obsidian

## 许可证

MIT License
