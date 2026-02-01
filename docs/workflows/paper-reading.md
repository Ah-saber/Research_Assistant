# 论文阅读工作流

本文档描述使用Research Assistant进行论文阅读的完整工作流程。

## 工作流概览

```
搜索论文 → 查看详情 → 阅读论文 → 提取注释 → 创建笔记 → 记录Idea
```

## 工作流变体

### 完整工作流
适用于重要论文，需要深入研究和建立关联。

```
/paper-search → /annotation-extract → /paper-notes → /note-link → /note-standardize
```

### 快速工作流
用于快速浏览或了解论文概况。

```
/paper-search → /paper-notes
```

### 可视化增强工作流
当需要建立论文关系图谱或追踪阅读进度时使用。

```
/paper-search → /paper-notes → /paper-graph → /paper-dashboard
```

## 详细步骤

### 1. 搜索论文

使用 `/paper-search` 在Zotero中搜索相关论文。

```bash
/paper-search "transformer可解释性"
```

**输出**：
- 相关论文列表（10-15篇）
- 每篇论文包含标题、作者、年份、简要摘要

**操作**：
- 选择感兴趣的论文
- 记录论文序号或标题

### 2. 查看论文详情

基于搜索结果，选择论文并获取更多信息。

```bash
用户: 总结第5篇论文
```

AI将根据搜索结果中的摘要信息生成论文总结。

**输出**：
- 研究背景
- 研究问题
- 创新方法
- 主要结果
- 结论与贡献
- 关键公式

### 3. 提取PDF注释

如果已在Zotero中阅读并添加注释，提取注释内容。

```bash
/annotation-extract "Attention Is All You Need"
```

**输出**：
- 按颜色分组的高亮
- 用户笔记
- 页码引用

### 4. 创建Obsidian笔记

使用 `/paper-notes` 创建完整的论文笔记。

```bash
/paper-notes "Attention Is All You Need"
```

**输出**：
- 包含MyPoint模块的完整笔记
- **概率框架分析**模块（概率建模、信息论视角、贝叶斯视角）
- 论文深入研究报告
- 元数据和引用信息
- 自动链接相关笔记

### 5. 建立笔记关联

使用 `/note-link` 建立与其他笔记的关联。

```bash
/note-link "Transformer架构"
```

**功能**：
- 发现语义相关的笔记
- 建议链接位置
- 添加描述性链接

### 6. 笔记标准化

使用 `/note-standardize` 规范化笔记格式。

```bash
/note-standardize "Attention Is All You Need"
```

**处理内容**：
- Callout格式规范化
- Wikilink验证和修复
- Frontmatter补全
- 标签规范化
- Embeds引用检查

### 7. 记录研究想法

阅读过程中产生想法时，使用 `/idea-capture` 记录。

```bash
记录Idea：将自注意力机制应用于时序数据异常检测
```

**输出**：
- 保存到Inspiration目录
- 自动添加标签和关联
- 包含动机和下一步建议

## 完整示例

```
用户: /paper-search transformer可解释性

你: 找到12篇相关论文：

[1] Attention is All You Need
Vaswani et al. · 2017 · NeurIPS
摘要：提出纯注意力机制的Transformer架构...

用户: 总结第1篇

你: # Attention Is All You Need - 论文总结

[详细摘要内容...]

用户: 为这篇论文创建笔记

你: 正在创建笔记...

✓ 获取论文元数据
✓ 检测到3篇相关笔记
✓ 生成笔记内容

笔记已创建：Attention Is All You Need.md

用户: 我有个想法，能不能用注意力来解释CNN的决策？

你: [使用/idea-capture记录]

✓ 已记录Idea到Inspiration/2024/01-15-注意力解释CNN.md
```

## 快速工作流

对于快速阅读，可以使用简化流程：

```
/paper-search → 选择论文 → /paper-notes
```

这将：
1. 搜索论文
2. 自动生成摘要
3. 创建完整笔记
4. 一次性完成

## 高级用法

### 批量处理

```bash
# 为多篇论文创建笔记
/paper-notes "论文1, 论文2, 论文3"
```

### 带注释创建

如果论文已有PDF注释，使用 `/annotation-extract` 提取后，可以在创建笔记时包含注释内容。

```bash
# 先提取注释
/annotation-extract "论文标题"

# 再创建笔记（包含注释）
/paper-notes "论文标题"
```

### 自定义模板

```bash
# 使用自定义模板
/paper-notes "论文标题" --template "我的模板.md"
```

## 最佳实践

1. **先搜索后阅读**：使用`/paper-search`找到相关论文，评估相关性后再深入阅读
2. **笔记结构化**：使用标准的论文笔记模板，保持一致性
3. **及时记录想法**：阅读时产生的Idea立即用`/idea-capture`记录
4. **建立链接**：创建笔记后，使用`/note-link`建立与其他笔记的关联
5. **定期回顾**：使用`/idea-review`回顾Inspiration中的想法

## 常见问题

### Q: 如何找到论文的Zotero key？
A: 使用`/paper-search`搜索，结果中会显示key。或使用论文标题。

### Q: 笔记保存在哪里？
A: 默认保存在Obsidian vault的科研目录，创建时可以指定位置。

### Q: 如何更新已有笔记？
A: 使用`Read`和`Edit`工具修改，或重新运行`/paper-notes`选择追加模式。

### Q: Idea记录在哪里？
A: 临时保存在Inspiration目录，确认价值后手动移至科研/IDEA目录。

## 相关技能

- `/paper-search` - 搜索论文
- `/paper-summary` - 总结论文
- `/annotation-extract` - 提取注释
- `/paper-notes` - 创建笔记
- `/idea-capture` - 记录想法
- `/note-link` - 建立关联
- `/note-standardize` - 标准化笔记格式
