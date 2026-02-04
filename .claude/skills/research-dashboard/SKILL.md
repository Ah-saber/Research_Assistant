---
name: research-dashboard
description: Generate comprehensive Obsidian Bases dashboard integrating papers, ideas, concepts, and projects. Use when getting a complete overview of research progress, or when the user mentions "研究仪表盘", "进度总览", "研究全景".
version: 1.0.0
---

# 综合研究进度仪表盘

创建 Obsidian Bases 仪表盘，综合展示研究进度，包括论文阅读、Idea 管理、概念笔记等。

## When to Activate（何时启用）

- 用户说"研究仪表盘"、"进度总览"、"研究全景"
- 用户需要整合多种内容类型
- 用户需要查看综合研究进度

## 格式参考

**执行前查阅**：
- [obsidian-bases.md](./ref/obsidian-bases.md) - 获取 Bases (.base) 格式规范（视图、公式、分组排序）

## 核心执行规则（CRITICAL）

### (CRITICAL) 访问控制
- **ALWAYS** 科研/Inspiration 目录可自由访问
- **NEVER** 访问 IDEA 目录（除非用户明确授权）
- **ALWAYS** 使用 AskUserQuestion 获取授权

### (CRITICAL) 内容类型标识
- **ALWAYS** 检查 content_type 属性
- **ALWAYS** 正确设置内容类型
- **NEVER** 假设所有文件都有 content_type

### (REQUIRED) Frontmatter 一致性
- **RECOMMENDED** 确保同类型内容使用相同属性名称
- **RECOMMENDED** 及时更新 updated_date 属性

## 核心功能

### 功能1：多内容类型整合
- **用途**：同时追踪论文、Idea、概念、项目
- **类型**：paper、idea、concept、project、note

### 功能2：研究主题全景
- **用途**：按研究主题分组展示
- **字段**：theme

### 功能3：进度可视化
- **用途**：时间线视图展示研究进展
- **公式**：days_since_update、is_recent

### 功能4：统计汇总
- **用途**：计算各类型内容的数量和分布
- **汇总**：按类型统计 Count

## 工作流程

### Step 1: 扫描研究相关目录
- 使用 Glob 扫描多个目录
- 目录：科研/、Inspiration/

### Step 2: 识别内容类型
- 根据文件位置和标签识别
- **ALWAYS** 为缺失 content_type 的文件添加标识

### Step 3: 检查 Frontmatter 完整性
- 检查每种内容类型的必要属性
- **REQUIRED 字段**：
  - paper: status、authors、year
  - idea: status、priority、theme
  - concept: difficulty
  - project: status、progress

### Step 4: 生成 Base 文件
- 使用 Write 创建 .base 文件
- 定义 filters、formulas、views
- 创建多类型整合视图

### Step 5: 嵌入到索引笔记
- 在研究总览笔记中嵌入 Base 文件
- 使用 Embeds 语法：`![[研究进度仪表盘.base]]`

## GOOD vs BAD（对比示例）

### 示例1：内容类型识别

#### ✅ GOOD
```python
# 正确的内容类型识别
for file in all_files:
    content_type = identify_type(file)
    metadata = parse_frontmatter(read_file(file))
    if 'content_type' not in metadata:
        metadata['content_type'] = content_type
        # 更新文件或添加到公式中
```

#### ❌ BAD
```python
# 假设所有文件都有 content_type
# 未识别可能导致内容类型错误
```

### 示例2：多类型整合

#### ✅ GOOD
```python
# 分别处理不同类型，统一数据格式
papers = collect_papers()
ideas = collect_ideas()
concepts = collect_concepts()

all_items = []
all_items.extend(format_as_dashboard_items(papers, "paper"))
all_items.extend(format_as_dashboard_items(ideas, "idea"))
all_items.extend(format_as_dashboard_items(concepts, "concept"))
```

#### ❌ BAD
```python
# 混合处理不同类型
for item in all_items:
    if item.type == "paper":
        # 论文处理
    elif item.type == "idea":
        # Idea处理
    # 类型判断混乱，容易出错
```

### 示例3：视图设计

#### ✅ GOOD
```yaml
# 按内容类型分组的视图
views:
  - type: table
    name: "全部内容"
    groupBy:
      property: content_type
    order:
      - formula.type_icon
      - file.name
      - formula.status_icon
```

#### ❌ BAD
```yaml
# 缺少分组，难以区分内容类型
views:
  - type: table
    name: "全部"
    order:
      - file.name
```

### 示例4：内容类型识别算法

#### ✅ GOOD
```python
# 多种方法组合识别
def identify_content_type(file):
    content = read_file(file)
    metadata = parse_frontmatter(content)

    # 方法1：显式 content_type
    if 'content_type' in metadata:
        return metadata['content_type']

    # 方法2：基于目录
    if 'Paper' in file.path:
        return 'paper'
    elif 'Inspiration' in file.path:
        return 'idea'
    elif 'Concepts' in file.path:
        return 'concept'

    # 方法3：基于标签
    tags = metadata.get('tags', [])
    if 'paper' in tags:
        return 'paper'
    elif 'idea' in tags:
        return 'idea'

    return 'note'  # 默认
```

#### ❌ BAD
```python
# 仅基于单一判断
def identify_content_type(file):
    if 'Paper' in file.path:
        return 'paper'
    else:
        return 'note'  # 误判率极高
```

## Frontmatter 要求

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

# Idea 特有属性
# status: sprout | thinking | implemented | abandoned
# priority: high | medium | low

# 项目笔记特有属性
# status: planning | active | completed | archived
# progress: 0-100
```

## 视图类型

| 类型 | 说明 | 用途 |
|------|------|------|
| table | 表格视图 | 详细列表，支持排序筛选 |
| cards | 卡片视图 | 内容概览 |
| list | 列表视图 | 简洁列表 |

## 快速参考表

| 视图 | 说明 | 过滤条件 |
|------|------|----------|
| 全部内容 | 按类型分组 | content_type |
| 活跃内容 | 正在进行 | is_active |
| 最近更新 | 7天内更新 | is_recent |
| 论文研究 | 论文类型 | content_type == "paper" |
| Idea 管理 | Idea类型 | content_type == "idea" |
| 概念笔记 | 概念类型 | content_type == "concept" |
| 项目追踪 | 项目类型 | content_type == "project" |
| 主题全景 | 按主题分组 | theme |
| 核心内容 | 高链接 | link_count > 2 |
| 待处理 | 待开始 | 状态相关 |

## 常用公式

| 公式 | 说明 |
|------|------|
| type_icon | 内容类型图标 |
| type_label | 内容类型标签（中文） |
| status_icon | 状态图标（根据类型） |
| days_since_update | 更新距今天数 |
| is_recent | 是否最近更新（7天内） |
| is_active | 是否活跃 |
| link_count | 相关内容数量 |
| backlink_count | 被链接数 |

## 与其他仪表盘的关系

| 技能 | 范围 | 说明 |
|------|------|------|
| /paper-dashboard | 论文 | 专注论文阅读进度 |
| /idea-tracker | Idea | 专注 Idea 状态管理 |
| /research-dashboard | 全部 | 整合所有研究内容 |

## 配置选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --directories | 扫描目录 | 科研/, Inspiration/ |
| --content-types | 内容类型 | paper,idea,concept,project,note |
