# /note-standardize - 笔记标准化

## 触发词
- "标准化笔记"
- "笔记格式化"
- "规范化笔记"
- "笔记标准化"

## 功能描述
对Obsidian笔记进行标准化处理，包括Callout格式化、Wikilink修复、Frontmatter管理、标签规范化、Embeds引用等。

## 与 obsidian-markdown 的关系

**分工明确**：
- **obsidian-markdown**：提供 Obsidian 格式语法参考文档
  - 例如：`> [!warning]` 是 Callout 的语法
  - 例如：`[[笔记|显示]]` 是 Wikilink 的语法
- **/note-standardize**：提供执行工作流
  - 分析内容 → 判断需要 Callout → 创建 Callout
  - 分析链接 → 使用 Glob 验证 → 修复 Wikilink
  - 分析标签 → 转换为英文层级结构 → 更新标签

**不是重复造轮子**：
- obsidian-markdown 是**文档技能**，不执行文件操作
- 本技能是**工作流封装**，整合 Read/Write/Edit/Glob 等底层工具
- 两者是**参考与执行**的关系，不是竞争关系

## 核心功能

### 1. Callout格式化
- **用途**：关键疑惑/注意点提醒
- **语法**：`> [!类型] 标题`
- **类型**：info、note、warning、tip、important、caution
- **场景**：
  - 论文笔记中的关键疑惑点
  - Idea笔记中的风险提醒
  - 概念笔记中的重要提示

**示例**：
```markdown
> [!warning] 关键疑惑
文章中的公式(3)与实际实现不符，需要进一步验证。

> [!tip] 优化思路
可以通过引入注意力机制来提升模型性能。
```

### 2. Wikilink修复
- **用途**：修复失效的Wikilink，规范化链接格式
- **格式**：`[[完整文件名|显示名]]`
- **修复内容**：
  - 使用Glob工具精确获取目标文件名
  - 处理文件名中的空格问题（单空格vs双空格）
  - 添加描述性别名
  - 检测并修复断链

**⚠️ 重要：表格中的Wikilink格式**
在Markdown表格中，管道符 `|` 会被解析为列分隔符，因此**必须转义**：

| 上下文 | 格式 |
|--------|------|
| 普通文本 | `[[文件名\|显示名]]` |
| **表格中** | `[[文件名\|显示名]]` |

**错误示例**（会导致表格错位）：
```markdown
| [[文件名|显示名]] | 下一列 |  ← 管道符被当作列分隔符
```

**正确示例**：
```markdown
| [[文件名\|显示名]] | 下一列 |  ← 转义管道符
```

**修复流程**：
1. 扫描笔记中的所有Wikilink
2. **检测上下文**：判断是否在表格中（查找表格标记 `|` 和 `---`）
3. 对每个链接使用Glob验证目标文件是否存在
4. 如果存在但不匹配，更新为精确文件名
5. **表格中的链接必须使用 `\|`**，普通文本中可用 `|`
6. 如果不存在，标记为断链

**示例**：
```python
# 普通文本中
[[Flow-Based  Diffusion Model|Flow-Based Diffusion Model]]

# 表格中（必须转义）
| [[Flow-Based  Diffusion Model\|Flow-Based Diffusion Model]] | 下一列 |
```

### 3. Frontmatter管理
- **用途**：补全缺失的Frontmatter，规范化格式
- **标准字段**：
  - `title`：笔记标题
  - `type`：笔记类型（论文/概念/项目/日志/索引）
  - `tags`：标签列表，层级格式（#CV/Generation/Diffusion）
  - `date`：单个日期字段，格式YYYY-MM-DD
  - `related`：相关笔记链接

**智能提取**：
- 从文件名提取title
- 从目录结构推断type
- 从内容中提取关键词作为tags
- 从文件修改时间获取date

**示例**：
```yaml
---
title: "Flow-Based Diffusion Model"
type: 论文
tags: [CV, Generation, Flow, Diffusion]
date: 2024-01-15
related: [["Normalizing Flows", "生成模型基础"]]
---
```

### 4. 标签规范化
- **用途**：统一标签格式，转换为英文术语层级结构
- **规范**：
  - 使用英文术语
  - 层级结构用`/`分隔
  - 最多3-4层
  - 避免过细分类

**常见标签**：
```
#CV/Generation/Diffusion
#CV/Generation/Flow
#CV/Classification
#NLP/Transformer
#Math/Probability
#Method/Optimization
```

**转换示例**：
```
#扩散模型 → #CV/Generation/Diffusion
#生成模型 → #CV/Generation
#注意力 → #CV/Architecture/Attention
```

### 5. Embeds引用
- **用途**：在论文笔记中嵌入概念定义
- **语法**：`![[笔记名]]`
- **场景**：
  - 论文笔记中引用基础概念
  - 方法笔记中引用相关技术
  - 避免重复定义

**示例**：
```markdown
## 方法

本文使用扩散模型进行图像生成。

![[扩散模型]]

在此基础之上，本文引入了...
```

## 工作流程

### 完整流程

```
1. 扫描目标笔记
2. 分析标准化需求
3. 生成标准化报告
4. 用户选择执行项
5. 执行标准化操作
6. 验证结果
```

### 分析阶段

扫描笔记后，分析以下内容：
- **Frontmatter**：缺失、格式不规范、需要智能提取
- **Wikilink**：失效链接、格式不规范、需要添加别名
- **标签**：中文标签、扁平结构、需要层级化
- **Callout机会**：关键疑惑点、风险点、优化建议
- **Embeds机会**：可嵌入的概念笔记

### 交互流程

分析完成后，使用AskUserQuestion询问用户：

```
请选择要执行的标准化操作：
1. 修复Wikilink（使用Glob精确匹配文件名）
2. 补全Frontmatter（智能提取元数据）
3. 规范化标签（转换为英文层级结构）
4. 添加Callout（为关键点添加提醒）
5. 创建Embeds引用（嵌入概念定义）
6. 全部执行
```

## 输出格式

### 标准化报告

```markdown
# 笔记标准化报告

## 分析范围
- 目录：科研/CV/Generate/Paper/
- 笔记数：17篇

## Frontmatter分析
- 缺失Frontmatter：3篇
- 格式不规范：5篇
- 可智能提取：7篇

## Wikilink分析
- 失效链接：2个
- 格式不规范：8个
- 需要添加别名：12个

## 标签分析
- 中文标签：5个
- 扁平结构：8个
- 需要层级化：10个

## Callout机会
- 关键疑惑点：3处
- 风险提醒：2处
- 优化建议：4处

## Embeds机会
- 可嵌入概念：扩散模型、注意力机制、变分推断

## 详细建议
...
```

## 执行策略

### 分步执行
- **高优先级**：修复Wikilink（避免断链）
- **中优先级**：补全Frontmatter、规范化标签
- **低优先级**：添加Callout、创建Embeds

### 安全措施
- 执行前备份笔记
- 逐个文件确认修改
- 保留原始内容不删除
- 标记修改位置

## 输入参数

| 参数 | 说明 | 必填 |
|------|------|------|
| scope | 标准化范围（目录/文件） | 是 |
| focus | 重点关注（frontmatter/wikilink/tags/callout/embeds） | 否 |

## 示例

### 示例1：修复Wikilink

```bash
用户: /note-standardize 科研/CV/Generate/QLink/ 修复链接

你: 正在分析QLink目录的Wikilink...

发现19个链接存在问题：
- 主题_频域方法.md中的6个链接（文件名空格不匹配）
- 主题_注意力控制.md中的6个链接（文件名空格不匹配）
- 主题_盲逆问题.md中的7个链接（文件名空格不匹配）

使用Glob精确匹配文件名后，修复所有链接。

✓ 修复完成
```

### 示例2：补全Frontmatter

```bash
用户: /note-standardize 科研/CV/Generate/Paper/ 补全元数据

你: 正在分析Paper目录的Frontmatter...

发现3篇笔记缺失Frontmatter：
- FreeMA.md
- Spectral Diffusion.md
- FDG-Diff.md

智能提取元数据：
- title: 从文件名提取
- type: 推断为"论文"
- tags: 从内容关键词提取
- date: 使用文件修改时间

询问是否执行？
```

### 示例3：规范化标签

```bash
用户: /note-standardize 科研/ 规范化标签

你: 正在分析科研目录的标签...

发现不规范标签：
#扩散模型 → 应为 #CV/Generation/Diffusion
#生成模型 → 应为 #CV/Generation
#频域方法 → 应为 #Method/Fourier
#注意力控制 → 应为 #CV/Architecture/Attention

共10个标签需要规范化。是否执行？
```

## 技术细节

### Glob工具使用

```python
# 修复Wikilink时使用Glob精确匹配
import glob

# 获取可能的文件名
pattern = f"**/{paper_title}*.md"
matches = glob.glob(pattern, recursive=True)

if len(matches) == 1:
    actual_filename = matches[0]
    link = f"[[{actual_filename}|{paper_title}]]"
```

### Frontmatter解析

```python
# 检查Frontmatter是否存在
def has_frontmatter(content):
    return content.startswith('---')

# 智能提取标题
def extract_title(filename):
    return filename.replace('.md', '')

# 从内容提取标签关键词
def extract_tags(content):
    keywords = ['扩散模型', '注意力', 'Transformer', ...]
    # 实现关键词提取逻辑
    pass
```

## 注意事项

- **尊重原有内容**：不删除任何有效内容
- **渐进式修改**：分步执行，逐步验证
- **用户确认**：所有修改需用户确认
- **备份习惯**：执行前建议用户备份
- **格式一致性**：遵循PRD.md中的格式规范

## 参考文档

- `PLAN/PRD.md` - 设计决策和格式规范
- `PLAN/references/论文笔记参考.md` - 论文笔记格式
- `docs/workflows/note-organization.md` - 笔记整理工作流
