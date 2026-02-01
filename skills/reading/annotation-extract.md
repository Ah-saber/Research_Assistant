# Annotation Extract Skill

从Zotero中提取PDF注释和高亮。

## 使用场景

当用户说：
- "提取注释"
- "获取高亮"
- "查看标注"
- "提取[paper_key]的注释"

## 工作流程

1. **获取论文信息**
   - 如果提供了paper_key：使用`zotero_get_annotations`获取注释
   - 如果没有：先使用`/paper-search`搜索

2. **提取注释**
   - 使用`zotero_get_annotations`工具
   - 获取所有高亮、下划线、笔记

3. **整理注释**
   - 按页码排序
   - 区分不同类型的注释（高亮、笔记、下划线）
   - 保留原文引用

4. **格式化输出**
   - 使用markdown格式
   - 中文输出
   - 包含页码和位置信息

## 示例输出

```markdown
# Attention Is All You Need - 注释提取

## 高亮内容

### 第2页
> "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks..."

### 第3页
> "We propose a new simple network architecture, the Transformer..."

## 手动笔记

### 第4页
- 注意力机制可以并行计算，这是相比RNN的优势

### 第7页
- 多头注意力允许模型在不同位置关注不同子空间

## 统计
- 高亮数量: 15
- 笔记数量: 5
- 涵盖页数: 8
```

## 相关命令

- `/paper-search` - 搜索论文
- `/paper-summary` - 总结论文
- `/paper-notes` - 创建论文笔记
