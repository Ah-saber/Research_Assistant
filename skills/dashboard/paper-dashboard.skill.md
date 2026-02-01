# `/paper-graph` - 论文阅读进度追踪

创建 Obsidian Bases 仪表盘，用于追踪和管理论文阅读进度。

## 与 obsidian-bases 的关系

obsidian-bases 是**格式参考**技能，提供完整的 Bases (.base) 语法规范文档。

本技能是**工作流封装**，组合 Read/Write/Edit 工具创建符合规范的 .base 文件。

## 功能说明

### 核心功能

- **阅读状态追踪**：按状态（待阅读、阅读中、已完成）分组展示
- **领域分类管理**：按研究领域（CV/NLP/ML等）自动分类
- **时间线视图**：按阅读日期排序的进度跟踪
- **统计汇总**：计算阅读数量、时间分布、领域占比

### 支持的视图

| 视图类型 | 说明 | 用途 |
|---------|------|------|
| Table | 表格视图 | 详细列表，支持排序和筛选 |
| Cards | 卡片视图 | 封面展示，适合浏览 |
| List | 列表视图 | 简洁列表，快速浏览 |

## 前置条件

### 论文笔记 Frontmatter 要求

论文笔记需要包含以下属性：

```yaml
---
title: "论文标题"
status: to-read | reading | done
date: YYYY-MM-DD
authors: ["作者1", "作者2"]
year: 2024
venue: "会议/期刊名称"
tags: ["CV", "Generation", "Diffusion"]
field: "CV"  # 研究领域
field_sub: "Generation"  # 子领域
read_date: 2024-01-15  # 阅读完成日期
read_time: 120  # 阅读时长（分钟）
rating: 5  # 评分（1-5）
importance: core | important | extension | application
---
```

## Base 文件结构

### 完整示例

```yaml
filters:
  and:
    - file.hasTag("paper")
    - 'file.ext == "md"'

formulas:
  # 状态图标
  status_icon: 'if(status == "to-read", "📚", if(status == "reading", "📖", "✅"))'

  # 重要性标签
  importance_label: 'if(importance == "core", "🔴 核心", if(importance == "important", "🟠 重要", if(importance == "extension", "🟡 扩展", "🟢 应用")))'

  # 阅读进度天数
  days_reading: 'if(read_date, ((date(read_date) - date(file.ctime)) / 86400000).round(0), "")'

  # 是否最近阅读
  is_recent: 'read_date && (now() - date(read_date)) < "30d"'

  # 简短标题（截断过长标题）
  short_title: 'file.basename.slice(0, 50)'

  # 领域+子领域组合
  field_full: 'field + "/" + field_sub'

  # 作者简写
  authors_short: 'if(authors.length > 2, authors[0] + " et al.", authors.join(", "))'

properties:
  status:
    displayName: 状态
  formula.status_icon:
    displayName: ""
  formula.importance_label:
    displayName: 重要性
  formula.field_full:
    displayName: 领域
  formula.authors_short:
    displayName: 作者
  read_date:
    displayName: 阅读日期
  read_time:
    displayName: 阅读时长
  rating:
    displayName: 评分

summaries:
  total_papers: 'values.length'
  avg_rating: 'values.filter(v => v.isType("number") && v > 0).mean().round(2)'
  total_read_time: 'values.filter(v => v.isType("number")).sum()'

views:
  # 视图1：按状态分组
  - type: table
    name: "阅读状态"
    groupBy:
      property: status
      direction: ASC
    order:
      - formula.status_icon
      - file.name
      - formula.authors_short
      - year
      - formula.importance_label
      - read_date
      - rating
    summaries:
      read_time: Sum
      rating: Average

  # 视图2：待阅读
  - type: table
    name: "待阅读"
    filters:
      and:
        - 'status == "to-read"'
    order:
      - formula.importance_label
      - file.name
      - formula.authors_short
      - year
      - venue

  # 视图3：阅读中
  - type: table
    name: "阅读中"
    filters:
      and:
        - 'status == "reading"'
    order:
      - file.mtime
      - file.name
      - read_time

  # 视图4：已完成
  - type: table
    name: "已完成"
    filters:
      and:
        - 'status == "done"'
    order:
      - read_date
      - file.name
      - rating
      - formula.importance_label
    summaries:
      read_time: Sum
      rating: Average

  # 视图5：按领域分类
  - type: table
    name: "领域分类"
    groupBy:
      property: field
      direction: ASC
    order:
      - formula.field_full
      - file.name
      - status
      - year
    summaries:
      rating: Average
      read_time: Sum

  # 视图6：核心论文
  - type: table
    name: "核心论文"
    filters:
      and:
        - 'importance == "core"'
    order:
      - status
      - rating
      - file.name

  # 视图7：最近阅读
  - type: table
    name: "最近阅读（30天）"
    filters:
      and:
        - formula.is_recent
    order:
      - read_date
      - file.name
      - rating

  # 视图8：高评分论文
  - type: table
    name: "高评分论文（4+）"
    filters:
      and:
        - 'rating >= 4'
    order:
      - rating
      - file.name
      - year

  # 视图9：卡片视图（带封面）
  - type: cards
    name: "论文卡片"
    order:
      - cover
      - file.name
      - formula.status_icon
      - formula.authors_short

  # 视图10：时间线
  - type: list
    name: "阅读时间线"
    filters:
      and:
        - 'status == "done"'
        - read_date
    order:
      - read_date
      - file.name
```

## 执行流程

### 1. 分析现有论文笔记

使用 Glob 工具扫描指定目录下的论文笔记：

```python
# 扫描论文目录
pattern = "**/Paper/*.md"
papers = glob.glob(pattern, recursive=True)
```

### 2. 检查 Frontmatter 完整性

检查每篇论文笔记是否包含必要的属性：
- `status`: 阅读状态
- `importance`: 重要性
- `field`: 研究领域
- `read_date`: 阅读日期（已完成时）
- `rating`: 评分（可选）

### 3. 生成 Base 文件

使用 Write 工具创建 `.base` 文件：

```yaml
# 文件路径：科研/CV/论文阅读进度.base
filters:
  and:
    - file.inFolder("科研/CV/Paper")
    - 'file.ext == "md"'

formulas:
  # ... 公式定义

views:
  # ... 视图定义
```

### 4. 嵌入到索引笔记

在索引笔记中嵌入 Base 文件：

```markdown
## 论文阅读进度

![[论文阅读进度.base]]

## 阅读状态

![[论文阅读进度.base#阅读状态]]
```

## 使用场景

### 场景1：开始阅读新论文

1. 在 Zotero 中找到论文
2. 使用 `/paper-notes` 创建笔记
3. 设置 `status: reading`
4. 在仪表盘中跟踪进度

### 场景2：完成论文阅读

1. 更新 `status: done`
2. 添加 `read_date` 和 `rating`
3. 在仪表盘中查看统计

### 场景3：规划阅读清单

1. 查看"待阅读"视图
2. 按 `importance` 排序
3. 选择高优先级论文

### 场景4：领域研究回顾

1. 查看"领域分类"视图
2. 按领域分组查看
3. 了解各领域进展

## 配置选项

### 目录配置

默认扫描 `科研/CV/Paper/` 目录，可通过以下参数调整：

- `--directory`: 指定论文目录
- `--recursive`: 是否递归扫描子目录
- `--filter`: 文件名过滤器

### 视图配置

支持自定义视图：
- 添加新视图
- 修改过滤条件
- 调整显示顺序
- 自定义分组方式

### 公式配置

支持自定义公式：
- 状态转换
- 数据计算
- 格式化输出

## 注意事项

1. **Frontmatter 一致性**：确保所有论文笔记使用相同的属性名称
2. **日期格式**：使用 YYYY-MM-DD 格式
3. **状态枚举**：使用预定义的状态值（to-read/reading/done）
4. **性能考虑**：大量论文时考虑使用 `limit` 限制显示数量

## 相关技能

- `/paper-search` - 搜索论文
- `/paper-notes` - 创建论文笔记
- `/note-standardize` - 标准化笔记格式
- `/paper-graph` - 论文引用关系图谱
