---
name: idea-capture
description: Capture and record research ideas to Inspiration directory with automatic tagging and linking. Use when the user has a research thought or inspiration to save, or mentions "记录Idea", "捕捉想法", "有个想法".
version: 1.0.0
---

# Idea捕捉技能

快速记录研究想法和灵感到Inspiration目录，自动添加标签和关联内容。

## When to Activate（何时启用）

- 用户说"记录Idea"、"捕捉想法"、"记下来"、"有个想法"
- 用户说"Idea记录"
- 用户想要快速保存突发的想法
- 用户想从现有笔记中提取想法

## 格式参考

**执行前查阅**：
- [obsidian-markdown.md](./ref/obsidian-markdown.md) - 获取 Markdown 语法规范（Wikilink、Callout、Frontmatter、Tags）

## 核心执行规则（CRITICAL）

### (CRITICAL) 存储位置
- **ALWAYS** 保存到 Inspiration 目录：`C:\Note\MyNote_Obs\Inspiration\`
- **NEVER** 直接保存到 IDEA 目录（用户手动移动）
- **ALWAYS** 询问用户确认后才能访问 IDEA 目录

### (CRITICAL) 自动链接相关论文
- **ALWAYS** 使用 Glob 精确匹配文件名
- **ALWAYS** 创建 Wikilink 格式：`[[完整文件名|显示名]]`
- **NEVER** 直接使用论文标题作为文件名

### (REQUIRED) Idea笔记结构
- **ALWAYS** 包含 Frontmatter 元数据
- **ALWAYS** 包含理论动机分析（学术型Idea）
- **ALWAYS** 使用层级标签格式：`#Idea/主题/子主题`

## 核心功能

### 功能1：快速记录
- **用途**：突发的简短想法
- **格式**：Inspiration/YYYY-MM-DD-简短标题.md

### 功能2：完整想法记录
- **用途**：需要详细描述的想法
- **格式**：包含动机、可行性、相关工作的完整笔记

### 功能3：从笔记提取
- **用途**：从现有笔记中提取想法
- **工具**：Read + Glob

### 功能4：自动关联论文
- **用途**：自动链接相关论文笔记
- **工具**：Glob 搜索匹配文件

## 工作流程

### Step 1: 分析用户输入
分析用户提供的想法内容，提取关键信息：
- 核心想法
- 动机/背景
- 相关论文/方法/模型

### Step 2: 生成Idea笔记
使用 Write 工具创建 Idea 笔记：
- **ALWAYS** 包含完整的 Frontmatter
- **ALWAYS** 设置初始状态为 `sprout`
- **ALWAYS** 添加层级标签
- **完整模板**：模板结构已在本文档中定义

**REQUIRED Frontmatter 字段**：
- `title`: Idea标题
- `type`: "idea"
- `status`: "sprout" | "thinking" | "implemented" | "abandoned"
- `tags`: [标签数组]
- `created`: 创建时间 (YYYY-MM-DD)
- `updated`: 更新时间 (YYYY-MM-DD)
- `related`: [[相关笔记]]
- `priority`: "low" | "medium" | "high"

### Step 3: 自动关联论文
- **ALWAYS** 使用 Glob 精确匹配文件名
- 创建 Wikilink：`[[实际文件名|显示名]]`
- 添加到 Frontmatter 的 `related` 字段

### Step 4: 确认并提示
- 显示创建的Idea笔记路径
- 提示用户定期查看Inspiration目录
- 提示用户手动将有价值的Idea移至IDEA目录

## GOOD vs BAD（对比示例）

### 示例1：访问控制

#### ✅ GOOD
```python
# 先询问用户
user_input = ask_user("需要访问IDEA目录吗？")
if user_input == "是" or user_input == "可以":
    # 用户明确授权后才访问
    scan_idea_directory()
```

#### ❌ BAD
```python
# 直接访问IDEA目录，未询问用户
scan_idea_directory()  # 违反访问控制规则
```

### 示例2：文件名匹配

#### ✅ GOOD
```python
# 使用 Glob 精确匹配文件名
pattern = f"**/Paper/**/*{keyword}*.md"
matches = glob_search(pattern, recursive=True)
if matches:
    actual_filename = matches[0]
    link = f"[[{actual_filename}|{paper_title}]]"
```

#### ❌ BAD
```python
# 直接使用论文标题创建链接
link = f"[[{paper_title}]]"  # 文件名可能包含特殊字符
```

### 示例3：状态设置

#### ✅ GOOD
```python
# 新Idea默认状态为萌芽
status = "sprout"  # 符合Idea生命周期
```

#### ❌ BAD
```python
# 新Idea直接设置为已实现
status = "implemented"  # 不符合逻辑
```

### 示例4：模板使用

#### ✅ GOOD
```python
# 引用外部模板文件
template_path = "PLAN/references/Idea笔记参考.md"
template = read_template(template_path)
fill_template(template, user_input)
```

#### ❌ BAD
```python
# 硬编码模板内容
content = f"""
---
title: {title}
type: idea
status: sprout
...
"""  # 模板难以维护，应使用 SKILL.md 中定义的模板结构
```

## Idea状态流转

```
萌芽(sprout) -> 思考中(thinking) -> 已实现(implemented)
                    |
                    v
                  已放弃(abandoned)
```

| 状态 | 说明 |
|------|------|
| sprout | 刚萌芽的想法，未深入思考 |
| thinking | 正在思考和研究 |
| abandoned | 经评估后放弃 |
| implemented | 已实现/完成 |

## 标签规范

### 层级格式
```
#Idea                # 所有Idea
#Idea/方法           # 方法类想法
#Idea/实验           # 实验类想法
#Idea/应用           # 应用类想法
#Idea/理论           # 理论类想法
```

## Callout用法

在"挑战与风险"部分使用Callout格式化：

```markdown
> [!warning] 技术风险
当前GPU内存可能不足以支持大规模实验，需要考虑分布式训练或模型压缩。

> [!caution] 理论障碍
该方法缺乏理论保证，可能存在收敛性问题，需要理论分析支持。

> [!note] 实验限制
数据集规模有限，需要验证方法的泛化能力。
```

## 快速参考表

| 场景 | 文件位置 | 说明 |
|------|---------|------|
| 快速记录 | Inspiration/YYYY-MM-DD-标题.md | 简短想法 |
| 完整记录 | Inspiration/themes/主题/标题.md | 详细想法 |
| 临时存放 | Inspiration/ | 用户手动移至IDEA |

## 后续工作流

```
Inspiration/ (临时)     科研/IDEA/ (永久)
     ↓                      ^
   定期查看              用户手动移动
     ↓                      ^
   确认价值  ──────────>  分类存储
```

用户工作流程：
1. Ideas记录到Inspiration
2. 定期查看Inspiration目录
3. 确认有价值的Idea
4. 手动移至科研/IDEA目录
