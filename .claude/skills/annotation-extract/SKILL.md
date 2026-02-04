---
name: annotation-extract
description: Extract PDF highlights and annotations from Zotero, organize by color groups, and format for Obsidian import. Use when the user has highlighted passages in PDFs and wants to extract them to notes, or mentions "提取注释", "获取高亮", "PDF笔记".
version: 1.0.0
---

# 注释提取 (Annotation Extract)

从Zotero中提取PDF的高亮和笔记，按颜色分组组织。

## When to Activate

- 用户说："提取注释"、"获取高亮"、"导出笔记"
- 用户说："提取PDF注释"、"查看标注"
- 用户需要整理在Zotero Reader中添加的标注

## Critical Rules (CRITICAL)

### Rule 1: item_key is REQUIRED (CRITICAL)

**MUST** always specify `item_key` parameter when calling `zotero_get_annotations`:

```python
# ✅ GOOD: 指定 item_key
annotations = mcp__zotero__zotero_get_annotations(item_key="XXX")

# ❌ BAD: 不指定 item_key（可能返回60万+字符）
annotations = mcp__zotero__zotero_get_annotations()
```

### Rule 2: Empty Annotations Handling (REQUIRED)

**MUST** check for "No annotations found" and provide friendly message:

```python
# ✅ GOOD: 检查空注释
annotations = mcp__zotero__zotero_get_annotations(item_key=item_key)

if annotations == "No annotations found" or not annotations:
    return """
    该论文暂无PDF注释。

    建议：
    1. 在 Zotero Reader 中打开 PDF
    2. 添加高亮或笔记
    3. 重新运行提取

    或者提供其他有注释的论文。
    """

# ❌ BAD: 假设注释总是存在
annotations = mcp__zotero__zotero_get_annotations(item_key=item_key)
# 直接处理，可能报错
```

### Rule 3: Limit Parameter for Large Data (CRITICAL)

**MUST** use `limit` parameter when dealing with large annotation sets:

```python
# ✅ GOOD: 使用 limit 参数
annotations = mcp__zotero__zotero_get_annotations(
    item_key="XXX",
    limit=100  # 限制返回数量
)

# ❌ BAD: 不限制数量
annotations = mcp__zotero__zotero_get_annotations(item_key="XXX")
# 可能有数百条注释，导致超限
```

## 工作流程

### Step 1: 获取论文信息

```python
# 如果提供了 item_key，直接使用
if item_key:
    pass
# 否则，先搜索论文
else:
    results = mcp__zotero__zotero_search_items(query)
    item_key = results[0]["key"]
```

### Step 2: 提取注释

```python
# ✅ GOOD: 检查空注释
annotations = mcp__zotero__zotero_get_annotations(
    item_key=item_key,
    limit=200  # 设置合理上限
)

if not annotations or annotations == "No annotations found":
    return friendly_no_annotations_message()

# ❌ BAD: 未检查空注释
annotations = mcp__zotero__zotero_get_annotations(item_key=item_key)
# 如果无注释，后续处理会失败
```

### Step 3: 整理注释

```python
# 按颜色分组
color_groups = {
    "yellow": [],   # 重要概念
    "green": [],    # 方法细节
    "blue": [],     # 实验结果
    "red": [],      # 疑问/待研究
    "other": []     # 其他颜色
}

for annotation in annotations:
    color = annotation.get("color", "unknown")
    text = annotation.get("text", "")
    page = annotation.get("page", "")
    note = annotation.get("note", "")

    color_groups[color].append({
        "text": text,
        "page": page,
        "note": note
    })
```

### Step 4: 格式化输出

```python
output = f"""
# {paper_title} - PDF注释

## 黄色 - 重要概念

### Page 23
> "Transformer架构的核心是自注意力机制..."

[笔记] 这是论文的核心贡献

---

## 绿色 - 方法细节

### Page 45
> "我们使用多头注意力机制..."

---

## 蓝色 - 实验结果

...

## 红色 - 疑问/待研究

...
"""
```

## GOOD vs BAD

### ✅ GOOD: 指定 item_key 并检查空注释

```python
# 指定 item_key
annotations = mcp__zotero__zotero_get_annotations(item_key="XXX")

# 检查空注释
if annotations == "No annotations found":
    print("该论文暂无PDF注释。")
    print("建议：在 Zotero Reader 中添加高亮或笔记。")
    return
```

### ❌ BAD: 未指定 item_key

```python
# 不指定 item_key，可能返回所有论文的注释
annotations = mcp__zotero__zotero_get_annotations()
# 可能返回 60万+ 字符，导致超限
```

### ✅ GOOD: 使用 limit 参数

```python
# 使用 limit 控制数量
annotations = mcp__zotero__zotero_get_annotations(
    item_key="XXX",
    limit=100
)

if len(annotations) == 100:
    print(f"注释较多，已显示前100条。")
```

### ❌ BAD: 不限制数量

```python
# 不使用 limit，可能返回数百条注释
annotations = mcp__zotero__zotero_get_annotations(item_key="XXX")
# 可能有数百条注释
```

### ✅ GOOD: 处理颜色分组失败

```python
# 处理未知颜色
for annotation in annotations:
    color = annotation.get("color", "unknown")

    if color in color_groups:
        color_groups[color].append(annotation)
    else:
        color_groups["other"].append(annotation)
        # 提示用户有其他颜色
```

### ❌ BAD: 假设颜色总是已知

```python
# 直接使用颜色作为键，可能报错
color_groups[annotation["color"]].append(annotation)
# 如果颜色不在预定义列表中，会报错
```

### ✅ GOOD: 处理缺失笔记

```python
# 处理缺失的笔记
for annotation in annotations:
    text = annotation.get("text", "")
    note = annotation.get("note", "")
    page = annotation.get("page", "")

    output = f"> {text}\n"
    if note:
        output += f"\n[笔记] {note}\n"
    else:
        output += "\n"  # 保留格式一致
```

### ❌ BAD: 假设笔记总是存在

```python
# 直接使用 note 字段
output = f"[笔记] {annotation['note']}\n"
# 如果 note 为 None，会显示 "None"
```

## 颜色分组

| 颜色 | 用途 | 说明 |
|------|------|------|
| 黄色 | 重要概念 | 核心概念、定义、定理 |
| 绿色 | 方法细节 | 算法步骤、公式推导 |
| 蓝色 | 实验结果 | 数据、图表、结论 |
| 红色 | 疑问/待研究 | 不理解的地方、待验证 |
| 其他 | 按实际颜色 | 保持原始颜色 |

## MCP 工具说明

| 工具 | 用途 | 关键限制 |
|------|------|----------|
| `mcp__zotero__zotero_get_annotations` | 获取PDF注释 | 必须指定 item_key |

**CRITICAL**:
1. **必须**指定 `item_key` 参数
2. 不指定可能返回所有注释（60万+字符）
3. 大量注释时使用 `limit` 参数
4. 检查 "No annotations found" 返回值

## 输入参数

| 参数 | 说明 | 必填 |
|------|------|------|
| paper | 论文（标题/ID/Zotero key） | 是 |
| group_by | 分组方式（color/page） | 否，默认 color |
| limit | 返回数量限制 | 否，默认200 |

## 输出格式

```markdown
# [论文标题] - PDF注释

## 黄色 - 重要概念

### Page 23
> "Transformer架构的核心是自注意力机制..."

[笔记] 这是论文的核心贡献

---

## 绿色 - 方法细节

### Page 45
> "我们使用多头注意力机制..."

---

## 蓝色 - 实验结果

...

## 红色 - 疑问/待研究

...

## 其他颜色

...
```

## 后续操作

提取后询问用户：

```markdown
## 后续操作

- 是否创建为独立笔记（调用 `/paper-notes`）
- 是否附加到现有笔记
- 是否需要按页码重新分组
```

## 快速参考

| 场景 | 参数 | 说明 |
|------|------|------|
| 标准提取 | group_by: color | 按颜色分组（默认） |
| 页码分组 | group_by: page | 按页码排序 |
| 限制数量 | limit: 50 | 仅前50条注释 |
| 基于 key | item_key: "XXX" | 直接引用，避免搜索 |
