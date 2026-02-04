---
name: note-organize
description: Organize and restructure notes based on analysis results, including tag normalization, link establishment, and duplicate note merging. Use when organizing note directories or creating index notes, or when the user mentions "整理笔记", "优化笔记", "重组笔记".
version: 1.0.0
---

# 笔记整理 (Note Organize)

根据分析结果，整理和优化笔记结构，包括标签规范化、建立链接、合并重复笔记等。

## When to Activate

- 用户说："整理笔记"、"优化笔记"、"重组笔记"
- 需要规范化标签格式
- 需要合并重复内容
- 需要创建索引笔记（**论文目录整理专项**）

## Critical Rules (CRITICAL)

### Rule 1: User Confirmation Required (CRITICAL)

**MUST** use `AskUserQuestion` before any destructive operations:

```markdown
## 整理方案概览
- 标签规范化：15个
- 建议链接：8对
- 建议合并：2组
- 目录调整：3个

请选择：
1. 全部执行
2. 部分执行（可选择标签规范化、建立链接等）
3. 仅预览（dry_run模式）
4. 取消
```

### Rule 2: Index Notes MUST Use Tables (REQUIRED)

**索引笔记必须使用表格格式**（便于 Dataview 自动索引）：

```markdown
## 1. Flow-based 方法

| 论文 | 会议 | 方法类型 | 状态 |
|------|------|----------|------|
| [[FlowEdit：Inversion-Free  Text-Based Editing\|FlowEdit]] | ICCV 2023 | Flow模型 | 已读完 |
| [[Flow-Based  Diffusion Model\|Flow-Based Diffusion]] | ICLR 2024 | Flow+Diffusion | 已读完 |
```

**表格中 Wikilink 的管道符必须转义**。

### Rule 3: Glob for Exact Filenames (CRITICAL)

**创建链接时必须使用 Glob 精确匹配文件名**：

```python
# ❌ BAD: 假设文件名
link = f"[[{paper_title}]]"

# ✅ GOOD: 使用 Glob 精确匹配
pattern = f"**/*{paper_title}*.md"
matches = glob.glob(pattern, recursive=True)
if matches:
    actual_filename = matches[0]
    link = f"[[{actual_filename}|{paper_title}]]"
```

### Rule 4: Paper Frontmatter Required (REQUIRED)

**整理论文目录时，必须为每篇论文添加统一的 frontmatter**：

```yaml
---
title: 论文完整标题（与文件名一致）
tags:
  - CV
  - Diffusion
  - CVPR
  - train-free
category: 图像编辑/图像恢复/逆问题/采样加速/Flow模型
created: YYYY-MM-DD
---
```

## 工作流程

### Step 1: 分析现状

使用 Glob 和 Read 工具分析笔记：

```python
# 扫描目标目录
pattern = f"{scope}/**/*.md"
notes = glob.glob(pattern, recursive=True)

# 分析每篇笔记
for note in notes:
    content = read_file(note)
    # 检查标签格式、Frontmatter、链接等
```

### Step 2: 生成整理方案

```python
# 生成整理方案
proposal = {
    "tag_normalization": find_tag_issues(notes),
    "link_suggestions": suggest_links(notes),
    "merge_candidates": find_duplicates(notes),
    "directory_adjustments": suggest_moves(notes)
}
```

### Step 3: 用户确认

使用 `AskUserQuestion` 让用户选择：

```markdown
## 整理方案概览
- 标签规范化：15个
- 建议链接：8对
- 建议合并：2组
- 目录调整：3个

请选择操作：
1. 全部执行
2. 部分执行（可选择具体操作）
3. 仅预览（dry_run模式）
4. 取消
```

### Step 4: 执行整理

根据用户选择执行：

```python
# 标签规范化
for tag_issue in proposal["tag_normalization"]:
    old_tag = tag_issue["old"]
    new_tag = tag_issue["new"]
    edit_file(note, old_tag, new_tag)

# 建立链接（使用 Glob 精确匹配）
for link in proposal["link_suggestions"]:
    pattern = f"**/*{link.target}*.md"
    matches = glob.glob(pattern, recursive=True)
    if matches:
        actual_filename = matches[0]
        link_text = f"[[{actual_filename}|{link.display}]]"
        edit_file(link.note, "", link_text, position=link.position)

# 合并笔记
for merge in proposal["merge_candidates"]:
    # 保留更完整的版本，添加合并记录
    merged_content = merge_notes(merge.notes)
    write_file(merge.target, merged_content)
```

### Step 5: 验证结果

重新扫描验证修改是否正确。

## GOOD vs BAD

### ✅ GOOD: 正确合并相似内容

```markdown
## 建议合并

| 笔记A | 笔记B | 相似度 | 建议 |
|-------|-------|--------|------|
| 注意力机制 | Attention机制 | 95% | 合并为一篇，保留中文标题 |

合并原因：
- 内容重复度95%
- 讨论同一概念
- A篇更完整，保留A篇
- 在B篇位置添加合并记录
```

### ❌ BAD: 错误合并不同内容

```markdown
发现以下笔记可以合并：
- Transformer架构 + BERT模型  ← ❌ 这是不同的论文，不应合并
- 扩散模型 + 图像生成        ← ❌ 主题不同，不应合并
```

### ✅ GOOD: 分步确认

```markdown
## 整理方案

### 标签规范化（安全操作）
- #扩散模型 → #CV/Generation/Diffusion
- #生成模型 → #CV/Generation

### 建议合并（需确认）
- 《注意力机制》 + 《Attention机制》
  请确认是否合并？

### 目录调整（需确认）
- 移动《PyTorch入门》→ 工具/编程/Python/
  请确认是否移动？
```

### ❌ BAD: 一次性执行所有操作

```python
# 直接执行所有操作，没有用户确认
for note in notes:
    normalize_tags(note)
    create_links(note)
    merge_duplicates(note)
```

### ✅ GOOD: 表格中转义管道符

```markdown
| [[FlowEdit：Inversion-Free  Text-Based Editing\|FlowEdit]] | ICCV 2023 | Flow模型 |
| [[Flow-Based  Diffusion Model\|Flow-Based Diffusion]] | ICLR 2024 | Flow+Diffusion |
```

### ❌ BAD: 表格中未转义

```markdown
| [[FlowEdit|FlowEdit]] | ICCV 2023 | Flow模型 |  ← 表格错位
```

## 核心功能

### 1. 标签规范化

```yaml
转换规则:
  - 中文标签 → 英文层级标签
  - 扁平标签 → 层级结构 (#一级/二级/三级)
  - 同义词 → 统一术语

示例:
  #扩散模型 → #CV/Generation/Diffusion
  #DL → #CV/DeepLearning
  #transformer → #CV/Architecture/Transformer
```

### 2. 建立链接

- 根据语义分析创建链接
- 使用 Glob 精确匹配文件名
- 智能判断链接位置
- 表格中必须转义管道符

### 3. 合并笔记

| 规则 | 说明 |
|------|------|
| 相似度阈值 | 85%以上才建议合并 |
| 保留策略 | 保留更完整的版本 |
| 历史记录 | 添加 merged_from 字段 |
| Frontmatter | 追融合并来源信息 |

### 4. 目录整理

- 优化目录结构
- 移动错位的笔记
- 创建目录索引
- 统一命名规范

## 论文目录整理（专项）

### 触发条件

- 用户明确指定"论文目录"、"Paper文件夹"
- 目录中包含大量论文笔记（>10篇）
- 笔记标题为论文名

### 工作流程

```
分析论文 → 创建索引 → 主题概览 → 建立链接 → Idea捕获 → 移动汇总
```

### 输出文件

1. **汇总索引**（`00_论文索引_[主题].md`）
   - 按研究方法分类（使用表格格式）
   - 概率框架分析
   - 交叉关联

2. **主题概览**（`主题_[名称].md`）
   - 概率视角分析
   - 方法对比
   - 理论延伸

3. **Idea笔记**（保存到 `Inspiration/`）
   - 理论动机
   - 可行性评估
   - 下一步方向

### 重要约定

**汇总文件必须移动到 `Conclusion/` 目录**：

```python
# 整理完成后移动汇总文件
mv Paper/00_论文索引_*.md Conclusion/
mv Paper/主题_*.md Conclusion/
```

### 参考案例

2026-01-27 `科研/CV/Generate/Paper/` 整理：
- 17篇论文分类
- 3个主题概览
- 4个Idea捕获
- 汇总移至 `Conclusion/`

## 输出格式

```markdown
# 笔记整理方案

## 标签规范化
- `#深度学习` → `#CV/DeepLearning`
- `#DL` → `#CV/DeepLearning`
- `#transformer` → `#CV/Architecture/Transformer`

## 建议链接
- 《Transformer架构》 ←→ 《自注意力机制》
- 《梯度下降》 ←→ 《优化算法》

## 建议合并
- 《注意力机制》 + 《Attention机制》 → 《注意力机制》
  原因：内容重复度95%

## 目录调整
- 移动《PyTorch入门》→ 工具/编程/Python/

## 确认执行？
1. 全部执行
2. 选择性执行
3. 取消
```

## 使用的工具

| 工具 | 用途 |
|------|------|
| `Glob` | 精确匹配文件名，扫描目录 |
| `Read` | 读取笔记内容 |
| `Write` | 创建新笔记，合并笔记 |
| `Edit` | 修改标签、添加链接 |
| `AskUserQuestion` | 用户确认操作 |

## 注意事项

- 不破坏用户现有内容
- 不删除用户原始数据
- 保留操作记录
- 可逆操作优先
- 执行前建议用户备份
