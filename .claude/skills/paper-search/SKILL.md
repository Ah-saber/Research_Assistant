---
name: paper-search
description: Search for papers in Zotero library using semantic search, keyword search, and advanced filters. Use when the user wants to find papers, search literature, query specific authors or years, or mentions "搜索论文", "找论文", "查找相关文献".
version: 1.0.0
---

# 论文搜索 (Paper Search)

在Zotero库中搜索与用户查询相关的论文。

## When to Activate

- 用户说："搜索论文"、"找论文"、"查找相关文献"
- 用户说："搜索关于xxx的论文"
- 用户需要查找特定作者或年份的论文

## Critical Rules (CRITICAL)

### Rule 1: Multi-Strategy Search (REQUIRED)

**ALWAYS** try multiple search approaches in order:

| Priority | Strategy | Tool | Use Case |
|----------|----------|------|----------|
| 1 | Semantic search | `semantic_search` | Intent-based queries |
| 2 | Keyword search | `search_items` | Specific terms |
| 3 | Title-only search | `search_items(qmode="titleCreatorYear")` | Known paper title |

**NEVER** rely on a single search method.

### Rule 2: Empty Results Handling (CRITICAL)

**MUST** provide actionable suggestions when no results found:

```python
# ❌ BAD: Direct failure report
"未找到论文。"

# ✅ GOOD: Actionable suggestions
"""
未找到精确匹配，建议：
1. 尝试简化搜索词："Attention"
2. 搜索作者："Vaswani"
3. 检查 Zotero 同步状态

需要我尝试这些方案吗？
"""
```

### Rule 3: Multiple Matches Handling (REQUIRED)

**MUST** ask user to select when multiple papers match:

```python
# ❌ BAD: Assume first result
result = results[0]

# ✅ GOOD: Ask user to select
"""
找到 3 篇同名论文：
[1] Attention Is All You Need (2017) - Vaswani et al.
[2] Attention is all you need (2018) - 不同作者
[3] Attention Is All You Need (2019) - 综述

请选择序号：
"""
```

## 工作流程

### Step 1: 确定搜索策略

分析用户输入，选择搜索方式：

```python
# 用户输入分析
if contains_title_and_author(user_input):
    strategy = "组合搜索：titleCreatorYear"
    tool = "mcp__zotero__zotero_search_items"
    params = {"qmode": "titleCreatorYear"}

elif contains_technical_terms(user_input):
    strategy = "语义搜索优先"
    tool = "mcp__zotero__zotero_semantic_search"

    # 如果语义搜索失败，降级到关键词搜索
    fallback = "mcp__zotero__zotero_search_items"

else:
    strategy = "关键词搜索"
    tool = "mcp__zotero__zotero_search_items"
```

### Step 2: 执行搜索

按策略顺序尝试搜索：

```python
# ✅ GOOD: 多策略降级
def search_paper(query):
    # 优先语义搜索
    results = mcp__zotero__zotero_semantic_search(query)
    if results:
        return results

    # 降级到关键词搜索
    results = mcp__zotero__zotero_search_items(query)
    if results:
        return results

    # 最后尝试标题搜索
    results = mcp__zotero__zotero_search_items(
        query, qmode="titleCreatorYear"
    )
    return results

# ❌ BAD: 单一搜索（可能因不匹配导致无结果）
results = mcp__zotero__zotero_search_items(query)
if not results:
    return "未找到论文"
```

### Step 3: 处理结果

处理搜索结果：

```python
# ✅ GOOD: 检查多匹配
if len(results) > 1:
    # 按年份排序，提示用户选择
    results.sort(key=lambda x: x.get("year", 0), reverse=True)
    display_results_with_selection(results)

# ❌ BAD: 假设唯一结果
result = results[0]  # 可能不是用户想要的
```

### Step 4: 展示结果

使用卡片列表格式展示：

```markdown
[1] Attention Is All You Need
作者：Ashish Vaswani et al. · 年份：2017 · 期刊：NeurIPS
摘要：我们提出了一种新的简单网络架构 Transformer...
相关度：★★★★★

[2] BERT: Pre-training of Deep Bidirectional Transformers
作者：Jacob Devlin et al. · 年份：2019 · 期刊：NAACL
摘要：我们介绍了 BERT，一种新的语言表示模型...
相关度：★★★★☆
```

## GOOD vs BAD

### ✅ GOOD: 组合搜索策略

用户说："找一下 Attention Is All You Need 这篇论文"

```
执行策略：
1. 语义搜索："Attention Is All You Need"
2. 如果精确匹配，直接返回
3. 如果多匹配，按年份筛选（2017+）
4. 展示结果让用户确认
```

### ❌ BAD: 单一搜索

用户说："找一下 Attention Is All You Need 这篇论文"

```
执行：zotero_search_items("Attention Is All You Need")
问题：如果标题稍有不同（如"Attention is all you need"），可能找不到
```

### ✅ GOOD: 无结果时提供方案

```
未找到精确匹配，建议：
1. 尝试简化搜索词："Attention"
2. 搜索作者："Vaswani"
3. 检查 Zotero 同步状态

需要我尝试这些方案吗？
```

### ❌ BAD: 直接报告失败

```
未找到论文。
```

### ✅ GOOD: 多匹配时让用户选择

```
找到 3 篇同名论文：
[1] Attention Is All You Need (2017) - Vaswani et al. NeurIPS
[2] Attention is all you need (2018) - 其他作者
[3] Attention Is All You Need (2019) - 综述论文

请选择序号 [1-3]：
```

### ❌ BAD: 自动选择第一个

```
# 直接返回第一个结果，可能不是用户想要的
result = results[0]
```

### ✅ GOOD: 语义搜索失败时降级

```python
# 语义搜索优先
results = mcp__zotero__zotero_semantic_search(query)

# 如果失败，降级到关键词搜索
if not results:
    results = mcp__zotero__zotero_search_items(query)

if not results:
    # 提供替代方案
    return suggest_alternatives(query)
```

### ❌ BAD: 单一搜索后直接失败

```python
results = mcp__zotero__zotero_search_items(query)

if not results:
    return "未找到论文"  # 没有尝试其他搜索方式
```

## MCP 工具说明

| 工具 | 用途 | 关键限制 |
|------|------|----------|
| `mcp__zotero__zotero_semantic_search` | 语义搜索论文 | 需要索引数据库 |
| `mcp__zotero__zotero_search_items` | 关键词搜索 | 需要精确匹配 |
| `mcp__zotero__zotero_advanced_search` | 高级搜索 | 需要多个条件 |

**CRITICAL**: 语义搜索依赖索引，如果失败立即降级到关键词搜索。

## 输入参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| query | 搜索关键词 | 用户输入 |
| limit | 结果数量 | 10 |
| year_from | 起始年份 | 无限制 |
| year_to | 结束年份 | 无限制 |

## 后续操作提示

在搜索结果后，提示用户可执行的操作：

```markdown
## 后续操作

- 选择序号查看论文详情
- `/paper-summary <序号>` - 总结论文内容
- `/annotation-extract <序号>` - 提取PDF注释
- `/paper-notes <序号>` - 创建Obsidian笔记
```

## 快速参考

| 场景 | 搜索策略 | 工具 |
|------|----------|------|
| 已知标题+作者 | 组合搜索 | `search_items(titleCreatorYear)` |
| 模糊描述 | 语义搜索 | `semantic_search` + 降级 |
| 浏览集合 | 列表浏览 | `get_collections` |
| 高级筛选 | 多条件搜索 | `advanced_search` |
