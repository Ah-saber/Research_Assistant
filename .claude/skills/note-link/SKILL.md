---
name: note-link
description: Discover and establish semantic connections between notes, create reasonable Wikilinks to enhance note network connectivity. Use when connecting related notes, or when the user mentions "建立关联", "链接笔记", "笔记链接".
version: 1.0.0
---

# 笔记关联 (Note Link)

发现笔记之间的语义关联，创建合理的 Wikilink，增强笔记网络的连通性。

## When to Activate

- 用户说："建立关联"、"链接笔记"、"发现关联"
- 需要为孤立笔记建立连接
- 需要发现并创建笔记间的语义关联
- 链接完成后需要生成可视化预览

## Critical Rules (CRITICAL)

### Rule 1: Glob MUST Be Used for Link Creation (CRITICAL)

**NEVER** assume filename format. **ALWAYS** use Glob tool to get exact filename.

```python
# ❌ BAD: Creating link without verification
link = f"[[{note_title}]]"

# ✅ GOOD: Use Glob to verify and get exact filename
pattern = f"**/*{note_title}*.md"
matches = glob.glob(pattern, recursive=True)
if matches:
    actual_filename = matches[0]
    link = f"[[{actual_filename}|{note_title}]]"
```

### Rule 2: Context-Aware Link Placement (REQUIRED)

**MUST** intelligently determine link position based on relationship type:

| Relationship | Position | Format |
|--------------|----------|--------|
| 内容中提及 | 相关段落内 | `[[笔记\|描述]]` |
| 主题相关 | 笔记末尾 | `## 相关笔记\n- [[笔记]]` |
| 概念定义 | 概念处 | `[[笔记]]` |

### Rule 3: Pipe Escape in Tables (CRITICAL)

**MUST** escape pipe character in Markdown tables:

```python
# ❌ BAD: Unescaped pipe in table
| [[FlowEdit|FlowEdit]] | 说明 |

# ✅ GOOD: Escaped pipe in table
| [[FlowEdit：Inversion-Free  Text-Based Editing\|FlowEdit]] | 说明 |
```

### Rule 4: User Confirmation Required (REQUIRED)

**MUST** use `AskUserQuestion` before adding links:

```markdown
## 发现的笔记关联

### 高度相关（关联度>80%）
1. [[自注意力机制]] (95%)
2. [[多头注意力]] (88%)

请选择要添加的链接：
- 全部添加
- 选择性添加
- 仅预览
- 取消
```

## 工作流程

### Step 1: 发现关联

```python
# 分析目标笔记
content = read_file(target_note)

# 提取关键词
keywords = extract_keywords(content)

# 搜索相关笔记
related_notes = search_related(keywords, scope)

# 计算关联度
for note in related_notes:
    score = calculate_relevance(target_note, note)
```

### Step 2: 建议链接

使用 `AskUserQuestion` 让用户选择：

```markdown
## 发现的笔记关联

### 高度相关（关联度>80%）
1. [[自注意力机制]] (95%)
   理由：核心组件，多次提及

2. [[多头注意力]] (88%)
   理由：架构组成部分

### 中度相关（关联度50-80%）
3. [[BERT模型]] (75%)
   理由：基于Transformer

请选择要添加的链接：
```

### Step 3: 创建链接

根据用户选择，使用 `Edit` 工具添加链接：

```python
# 智能判断链接位置
def determine_link_position(relationship_type):
    if relationship_type == "content_mention":
        return find_relevant_paragraph()  # 内容中
    elif relationship_type == "topic_related":
        return "end"  # 笔记末尾
    else:
        return "concept_definition"  # 概念定义处

# 添加链接
for link in selected_links:
    position = determine_link_position(link.type)
    edit_file(note.file, "", link.text, position=position)
```

### Step 4: 验证链接

```python
# 使用 Glob 验证链接有效性
def verify_link(link_text):
    target = extract_link_target(link_text)
    pattern = f"**/*{target}*.md"
    matches = glob.glob(pattern, recursive=True)
    return len(matches) > 0
```

### Step 5: 可视化建议

链接完成后，建议生成可视化图谱：

```markdown
链接创建完成！是否生成可视化预览？

1. /paper-graph - 论文引用关系图谱
2. /idea-map - Idea概念关系图谱
3. /knowledge-canvas - 综合知识画布
4. 跳过
```

## GOOD vs BAD

### ✅ GOOD: 使用 Glob 精确匹配

```python
# 创建链接时
pattern = f"**/{paper_title}*.md"
matches = glob.glob(pattern, recursive=True)

if len(matches) == 1:
    actual_filename = matches[0]
    link = f"[[{actual_filename}|{paper_title}]]"
```

### ❌ BAD: 假设文件名

```python
# 直接使用标题创建链接（可能因空格不匹配而失效）
link = f"[[{paper_title}|{paper_title}]]"
```

### ✅ GOOD: 智能判断链接位置

```markdown
# 内容中提及 - 链接放在相关段落
Transformer 架构的核心是 [[自注意力机制\|Self-Attention]] 机制。

# 主题相关 - 链接放在笔记末尾
## 相关笔记
- [[自注意力机制]] - Transformer的核心组件
- [[多头注意力]] - 注意力机制的扩展
```

### ❌ BAD: 固定放在末尾

```markdown
# 所有链接都放在末尾（不够智能）
本文介绍了Transformer架构...

## 相关链接
- [[自注意力机制]]
- [[编码器]]
- [[解码器]]
```

### ✅ GOOD: 表格中转义管道符

```markdown
| [[FlowEdit：Inversion-Free  Text-Based Editing\|FlowEdit]] | 图像编辑 |
| [[SDEdit\|SDEdit]] | 图像编辑 |
```

### ❌ BAD: 表格中未转义

```markdown
| [[FlowEdit|FlowEdit]] | 图像编辑 |  ← 表格错位
```

### ✅ GOOD: 提供关联理由

```markdown
## 发现的关联

1. [[自注意力机制]] (95%)
   理由：本文多次引用该概念，是核心组件

2. [[多头注意力]] (88%)
   理由：本文架构的组成部分
```

### ❌ BAD: 无理由的关联列表

```markdown
相关笔记：
- [[自注意力机制]]
- [[多头注意力]]
- [[BERT]]
- [[GPT]]
```

## 核心功能

### 1. 关联发现算法

```python
关联度 = w1*标题相似 + w2*内容相似 + w3*标签重叠 + w4*引用关系

其中：
- 标题相似：关键词匹配
- 内容相似：语义相似度
- 标签重叠：共同标签数量
- 引用关系：是否互相引用
```

### 2. 链接位置智能判断

| 情况 | 链接位置 | 格式示例 |
|------|----------|----------|
| 内容中提及 | 相关段落 | `[[笔记\|描述]]` |
| 主题相关 | 笔记末尾 | `## 相关笔记\n- [[笔记]]` |
| 概念关联 | 概念定义处 | `[[笔记]]` |
| 扩展阅读 | 末尾独立节 | `## 扩展阅读` |

### 3. 链接验证和修复

```python
# 验证链接
def verify_wikilink(link_text):
    target = extract_link_target(link_text)
    pattern = f"**/*{target}*.md"
    matches = glob.glob(pattern, recursive=True)
    return len(matches) > 0

# 修复断链
def fix_broken_link(link_text):
    target = extract_link_target(link_text)
    matches = glob.glob(f"**/*{target[:20]}*.md")
    if len(matches) == 1:
        return f"[[{matches[0]}|{target}]]"
```

## 输出格式

```markdown
# 发现的笔记关联

## 目标笔记：《Transformer架构》

### 高度相关（关联度>80%）
1. [[自注意力机制]] (95%)
   理由：核心组件，多次提及
   建议位置："架构"段落

2. [[多头注意力]] (88%)
   理由：架构组成部分
   建议位置："架构组件"节

### 中度相关（关联度50-80%）
3. [[BERT模型]] (75%)
   理由：基于Transformer
   建议位置：末尾"应用"

### 标签关联
- 共享标签 #深度学习 的笔记：12篇

请选择要添加的链接：
```

## 后续操作

链接完成后建议：

| 操作 | 调用技能 | 说明 |
|------|----------|------|
| 论文引用关系 | `/paper-graph` | 层次布局引用图谱 |
| Idea概念关联 | `/idea-map` | 力导向布局概念图谱 |
| 综合知识视图 | `/knowledge-canvas` | 区域布局知识画布 |

**Canvas 可视化技能参考 json-canvas 格式规范**。

## 使用的工具

| 工具 | 用途 |
|------|------|
| `Glob` | 精确匹配文件名，验证链接 |
| `Read` | 读取笔记内容 |
| `Edit` | 添加链接到笔记 |
| `AskUserQuestion` | 用户选择确认 |

## 注意事项

- 适度链接，不要过度
- 使用描述性文字说明链接关系
- 链接放在逻辑相关的位置
- 表格中的链接必须转义管道符
