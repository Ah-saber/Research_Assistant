---
name: idea-review
description: Review and manage ideas in Inspiration directory with filtering, sorting, and action suggestions. Use when checking on existing ideas, or when the user mentions "回顾Idea", "查看想法".
version: 1.0.0
---

# Idea回顾技能

回顾Inspiration目录中的Idea，按不同维度查看和评估，提供行动建议。

## When to Activate（何时启用）

- 用户说"回顾Idea"、"查看想法"、"Idea回顾"
- 用户说"查看Inspiration"、"我的想法"
- 用户想查看Inspiration中的Idea
- 用户需要评估Idea价值

## 格式参考

**执行前查阅**：
- [obsidian-markdown.md](./ref/obsidian-markdown.md) - 获取 Markdown 语法规范（Frontmatter、Wikilink）
- [obsidian-bases.md](./ref/obsidian-bases.md) - 当Idea数量较多时，建议调用仪表盘技能

## 核心执行规则（CRITICAL）

### (CRITICAL) 访问控制
- **ALWAYS** 仅回顾 Inspiration 目录
- **NEVER** 访问 IDEA 目录（除非用户明确授权）
- **ALWAYS** 使用 AskUserQuestion 获取授权

### (CRITICAL) 只读模式
- **ALWAYS** 不修改Idea状态（除非用户明确指示）
- **ALWAYS** 建议仅供参考
- **NEVER** 自动删除或合并Idea
- **NEVER** 自动修改状态

### (REQUIRED) 行动建议
- **RECOMMENDED** 根据Idea状态提供建议
- **RECOMMENDED** 建议调用仪表盘技能（当Idea数量多时）

## 核心功能

### 功能1：按状态筛选
- **用途**：查看特定状态的Idea
- **状态**：sprout、thinking、implemented、abandoned

### 功能2：按时间排序
- **用途**：查看最新或长期未更新的Idea
- **排序**：最新创建、最近更新、长期未更新

### 功能3：按主题分组
- **用途**：按研究领域查看Idea
- **分组**：深度学习、实验想法、理论思考等

### 功能4：行动建议
- **用途**：根据Idea内容提供建议
- **类型**：阅读建议、实验建议、笔记建议、状态更新建议

### 功能5：仪表盘建议
- **用途**：当Idea数量多时，建议生成仪表盘
- **触发**：Idea数量 > 10个

## 工作流程

### Step 1: 扫描Inspiration目录
- 使用 Glob 扫描所有 Idea 笔记
- **ALWAYS** 限制在 Inspiration 目录内

### Step 2: 读取并解析Idea
- 使用 Read 读取每个文件
- 提取 Frontmatter：status、priority、tags、created、updated
- 提取标题、核心想法、相关工作

### Step 3: 按条件筛选和排序
- 按状态筛选
- 按时间排序
- 按优先级排序

### Step 4: 生成回顾报告
- 概览统计：总数、新增、待推进
- 按状态分组
- 长期未更新
- 高优先级Idea
- 行动建议汇总
- 仪表盘建议

### Step 5: 交互操作
- 输入序号查看详情
- 输入序号+状态更新状态（需用户确认）
- 输入 "done" 完成回顾

### Step 6: 生成行动建议清单
- 立即行动（高优先级）
- 本周计划
- 本月计划
- 仪表盘追踪建议
- 待移至IDEA

## GOOD vs BAD（对比示例）

### 示例1：只读模式

#### ✅ GOOD
```python
# 只读模式，不修改
for idea in ideas:
    display_idea_summary(idea)
    # 不自动修改状态

# 建议仅供参考
suggestions = generate_suggestions(idea)
display("建议仅供参考，请自行判断")
```

#### ❌ BAD
```python
# 自动修改状态
for idea in ideas:
    if idea.age > 30:
        idea.status = "abandoned"  # 未经用户同意
```

### 示例2：访问控制

#### ✅ GOOD
```python
# 先询问用户
user_input = ask_user("是否访问IDEA目录？", ["是", "否"])
if user_input == "是":
    idea_files = scan_idea_directory()
else:
    idea_files = []
```

#### ❌ BAD
```python
# 直接访问IDEA目录
idea_files = scan_idea_directory()  # 违反访问控制
```

### 示例3：筛选逻辑

#### ✅ GOOD
```python
# 灵活的多条件筛选
def filter_ideas(ideas, status=None, priority=None, theme=None):
    filtered = ideas
    if status:
        filtered = [i for i in filtered if i.status == status]
    if priority:
        filtered = [i for i in filtered if i.priority == priority]
    if theme:
        filtered = [i for i in filtered if i.theme == theme]
    return filtered
```

#### ❌ BAD
```python
# 硬编码筛选条件
filtered = [i for i in ideas if i.status == "sprout" and i.priority == "high"]
```

### 示例4：排序逻辑

#### ✅ GOOD
```python
# 多维度排序支持
def sort_ideas(ideas, sort_by="created"):
    if sort_by == "created":
        return sorted(ideas, key=lambda x: x.created, reverse=True)
    elif sort_by == "updated":
        return sorted(ideas, key=lambda x: x.updated, reverse=True)
    elif sort_by == "priority":
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(ideas, key=lambda x: priority_order[x.priority])
```

#### ❌ BAD
```python
# 单一排序方式
sorted_ideas = sorted(ideas, key=lambda x: x.created)
```

## 行动建议生成规则

### 阅读建议
```
当Idea包含未读相关工作时：
-> 建议：阅读[[论文X]]以了解该方法
-> 预期：更好地评估Idea可行性
```

### 实验建议
```
当Idea是实验类且状态为思考中时：
-> 建议：设计小规模实验验证
-> 方向：对比baseline效果
-> 预期：初步验证想法有效性
```

### 笔记建议
```
当Idea相关但缺少详细笔记时：
-> 建议：创建详细笔记记录思考过程
-> 内容：动机、方法、预期结果
```

### 状态更新建议
```
根据Idea状态和时间：
- 萌芽超过30天 -> 评估是否推进
- 思考中超过60天 -> 决定实施或搁置
- 长期无更新 -> 确认是否仍相关
```

## 仪表盘建议触发条件

| 条件 | 建议 |
|------|------|
| Idea数量 > 10个 | 调用 `/idea-tracker` 生成状态追踪仪表盘 |
| 需要全景视图 | 调用 `/research-dashboard` 生成综合研究进度仪表盘 |
| 需要按主题/状态/优先级筛选 | 建议使用仪表盘的多视图功能 |

## 输入参数

| 参数 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| filter | 筛选条件 | 否 | 全部 |
| sort | 排序方式 | 否 | 时间 |
| status | 状态筛选 | 否 | - |
| limit | 显示数量 | 否 | 20 |

## 快速参考表

| 操作 | 命令 | 说明 |
|------|------|------|
| 全部回顾 | /idea-review | 显示所有Idea |
| 按状态 | /idea-review --status sprout | 筛选特定状态 |
| 按主题 | /idea-review --theme 深度学习 | 主题分组 |
| 快速查看 | 查看最近的想法 | 最近7天 |

## 状态流转建议

根据Idea状态和时间提供建议：
- 萌芽超过30天 -> 评估是否推进
- 思考中超过60天 -> 决定实施或搁置
- 长期无更新 -> 确认是否仍相关

## 移至IDEA建议

回顾时提示：
```
以下Idea建议移至科研/IDEA：
1. 已实现的Idea（3个）
2. 高价值思考中Idea（2个）

移至IDEA前请确保：
- [ ] 内容完整
- [ ] 有详细思考
- [ ] 有明确价值

手动移至：科研/IDEA/相应主题目录
```
