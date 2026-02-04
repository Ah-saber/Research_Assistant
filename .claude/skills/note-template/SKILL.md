---
name: note-template
description: Create standard templates for different note types including paper notes, concept notes, project notes, and index notes. Use when starting new notes with consistent structure, or when the user mentions "创建笔记模板", "笔记模板".
version: 1.0.0
---

# 笔记模板 (Note Template)

为不同类型的笔记创建标准模板，包括 Frontmatter、结构格式和示例内容。

## When to Activate

- 用户说："创建笔记模板"、"新笔记格式"、"创建xxx笔记"
- 需要创建特定类型的新笔记
- 需要为笔记库建立标准格式

## Critical Rules (CRITICAL)

### Rule 1: Index Notes MUST Use Tables (CRITICAL)

**索引笔记必须使用表格格式**（便于 Dataview 自动索引）：

```python
# ❌ BAD: 使用列表格式
## Flow-based 方法
- FlowEdit - ICCV 2023
- Flow-Based Diffusion - ICLR 2024

# ✅ GOOD: 使用表格格式
## Flow-based 方法

| 论文 | 会议 | 方法类型 | 状态 |
|------|------|----------|------|
| [[FlowEdit：Inversion-Free  Text-Based Editing\|FlowEdit]] | ICCV 2023 | Flow模型 | 已读完 |
| [[Flow-Based  Diffusion Model\|Flow-Based Diffusion]] | ICLR 2024 | Flow+Diffusion | 已读完 |
```

### Rule 2: Pipe Escape in Tables (CRITICAL)

**表格中带别名的 Wikilink 必须转义管道符**：

| 情况 | 格式 |
|------|------|
| 无别名 | `[[笔记名称]]` |
| 有别名 | `[[笔记名称\|显示名]]` |

```python
# ❌ BAD: 表格中未转义
| [[FlowEdit|FlowEdit]] | 说明 |

# ✅ GOOD: 表格中转义
| [[FlowEdit：Inversion-Free  Text-Based Editing\|FlowEdit]] | 说明 |
```

### Rule 3: Reference Template Files (REQUIRED)

**完整模板内容参考 [./ref/](./ref/) 目录**：

| 笔记类型 | 参考文件 |
|----------|----------|
| 论文笔记 | [论文笔记参考.md](./ref/论文笔记参考.md) |
| 概念笔记 | [概念笔记参考.md](./ref/概念笔记参考.md) |
| 项目笔记 | [项目笔记参考.md](./ref/项目笔记参考.md) |
| 日志笔记 | [日志笔记参考.md](./ref/日志笔记参考.md) |
| 索引笔记 | [索引笔记参考.md](./ref/索引笔记参考.md) |

### Rule 4: User Confirmation Required (REQUIRED)

**必须使用 `AskUserQuestion` 让用户选择笔记类型**：

```markdown
请选择要创建的笔记类型：
1. 论文笔记（阅读论文后记录）
2. 概念笔记（解释概念、定义）
3. 项目笔记（记录项目进度）
4. 日志笔记（日常记录）
5. 索引笔记（组织主题相关笔记，**必须使用表格格式**）
```

## 工作流程

### Step 1: 询问笔记类型

使用 `AskUserQuestion` 让用户选择：

```python
# 询问笔记类型
note_type = ask_user(
    "请选择笔记类型",
    options=["论文", "概念", "项目", "日志", "索引"]
)
```

### Step 2: 收集基本信息

```python
# 收集必要信息
title = ask_user("笔记标题")
tags = ask_user("标签（可选）")

# 根据类型收集特定信息
if note_type == "论文":
    authors = ask_user("作者（可选）")
    venue = ask_user("会议/期刊（可选）")
```

### Step 3: 生成模板

```python
# 根据类型生成模板内容
template = generate_template(note_type, {
    "title": title,
    "tags": tags,
    "date": datetime.now().strftime("%Y-%m-%d"),
    # 其他字段...
})
```

### Step 4: 使用 Write 创建笔记

```python
# 使用 Write 工具创建新笔记
file_path = f"{target_dir}/{title}.md"
write_file(file_path, template)
```

### Step 5: 提醒用户完善内容

```markdown
模板已创建！请完善以下内容：
- [ ] 填写详细信息
- [ ] 添加相关链接（使用 Glob 精确匹配文件名）
- [ ] 根据需要添加标签
```

## GOOD vs BAD

### ✅ GOOD: 索引笔记使用表格格式

```markdown
## 1. Flow-based 方法

| 论文 | 会议 | 方法类型 | 状态 |
|------|------|----------|------|
| [[FlowEdit：Inversion-Free  Text-Based Editing\|FlowEdit]] | ICCV 2023 | Flow模型 | 已读完 |
| [[Flow-Based  Diffusion Model\|Flow-Based Diffusion]] | ICLR 2024 | Flow+Diffusion | 已读完 |
```

### ❌ BAD: 索引笔记使用列表格式

```markdown
## Flow-based 方法
- [[FlowEdit]] - ICCV 2023
- [[Flow-Based Diffusion]] - ICLR 2024
```

### ✅ GOOD: 表格中转义管道符

```markdown
| [[FlowEdit：Inversion-Free  Text-Based Editing\|FlowEdit]] | ICCV 2023 | Flow模型 |
| [[Flow-Based  Diffusion Model\|Flow-Based Diffusion]] | ICLR 2024 | Flow+Diffusion |
```

### ❌ BAD: 表格中未转义

```markdown
| [[FlowEdit|FlowEdit]] | ICCV 2023 | Flow模型 |  ← 表格错位
```

### ✅ GOOD: 参考 obsidian-markdown 创建 Callout

```markdown
> [!warning] 关键疑惑
需要进一步验证的公式或概念。
```

### ❌ BAD: 自己猜测格式

```markdown
> **关键疑惑**  ← 格式错误，无法被识别为 Callout
需要验证的内容。
```

## 核心功能

### 1. 笔记类型

| 类型 | 用途 | 参考文件 |
|------|------|----------|
| 论文笔记 | 阅读学术论文后记录 | [论文笔记参考.md](./ref/论文笔记参考.md) |
| 概念笔记 | 解释概念、定义、术语 | [概念笔记参考.md](./ref/概念笔记参考.md) |
| 项目笔记 | 记录项目进度、实验、代码 | [项目笔记参考.md](./ref/项目笔记参考.md) |
| 日志笔记 | 日常记录、学习日志 | [日志笔记参考.md](./ref/日志笔记参考.md) |
| 索引笔记 | 组织和链接相关主题的笔记 | [索引笔记参考.md](./ref/索引笔记参考.md) |

### 2. Frontmatter 规范

```yaml
---
title: "笔记标题"
type: [paper|concept|project|daily|index]
tags: [标签1, 标签2]
date: 2024-01-15
status: [reading|draft|done|active]
related: []
created: 2024-01-15
updated: 2024-01-15
---
```

### 3. 索引笔记模板（重要）

**索引笔记必须使用表格格式！**

参考：[索引笔记参考.md](./ref/索引笔记参考.md)

```markdown
---
title: "主题索引"
type: index
tags: [索引, 主题]
date: {{日期}}
related: [["相关主题"]]
---

# 主题索引

本索引整合了主题相关的所有笔记。

## 1. 分类1

| 笔记 | 说明 |
|------|------|
| [[笔记名称]] | 笔记说明 |
| [[笔记名称\|显示名]] | 笔记说明 |  ← 有别名时需要转义

## 2. 分类2

| 时间/类别 | 笔记 |
|----------|------|
| 时间/类别名 | [[笔记名称]] |

## 相关主题

- [[相关主题]] - 说明

## 更新记录

- {{日期}}: 创建索引笔记
```

### 4. 论文笔记模板（核心）

参考：[论文笔记参考.md](./ref/论文笔记参考.md)

```markdown
---
title: "{{论文标题}}"
type: paper
authors: []
year: {{年份}}
venue: ""
tags: [CV, {{主题}}]
date: {{日期}}
status: reading
zotero_key: ""
related: []
category: {{子领域}}
---

## MyPoint

### 我的思考

### 疑惑与问题

### TODO
- [ ]

## 概率框架分析

### 概率建模

### 信息论视角

### 生成式/判别式

### 贝叶斯视角

## 论文笔记

### 基本信息

### 研究背景

### 研究问题

### 创新方法

### 主要公式

### 实验结果

### 总结与评价

## 相关工作关联

## 方法论深度剖析

## 实验与评价
```

## 使用的工具

| 工具 | 用途 |
|------|------|
| `Write` | 创建新笔记文件 |
| `AskUserQuestion` | 确认笔记类型和参数 |

## 注意事项

- 模板中的变量需要用户填写
- 创建后提醒用户完善内容
- 参考完整模板内容位于 [./ref/](./ref/) 目录
- 索引笔记必须使用表格格式
- 表格中的 Wikilink 需要转义管道符
