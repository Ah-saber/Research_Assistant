---
name: paper-summary
description: 生成论文的详细中文摘要，包括背景、问题、方法、结果和结论
version: 1.0.0
---

# 论文总结

生成论文的详细中文摘要。

## When to Activate（何时启用）

- 用户说："总结论文"、"论文概要"、"论文摘要"
- 用户说："总结xxx论文"、"这篇论文讲了什么"
- 用户搜索论文后希望了解某篇论文的内容

## 与外部格式参考技能的关系

本技能**不直接使用**格式参考技能，因为总结结果仅用于展示。

如果需要将总结保存为笔记，会使用 `/paper-notes` 技能（该技能使用 obsidian-markdown 格式）。

## 工作流程

1. **获取论文信息**
   - 如果提供了 item_key：使用 `mcp__zotero__zotero_get_item_metadata` 获取元数据
   - 如果没有：先使用 `/paper-search` 搜索

2. **提取论文内容**
   - 使用 `mcp__zotero__zotero_get_item_fulltext` 获取全文
   - 如果全文超限，降级到摘要生成

3. **生成摘要**
   - **研究背景**：为什么做这个研究
   - **研究问题**：要解决什么问题
   - **方法**：用了什么方法
   - **主要发现**：关键结果
   - **结论**：研究意义
   - **局限性**：研究的限制

4. **格式化输出**
   - 使用 markdown 格式
   - 中文输出，保留英文术语
   - 包含 BibTeX 引用

## 摘要结构

### 1. 研究背景（Background）
- 领域现状和背景
- 相关工作简介

### 2. 研究问题（Problem）
- 要解决的核心问题
- 现有方法的不足

### 3. 研究动机（Motivation）
- 为什么需要解决这个问题
- 解决这个问题的意义

### 4. 创新方法（Method）
- 核心方法和算法
- 关键技术细节
- 模型架构（如有图示）

### 5. 实验结果（Results）
- 主要实验设置
- 关键结果数据
- 与 baseline 的比较

### 6. 结论与贡献（Conclusion）
- 主要发现
- 贡献总结
- 局限性讨论

## 额外内容

### 关键公式提取
- 列出核心公式
- 解释公式含义
- 说明公式作用

### 技术深度
- 详细版：800字以上
- 包含技术细节
- 学术风格表达

## 输入参数

| 参数 | 说明 | 必填 |
|------|------|------|
| paper | 论文（标题/ID/Zotero key） | 是 |
| detail | 详细程度（simple/detailed） | 否 |

## 输出格式

```markdown
# [论文标题] - 论文总结

## 基本信息
- **作者**：xxx
- **年份**：xxxx
- **发表**：xxx

## 研究背景
...

## 研究问题
...

## 核心方法
...

## 主要结果
...

## 关键公式
...

## 结论
...
```

## 使用的 MCP 工具

| 工具 | 用途 | 使用场景 | 限制 |
|------|------|----------|------|
| `mcp__zotero__zotero_get_item_fulltext` | 获取论文全文 | 生成详细摘要 | 可能超token限制 |
| `mcp__zotero__zotero_get_item_metadata` | 获取论文元数据 | 获取基本信息和摘要 | 总是成功 |

## GOOD vs BAD（对比示例）

### ✅ GOOD

```bash
用户: 总结 Attention Is All You Need

AI: 1. 使用 mcp__zotero__zotero_get_item_fulltext 获取全文
    2. 全文超限，降级到 metadata["abstract"]
    3. 基于摘要生成结构化总结，明确标注"基于摘要生成"
    4. 输出包含：背景、问题、方法、结果、结论
```

### ❌ BAD

```bash
用户: 总结论文

AI: 1. 直接调用全文工具，未处理超限错误
    2. 失败后没有降级策略
    3. 没有明确标注数据来源
    4. 总结结构不完整
```

## MCP工具使用注意事项

### 全文超限处理
当 `mcp__zotero__zotero_get_item_fulltext` 返回内容超过token限制时：

1. **检测超限**：
   ```
   Error: result (122,415 characters) exceeds maximum allowed tokens
   Output has been saved to: [file_path]
   ```

2. **分页读取**：
   ```bash
   # 使用 Read 工具分段读取
   Read(file_path, offset=1, limit=500)
   Read(file_path, offset=501, limit=500)
   ```

3. **降级策略**：
   - 优先使用论文摘要生成基础总结
   - 明确标注"基于摘要生成，建议补充全文细节"

### 路径格式问题
- **Bash 工具**: 使用正斜杠 `/` 或双反斜杠 `\\`
- **Read 工具**: 使用双反斜杠 `\\` 转义
- **路径变量**: 避免直接使用包含反斜杠的路径变量

## 快速参考表

| 场景 | 命令 | 说明 |
|------|------|------|
| 简单总结 | /paper-summary 论文标题 detail:simple | 快速概览 |
| 详细总结 | /paper-summary 论文标题 | 完整分析 |
| 基于 key | /paper-summary ABCD123 | 直接引用 |
