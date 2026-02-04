---
name: paper-summary
description: Generate detailed Chinese summary of research papers including background, problem statement, methodology, results, and conclusions. Use when the user wants to understand a paper's content without reading the full text, or mentions "总结论文", "论文概要", "生成摘要".
version: 1.0.0
---

# 论文总结 (Paper Summary)

生成论文的详细中文摘要，包括研究背景、问题、方法、结果和结论。

## When to Activate

- 用户说："总结论文"、"论文概要"、"论文摘要"
- 用户说："总结xxx论文"、"这篇论文讲了什么"
- 用户搜索论文后希望了解某篇论文的内容

## Critical Rules (CRITICAL)

### Rule 1: Abstract-First Strategy (REQUIRED)

**ALWAYS** try to use abstract first, fulltext as fallback:

```python
# ✅ GOOD: 先使用摘要
metadata = mcp__zotero__zotero_get_item_metadata(item_key)
abstract = metadata.get("abstract", "")

if abstract:
    summary = generate_from_abstract(abstract)
    quality = "abstract"
else:
    # 才尝试获取全文
    fulltext = mcp__zotero__zotero_get_item_fulltext(item_key)
    summary = generate_from_fulltext(fulltext)
    quality = "full"

# ❌ BAD: 直接使用全文
fulltext = mcp__zotero__zotero_get_item_fulltext(item_key)  # 可能超限
summary = generate_from_fulltext(fulltext)
```

### Rule 2: Quality Labeling (CRITICAL)

**MUST** clearly indicate data source:

```python
# ✅ GOOD: 明确标注
"""
# 论文总结

**数据来源**：基于论文摘要生成（建议补充全文细节）

## 研究背景
...
"""

# ❌ BAD: 未标注来源
"""
# 论文总结

## 研究背景
...
"""
```

### Rule 3: Token Limit Handling (CRITICAL)

**MUST** handle fulltext token limit errors gracefully:

```python
# ✅ GOOD: 降级到摘要
try:
    fulltext = mcp__zotero__zotero_get_item_fulltext(item_key)
    summary = generate_from_fulltext(fulltext)
except TokenLimitError:
    # 降级到摘要
    metadata = mcp__zotero__zotero_get_item_metadata(item_key)
    summary = generate_from_abstract(metadata["abstract"])
    quality_label = "**数据来源**：基于摘要生成（全文超token限制）"

# ❌ BAD: 直接失败
fulltext = mcp__zotero__zotero_get_item_fulltext(item_key)
# 如果超限，直接报错，没有降级策略
```

## 工作流程

### Step 1: 获取论文信息

```python
# 首先获取元数据（总是成功）
metadata = mcp__zotero__zotero_get_item_metadata(item_key)

# 提取基本信息
title = metadata["title"]
authors = metadata["authors"]
year = metadata["year"]
abstract = metadata.get("abstract", "")
```

### Step 2: 生成摘要

```python
# ✅ GOOD: 优先使用摘要
if abstract:
    summary = generate_structured_summary(
        abstract=abstract,
        metadata=metadata
    )
    quality = "abstract"

# ❌ BAD: 直接尝试全文（可能超限）
fulltext = mcp__zotero__zotero_get_item_fulltext(item_key)
summary = generate_structured_summary(fulltext=fulltext)
```

### Step 3: 处理摘要缺失

```python
# ✅ GOOD: 处理缺失摘要
if not abstract:
    # 尝试获取全文
    fulltext = mcp__zotero__zotero_get_item_fulltext(item_key)

    # 如果全文也获取失败
    if not fulltext:
        return """
        **错误**：该论文既无摘要，全文也无法获取。

        可能原因：
        1. Zotero 未同步 PDF
        2. PDF 未索引
        3. 网络连接问题

        建议：
        - 检查 Zotero 同步状态
        - 尝试在 Zotero Reader 中打开 PDF
        """
```

### Step 4: 格式化输出

```python
# 使用结构化格式
output = f"""
# {title} - 论文总结

**数据来源**：{quality_label}

## 基本信息
- **作者**：{authors}
- **年份**：{year}
- **发表**：{venue}

## 研究背景
{background}

## 研究问题
{problem}

## 核心方法
{method}

## 主要结果
{results}

## 结论
{conclusion}
"""
```

## GOOD vs BAD

### ✅ GOOD: 使用摘要生成

```python
metadata = mcp__zotero__zotero_get_item_metadata(item_key)
abstract = metadata.get("abstract", "")

if abstract:
    summary = generate_from_abstract(abstract)
    print("**数据来源**：基于论文摘要生成")
```

### ❌ BAD: 直接使用全文

```python
fulltext = mcp__zotero__zotero_get_item_fulltext(item_key)
summary = generate_from_fulltext(fulltext)
# 问题：可能超token限制，导致失败
```

### ✅ GOOD: 处理缺失摘要

```
**注意**：该论文无摘要，已使用全文生成。

如需更详细的内容，请提供论文具体问题。
```

### ❌ BAD: 假设摘要存在

```python
# 假设摘要总是存在
summary = generate_from_abstract(metadata["abstract"])
# 如果 abstract 为 None，会报错
```

### ✅ GOOD: 超限时降级

```python
try:
    fulltext = mcp__zotero__zotero_get_item_fulltext(item_key)
except TokenLimitError as e:
    # 降级到摘要
    abstract = metadata.get("abstract", "")
    summary = generate_from_abstract(abstract)
    print("**数据来源**：基于摘要生成（全文超token限制）")
```

### ❌ BAD: 超限后直接失败

```python
fulltext = mcp__zotero__zotero_get_item_fulltext(item_key)
# 如果超限，返回错误，没有降级策略
```

### ✅ GOOD: 明确标注质量级别

```markdown
# 论文总结

**数据来源**：基于论文摘要生成

**建议**：如需更详细的内容，可以：
1. 提供具体问题，我可以针对性分析
2. 确认全文可访问后，我可以获取全文细节
```

### ❌ BAD: 未标注来源

```markdown
# 论文总结

## 研究背景
...  # 用户不知道这是基于摘要还是全文
```

## 摘要结构

### 1. 研究背景（Background）
- 领域现状和背景
- 相关工作简介

### 2. 研究问题（Problem）
- 要解决的核心问题
- 现有方法的不足

### 3. 研究动机（Motivation）
- 为什么需要解决这个问题
- 解决这个问题的意义

### 4. 创新方法（Method）
- 核心方法和算法
- 关键技术细节
- 模型架构

### 5. 实验结果（Results）
- 主要实验设置
- 关键结果数据
- 与 baseline 的比较

### 6. 结论与贡献（Conclusion）
- 主要发现
- 贡献总结
- 局限性讨论

### 7. 关键公式（可选）
- 列出核心公式
- 解释公式含义

## 输出格式

```markdown
# [论文标题] - 论文总结

**数据来源**：[数据来源说明]

## 基本信息
- **作者**：xxx
- **年份**：xxxx
- **发表**：xxx

## 研究背景
...

## 研究问题
...

## 核心方法
...

## 主要结果
...

## 关键公式（可选）
...

## 结论
...
```

## MCP 工具说明

| 工具 | 用途 | 关键限制 |
|------|------|----------|
| `mcp__zotero__zotero_get_item_metadata` | 获取元数据 | 总是成功，包含摘要 |
| `mcp__zotero__zotero_get_item_fulltext` | 获取论文全文 | 可能超token限制 |

**CRITICAL**:
1. 优先使用 `metadata["abstract"]`
2. 仅在摘要不存在时才尝试全文
3. 全文超限时降级到摘要

## 输入参数

| 参数 | 说明 | 必填 |
|------|------|------|
| paper | 论文（标题/ID/Zotero key） | 是 |
| detail | 详细程度（simple/detailed） | 否，默认 detailed |

## 快速参考

| 场景 | 数据来源 | 说明 |
|------|----------|------|
| 标准总结 | 摘要 | 优先使用，避免超限 |
| 详细总结 | 全文 | 需检查 token 限制 |
| 摘要缺失 | 全文 → 降级 | 先全文，超限则提示用户 |
| 无摘要无全文 | 错误提示 | 建议 Zotero 同步 |
