---
name: idea-tracker
description: Generate Obsidian Bases dashboard for tracking idea status and progress. Use when managing idea states and identifying ideas needing attention, or when the user mentions "Idea追踪", "想法管理", "Idea仪表盘".
version: 1.0.0
---

# Idea状态管理追踪仪表盘

创建 Obsidian Bases 仪表盘，用于追踪和管理研究 Idea 的状态和进展。

## When to Activate（何时启用）

- 用户说"Idea追踪"、"想法管理"、"Idea仪表盘"
- 用户需要管理 Idea 状态
- 用户需要查看 Idea 进展统计

## 格式参考

**执行前查阅**：
- [obsidian-bases.md](./ref/obsidian-bases.md) - 获取 Bases (.base) 格式规范（视图、公式、分组排序）

## 核心执行规则（CRITICAL）

### (CRITICAL) 访问控制
- **ALWAYS** Inspiration 目录可自由访问
- **NEVER** 访问 IDEA 目录（除非用户明确授权）
- **ALWAYS** 使用 AskUserQuestion 获取授权

### (CRITICAL) Frontmatter 完整性
- **ALWAYS** 检查 Idea 笔记包含必要属性
- **ALWAYS** 使用一致的属性名称
- **ALWAYS** 验证属性值格式正确

### (REQUIRED) 状态枚举
- **RECOMMENDED** 使用预定义状态值
- 状态：sprout、thinking、implemented、abandoned

## 核心功能

### 功能1：状态追踪
- **用途**：按状态分组展示
- **分组**：萌芽、思考中、已实现、已放弃

### 功能2：主题分类
- **用途**：按研究领域或主题分类
- **字段**：theme

### 功能3：时间追踪
- **用途**：计算 Idea 存在时长、最后更新时间
- **公式**：days_since_created、days_since_updated

### 功能4：行动建议
- **用途**：根据状态和时间自动生成行动建议
- **公式**：action_suggestion

## 工作流程

### Step 1: 扫描 Idea 目录
- 使用 Glob 扫描 Inspiration 目录
- **ALWAYS** 限制在 Inspiration 目录内
- IDEA 目录需要用户授权

### Step 2: 检查 Frontmatter 完整性
- 使用 Read 读取并检查必要属性
- **REQUIRED 字段**：status、priority、theme
- 报告缺失字段

### Step 3: 生成 Base 文件
- 使用 Write 创建 .base 文件
- 定义 filters、formulas、views
- 创建多个视图满足不同需求

### Step 4: 嵌入到索引笔记
- 在索引笔记中嵌入 Base 文件
- 使用 Embeds 语法：`![[Idea追踪.base]]`

## GOOD vs BAD（对比示例）

### 示例1：访问控制

#### ✅ GOOD
```python
# 正确的访问控制
inspiration_ideas = glob_search("Inspiration/**/*.md", recursive=True)

# IDEA 目录需要授权
if user_authorized:
    idea_ideas = glob_search("科研/IDEA/**/*.md", recursive=True)
```

#### ❌ BAD
```python
# 直接访问 IDEA 目录，未获取授权
idea_ideas = glob_search("科研/IDEA/**/*.md", recursive=True)
```

### 示例2：needs_attention 公式

#### ✅ GOOD
```yaml
# 正确的 needs_attention 公式
needs_attention: 'status == "thinking" && updated_date && (now() - date(updated_date)) > "7d"'

# 正确的 long_sprout 公式
long_sprout: 'status == "sprout" && created_date && (now() - date(created_date)) > "30d"'
```

#### ❌ BAD
```yaml
# 逻辑错误
needs_attention: 'status == "thinking" && updated_date > "7d"'  # 日期比较语法错误

# 缺少空值检查
long_sprout: '(now() - date(created_date)) > "30d"'  # created_date 为空时报错
```

### 示例3：状态流转

#### ✅ GOOD
```python
# 清晰的状态流转规则
def suggest_status_update(idea):
    if idea.status == "sprout":
        days_since_created = (now() - idea.created_date).days
        if days_since_created > 30:
            return "评估是否推进或标记为已放弃"
    elif idea.status == "thinking":
        days_since_updated = (now() - idea.updated_date).days
        if days_since_updated > 60:
            return "决定实施或搁置"
    return "继续推进"
```

#### ❌ BAD
```python
# 简单的时间判断，忽略状态
if idea.age > 30:
    return "需要更新状态"  # 不区分当前状态
```

### 示例4：视图设计

#### ✅ GOOD
```yaml
# 按状态分组的视图
views:
  - type: table
    name: "状态总览"
    groupBy:
      property: status
    order:
      - formula.status_icon
      - file.name
      - formula.days_since_updated
```

#### ❌ BAD
```yaml
# 缺少分组，难以查看状态分布
views:
  - type: table
    name: "全部"
    order:
      - file.name
```

## Frontmatter 要求

Idea 笔记需要包含以下属性：

```yaml
---
title: "Idea 标题"
status: sprout | thinking | implemented | abandoned
date: YYYY-MM-DD
tags: ["CV", "Generation", "Diffusion"]
theme: "生成模型"
difficulty: easy | medium | hard
feasibility: high | medium | low
priority: high | medium | low
related_papers: ["论文1", "论文2"]
created_date: 2024-01-15
updated_date: 2024-01-20
next_action: "查阅相关文献"
---
```

## 视图类型

| 类型 | 说明 | 用途 |
|------|------|------|
| table | 表格视图 | 详细列表，支持排序筛选 |
| cards | 卡片视图 | 展示 Idea 概览 |
| list | 列表视图 | 简洁列表 |

## 快速参考表

| 视图 | 说明 | 过滤条件 |
|------|------|----------|
| 状态总览 | 按状态分组 | status |
| 萌芽中的 Idea | 萌芽状态 | status == "sprout" |
| 思考中的 Idea | 思考中 | status == "thinking" |
| 需要关注 | 超过7天未更新 | needs_attention |
| 长期萌芽 | 超过30天 | long_sprout |
| 已实现 | 已完成 | status == "implemented" |
| 已放弃 | 已放弃 | status == "abandoned" |
| 高优先级 | 高优先级 | priority == "high" |
| 主题分类 | 按主题分组 | theme |

## 常用公式

| 公式 | 说明 |
|------|------|
| status_icon | 状态图标转换 |
| status_label | 状态标签（中文） |
| priority_icon | 优先级图标 |
| days_since_created | Idea 存在天数 |
| days_since_updated | 更新距今天数 |
| needs_attention | 是否需要关注 |
| long_sprout | 是否长期萌芽 |
| action_suggestion | 行动建议 |

## 颜色编码

| 状态 | 颜色 | 颜色代码 |
|------|------|----------|
| 萌芽 | 黄色 | #ffd700 |
| 思考中 | 橙色 | #ffa500 |
| 已实现 | 绿色 | #90ee90 |
| 已放弃 | 灰色 | #a9a9a9 |

## 配置选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --inspiration-dir | Inspiration 目录 | Inspiration/ |
| --idea-dir | IDEA 目录（需授权） | 科研/IDEA/ |
