---
name: paper-dashboard
description: 创建 Obsidian Bases 仪表盘，用于追踪和管理论文阅读进度。**必须使用此技能**当用户说"论文仪表盘"、"阅读进度"、"论文追踪"、"论文阅读统计"、"阅读管理"、"阅读状态追踪"，或用户需要管理论文阅读状态、查看论文阅读统计时。
version: 1.0.0
---

# 论文阅读进度追踪仪表盘

创建 Obsidian Bases 仪表盘，用于追踪和管理论文阅读进度。

## When to Activate（何时启用）

- 用户说"论文仪表盘"、"阅读进度"、"论文追踪"
- 用户需要管理论文阅读状态
- 用户需要查看论文阅读统计

## 格式参考

**执行前查阅**：
- [obsidian-bases.md](./ref/obsidian-bases.md) - 获取 Bases (.base) 格式规范（视图、公式、分组排序）

## 核心执行规则（CRITICAL）

### (CRITICAL) Frontmatter 完整性
- **ALWAYS** 检查论文笔记包含必要属性
- **ALWAYS** 使用一致的属性名称
- **ALWAYS** 验证属性值格式正确

### (CRITICAL) 日期格式
- **ALWAYS** 使用 YYYY-MM-DD 格式
- **ALWAYS** 确保日期字段正确
- **NEVER** 使用其他日期格式

### (REQUIRED) 状态枚举
- **RECOMMENDED** 使用预定义状态值
- 状态：to-read、reading、done

## 核心功能

### 功能1：阅读状态追踪
- **用途**：按状态分组展示
- **分组**：待阅读、阅读中、已完成

### 功能2：领域分类管理
- **用途**：按研究领域自动分类
- **字段**：field、field_sub

### 功能3：时间线视图
- **用途**：按阅读日期排序
- **公式**：计算距今天数

### 功能4：统计汇总
- **用途**：计算阅读数量、时间分布
- **汇总**：Sum、Average、Count

## 工作流程

### Step 1: 扫描论文目录
- 使用 Glob 扫描论文笔记
- 按目录扫描或按标签筛选

### Step 2: 检查 Frontmatter 完整性
- 使用 Read 读取并检查必要属性
- **REQUIRED 字段**：status、importance、field
- 报告缺失字段

### Step 3: 生成 Base 文件
- 使用 Write 创建 .base 文件
- 定义 filters、formulas、views
- 创建多个视图满足不同需求

### Step 4: 嵌入到索引笔记
- 在索引笔记中嵌入 Base 文件
- 使用 Embeds 语法：`![[论文阅读进度.base]]`

## GOOD vs BAD（对比示例）

### 示例1：Frontmatter 验证

#### ✅ GOOD
```yaml
# 正确的 Frontmatter 字段检查
required_fields = ['status', 'importance', 'field']
for paper in papers:
    metadata = parse_frontmatter(read_file(paper))
    missing = [f for f in required_fields if f not in metadata]
    if missing:
        report_missing(paper, missing)
```

#### ❌ BAD
```yaml
# 未检查 Frontmatter 直接生成 Base
# 可能导致公式计算错误或显示异常
```

### 示例2：视图创建

#### ✅ GOOD
```yaml
# 清晰的视图定义
views:
  - type: table
    name: "阅读状态"
    groupBy:
      property: status
    order:
      - formula.status_icon
      - file.name
      - formula.importance_label
```

#### ❌ BAD
```yaml
# 视图定义混乱，缺少分组和排序
views:
  - type: table
    name: "全部"
```

### 示例3：公式使用

#### ✅ GOOD
```yaml
# 正确的状态图标公式
status_icon: 'if(status == "to-read", "📚", if(status == "reading", "📖", "✅"))'

# 正确的日期计算公式
days_reading: 'if(read_date, ((date(read_date) - date(file.ctime)) / 86400000).round(0), "")'
```

#### ❌ BAD
```yaml
# 公式语法错误
status_icon: 'if(status == "to-read", "📚", "📖", "✅")'  # if 嵌套错误

# 日期单位错误
days_reading: '(date(read_date) - date(file.ctime))'  # 结果是毫秒，不是天数
```

### 示例4：内容识别

#### ✅ GOOD
```python
# 基于目录和标签识别论文
def identify_papers(files):
    papers = []
    for file in files:
        content = read_file(file)
        # 方法1：检查目录
        if "Paper" in file.path:
            papers.append(file)
        # 方法2：检查标签
        metadata = parse_frontmatter(content)
        if "paper" in metadata.get("tags", []):
            papers.append(file)
    return papers
```

#### ❌ BAD
```python
# 简单的文件扩展名判断
papers = [f for f in files if f.endswith(".md")]  # 包含非论文文件
```

## Frontmatter 要求

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
field: "CV"
field_sub: "Generation"
read_date: 2024-01-15
read_time: 120
rating: 5
importance: core | important | extension | application
---
```

## 视图类型

| 类型 | 说明 | 用途 |
|------|------|------|
| table | 表格视图 | 详细列表，支持排序筛选 |
| cards | 卡片视图 | 封面展示，适合浏览 |
| list | 列表视图 | 简洁列表，快速浏览 |

## 快速参考表

| 视图 | 说明 | 过滤条件 |
|------|------|----------|
| 阅读状态 | 按状态分组 | status |
| 待阅读 | 未开始阅读 | status == "to-read" |
| 阅读中 | 正在阅读 | status == "reading" |
| 已完成 | 完成阅读 | status == "done" |
| 领域分类 | 按领域分组 | field |
| 核心论文 | 重要论文 | importance == "core" |
| 最近阅读 | 30天内 | read_date 最近30天 |
| 高评分论文 | 评分4+ | rating >= 4 |

## 常用公式

| 公式 | 说明 |
|------|------|
| status_icon | 状态图标转换 |
| importance_label | 重要性标签转换 |
| days_reading | 阅读进度天数 |
| is_recent | 是否最近阅读 |
| short_title | 标题截断 |
| field_full | 领域+子领域组合 |
| authors_short | 作者简写 |

## 配置选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --directory | 论文目录 | 科研/CV/Paper/ |
| --recursive | 递归扫描 | true |
| --filter | 文件名过滤器 | *.md |
