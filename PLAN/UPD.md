# Research Assistant 技能系统升级实施计划

**版本**: v1.1
**创建日期**: 2026-02-02
**参考项目**: everything-claude-code
**参考项目路径**: `D:\work_project\my_project\Ref_pro\everything-claude-code\`

---

## 一、项目概述

基于 `everything-claude-code` 参考项目，对 Research Assistant 的技能系统进行标准化升级：

1. **格式标准化**：添加 YAML frontmatter，统一文件名为 SKILL.md
2. **插件配置**：创建 `plugin.json` 支持插件化分发
3. **Commands 系统**：创建快捷命令封装常用工作流
4. **Hooks 自动化**：实现自动化触发机制
5. **Rules 模块化**：将 CLAUDE.md 拆分为模块化规则
6. **Document Format Skills**：创建外部格式参考技能
7. **自我进化**：支持从会话中提取模式的能力

---

## 二、语言规范

| 内容类型 | 语言 |
|---------|------|
| 技能/命令描述 | 简体中文 |
| 技能/命令名称 | 英文 (kebab-case) |
| YAML frontmatter | 英文 (name, description) |
| 代码示例 | 中文 + 英文术语保持原格式 |
| 标签、论文标题、技术术语 | 英文 |

---

## 三、目标目录结构

```
Research_Assistant/
├── .claude-plugin/
│   ├── plugin.json              # 新建：插件清单
│   └── PLUGIN_SCHEMA_NOTES.md   # 新建：约束说明
│
├── skills/                      # 重构：扁平化
│   │
│   │─── Notes Skills (5个)
│   ├── note-analyze/SKILL.md
│   ├── note-organize/SKILL.md
│   ├── note-standardize/SKILL.md
│   ├── note-template/SKILL.md
│   ├── note-link/SKILL.md
│   │
│   │─── Reading Skills (4个)
│   ├── paper-search/SKILL.md
│   ├── paper-summary/SKILL.md
│   ├── annotation-extract/SKILL.md
│   ├── paper-notes/SKILL.md
│   │
│   │─── Ideas Skills (3个)
│   ├── idea-capture/SKILL.md
│   ├── idea-organize/SKILL.md
│   ├── idea-review/SKILL.md
│   │
│   │─── Visualization Skills (3个)
│   ├── paper-graph/SKILL.md
│   ├── idea-map/SKILL.md
│   ├── knowledge-canvas/SKILL.md
│   │
│   │─── Dashboard Skills (3个)
│   ├── paper-dashboard/SKILL.md
│   ├── idea-tracker/SKILL.md
│   ├── research-dashboard/SKILL.md
│   │
│   │─── Document Format Skills (格式参考技能 - 新建)
│   │     这些技能提供格式规范文档，供其他技能参考
│   ├── obsidian-markdown/SKILL.md     # Obsidian Markdown 格式参考
│   ├── json-canvas/SKILL.md           # Canvas (.canvas) 格式参考
│   ├── obsidian-bases/SKILL.md        # Bases (.base) 格式参考
│   │
│   │─── Self-Evolution
│   └── continuous-learning/
│       ├── SKILL.md                   # 自我进化技能
│       └── config.json                # 配置文件
│
├── commands/                    # 新建：快捷命令
│   ├── search-paper.md
│   ├── create-paper-note.md
│   ├── standardize-notes.md
│   ├── analyze-notes.md
│   ├── organize-notes.md
│   ├── link-notes.md
│   ├── capture-idea.md
│   ├── review-ideas.md
│   ├── organize-ideas.md
│   ├── learn.md
│   └── evolve.md
│
├── hooks/                       # 新建：自动化触发
│   └── hooks.json
│
├── rules/                       # 新建：模块化规则
│   ├── agents.md
│   ├── coding-style.md
│   ├── hooks.md
│   ├── workflow.md
│   ├── zotero-integration.md
│   └── obsidian-integration.md
│
├── PLAN/
│   ├── references/              # 参考模板（保持不变）
│   │   ├── 论文笔记参考.md
│   │   ├── 概念笔记参考.md
│   │   ├── 项目笔记参考.md
│   │   └── 日志笔记参考.md
│   ├── UPD.md
│   └── PRO_UPD.md
```

**关键说明**：
- **Document Format Skills** 是**格式参考技能**，提供对应格式的语法规范文档
- 这些技能不执行文件操作，而是作为其他技能的格式参考
- 例如：`/note-standardize` 创建 Callout 时参考 `obsidian-markdown` 的语法
- 例如：`/paper-graph` 创建 Canvas 时参考 `json-canvas` 的格式

---

## 四、标准文件格式

### 4.1 SKILL.md 标准格式

```markdown
---
name: skill-name
description: Brief description in English
version: 1.0.0
---

# 技能名称（中文）

简短描述（1-2句话，中文）

## When to Activate（何时启用）

- 触发条件1
- 触发条件2
- 触发条件3

## 与外部格式参考技能的关系

**重要**：本技能参考以下格式参考技能获取语法规范：

- **obsidian-markdown**：提供 Obsidian Markdown 语法规范
  - Wikilink: `[[笔记|显示]]`
  - Callout: `> [!类型] 标题`
  - Frontmatter: YAML 格式
  - Tags: `#标签` 层级结构
  - Embeds: `![[笔记]]`

- **json-canvas**：提供 Canvas (.canvas) 格式规范
  - 节点类型: file, text, group
  - 边类型: 实线、虚线、点线
  - 布局算法: 层次、力导向、区域

- **obsidian-bases**：提供 Bases (.base) 格式规范
  - 视图类型: table, cards, list
  - 公式: 状态转换、数据计算
  - 分组: 按属性分组

**分工明确**：
- 格式参考技能：提供语法文档，不执行操作
- 本技能：工作流封装，使用 Read/Write/Edit + Glob 执行操作

## 模板文件参考

本技能使用以下模板文件：
- `PLAN/references/论文笔记参考.md` - 论文笔记完整模板
- `PLAN/references/概念笔记参考.md` - 概念笔记模板
- `PLAN/references/项目笔记参考.md` - 项目笔记模板
- `PLAN/references/日志笔记参考.md` - 日志笔记模板

## 核心功能

### 功能1
- **用途**：说明
- **语法**：格式（参考对应的格式参考技能）
- **场景**：使用场景

### 功能2
- **用途**：说明
- **MCP 工具**：`mcp__zotero__xxx`

## GOOD vs BAD（对比示例）

### ✅ GOOD
```markdown
<!-- 正确示例，中文内容，术语保持英文 -->
创建 Callout 时参考 obsidian-markdown:
> [!warning] 关键疑惑
使用 Wikilink 时使用 Glob 精确匹配:
[[实际文件名|显示名]]
```

### ❌ BAD
```markdown
<!-- 错误示例 -->
直接使用假设的文件名创建链接，未使用 Glob 验证
Callout 格式错误
```

## 工作流程

### 步骤1：描述
[详细步骤，说明如何参考格式技能、如何使用 MCP 工具]

### 步骤2：执行
[使用 Read/Write/Edit/Glob 执行具体操作]

## 使用的 MCP 工具

| 工具 | 用途 | 使用场景 |
|------|------|----------|
| `mcp__zotero__zotero_search_items` | 搜索论文 | 按关键词搜索 |
| `mcp__zotero__zotero_get_item_metadata` | 获取元数据 | 获取 BibTeX |
| `mcp__zotero__zotero_get_item_fulltext` | 获取全文 | 可能源超限 |

## 快速参考表

| 场景 | 命令 | 使用的格式参考 | 说明 |
|------|------|----------------|------|
| 创建笔记 | /note-standardize | obsidian-markdown | 格式化笔记 |
| 创建图谱 | /paper-graph | json-canvas | 创建 Canvas |
| 创建仪表盘 | /paper-dashboard | obsidian-bases | 创建 Base |
```

### 4.2 Document Format Skills 格式

这些技能提供格式规范文档，内容结构：

```markdown
---
name: obsidian-markdown
description: Complete Obsidian Markdown format reference including Wikilinks, Callouts, Frontmatter, Tags, and Embeds
version: 1.0.0
---

# Obsidian Markdown 格式参考

提供完整的 Obsidian Markdown 语法规范文档。

## Wikilink

### 基本语法
```
[[笔记名]]
[[笔记名|显示名]]
[[笔记名#标题]]
[[笔记名#标题|显示名]]
```

### 表格中的转义
在 Markdown 表格中，管道符 `|` 需要转义为 `\|`：
```
| [[文件名\|显示名]] | 下一列 |
```

## Callout

### 语法
```
> [!类型] 标题
内容
```

### 类型
- info, note, tip, important, warning, caution

## Frontmatter

### YAML 格式
```yaml
---
title: "标题"
tags: [标签1, 标签2]
date: YYYY-MM-DD
---
```

## Tags

### 层级标签
```
#一级/二级/三级
#CV/Generation/Diffusion
```

## Embeds

### 语法
```
![[笔记名]]
![[笔记名#标题]]
![[文件名.canvas]]
```
```

### 4.3 plugin.json 标准格式

```json
{
  "name": "research-assistant",
  "version": "1.0.0",
  "description": "Personal academic assistant for computer vision scholars",
  "author": {
    "name": "Your Name"
  },
  "homepage": "https://github.com/yourusername/Research_Assistant",
  "repository": "https://github.com/yourusername/Research_Assistant",
  "license": "MIT",
  "keywords": ["research-assistant", "zotero", "obsidian", "academic"],
  "skills": ["./skills/", "./commands/"]
}
```

**重要约束**：
- ✅ `version` 字段必需
- ✅ `skills` 必须是数组
- ❌ 不添加 `hooks` 字段（自动加载）
- ❌ 不使用 `agents` 字段（本项目不需要）

---

## 五、分阶段实施计划

### 阶段1：基础架构（第1天）

**目标**：建立标准化的目录结构和配置

#### 1.1 创建目录结构
```bash
mkdir -p .claude-plugin
mkdir -p commands
mkdir -p hooks
mkdir -p rules
```

#### 1.2 创建 plugin.json
- 路径：`.claude-plugin/plugin.json`
- 内容：按上述标准格式
- 关键点：skills 路径包含 `./skills/` 和 `./commands/`

#### 1.3 创建 PLUGIN_SCHEMA_NOTES.md
- 路径：`.claude-plugin/PLUGIN_SCHEMA_NOTES.md`
- 内容：约束说明（version 必需、paths 是数组、不添加 hooks）

#### 1.4 创建 hooks/hooks.json
- 路径：`hooks/hooks.json`
- 初始场景：
  - `PostToolWrite`: 笔记格式检查
  - `PostToolEdit`: 格式化建议
  - `SessionEnd`: 持久化状态

#### 1.5 创建 rules/ 目录文件
- `rules/agents.md`：Agent 相关规则
- `rules/coding-style.md`：代码风格规范
- `rules/hooks.md`：Hooks 使用说明
- `rules/workflow.md`：工作流规范
- `rules/zotero-integration.md`：Zotero 集成规范
- `rules/obsidian-integration.md`：Obsidian 集成规范

**验证标准**：
- [ ] plugin.json 格式正确
- [ ] hooks.json 格式正确
- [ ] 目录结构完整

---

### 阶段2：创建 Document Format Skills（第2天）

**优先级**：P0（最高，其他技能依赖这些格式参考）

**技能清单**（3个）：
1. `obsidian-markdown` - Obsidian Markdown 格式参考
2. `json-canvas` - Canvas (.canvas) 格式参考
3. `obsidian-bases` - Bases (.base) 格式参考

#### 2.1 创建 obsidian-markdown/SKILL.md

**内容结构**：
- Wikilink 语法（基本、表格转义、精确匹配）
- Callout 语法（类型、格式）
- Frontmatter 语法（YAML 格式、标准字段）
- Tags 语法（层级结构、英文术语）
- Embeds 语法（嵌入笔记、嵌入 Canvas）

**示例内容**：
```markdown
## Wikilink

### 基本语法
[[笔记名]]
[[笔记名|显示名]]

### 表格中的转义（重要）
在 Markdown 表格中，管道符 `|` 需要转义：
| [[文件名\|显示名]] | 下一列 |

### 使用 Glob 精确匹配
创建 Wikilink 时必须使用 Glob 精确获取文件名：
```python
pattern = f"**/*{paper_title}*.md"
matches = glob.glob(pattern, recursive=True)
if matches:
    actual_filename = matches[0]
    link = f"[[{actual_filename}|{paper_title}]]"
```
```

#### 2.2 创建 json-canvas/SKILL.md

**内容结构**：
- Canvas 文件结构
- 节点类型（file, text, group）
- 边类型（实线、虚线、点线）
- 颜色编码
- 布局算法

**示例内容**：
```markdown
## Canvas 文件结构

```json
{
  "nodes": [
    {
      "id": "node1",
      "type": "file",
      "x": 0,
      "y": 0,
      "width": 300,
      "height": 200,
      "file": "路径/文件.md",
      "color": "1"
    }
  ],
  "edges": [
    {
      "id": "edge1",
      "fromNode": "node1",
      "toNode": "node2",
      "fromEnd": "arrow",
      "toEnd": "none"
    }
  ]
}
```

## 颜色编码

| 颜色 | 说明 | 代码 |
|------|------|------|
| 红色 | 核心/重要 | "1" |
| 橙色 | 重要进展 | "2" |
| 黄色 | 扩展 | "3" |
| 绿色 | 应用 | "4" |
```

#### 2.3 创建 obsidian-bases/SKILL.md

**内容结构**：
- Base 文件结构
- 视图类型（table, cards, list）
- 公式（状态转换、数据计算）
- 分组排序
- 统计汇总

**示例内容**：
```markdown
## 视图类型

| 类型 | 说明 | 用途 |
|------|------|------|
| table | 表格视图 | 详细列表，支持排序筛选 |
| cards | 卡片视图 | 封面展示，适合浏览 |
| list | 列表视图 | 简洁列表，快速浏览 |

## 公式示例

```yaml
formulas:
  # 状态图标
  status_icon: 'if(status == "done", "✅", "📚")'

  # 日期计算
  days_ago: '((now() - date(date)) / 86400000).round(0)'
```

## 分组排序

```yaml
views:
  - type: table
    groupBy:
      property: status
    order:
      - file.name
      - date
```
```

**验证标准**：
- [ ] 3个格式参考技能创建完成
- [ ] YAML frontmatter 正确
- [ ] 语法规范完整准确
- [ ] 示例代码正确

---

### 阶段3-9：（本次会话不执行）

略，详见完整计划

---

## 六、本次会话执行范围

**会话目标**：仅执行到阶段2完成

**执行内容**：
- ✅ 阶段1：基础架构（目录结构、配置文件）
- ✅ 阶段2：Document Format Skills（3个格式参考技能）

**不执行**：
- ❌ 阶段3及以后：Notes/Reading/Ideas/Visualization/Dashboard Skills 标准化
- ❌ Commands 创建
- ❌ Rules 模块化
- ❌ 自我进化实现

---

## 七、进度跟踪

**进展文档**：`PLAN/PRO_UPD.md`

各阶段完成后更新 `PRO_UPD.md`，记录：
- 完成时间
- 遇到的问题
- 解决方案
- 待完成事项
