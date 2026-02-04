---
name: paper-notes
description: Create complete Obsidian notes for research papers with metadata, abstract, formulas, probability framework analysis, and personal reflections (MyPoint). Use when the user finishes reading a paper and wants to save notes, or mentions "创建论文笔记", "为论文写笔记", "论文笔记".
version: 1.0.0
---

# 论文笔记 (Paper Notes)

为论文创建完整的Obsidian笔记，包含元数据、摘要、公式、概率框架分析和个人思考。

## When to Activate

- 用户说："创建论文笔记"、"为论文写笔记"
- 用户说："生成论文笔记"、"论文笔记"
- 用户阅读完论文后需要保存笔记

## Critical Rules (CRITICAL)

### Rule 1: Check Existing Notes (REQUIRED)

**MUST** check for existing notes before creating:

```python
# ✅ GOOD: 检查是否已有笔记
pattern = f"**/*{paper_title}*.md"
matches = glob.glob(pattern, recursive=True)

if matches:
    return f"发现已有笔记：{matches[0]}。是否覆盖或追加？"

# ❌ BAD: 直接创建（可能覆盖已有笔记）
write_file(f"{paper_title}.md", content)
```

### Rule 2: Glob for Wikilinks (CRITICAL)

**NEVER** assume filename format. **ALWAYS** use Glob:

```python
# ✅ GOOD: 使用 Glob 精确匹配
pattern = f"**/*{concept_name}*.md"
matches = glob.glob(pattern, recursive=True)

if matches:
    actual_filename = matches[0]
    link = f"[[{actual_filename}|{concept_name}]]"

# ❌ BAD: 假设文件名
link = f"[[{concept_name}]]"  # 可能因空格不匹配而失效
```

### Rule 3: Reference Format Skills (REQUIRED)

**执行要求**：创建笔记前参考以下格式技能：

| 操作 | 参考技能 | 语法示例 |
|------|----------|----------|
| Callout | obsidian-markdown | `> [!warning] 标题` |
| Wikilink | obsidian-markdown | `[[笔记名\|显示名]]` |
| Embeds | obsidian-markdown | `![[笔记名]]` |
| Frontmatter | obsidian-markdown | `---\nkey: value\n---` |

### Rule 4: Abstract-First Strategy (CRITICAL)

**ALWAYS** use abstract first, fulltext as fallback:

```python
# ✅ GOOD: 优先摘要
metadata = mcp__zotero__zotero_get_item_metadata(item_key)
abstract = metadata.get("abstract", "")

if abstract:
    content = generate_from_abstract(abstract)
    quality = "abstract"
else:
    fulltext = mcp__zotero__zotero_get_item_fulltext(item_key)
    content = generate_from_fulltext(fulltext)
    quality = "full"

# ❌ BAD: 直接使用全文
fulltext = mcp__zotero__zotero_get_item_fulltext(item_key)  # 可能超限
```

## 工作流程

### Step 1: 获取论文信息

```python
# 获取元数据（总是成功）
metadata = mcp__zotero__zotero_get_item_metadata(item_key)
title = metadata["title"]
authors = metadata["authors"]
year = metadata["year"]
abstract = metadata.get("abstract", "")
```

### Step 2: 检查现有笔记

```python
# ✅ GOOD: 检查是否已有笔记
pattern = f"**/*{title}*.md"
matches = glob.glob(pattern, recursive=True)

if matches:
    print(f"发现已有笔记：{matches[0]}")
    print("是否覆盖、追加或取消？")
    # 等待用户确认

# ❌ BAD: 直接创建，可能覆盖已有内容
write_file(f"{title}.md", content)
```

### Step 3: 生成笔记内容

```python
# 优先使用摘要
if abstract:
    content = generate_note_content(metadata, abstract)
    quality = "abstract"
else:
    # 降级到全文
    try:
        fulltext = mcp__zotero__zotero_get_item_fulltext(item_key)
        content = generate_note_content(metadata, fulltext)
        quality = "full"
    except TokenLimitError:
        content = generate_basic_note(metadata)
        quality = "basic"
```

### Step 4: 创建笔记文件

```python
# 使用 Write 工具创建
filename = f"{title}.md"
filepath = f"{target_dir}/{filename}"

write_file(filepath, content)
print(f"笔记已创建：{filepath}")
```

### Step 5: 添加相关链接

```python
# 使用 Glob 精确匹配创建 Wikilink
for related_concept in concepts:
    pattern = f"**/*{related_concept}*.md"
    matches = glob.glob(pattern, recursive=True)

    if matches:
        actual_filename = matches[0]
        link = f"[[{actual_filename}|{related_concept}]]"
        # 添加到笔记
```

## GOOD vs BAD

### ✅ GOOD: 使用 Glob 精确匹配

```python
# 创建 Wikilink 时
pattern = f"**/*{paper_title}*.md"
matches = glob.glob(pattern, recursive=True)

if len(matches) == 1:
    actual_filename = matches[0]
    link = f"[[{actual_filename}|{paper_title}]]"
```

### ❌ BAD: 假设文件名格式

```python
# 直接使用标题创建链接（可能因空格数量不匹配而失效）
link = f"[[{paper_title}|{paper_title}]]"
```

### ✅ GOOD: 检查笔记是否已存在

```python
pattern = f"**/*{title}*.md"
matches = glob.glob(pattern, recursive=True)

if matches:
    print(f"发现已有笔记：{matches[0]}")
    print("是否覆盖、追加或取消？")
    # 等待用户确认
```

### ❌ BAD: 直接覆盖已有笔记

```python
# 直接创建，可能覆盖已有内容
write_file(f"{title}.md", content)
```

### ✅ GOOD: 使用 Callout 标记关键疑惑

```markdown
> [!warning] 关键疑惑
文章中的公式(3)推导过程不清晰，需要查阅原始文献验证。

> [!note] 需要验证
实验设置中batch size的选择缺乏消融实验支持。
```

### ❌ BAD: Callout 格式错误

```markdown
> **关键疑惑**  ← 格式错误，无法被识别为 Callout
文章中的公式(3)推导过程不清晰。
```

### ✅ GOOD: 处理特殊字符文件名

```python
# 处理文件名中的特殊字符
safe_filename = title.replace("/", "-").replace(":", "-")
safe_filename = safe_filename.replace("<", "").replace(">", "")

# 使用处理后的文件名
filepath = f"{target_dir}/{safe_filename}.md"
```

### ❌ BAD: 直接使用原始标题

```python
# 标题中的特殊字符可能导致路径错误
filepath = f"{target_dir}/{title}.md"
# 如果 title = "Attention: Is All You Need?" 可能导致路径错误
```

### ✅ GOOD: 全文超限时降级

```python
try:
    fulltext = mcp__zotero__zotero_get_item_fulltext(item_key)
    content = generate_from_fulltext(fulltext)
except TokenLimitError:
    # 降级到摘要
    abstract = metadata.get("abstract", "")
    content = generate_from_abstract(abstract)
    print("**注意**：全文超token限制，使用摘要生成。")
```

### ❌ BAD: 超限后直接失败

```python
fulltext = mcp__zotero__zotero_get_item_fulltext(item_key)
# 如果超限，直接报错，没有降级策略
```

## 笔记结构

### Frontmatter

```yaml
---
title: "论文标题"
authors: [作者1, 作者2]
year: 2024
venue: "会议/期刊名"
tags: [CV, Generation, Diffusion]
date: 2024-01-15
status: reading
zotero_key: XXXXX
related: []
---
```

### MyPoint（个人思考）

```markdown
## MyPoint

### 我的思考
- 论文给我的启发
- 与我研究的关系

### 疑惑与问题
> [!warning] 关键疑惑
不理解的地方

### TODO
- [ ] 阅读引用的论文X
- [ ] 复现实验Y
```

### 概率框架分析（如适用）

```markdown
## 概率框架分析

### 概率建模
- **似然函数**：$p(x|z)$ 的形式
- **后验推断**：$p(z|x)$ 的推断目标
- **变分推断**：ELBO、KL散度

### 信息论视角
- **目标函数**：互信息最大化、KL散度最小化
- **熵的作用**：熵正则化、不确定性建模

### 生成式/判别式
- **模型类型**：生成式 $p(x,y)$ vs 判别式 $p(y|x)$

### 贝叶斯视角
- **先验选择**：隐含或显式的先验假设
- **推断方法**：变分推断、MCMC、MAP
```

### 论文笔记（深入研究）

```markdown
## 论文笔记

### 基本信息
- 论文标题（中英）
- 作者与机构
- 发表信息

### 研究背景
- 领域现状
- 相关工作

### 研究问题
- 核心问题
- 现有方法不足

### 创新方法
- 核心方法
- 技术细节
- 模型架构

### 主要公式
```
公式1：Attention(Q,K,V) = softmax(QK^T/√d_k)V
```

### 实验结果
- 实验设置
- 主要结果

### 总结与评价
- 主要贡献
- 方法局限性
```

### Embeds 引用

```markdown
## 方法

本文基于扩散模型进行图像生成：

![[扩散模型]]

在此基础之上，本文引入了频域变换：

![[傅里叶变换]]
```

## MCP 工具说明

| 工具 | 用途 | 关键限制 |
|------|------|----------|
| `mcp__zotero__zotero_get_item_metadata` | 获取元数据 | 总是成功 |
| `mcp__zotero__zotero_get_item_fulltext` | 获取全文 | 可能超token限制 |
| `mcp__zotero__zotero_get_annotations` | 获取注释 | 可选 |

**CRITICAL**: 优先使用摘要，全文超限时降级。

## 输入参数

| 参数 | 说明 | 必填 |
|------|------|------|
| paper | 论文（标题/ID/Zotero key） | 是 |
| template | 模板类型 | 否，默认完整版 |
| attach_annotations | 是否附加注释 | 否，默认false |

## 笔记命名规则

- 使用论文英文标题
- 不加日期前缀
- 处理特殊字符（`/`, `:`, `<`, `>` 等）
- 例如：`Attention Is All You Need.md`

## 后续操作

笔记创建后建议：

```markdown
## 后续操作

- 检查 Frontmatter 是否完整
- 补充 MyPoint 模块的个人思考
- 添加概率框架分析（如适用）
- 建立 Wikilink 链接相关笔记
- 考虑调用 `/paper-graph` 生成引用关系图谱
```

## 快速参考

| 场景 | 操作 | 说明 |
|------|------|------|
| 创建笔记 | /paper-notes 论文标题 | 完整版笔记 |
| 简化版 | /paper-notes 论文标题 template:simple | 不含概率框架 |
| 带注释 | /paper-notes 论文标题 attach_annotations:true | 包含PDF注释 |
| 基于 key | /paper-notes ABCD123 | 直接引用 |

## 执行要求（格式参考技能）

创建笔记时必须参考以下格式技能：

| 技能 | 提供内容 | 执行方式 |
|------|----------|----------|
| obsidian-markdown | Callout/Wikilink/Frontmatter/Tags/Embeds 语法 | Read/Write/Edit + Glob |
| json-canvas | Canvas 格式规范 | 用于生成引用图谱 |
