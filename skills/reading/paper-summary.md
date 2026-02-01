# Paper Summary Skill

生成学术论文的中文摘要。

## 使用场景

当用户说：
- "总结论文"
- "论文概要"
- "总结[paper_key]"
- "这篇论文讲了什么"

## 工作流程

1. **获取论文信息**
   - 如果提供了paper_key：使用`zotero_get_item_metadata`获取元数据
   - 如果没有：先使用`/paper-search`搜索

2. **提取论文内容**
   - 使用`zotero_get_item_fulltext`获取全文
   - 如果PDF可访问，使用pdf skill提取结构化内容

3. **生成摘要**
   - 包含以下部分：
     - **研究背景**：为什么做这个研究
     - **研究问题**：要解决什么问题
     - **方法**：用了什么方法
     - **主要发现**：关键结果
     - **结论**：研究意义
     - **局限性**：研究的限制

4. **格式化输出**
   - 使用markdown格式
   - 中文输出
   - 包含BibTeX引用

## 示例输出

```markdown
# Attention Is All You Need

## 基本信息
- **作者**: Vaswani et al.
- **年份**: 2017
- **会议**: NeurIPS

## 研究背景
传统的序列到序列模型主要使用循环神经网络或卷积神经网络作为编码器-解码器...

## 研究问题
能否完全依赖注意力机制来构建序列模型，而不使用循环或卷积？

## 方法
提出了Transformer架构，完全基于注意力机制...

## 主要发现
1. Transformer在机器翻译任务上取得了SOTA效果
2. 训练速度显著快于RNN/CNN模型
3. 注意力可视化提供了模型可解释性

## BibTeX
```bibtex
@inproceedings{vaswani2017attention,
  title={Attention is all you need},
  author={Vaswani, Ashish and others},
  booktitle={NeurIPS},
  year={2017}
}
```
```

## 相关命令

- `/paper-search` - 搜索论文
- `/paper-notes` - 创建论文笔记
- `/annotation-extract` - 提取PDF注释
