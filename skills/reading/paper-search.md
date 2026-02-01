# Paper Search Skill

在Zotero中搜索学术论文。

## 使用场景

当用户说：
- "搜索论文"
- "找论文"
- "搜索关于[主题]的论文"
- "查找[作者]的论文"

## 工作流程

1. **确定搜索策略**
   - 如果用户提供具体关键词：使用`zotero_search_items`
   - 如果用户描述主题：使用`zotero_semantic_search`
   - 如果需要高级筛选：使用`zotero_advanced_search`

2. **执行搜索**
   - 使用适当的搜索工具
   - 限制结果数量（默认10条）

3. **展示结果**
   - 以表格形式展示：标题、作者、年份、期刊
   - 包含论文的key（用于后续操作）
   - 按相关性排序

4. **询问下一步**
   - 是否需要查看某篇论文的详细信息
   - 是否需要总结某篇论文
   - 是否需要创建笔记

## 示例输出

| # | 标题 | 作者 | 年份 | 期刊 |
|---|------|------|------|------|
| 1 | Attention Is All You Need | Vaswani et al. | 2017 | NeurIPS |
| 2 | BERT: Pre-training of Deep Bidirectional Transformers | Devlin et al. | 2019 | NAACL |

## 相关命令

- `/paper-summary` - 总结论文内容
- `/paper-notes` - 创建论文笔记
- `/annotation-extract` - 提取PDF注释
