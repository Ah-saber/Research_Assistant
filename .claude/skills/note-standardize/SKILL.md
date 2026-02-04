---
name: note-standardize
description: Standardize Obsidian note formats including Callouts, Wikilinks, Frontmatter, tags, and embeds. Use when fixing note format issues, or when the user mentions "标准化笔记", "笔记格式化", "规范化笔记".
version: 1.0.0
---

# 笔记标准化 (Note Standardize)

对 Obsidian 笔记进行标准化处理，包括 Callout 格式化、Wikilink 修复、Frontmatter 管理、标签规范化、Embeds 引用等。

## When to Activate

- 用户说："标准化笔记"、"笔记格式化"、"规范化笔记"
- 检测到笔记格式问题需要修复
- 批量处理笔记目录格式

## Critical Rules (CRITICAL)

### Rule 1: Format Reference FIRST (REQUIRED)

**ALWAYS** reference [obsidian-markdown.md](./ref/obsidian-markdown.md) before creating/modifying any Obsidian format.

| Operation | Reference | Example |
|-----------|-----------|---------|
| Callout | obsidian-markdown | `> [!warning] 标题` |
| Wikilink | obsidian-markdown | `[[笔记名\|显示名]]` (表格中转义) |
| Frontmatter | obsidian-markdown | `---\ntitle: "标题"\n---` |
| Tags | obsidian-markdown | `#CV/Generation/Diffusion` |
| Embeds | obsidian-markdown | `![[笔记名]]` |

### Rule 2: Glob MUST Be Used for Wikilinks (CRITICAL)

**NEVER** assume filename format. **ALWAYS** use Glob tool to get exact filename.

```python
# ❌ BAD: Assumed filename (will break if spaces don't match)
link = f"[[{paper_title}]]"

# ✅ GOOD: Use Glob to get actual filename
pattern = f"**/*{paper_title}*.md"
matches = glob.glob(pattern, recursive=True)
if matches:
    actual_filename = matches[0]
    link = f"[[{actual_filename}|{paper_title}]]"
```

### Rule 3: Context-Aware Link Format (REQUIRED)

**MUST** detect if link is in table. Pipe character **MUST** be escaped in tables.

| Context | Format | Example |
|----------|--------|---------|
| Plain text | `\|` | `[[Flow-Based  Diffusion Model\|Flow-Based Diffusion Model]]` |
| **In table** | `\|` | `\| [[Flow-Based  Diffusion Model\|Flow-Based Diffusion Model]] \| 下一列 \|` |

```python
# ❌ BAD: Unescaped pipe in table (breaks table structure)
| [[Flow-Based Diffusion Model|Flow-Based Diffusion Model]] | 下一列 |

# ✅ GOOD: Escaped pipe in table
| [[Flow-Based  Diffusion Model\|Flow-Based Diffusion Model]] | 下一列 |
```

## 工作流程

### Step 1: 扫描分析

使用 Glob 工具扫描目标目录，使用 Read 工具读取笔记内容：

```python
# 扫描目标笔记
pattern = f"{scope}/**/*.md"
notes = glob.glob(pattern, recursive=True)

# 读取笔记内容
for note_path in notes:
    content = read_file(note_path)
    # 分析标准化需求
```

**分析内容**：
- Frontmatter: 缺失、格式不规范
- Wikilink: 失效链接、格式不规范、文件名不匹配
- 标签: 中文标签、扁平结构
- Callout机会: 关键疑惑点、风险点

### Step 2: 生成报告

```markdown
# 笔记标准化报告

## Frontmatter 分析
- 缺失: 3篇
- 格式不规范: 5篇

## Wikilink 分析
- 失效链接: 2个
- 文件名不匹配: 8个（需使用 Glob 修复）

## 标签分析
- 中文标签: 5个 → 需转换为英文层级格式
```

### Step 3: 用户确认

**执行要求**：使用 `AskUserQuestion` 工具让用户选择操作：

```markdown
请选择要执行的标准化操作：
1. 修复 Wikilink（使用 Glob 精确匹配文件名）
2. 补全 Frontmatter
3. 规范化标签（转换为英文层级结构）
4. 添加 Callout（参考 obsidian-markdown 确认格式）
5. 全部执行
```

### Step 4: 执行标准化

根据用户选择，使用 `Edit` 或 `Write` 工具执行修改：

```python
# 修复 Wikilink
for link in broken_links:
    # 使用 Glob 精确匹配
    pattern = f"**/*{link.target}*.md"
    matches = glob.glob(pattern, recursive=True)
    if matches:
        # 使用 Edit 工具修复链接
        edit_file(link.file, old_link, new_link)

# 补全 Frontmatter
for note in notes_without_frontmatter:
    # 使用 Edit 工具在文件开头添加
    frontmatter = generate_frontmatter(note)
    edit_file(note, "", frontmatter, position="start")
```

### Step 5: 验证结果

重新扫描验证修改是否正确。

## GOOD vs BAD

### ✅ GOOD: 使用 Glob 精确匹配

```python
# 修复 Wikilink 时
pattern = f"**/{paper_title}*.md"
matches = glob.glob(pattern, recursive=True)

if len(matches) == 1:
    actual_filename = matches[0]
    link = f"[[{actual_filename}|{paper_title}]]"
```

### ❌ BAD: 假设文件名格式

```python
# 直接使用论文标题创建链接（可能因空格数量不匹配而失效）
link = f"[[{paper_title}|{paper_title}]]"
```

### ✅ GOOD: 表格中转义管道符

```markdown
| [[文件名\|显示名]] | 下一列 |
```

### ❌ BAD: 表格中未转义

```markdown
| [[文件名|显示名]] | 下一列 |  ← 管道符被当作列分隔符，表格错位
```

### ✅ GOOD: 参考 obsidian-markdown 创建 Callout

```markdown
> [!warning] 关键疑惑
文章中的公式(3)与实际实现不符，需要进一步验证。
```

### ❌ BAD: 自己猜测格式

```markdown
> **关键疑惑**  ← 格式错误，无法被 Obsidian 识别为 Callout
文章中的公式(3)与实际实现不符。
```

### ✅ GOOD: 层级标签格式

```markdown
#CV/Generation/Diffusion
#CV/Architecture/Attention
#Method/Optimization/Gradient
```

### ❌ BAD: 中文扁平标签

```markdown
#扩散模型  → 应为 #CV/Generation/Diffusion
#生成模型  → 应为 #CV/Generation
#注意力控制 → 应为 #CV/Architecture/Attention
```

## 核心功能

### 1. Callout 格式化

**执行要求**：创建 Callout 时参考 obsidian-markdown skill 的语法规范。

| 类型 | 语法 | 用途 |
|------|------|------|
| warning | `> [!warning] 标题` | 关键疑惑点 |
| tip | `> [!tip] 标题` | 优化思路 |
| important | `> [!important] 标题` | 重要提醒 |
| note | `> [!note] 标题` | 一般说明 |

### 2. Wikilink 修复

**执行要求**：
1. 使用 Glob 工具精确匹配文件名
2. 检测上下文（表格 vs 普通文本）
3. 表格中必须转义管道符

### 3. Frontmatter 管理

**标准格式**：
```yaml
---
title: "笔记标题"
type: 论文
tags: [CV, Generation, Diffusion]
date: 2024-01-15
related: [["相关笔记|别名"]]
---
```

### 4. 标签规范化

**转换规则**：
```markdown
#扩散模型 → #CV/Generation/Diffusion
#生成模型 → #CV/Generation
#注意力控制 → #CV/Architecture/Attention
```

**执行要求**：使用英文术语，层级结构用 `/` 分隔。

### 5. Embeds 引用

**语法**：`![[笔记名]]`

**执行要求**：参考 obsidian-markdown skill 的 Embeds 语法。

## 快速参考

| 场景 | 命令/操作 | 格式参考 |
|------|----------|----------|
| 创建 Callout | 参考 obsidian-markdown | `> [!类型] 标题` |
| 创建 Wikilink | 使用 Glob 精确匹配 | `[[实际文件名\|显示名]]` |
| 表格中链接 | 必须转义管道符 | `[[文件名\|显示名]]` |
| 创建 Frontmatter | YAML 格式 | `---\nkey: value\n---` |
| 创建标签 | 英文层级格式 | `#一级/二级/三级` |
| 创建 Embeds | 参考 obsidian-markdown | `![[笔记名]]` |

## 使用的工具

| 工具 | 用途 | 使用场景 |
|------|------|----------|
| `Glob` | 精确匹配文件名 | 创建 Wikilink 时必须使用 |
| `Read` | 读取笔记内容 | 分析标准化需求 |
| `Write` | 创建新笔记 | 创建笔记时使用 |
| `Edit` | 修改现有笔记 | 修复格式时使用 |
| `AskUserQuestion` | 用户交互 | 执行前确认操作 |

## 注意事项

- 尊重原有内容，不删除有效信息
- 所有修改需用户确认
- 建议执行前备份
- 分步执行，逐步验证
