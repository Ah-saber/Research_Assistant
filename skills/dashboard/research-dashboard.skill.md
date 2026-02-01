# `/research-dashboard` - 综合研究进度仪表盘

创建 Obsidian Bases 仪表盘，综合展示研究进度，包括论文阅读、Idea 管理、概念笔记等。

## 与 obsidian-bases 的关系

obsidian-bases 是**格式参考**技能，提供完整的 Bases (.base) 语法规范文档。

本技能是**工作流封装**，组合 Read/Write/Edit 工具创建符合规范的 .base 文件。

## 功能说明

### 核心功能

- **多内容类型整合**：同时追踪论文、Idea、概念笔记、项目笔记
- **研究主题全景**：按研究主题分组展示所有相关内容
- **进度可视化**：时间线视图展示研究进展
- **统计汇总**：计算各类型内容的数量和分布

### 支持的视图

| 视图类型 | 说明 | 用途 |
|---------|------|------|
| Table | 表格视图 | 详细列表，支持排序和筛选 |
| Cards | 卡片视图 | 内容概览 |
| List | 列表视图 | 简洁列表 |

## 前置条件

### 通用 Frontmatter 属性

所有研究相关的笔记应包含以下属性：

```yaml
---
title: "标题"
content_type: paper | idea | concept | project | note
date: YYYY-MM-DD
tags: ["CV", "Generation"]
theme: "研究主题"
status: # 根据类型有不同的值
updated_date: YYYY-MM-DD
---

# 论文特有属性
# status: to-read | reading | done
# authors: ["作者1"]
# year: 2024
# venue: "会议/期刊"

# Idea 特有属性
# status: sprout | thinking | implemented | abandoned
# priority: high | medium | low
# feasibility: high | medium | low

# 概念笔记特有属性
# difficulty: easy | medium | hard
# related_papers: ["论文1"]

# 项目笔记特有属性
# status: planning | active | completed | archived
# progress: 0-100
# due_date: YYYY-MM-DD
```

## Base 文件结构

### 完整示例

```yaml
filters:
  or:
    - file.hasTag("paper")
    - file.hasTag("idea")
    - file.hasTag("concept")
    - file.hasTag("project")
    - file.inFolder("科研")
    - file.inFolder("Inspiration")

formulas:
  # 内容类型图标
  type_icon: 'if(content_type == "paper", "📄", if(content_type == "idea", "💡", if(content_type == "concept", "📚", if(content_type == "project", "🚀", "📝"))))'

  # 内容类型标签（中文）
  type_label: 'if(content_type == "paper", "论文", if(content_type == "idea", "Idea", if(content_type == "concept", "概念", if(content_type == "project", "项目", "笔记"))))'

  # 状态图标（根据类型）
  paper_status_icon: 'if(content_type == "paper", if(status == "to-read", "📚", if(status == "reading", "📖", "✅")), "")'

  idea_status_icon: 'if(content_type == "idea", if(status == "sprout", "🌱", if(status == "thinking", "🤔", if(status == "implemented", "✅", "❌"))), "")'

  project_status_icon: 'if(content_type == "project", if(status == "planning", "📋", if(status == "active", "🔨", if(status == "completed", "✅", "📦"))), "")'

  # 统一状态图标
  status_icon: 'paper_status_icon + idea_status_icon + project_status_icon'

  # 更新距今天数
  days_since_update: 'if(updated_date, ((now() - date(updated_date)) / 86400000).round(0), "")'

  # 是否最近更新（7天内）
  is_recent: 'updated_date && (now() - date(updated_date)) < "7d"'

  # 是否活跃（论文阅读中、Idea思考中、项目进行中）
  is_active: 'or((content_type == "paper" && status == "reading"), (content_type == "idea" && status == "thinking"), (content_type == "project" && status == "active"))'

  # 进度条（项目）
  progress_bar: 'if(content_type == "project" && progress, "█".repeat(progress.round(0) / 5) + "░".repeat(20 - progress.round(0) / 5), "")'

  # 领域+主题组合
  domain_theme: 'if(theme, theme, "未分类")'

  # 相关内容数量（链接数）
  link_count: 'file.links.length'

  # 被链接数
  backlink_count: 'file.backlinks.length'

  # 文件大小（KB）
  size_kb: '(file.size / 1024).round(1)'

  # 阅读状态（论文）
  paper_status_label: 'if(content_type == "paper", if(status == "to-read", "待阅读", if(status == "reading", "阅读中", "已完成")), "")'

  # Idea 状态标签
  idea_status_label: 'if(content_type == "idea", if(status == "sprout", "萌芽", if(status == "thinking", "思考中", if(status == "implemented", "已实现", "已放弃"))), "")'

  # 项目状态标签
  project_status_label: 'if(content_type == "project", if(status == "planning", "计划中", if(status == "active", "进行中", if(status == "completed", "已完成", "已归档"))), "")'

properties:
  content_type:
    displayName: 类型
  formula.type_icon:
    displayName: ""
  formula.type_label:
    displayName: 类型
  status:
    displayName: 状态
  formula.status_icon:
    displayName: ""
  theme:
    displayName: 主题
  updated_date:
    displayName: 更新日期
  formula.days_since_update:
    displayName: 更新距今
  formula.link_count:
    displayName: 链接数
  formula.backlink_count:
    displayName: 被链接数

summaries:
  total_items: 'values.length'
  paper_count: 'values.filter(v => v == "paper").length'
  idea_count: 'values.filter(v => v == "idea").length'
  concept_count: 'values.filter(v => v == "concept").length'
  project_count: 'values.filter(v => v == "project").length'

views:
  # 视图1：全部内容（按类型分组）
  - type: table
    name: "全部内容"
    groupBy:
      property: content_type
      direction: ASC
    order:
      - formula.type_icon
      - file.name
      - formula.status_icon
      - theme
      - formula.days_since_update
    summaries:
      formula.days_since_update: Average
      formula.link_count: Sum

  # 视图2：活跃内容
  - type: table
    name: "活跃内容"
    filters:
      and:
        - formula.is_active
    order:
      - content_type
      - updated_date
      - file.name
      - formula.status_icon

  # 视图3：最近更新（7天内）
  - type: table
    name: "最近更新"
    filters:
      and:
        - formula.is_recent
    order:
      - updated_date
      - content_type
      - file.name

  # 视图4：论文相关
  - type: table
    name: "论文研究"
    filters:
      and:
        - 'content_type == "paper"'
    order:
      - status
      - file.name
      - year
      - theme

  # 视图5：Idea 相关
  - type: table
    name: "Idea 管理"
    filters:
      and:
        - 'content_type == "idea"'
    order:
      - status
      - priority
      - file.name
      - theme

  # 视图6：概念笔记
  - type: table
    name: "概念笔记"
    filters:
      and:
        - 'content_type == "concept"'
    order:
      - file.name
      - difficulty
      - theme

  # 视图7：项目追踪
  - type: table
    name: "项目追踪"
    filters:
      and:
        - 'content_type == "project"'
    order:
      - status
      - progress
      - file.name
      - due_date

  # 视图8：按主题分组
  - type: table
    name: "主题全景"
    groupBy:
      property: theme
      direction: ASC
    order:
      - theme
      - content_type
      - file.name
      - formula.status_icon
    summaries:
      file.name: Count
      formula.link_count: Sum

  # 视图9：时间线
  - type: list
    name: "研究时间线"
    order:
      - updated_date
      - content_type
      - file.name

  # 视图10：高链接内容
  - type: table
    name: "核心内容（高链接）"
    filters:
      and:
        - 'formula.link_count > 2'
    order:
      - formula.link_count
      - content_type
      - file.name

  # 视图11：待处理内容
  - type: table
    name: "待处理"
    filters:
      or:
        - and:
            - 'content_type == "paper"'
            - 'status == "to-read"'
        - and:
            - 'content_type == "idea"'
            - 'status == "sprout"'
        - and:
            - 'content_type == "project"'
            - 'status == "planning"'
    order:
      - content_type
      - file.name

  # 视图12：已完成内容
  - type: table
    name: "已完成"
    filters:
      or:
        - and:
            - 'content_type == "paper"'
            - 'status == "done"'
        - and:
            - 'content_type == "idea"'
            - 'status == "implemented"'
        - and:
            - 'content_type == "project"'
            - 'status == "completed"'
    order:
      - updated_date
      - content_type
      - file.name

  # 视图13：卡片视图
  - type: cards
    name: "内容卡片"
    order:
      - cover
      - file.name
      - formula.type_icon
      - theme

  # 视图14：统计汇总
  - type: table
    name: "内容统计"
    groupBy:
      property: content_type
      direction: ASC
    order:
      - formula.type_label
      - formula.type_label
    summaries:
      file.name: Count
      formula.size_kb: Sum

  # 视图15：跨主题关联
  - type: table
    name: "跨主题关联"
    filters:
      and:
        - 'formula.link_count > 0'
    order:
      - theme
      - file.name
      - formula.link_count
```

## 执行流程

### 1. 扫描研究相关目录

使用 Glob 工具扫描多个目录：

```python
# 扫描多个目录
patterns = [
    "科研/**/*.md",
    "Inspiration/**/*.md",
    "概念/**/*.md",
    "项目/**/*.md"
]

all_files = []
for pattern in patterns:
    files = glob.glob(pattern, recursive=True)
    all_files.extend(files)
```

### 2. 识别内容类型

根据文件位置和标签识别内容类型：
- 在 Paper 目录或有 paper 标签 → `paper`
- 在 Inspiration/IDEA 目录或有 idea 标签 → `idea`
- 在概念目录或有 concept 标签 → `concept`
- 在项目目录或有 project 标签 → `project`
- 其他 → `note`

### 3. 检查 Frontmatter 完整性

检查每种内容类型的必要属性：
- 通用：`content_type`, `theme`, `updated_date`
- 论文：`status`, `authors`, `year`, `venue`
- Idea：`status`, `priority`, `feasibility`
- 概念：`difficulty`, `related_papers`
- 项目：`status`, `progress`, `due_date`

### 4. 生成 Base 文件

使用 Write 工具创建 `.base` 文件：

```yaml
# 文件路径：科研/研究进度仪表盘.base

filters:
  or:
    - file.inFolder("科研")
    - file.inFolder("Inspiration")

formulas:
  # ... 公式定义

views:
  # ... 视图定义
```

### 5. 嵌入到索引笔记

在研究总览笔记中嵌入 Base 文件：

```markdown
# 研究进度仪表盘

## 总览

![[研究进度仪表盘.base#全部内容]]

## 活跃内容

![[研究进度仪表盘.base#活跃内容]]

## 主题全景

![[研究进度仪表盘.base#主题全景]]

## 最近更新

![[研究进度仪表盘.base#最近更新]]
```

## 使用场景

### 场景1：查看研究全景

1. 查看"全部内容"视图
2. 了解各类型内容的数量和分布
3. 按主题查看所有相关内容

### 场景2：追踪活跃项目

1. 查看"活跃内容"视图
2. 专注于当前正在进行的工作
3. 了解各活跃项目的进展

### 场景3：主题研究回顾

1. 查看"主题全景"视图
2. 选择特定研究主题
3. 查看该主题下的所有相关内容

### 场景4：发现核心内容

1. 查看"核心内容（高链接）"视图
2. 识别被频繁引用的内容
3. 重点关注核心概念和论文

### 场景5：管理待处理事项

1. 查看"待处理"视图
2. 查看所有待阅读、萌芽、计划中的内容
3. 决定下一步行动

## 配置选项

### 目录配置

默认扫描以下目录：
- `科研/` - 所有科研相关内容
- `Inspiration/` - 临时 Idea
- 可通过参数添加其他目录

### 内容类型配置

支持自定义内容类型：
- 默认：paper、idea、concept、project、note
- 可添加新类型或修改现有类型

### 状态配置

每种内容类型有独立的状态枚举：
- 论文：to-read、reading、done
- Idea：sprout、thinking、implemented、abandoned
- 项目：planning、active、completed、archived

### 主题配置

支持自定义研究主题分类：
- 通过 `theme` 属性指定
- 支持层级主题（如 `CV/Generation/Diffusion`）

## 注意事项

1. **访问控制**：IDEA 目录需要授权才能访问
2. **性能考虑**：大量内容时使用 `limit` 限制显示数量
3. **Frontmatter 一致性**：确保同类型内容使用相同的属性名称
4. **内容类型标识**：正确设置 `content_type` 属性
5. **定期更新**：及时更新 `updated_date` 属性

## 与其他技能的关系

| 技能 | 关系 |
|------|------|
| `/paper-dashboard` | 专注于论文阅读进度 |
| `/idea-tracker` | 专注于 Idea 状态管理 |
| `/research-dashboard` | 整合所有研究内容 |

## 相关技能

- `/paper-dashboard` - 论文阅读进度追踪
- `/idea-tracker` - Idea 状态管理追踪
- `/paper-search` - 搜索论文
- `/note-analyze` - 分析笔记
- `/knowledge-canvas` - 综合知识画布
