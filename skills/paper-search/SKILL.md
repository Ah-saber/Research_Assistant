---
name: paper-search
description: 在Zotero中搜索论文，支持关键词搜索、语义搜索和高级筛选
version: 1.0.0
---

# 论文搜索

在Zotero库中搜索与用户查询相关的论文。

## When to Activate（何时启用）

- 用户说："搜索论文"、"找论文"、"查找相关文献"
- 用户说："搜索关于xxx的论文"
- 用户需要查找特定作者或年份的论文

## 与外部格式参考技能的关系

本技能**不直接使用**格式参考技能（obsidian-markdown、json-canvas、obsidian-bases），因为搜索结果仅用于展示。

后续技能（如 `/paper-notes`）会使用这些格式参考技能创建笔记。

## 工作流程

1. **确定搜索策略**
   - 如果用户提供具体关键词：使用 `mcp__zotero__zotero_search_items`
   - 如果用户描述主题：使用 `mcp__zotero__zotero_semantic_search`
   - 如果需要高级筛选：使用 `mcp__zotero__zotero_advanced_search`

2. **执行搜索**
   - 使用适当的搜索工具
   - 限制结果数量（默认10条）

3. **展示结果**
   - 以卡片形式展示：标题、作者、年份、期刊、摘要
   - 包含论文的 item_key（用于后续操作）
   - 按相关性排序

4. **询问下一步**
   - 是否需要查看某篇论文的详细信息
   - 是否需要总结某篇论文
   - 是否需要创建笔记

## 搜索策略

- **组合搜索**：同时使用关键词搜索和语义搜索（如果可用）
- **排序**：按相关性排序
- **数量控制**：默认返回10-15篇，用户可指定数量

## 展示格式

使用卡片列表格式，每篇论文包含：

```
[序号] 论文标题
作者名 · 年份 · 期刊/会议
摘要：简要摘要（150字以内）
相关度：★★★★☆
```

## 搜索参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| query | 搜索关键词 | 用户输入 |
| limit | 结果数量 | 10 |
| year_from | 起始年份 | 无限制 |
| year_to | 结束年份 | 无限制 |
| sort | 排序方式 | relevance |

## 使用的 MCP 工具

| 工具 | 用途 | 使用场景 |
|------|------|----------|
| `mcp__zotero__zotero_semantic_search` | 语义搜索 | 用户描述主题 |
| `mcp__zotero__zotero_search_items` | 关键词搜索 | 用户提供具体关键词 |
| `mcp__zotero__zotero_advanced_search` | 高级搜索 | 需要年份/期刊筛选 |

## GOOD vs BAD（对比示例）

### ✅ GOOD

```bash
用户: 搜索 transformer 可解释性 的论文

AI: 使用 mcp__zotero__zotero_semantic_search 搜索
    找到 8 篇相关论文，按相关性排序：
    [1] Visualizing and Understanding Transformers
    ...
    后续可执行：/paper-summary、/paper-notes、/annotation-extract
```

### ❌ BAD

```bash
用户: 搜索论文

AI: 直接使用关键词搜索（未考虑语义搜索）
    结果过多且相关性低
    没有提示后续操作选项
```

## 后续操作提示

在搜索结果后，提示用户可执行的操作：
- 选择序号查看论文详情
- `/paper-summary <论文>` - 总结论文内容
- `/annotation-extract <论文>` - 提取PDF注释
- `/paper-notes <论文>` - 创建Obsidian笔记

## 快速参考表

| 场景 | 命令 | 说明 |
|------|------|------|
| 关键词搜索 | /paper-search "transformer" | 精确匹配 |
| 语义搜索 | /paper-search transformer可解释性 | 理解意图 |
| 高级搜索 | /paper-search year:2020-2024 | 筛选年份 |
