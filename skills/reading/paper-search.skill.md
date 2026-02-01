# /paper-search - 在Zotero中搜索论文

## 触发词
- "搜索论文"
- "找论文"
- "查找相关文献"
- "搜索关于xxx的论文"

## 功能描述
在Zotero库中搜索与用户查询相关的论文，支持关键词搜索、语义搜索和高级筛选。

## 搜索策略

1. **组合搜索**：同时使用关键词搜索和语义搜索（如果可用）
2. **排序**：按相关性排序
3. **数量控制**：默认返回10-15篇，用户可指定数量

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

## 后续操作提示

在搜索结果后，提示用户可执行的操作：
- 选择序号查看论文详情
- `/paper-summary <论文>` - 总结论文内容
- `/annotation-extract <论文>` - 提取PDF注释
- `/paper-notes <论文>` - 创建Obsidian笔记

## 示例

```bash
用户: /paper-search transformer可解释性

你: 找到12篇相关论文：

[1] Attention is All You Need
Vaswani et al. · 2017 · NeurIPS
摘要：提出纯注意力机制的Transformer架构...
相关度：★★★★★

[2] Visualizing and Understanding Transformers
...
```

## 使用的Zotero MCP工具

- `zotero_semantic_search` - 语义搜索
- `zotero_search_items` - 关键词搜索
- `zotero_advanced_search` - 高级搜索
