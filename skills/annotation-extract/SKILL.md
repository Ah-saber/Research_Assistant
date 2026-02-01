---
name: annotation-extract
description: 从Zotero中提取PDF的高亮和笔记，按颜色分组组织，输出为可导入Obsidian的格式
version: 1.0.0
---

# 注释提取

从Zotero中提取PDF的高亮和笔记。

## When to Activate（何时启用）

- 用户说："提取注释"、"获取高亮"、"导出笔记"
- 用户说："提取PDF注释"、"查看标注"
- 用户需要整理在Zotero Reader中添加的标注

## 与外部格式参考技能的关系

本技能**不直接使用**格式参考技能，因为提取结果仅用于展示。

如果需要将注释保存为笔记，会使用 `/paper-notes` 技能（该技能使用 obsidian-markdown 格式）。

## 工作流程

1. **获取论文信息**
   - 如果提供了 item_key：使用 `mcp__zotero__zotero_get_annotations` 获取注释
   - 如果没有：先使用 `/paper-search` 搜索

2. **提取注释**
   - 使用 `mcp__zotero__zotero_get_annotations` 工具
   - 获取所有高亮、下划线、笔记

3. **整理注释**
   - 按页码排序
   - 区分不同类型的注释（高亮、笔记、下划线）
   - 保留原文引用

4. **格式化输出**
   - 使用 markdown 格式
   - 中文组织结构，保留原文语言
   - 包含页码和位置信息

## 提取内容

### 1. 高亮文本
- 高亮文本内容
- 页码位置
- 上下文信息

### 2. 笔记注释
- 用户添加的笔记
- 对应的高亮
- 标签信息

### 3. 颜色分组
- 黄色：重要概念
- 绿色：方法细节
- 蓝色：实验结果
- 红色：疑问/待研究
- 其他：按颜色分类

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
```

## 输入参数

| 参数 | 说明 | 必填 |
|------|------|------|
| paper | 论文（标题/ID/Zotero key） | 是 |
| group_by | 分组方式（color/page） | 否，默认 color |

## 使用的 MCP 工具

| 工具 | 用途 | 使用场景 | 限制 |
|------|------|----------|------|
| `mcp__zotero__zotero_get_annotations` | 获取PDF注释 | 提取高亮和笔记 | 必须指定 item_key |

## GOOD vs BAD（对比示例）

### ✅ GOOD

```bash
用户: 提取 Attention Is All You Need 的注释

AI: 1. 使用 mcp__zotero__zotero_get_annotations(item_key="XXX")
    2. 检测到 15 条注释
    3. 按颜色分组：黄色5条、绿色7条、蓝色3条
    4. 输出 markdown 格式，包含页码和原文
```

### ❌ BAD

```bash
用户: 提取注释

AI: 1. 调用工具时未指定 item_key
    2. 返回 60万+ 字符的全部注释
    3. 未按颜色分组
    4. 缺少页码信息
```

## MCP工具使用注意事项

### 空注释处理
当论文没有注释时：
1. `mcp__zotero__zotero_get_annotations` 返回 "No annotations found"
2. 友好提示用户：该论文暂无PDF注释
3. 建议用户：
   - 在Zotero Reader中添加高亮/笔记
   - 或者提供其他有注释的论文

### 大量数据处理
当获取所有注释时数据量可能巨大（60万+字符）：
1. **按论文筛选**: 使用 `item_key` 参数获取单篇论文的注释
2. **使用 limit**: 设置合理的返回数量
3. **分批处理**: 如果需要全部注释，建议分批次处理

### 推荐工作流
```bash
# 1. 先检查论文是否有注释
mcp__zotero__zotero_get_annotations(item_key="XXX")

# 2. 如果有注释则提取，无则提示
# 3. 输出按颜色分组的 markdown 格式
```

## 后续操作

提取后询问用户：
- 是否创建为独立笔记
- 是否附加到现有笔记
- 是否需要整理和分类

## 快速参考表

| 场景 | 命令 | 说明 |
|------|------|------|
| 按颜色分组 | /annotation-extract 论文标题 | 默认方式 |
| 按页码分组 | /annotation-extract 论文标题 group_by:page | 另一种视图 |
| 基于 key | /annotation-extract ABCD123 | 直接引用 |
