---
name: paper-notes
description: 为论文创建完整的Obsidian笔记，包含元数据、摘要、公式和个人思考
version: 1.0.0
---

# 论文笔记

为论文创建完整的Obsidian笔记。

## When to Activate（何时启用）

- 用户说："创建论文笔记"、"为论文写笔记"
- 用户说："生成论文笔记"、"论文笔记"
- 用户阅读完论文后需要保存笔记

## 与外部格式参考技能的关系

**重要**：本技能参考以下格式参考技能获取语法规范：

- **obsidian-markdown**：提供 Obsidian Markdown 语法规范
  - Wikilink: `[[笔记|显示]]`
  - Callout: `> [!类型] 标题`
  - Frontmatter: YAML 格式
  - Tags: `#标签` 层级结构
  - Embeds: `![[笔记]]`

- **json-canvas**：提供 Canvas (.canvas) 格式规范
  - 节点类型: file, text, group
  - 边类型: 实线、虚线、点线
  - 布局算法: 层次、力导向、区域

**分工明确**：
- 格式参考技能：提供语法文档，不执行操作
- 本技能：工作流封装，使用 Read/Write/Edit + Glob 执行操作

## 工作流程

1. **获取论文信息**
   - 使用 `mcp__zotero__zotero_get_item_metadata` 获取元数据
   - 使用 `mcp__zotero__zotero_get_item_fulltext` 获取全文（可能超限）

2. **检查现有笔记**
   - 在Obsidian中搜索是否已有相关笔记
   - 避免重复创建

3. **生成笔记内容**
   - 使用论文笔记模板
   - 包含：Frontmatter、基本信息、摘要、方法、实验、MyPoint

4. **询问用户保存位置**
   - 提供默认路径建议
   - 接受自定义路径

5. **创建笔记文件**
   - 使用 Write 工具创建
   - 文件名：仅使用论文英文标题

6. **自动链接相关笔记**
   - 检查现有相关笔记
   - 添加双向链接（使用 Glob 精确匹配文件名）

## 笔记结构

### Frontmatter

```yaml
---
title: "论文标题"
authors: [作者1, 作者2]
year: 2024
venue: "会议/期刊名"
tags: [论文, 主题, 子主题]
date: 2024-01-15
status: reading
zotero_key: XXXXX
related: []
---
```

### 笔记内容模块

## 模块1: MyPoint（个人思考）

### 我的思考
- 论文给我的启发
- 与我研究的关系
- 可能的研究方向

### 疑惑与问题（使用Callout标记关键疑惑）
- 不理解的地方
- 需要进一步研究的问题

**Callout用法**：对关键疑惑点使用Callout格式化（语法参考 obsidian-markdown）：
```markdown
> [!warning] 关键疑惑
文章中的公式(3)推导过程不清晰，需要查阅原始文献验证。

> [!note] 需要验证
实验设置中batch size的选择缺乏消融实验支持。
```

支持的Callout类型：info, note, tip, important, warning, caution（详见 obsidian-markdown skill）

### TODO
- [ ] 阅读引用的论文X
- [ ] 复现实验Y
- [ ] 思考如何应用Z

## 模块2: 概率框架分析（如适用）

### 概率建模
- **似然函数**：$p(x|z)$ 或 $p(y|x)$ 的形式
- **后验推断**：$p(z|x)$ 或推断目标
- **变分推断**：ELBO、KL散度、近似分布
- **潜变量结构**：潜在空间的设计和解释

### 信息论视角
- **目标函数**：从信息论角度解释（如互信息最大化、KL散度最小化）
- **熵的作用**：熵正则化、不确定性建模
- **率失真**：压缩与重构的权衡（如VAE、向量量化）

### 生成式/判别式分析
- **模型类型**：生成式 $p(x,y)$ vs 判别式 $p(y|x)$
- **优势对比**：为什么选择这种范式
- **与相关工作的范式对比**

### 贝叶斯视角
- **先验选择**：隐含或显式的先验假设
- **推断方法**：变分推断、MCMC、MAP
- **共轭结构**：是否存在共轭分布简化推断
- **非贝叶斯解释**：从正则化、优化等角度理解

## 模块3: 论文笔记（深入研究报告）

### 基本信息区
- 论文标题（中英）
- 作者与机构
- 发表信息
- DOI/链接

### 研究背景
- 领域现状
- 相关工作

### 研究问题
- 核心问题
- 现有方法不足
- 研究动机

### 创新方法
- 核心方法
- 技术细节
- 模型架构

**Embeds引用**：对于论文中涉及的基础概念，使用Embeds嵌入概念笔记（语法参考 obsidian-markdown）：
```markdown
## 方法

本文基于扩散模型进行图像生成：

![[扩散模型]]

在此基础之上，本文引入了频域变换：

![[傅里叶变换]]

通过结合两种方法...
```

使用Embeds的场景：
- 论文基于某个经典方法/模型
- 涉及重要的数学/物理概念
- 引用其他技术作为组件

Embeds语法：`![[笔记名]]`、`![[笔记名#标题]]`（详见 obsidian-markdown skill）

### 主要公式
```
公式1：Attention(Q,K,V) = softmax(QK^T/√d_k)V
```
- 公式含义
- 符号说明

### 实验结果
- 实验设置
- 主要结果
- 与baseline比较

### 总结与评价
- 主要贡献
- 方法局限性
- 个人评价

### 参考文献
- 相关论文链接
- 引用格式

## 模板文件

参考 `PLAN/references/论文笔记参考.md` 获取完整模板。

## 输入参数

| 参数 | 说明 | 必填 |
|------|------|------|
| paper | 论文（标题/ID/Zotero key） | 是 |
| template | 模板类型 | 否，默认完整版 |
| attach_annotations | 是否附加注释 | 否，默认false |

## 使用的 MCP 工具

| 工具 | 用途 | 使用场景 | 限制 |
|------|------|----------|------|
| `mcp__zotero__zotero_get_item_metadata` | 获取元数据 | 获取基本信息和摘要 | 总是成功 |
| `mcp__zotero__zotero_get_item_fulltext` | 获取全文 | 生成详细笔记 | 可能超token限制 |
| `mcp__zotero__zotero_get_annotations` | 获取注释 | 附加PDF注释 | 可选 |

## 笔记命名规则

- 使用论文英文标题
- 不加日期前缀
- 例如：`Attention Is All You Need.md`

## 自动链接

创建笔记时自动：
- 检查现有相关笔记
- 添加双向链接
- 更新相关笔记的链接
- 链接到引用关系图谱（新增）← 调用 `/paper-graph` 生成或更新

**Canvas引用图谱链接**：
- 如果存在论文引用关系图谱（.canvas文件），在笔记中添加链接
- 链接格式：`![[论文引用关系图谱.canvas]]` 或相关图谱文件的Wikilink
- 建议调用 `/paper-graph` 生成或更新引用关系图谱

这些功能参考 **json-canvas** 格式规范，使用 Read/Write/Edit + Glob 执行

## GOOD vs BAD（对比示例）

### ✅ GOOD

```bash
用户: 为 Attention Is All You Need 创建笔记

AI: 1. 使用 mcp__zotero__zotero_get_item_metadata 获取元数据
    2. 检测到全文超限，使用 metadata["abstract"] 降级
    3. 使用 Glob 检查是否已有相关笔记
    4. 创建笔记时：
       - Frontmatter 格式参考 obsidian-markdown
       - 使用 Callout 标记关键疑惑
       - 使用 Glob 精确匹配创建 Wikilink
    5. 建议调用 /paper-graph 生成引用图谱
```

### ❌ BAD

```bash
用户: 创建论文笔记

AI: 1. 直接使用假设的文件名创建 Wikilink（未使用 Glob）
    2. Callout 格式错误
    3. 未检查是否已有重复笔记
    4. 全文超限后没有降级策略
    5. 未建议生成引用图谱
```

## MCP工具使用注意事项

### 全文超限处理策略
当 `mcp__zotero__zotero_get_item_fulltext` 返回内容超过token限制时：

1. **检测超限**：
   ```
   Error: result (122,415 characters) exceeds maximum allowed tokens
   Output has been saved to: [file_path]
   ```

2. **分页读取**：
   ```bash
   # 使用Read工具分段读取
   Read(file_path, offset=1, limit=500)
   Read(file_path, offset=501, limit=500)
   ```

3. **降级策略**：
   - 优先使用论文摘要生成基础笔记
   - MyPoint模块基于摘要和元数据生成
   - 明确标注"基于摘要生成，建议补充全文细节"

### 注释提取处理
当 `attach_annotations=true` 时：
1. 先调用 `mcp__zotero__zotero_get_annotations` 检查是否有注释
2. 无注释则跳过，不阻塞笔记创建流程
3. 有注释则附加到笔记末尾

### 推荐工作流优化
```bash
# 1. 获取元数据（总是成功）
metadata = mcp__zotero__zotero_get_item_metadata(item_key)

# 2. 尝试获取全文（可能超限）
try:
    fulltext = mcp__zotero__zotero_get_item_fulltext(item_key)
except TokenLimitError:
    # 使用摘要降级
    fulltext = metadata["abstract"]
    note_quality = "basic"

# 3. 检查注释（可选）
annotations = mcp__zotero__zotero_get_annotations(item_key)

# 4. 生成笔记
generate_note(metadata, fulltext, annotations)
```

## 与 Canvas 可视化的关系

**三层协作架构**：

| 层级 | 组件 | 作用 |
|------|------|------|
| **格式参考** | json-canvas skill | 提供 Canvas (.canvas) 格式规范文档 |
| **执行工具** | Read/Write/Edit + Glob | 底层文件操作 |
| **工作流封装** | /paper-graph 等 | 业务逻辑 |

**分工明确**：
- **json-canvas**：提供 Canvas 格式规范文档
  - 节点类型（file、text、group）、边类型、布局算法
- **Visualization Skills**：提供可视化工作流
  - `/paper-graph` - 论文引用关系图谱（层次布局）
  - `/knowledge-canvas` - 综合知识画布（区域布局）
- **/paper-notes**：创建论文笔记时，建议生成或链接到引用关系图谱

**不是重复造轮子**：
- json-canvas 是**文档技能**，不执行文件操作
- Visualization Skills 是**工作流封装**，使用 Read/Write/Edit + Glob 创建Canvas文件
- 本技能是**笔记创建层**，创建论文笔记后，建议调用对应可视化技能生成引用图谱

**可视化建议触发条件**：
- 创建新论文笔记时 → 检查是否存在引用关系图谱，建议更新
- 论文包含多个参考文献 → 建议调用 `/paper-graph` 生成引用关系图谱
- 笔记中添加Embeds引用多个概念笔记 → 建议调用 `/knowledge-canvas` 生成综合知识画布

## 快速参考表

| 场景 | 命令 | 说明 |
|------|------|------|
| 创建笔记 | /paper-notes 论文标题 | 完整版笔记 |
| 简化版 | /paper-notes 论文标题 template:simple | 不含概率框架 |
| 带注释 | /paper-notes 论文标题 attach_annotations:true | 包含PDF注释 |
| 基于 key | /paper-notes ABCD123 | 直接引用 |
