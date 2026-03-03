---
name: note-standardize
description: 标准化 Obsidian 笔记格式，包括 Callouts、Wikilinks、Frontmatter、标签和嵌入引用。**必须使用此技能**当用户说"标准化笔记"、"格式化标签"、"推荐标签"、"检查标签一致性"、"修复链接"、"添加标签"，或处理任何 Obsidian 笔记格式问题时自动触发。核心特性：维护标签数据库，利用语义理解确保同类型论文使用一致的标签。
version: 2.0.0
---

# 笔记标准化 (Note Standardize)

对 Obsidian 笔记进行标准化处理，包括 Callout 格式化、Wikilink 修复、Frontmatter 管理、**标签智能推荐与一致性检查**。

## Quick Start

```
用户请求 → 读取标签数据库 → 语义匹配 → 推荐/修复 → 用户确认 → 更新数据库 → 执行
```

---

## Critical Rules

### Rule 1: 标签数据库优先 (CRITICAL)

推荐标签前**必须先读取 `references/tags_database.md`**

1. 使用 `Read` 工具读取 `references/tags_database.md`
2. 利用**语义理解**找到与新论文最相似的已存在标签
3. 优先使用已有标签，保持一致性
4. 如果是全新标签类型，添加到数据库的"新标签记录区"

### Rule 2: Glob 精确匹配 (CRITICAL)

创建 Wikilink 时**必须**使用 Glob 工具精确匹配文件名。

### Rule 3: 参考格式规范

Obsidian 格式参考：`../obsidian-markdown copy/SKILL.md`

---

## 标签推荐流程

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: 读取标签数据库                                      │
│   Read("references/tags_database.md")                                  │
│   查看已有的标签和"相似关键词"列                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 2: 理解新论文                                         │
│   提取：标题 + 摘要 + 方法 + 任务                            │
│   识别：任务类型、方法类别、应用领域                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 3: 语义匹配                                           │
│   在数据库中找语义相似的标签                                  │
│   利用"相似关键词"列进行匹配                                  │
│   例如: "noise removal" ≈ "Denoising"                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 4: 推荐标签                                           │
│   如果找到相似标签 → 推荐已有标签                             │
│   如果是全新类型 → 创建新标签，添加到数据库                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 5: 用户确认                                           │
│   使用 AskUserQuestion 展示推荐标签和理由                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 6: 执行并更新                                         │
│   Edit 工具修改笔记                                          │
│   如果是新标签，更新 references/tags_database.md                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 标签层级结构

### 标准格式

```
CV/{Level}/{SubLevel}/{Task}      # 任务标签
Method/{Category}/{Specific}      # 方法标签
Math/{Category}/{Specific}        # 数学/理论标签
Venue/{Conference}                # 发表场所标签
```

### 示例

| 类型 | 标签示例 |
|------|----------|
| 任务 | `CV/Low-Level/Infrared/Enhancement` |
| 任务 | `CV/Generation/Image-Editing` |
| 方法 | `Method/Generation/Diffusion` |
| 方法 | `Method/Learning/Self-Supervised` |
| 方法 | `Method/Architecture/Attention` |
| 方法 | `Method/Frequency-Domain` |
| 数学 | `Math/Sampling/Posterior-Sampling` |
| 场所 | `Venue/CVPR` |

---

## 标签数据库

**位置**：`references/references/tags_database.md`

**内容结构**：
- 任务标签（按层级分类）
- 方法标签（按类型分类）
- 相似关键词列表（用于语义匹配）

**使用方式**：
1. 推荐标签前先 `Read("references/tags_database.md")`
2. 利用"相似关键词"列进行语义匹配
3. 新标签添加到"新标签记录区"

---

## GOOD vs BAD

### ✅ GOOD: 先查数据库，语义匹配

```
输入: "A method for removing noise from thermal images"

Step 1: Read("references/tags_database.md")
Step 2: 理解语义 → noise removal ≈ Denoising, thermal ≈ Infrared
Step 3: 推荐结果 → CV/Low-Level/Infrared/Denoising
```

### ❌ BAD: 不查数据库，直接编造

```
输入: "Noise Removal in Thermal Images"
输出: #Infrared #Denoising  # 扁平结构，与历史不一致！
```

### ✅ GOOD: Glob 精确匹配

```
pattern = f"**/*{title}*.md"
matches = glob.glob(pattern, recursive=True)
link = f"[[{matches[0]}|{title}]]"
```

### ❌ BAD: 假设文件名

```
link = f"[[{title}|{title}]]"  # 可能失效
```

---

## 快速参考

| 场景 | 操作 |
|------|------|
| 推荐标签 | 先 `Read("references/tags_database.md")`，再语义匹配 |
| 修复 Wikilink | Glob 精确匹配文件名 |
| 表格链接 | 转义管道符 `\|` |
| Callout 格式 | 参考 obsidian-markdown |
| 检查一致性 | 扫描目录，语义分组，生成报告 |

---

## 使用的工具

| 工具 | 用途 |
|------|------|
| `Read` | 读取标签数据库、笔记内容 |
| `Glob` | 精确匹配文件名 |
| `Edit` | 修改笔记、更新标签数据库 |
| `AskUserQuestion` | 用户确认 |

---

## 注意事项

- **历史标签优先**：推荐前先查 `references/tags_database.md`
- **语义理解**：利用 LLM 能力理解标签相似性
- **用户确认**：所有修改需用户确认
- **持续维护**：新标签及时添加到数据库
- **建议备份**：批量修改前建议备份
