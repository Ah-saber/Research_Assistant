---
name: idea-organize
description: Organize and classify ideas in Inspiration directory with tag normalization, deduplication, and grouping. Use when managing accumulated ideas, or when the user mentions "整理Idea", "分类想法".
version: 1.0.0
---

# Idea整理技能

整理Inspiration目录中的Idea，包括标签规范化、分组整理、去重识别等。

## When to Activate（何时启用）

- 用户说"整理Idea"、"分类想法"、"Idea整理"
- 用户说"整理Inspiration"
- 用户需要清理Inspiration目录
- 用户需要检查重复的Idea

## 格式参考

**执行前查阅**：
- [obsidian-markdown.md](./ref/obsidian-markdown.md) - 获取 Markdown 语法规范（Frontmatter、Wikilink、Tags）

## 核心执行规则（CRITICAL）

### (CRITICAL) 访问控制
- **ALWAYS** 仅整理 Inspiration 目录
- **NEVER** 访问 IDEA 目录（除非用户明确授权）
- **ALWAYS** 使用 AskUserQuestion 获取授权

### (CRITICAL) 用户确认
- **ALWAYS** 先生成整理报告
- **ALWAYS** 等待用户确认后执行
- **NEVER** 直接修改或删除内容

### (REQUIRED) 执行模式
- **RECOMMENDED** dry_run=true（仅预览）
- 需确认的操作：合并Idea、状态更新
- 安全操作：标签格式化

## 核心功能

### 功能1：标签规范化
- **用途**：统一Idea标签格式
- **格式**：层级标签 `#Idea/主题`
- **工具**：Edit + Glob

### 功能2：分组整理
- **用途**：按主题/状态/时间分组
- **输出**：整理报告

### 功能3：去重识别
- **用途**：检测相似或重复的Idea
- **阈值**：相似度 ≥ 75%

### 功能4：状态更新建议
- **用途**：根据时间和内容建议状态更新
- **规则**：萌芽>30天需评估

## 工作流程

### Step 1: 扫描Inspiration目录
- 使用 Glob 扫描所有 Idea 笔记
- **ALWAYS** 限制在 Inspiration 目录内

### Step 2: 分析每个Idea
- 使用 Read 读取每个文件
- 提取 Frontmatter：status、priority、tags
- 提取标题、内容、时间、链接

### Step 3: 识别整理需求
- 标签需要规范化：`#idea` → `#Idea`
- 重复Idea：计算相似度
- 状态需要更新：长期未更新的Idea
- 同义词标签：`#实验想法` → `#Idea/实验`

### Step 4: 生成整理报告
- 概览统计：总数、新增、状态分布
- 按主题分组
- 重复检测结果
- 状态更新建议
- 标签规范化建议
- 操作建议汇总

### Step 5: 等待用户确认
- 使用 AskUserQuestion 询问用户
- 选项：全部执行、选择执行、取消

### Step 6: 执行整理操作
- 标签规范化
- 合并重复Idea
- 状态更新

### Step 7: 生成整理结果
- 显示整理后的结果摘要

## GOOD vs BAD（对比示例）

### 示例1：用户确认

#### ✅ GOOD
```python
# 先生成报告，等待确认
report = generate_organize_report(ideas)
display(report)
user_choice = ask_user("确认执行整理？", ["全部执行", "选择执行", "取消"])
if user_choice == "全部执行":
    execute_organize()
```

#### ❌ BAD
```python
# 直接修改，未询问用户
for idea in ideas:
    edit_file(idea, new_content)  # 用户可能不希望这样修改
```

### 示例2：相似度计算

#### ✅ GOOD
```python
# 多维度综合评估
similarity = (
    title_similarity * 0.3 +
    content_similarity * 0.5 +
    tag_overlap * 0.2
)
threshold = 0.75
if similarity >= threshold:
    suggest_merge()
```

#### ❌ BAD
```python
# 仅标题相似度判断
if title_similarity > 0.7:
    merge_ideas()  # 可能误判
```

### 示例3：合并策略

#### ✅ GOOD
```python
# 保留更完整、更新的版本
def choose_merge_version(idea1, idea2):
    # 选择内容更完整的版本
    if len(idea1.content) > len(idea2.content):
        primary = idea1
        merged_from = idea2
    else:
        primary = idea2
        merged_from = idea1

    # 记录合并来源
    primary.frontmatter['merged_from'] = merged_from.file
    # 保留原始创建时间
    primary.frontmatter['created'] = min(idea1.created, idea2.created)
    return primary
```

#### ❌ BAD
```python
# 随机选择版本
primary = random.choice([idea1, idea2])  # 可能丢失重要信息
```

### 示例4：访问控制

#### ✅ GOOD
```python
# 询问用户后访问IDEA目录
user_authorize = ask_user("是否访问IDEA目录？", ["是", "否"])
if user_authorize == "是":
    idea_files = scan_idea_directory()
else:
    idea_files = []
```

#### ❌ BAD
```python
# 直接访问IDEA目录
idea_files = scan_idea_directory()  # 违反访问控制
```

## 去重规则

### 相似度计算
```
相似度 = 标题相似 * 0.3 + 内容相似 * 0.5 + 标签重叠 * 0.2

阈值：≥75% 建议合并
```

### 合并策略
- 保留：更完整、更新的版本
- 记录：在frontmatter添加`merged_from`字段
- 追溯：保留原始创建时间

## 标签规范

### 层级格式
```
#Idea                # 所有Idea
#Idea/方法           # 方法类想法
#Idea/实验           # 实验类想法
#Idea/应用           # 应用类想法
#Idea/理论           # 理论类想法
```

### 同义词映射
```
#idea, #想法, #思考 → #Idea
#实验, #实验想法 → #Idea/实验
#方法, #方法想法 → #Idea/方法
```

## 输入参数

| 参数 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| scope | 整理范围 | 否 | Inspiration全部 |
| dry_run | 仅预览 | 否 | true |
| group_by | 分组方式 | 否 | 主题 |

## 操作类型

| 类型 | 说明 | 需确认 |
|------|------|--------|
| 安全 | 标签格式化 | 否 |
| 需确认 | 合并Idea、状态更新 | 是 |
| 需审核 | 删除内容 | 是 |

## 快速参考表

| 操作 | 命令 | 说明 |
|------|------|------|
| 完整整理 | /idea-organize | 扫描、分析、报告 |
| 按主题 | /idea-organize --group_by 主题 | 主题分组 |
| 去重检查 | /idea-organize --focus duplicate | 仅检查重复 |

## 整理后建议

整理完成后建议：
- 查看整理结果
- `/idea-review` - 回顾整理后的Idea
- 将有价值的Idea移至IDEA目录
- 更新Idea状态
