---
name: note-analyze
description: Analyze Obsidian note structure and content, discover semantic connections between notes, identify isolated notes and duplicate content. Use when understanding the current state of notes, or when the user mentions "分析笔记", "笔记结构分析", "笔记语义分析".
version: 1.0.0
---

# 笔记分析 (Note Analyze)

分析 Obsidian 笔记库的结构和内容，发现笔记之间的联系、孤立笔记、重复内容等。**语义分析是核心功能**，可发现笔记之间的深层语义联系。

## When to Activate

- 用户说："分析笔记"、"笔记结构分析"、"检查笔记状态"
- 需要发现笔记之间的语义关联
- 需要识别孤立笔记或重复内容
- 需要生成整理或可视化建议

## Critical Rules (CRITICAL)

### Rule 1: Semantic Analysis is Core (REQUIRED)

**MUST** perform deep semantic analysis to discover:

| Analysis Type | Purpose |
|---------------|---------|
| 相似思考发现 | 识别讨论相同主题的不同笔记 |
| 主题关联分析 | 发现形成主题簇的笔记 |
| 概念同义词识别 | 识别指代相同概念的不同表述 |
| 本质分析 | 比较核心观点的异同 |

### Rule 2: Actionable Recommendations (REQUIRED)

**ALWAYS** provide actionable suggestions after analysis:

```python
# ❌ BAD: Analysis only
"发现5篇笔记讨论注意力机制"

# ✅ GOOD: Analysis + Actionable suggestion
"发现5篇笔记讨论注意力机制。建议：
1. 创建主题索引笔记《注意力机制》
2. 在相关笔记间建立 Wikilink
3. 调用 /note-standardize 规范化格式
4. 调用 /paper-graph 生成可视化图谱"
```

### Rule 3: User Confirmation Before Actions (REQUIRED)

**MUST** use `AskUserQuestion` before executing any suggestions:

```markdown
分析完成！发现以下改进机会：

## 建议操作
1. 标准化笔记格式（调用 /note-standardize）
2. 建立笔记关联（调用 /note-link）
3. 生成可视化图谱（调用 /paper-graph）
4. 创建主题索引笔记

请选择要执行的操作：
```

## 工作流程

### Step 1: 扫描笔记库

使用 Glob 工具扫描目标目录：

```python
# 扫描笔记
pattern = f"{scope}/**/*.md"
notes = glob.glob(pattern, recursive=True)

# 读取内容分析
for note_path in notes:
    content = read_file(note_path)
    # 提取关键词、标签、链接等信息
```

### Step 2: 结构分析

```python
# 分析笔记结构
stats = {
    "total_notes": len(notes),
    "isolated_notes": find_isolated(notes),  # 无入链/出链
    "popular_notes": find_popular(notes),     # 被引用最多
    "broken_links": find_broken(notes),       # 断链检测
    "missing_frontmatter": check_frontmatter(notes)
}
```

### Step 3: 语义分析（核心）

```python
# 语义聚类分析
def semantic_analysis(notes):
    # 提取每篇笔记的关键词
    keywords = extract_keywords(notes)

    # 计算相似度矩阵
    similarity = compute_similarity(keywords)

    # 发现主题簇
    clusters = find_clusters(similarity)

    # 识别同义词概念
    synonyms = find_synonyms(keywords)

    return {
        "similar_content": find_similar(notes, similarity),
        "topic_clusters": clusters,
        "concept_synonyms": synonyms
    }
```

### Step 4: 生成报告和建议

```python
# 生成分析报告
report = generate_report(stats, semantic_result)

# 提供可执行建议
suggestions = generate_suggestions(report)

# 使用 AskUserQuestion 让用户选择
ask_user(suggestions)
```

## GOOD vs BAD

### ✅ GOOD: 发现语义关联并建议操作

```markdown
## 语义分析发现

### 相似思考
《Transformer架构.md》和《自注意力机制.md》讨论了相同的本质：
- 核心都是 attention mechanism
- 建议合并或建立强关联

### 主题簇
发现以下笔记形成"注意力机制"主题簇：
- Transformer架构.md
- 自注意力机制.md
- 多头注意力.md
- 注意力可视化.md

**建议操作**：
1. 创建主题索引笔记 `00_注意力机制索引.md`
2. 调用 /note-link 建立关联
3. 调用 /knowledge-canvas 生成概念图谱
```

### ❌ BAD: 仅列出发现，无行动建议

```markdown
## 分析结果

发现以下笔记讨论注意力：
- Transformer架构.md
- 自注意力机制.md
- 多头注意力.md
```

### ✅ GOOD: 识别可合并内容

```markdown
## 内容重复分析

发现高度重复的笔记：

| 笔记A | 笔记B | 相似度 | 建议 |
|-------|-------|--------|------|
| 注意力机制 | Attention机制 | 95% | 合并为一篇，保留中文标题 |
| 梯度下降 | 梯度下降法 | 88% | 内容互补，建议合并 |
```

### ❌ BAD: 错误合并不同内容

```markdown
发现以下笔记可以合并：
- Transformer架构 + BERT模型  ← ❌ 这是不同的论文，不应合并
- 扩散模型 + 图像生成        ← ❌ 主题不同，不应合并
```

## 核心功能

### 1. 结构分析

| 维度 | 检查项 |
|------|--------|
| 笔记数量 | 总数、目录分布 |
| 链接分析 | 孤立笔记、热门笔记、断链 |
| 标签分析 | 使用统计、层级结构 |
| Frontmatter | 完整性检查 |

### 2. 语义分析（核心重点）

| 分析类型 | 方法 | 输出 |
|----------|------|------|
| 相似内容发现 | 关键词共现分析 | 相似笔记列表 |
| 主题关联 | 语义聚类 | 主题簇 |
| 概念同义词 | 术语匹配 | 同义词映射 |
| 本质分析 | 核心观点提取 | 观点比较 |

### 3. 改进建议

**可调用的技能**：

| 发现问题 | 调用技能 | 说明 |
|----------|----------|------|
| 格式不规范 | `/note-standardize` | Callout、Wikilink、Frontmatter、标签规范化 |
| 需要建立关联 | `/note-link` | 发现并创建 Wikilink |
| 论文引用关系 | `/paper-graph` | 生成层次布局引用图谱 |
| Idea概念关联 | `/idea-map` | 生成力导向布局概念图谱 |
| 综合研究主题 | `/knowledge-canvas` | 生成区域布局知识画布 |

**Canvas 可视化技能参考 json-canvas 格式规范**。

## 输出格式

```markdown
# 笔记分析报告

## 概览
- 笔记总数：234篇
- 孤立笔记：12篇
- 断链：5个

## 结构分析
[目录结构、链接密度...]

## 语义分析（重点）

### 相似内容发现
- 笔记A和笔记B讨论了相同的主题：注意力机制
  → 建议：建立 Wikilink 或合并

### 主题关联
- 发现"深度学习"主题簇：15篇笔记
  → 建议：创建索引笔记

### 相似概念
- "Transformer"和"自注意力模型"指代相同概念
  → 建议：统一术语

## 改进建议
1. 调用 /note-standardize 标准化格式
2. 调用 /note-link 建立关联
3. 调用 /paper-graph 生成可视化图谱
```

## 使用的工具

| 工具 | 用途 |
|------|------|
| `Glob` | 扫描笔记文件 |
| `Read` | 读取笔记内容 |
| `AskUserQuestion` | 确认执行操作 |

## 注意事项

- 尊重现有笔记结构
- 不破坏现有内容
- 建议需用户确认后执行
- 分析耗时可能较长，需提示用户
