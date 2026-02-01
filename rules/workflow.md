# 工作流规范

本文档定义 Research Assistant 项目的标准工作流。

---

## 什么是工作流

工作流是一系列有序的任务步骤，用于完成特定目标。

**工作流 vs Skill vs Command**：
- **Skill**：封装特定能力，可被工作流调用
- **Command**：快捷命令，触发特定工作流
- **Workflow**：完整的多步骤流程

---

## 标准工作流

### 1. 论文阅读工作流

```
搜索论文 → 获取摘要 → 阅读全文 → 创建笔记 → 捕捉 Idea
```

| 步骤 | Skill | Command | MCP 工具 |
|------|-------|---------|----------|
| 搜索论文 | paper-search | /search-paper | zotero_search_items |
| 获取摘要 | paper-summary | - | zotero_get_item_metadata |
| 阅读全文 | - | - | zotero_get_item_fulltext |
| 创建笔记 | paper-notes | /create-paper-note | - |
| 捕捉 Idea | idea-capture | /capture-idea | - |

### 2. 笔记整理工作流

```
分析笔记 → 发现问题 → 整理笔记 → 建立关联 → 标准化格式
```

| 步骤 | Skill | Command |
|------|-------|---------|
| 分析笔记 | note-analyze | /analyze-notes |
| 整理笔记 | note-organize | /organize-notes |
| 建立关联 | note-link | /link-notes |
| 标准化 | note-standardize | /standardize-notes |

### 3. Idea 管理工作流

```
捕捉 Idea → 保存到 Inspiration → 定期回顾 → 移至 IDEA 目录
```

| 步骤 | Skill | Command |
|------|-------|---------|
| 捕捉 Idea | idea-capture | /capture-idea |
| 整理 Idea | idea-organize | /organize-ideas |
| 回顾 Idea | idea-review | /review-ideas |

---

## 工作流触发条件

### 自动触发

当用户描述匹配工作流时，自动建议完整工作流：

```
用户："帮我阅读这篇论文"
AI："检测到论文阅读需求，建议执行完整工作流：
     1. 搜索论文（/search-paper）
     2. 获取摘要
     3. 创建笔记（/create-paper-note）
     "
```

### 手动触发

用户直接运行 Command：

```
用户：/search-paper attention mechanism
```

---

## 工作流执行原则

### 顺序执行

工作流中的步骤按顺序执行，前一步完成后再执行下一步。

### 可中断

用户可以随时中断工作流，选择只执行部分步骤。

### 状态保持

工作流执行过程中保持状态，允许从中断处继续。

---

## 工作流文档

详细工作流文档位于 `docs/workflows/`：

- `paper-reading.md` - 论文阅读工作流
- `note-organization.md` - 笔记整理工作流
- `idea-management.md` - Idea 管理工作流

---

## 参考

- **工作流文档**：`docs/workflows/`
- **技能文档**：`skills/*/SKILL.md`
- **命令文档**：`commands/*.md`
