# Obsidian 集成规范

本文档定义 Obsidian 集成规范，参考 `obsidian-skills` 项目。

---

## 格式参考技能

| 技能 | 项目路径 | 原参考项目 | 说明 |
|------|----------|-----------|------|
| obsidian-markdown | `skills/obsidian-markdown/SKILL.md` | obsidian-skills | Markdown 格式参考 |
| json-canvas | `skills/json-canvas/SKILL.md` | obsidian-skills | Canvas 格式参考 |
| obsidian-bases | `skills/obsidian-bases/SKILL.md` | obsidian-skills | Bases 格式参考 |

**说明**：这些格式参考技能已复制到项目 `skills/` 目录，可被其他技能引用。

---

## 访问控制

### 受保护目录

以下目录**禁止自动访问**，需要用户明确授权：

| 目录 | 路径 | 访问方式 |
|------|------|----------|
| IDEA | `C:\Note\MyNote_Obs\科研\IDEA` | 需要用户明确授权 |
| 思绪 | `C:\Note\MyNote_Obs\思绪` | 需要用户明确授权 |

### 可自由访问的目录

| 目录 | 路径 | 用途 |
|------|------|------|
| Inspiration | `C:\Note\MyNote_Obs\Inspiration` | 临时 Idea 存储 |
| Vault 根目录 | `C:\Note\MyNote_Obs\**` | 其他笔记 |

---

## Obsidian Markdown 格式规范

参考 `obsidian-markdown` 技能。

### Wikilink

**使用 Glob 精确匹配**（重要）：
```python
# ✅ GOOD
pattern = f"**/*{paper_title}*.md"
matches = glob.glob(pattern, recursive=True)
if matches:
    actual_filename = matches[0]
    link = f"[[{actual_filename}|{paper_title}]]"

# ❌ BAD
link = f"[[{paper_title}]]"  # 文件名可能有特殊空格
```

### 基本语法

| 格式 | 说明 | 示例 |
|------|------|------|
| `[[笔记名]]` | 基本链接 | `[[深度学习]]` |
| `[[笔记名\|显示名]]` | 带别名 | `[[DL\|深度学习]]` |
| `[[笔记名#标题]]` | 锚点链接 | `[[深度学习#CNN]]` |

### Callout

```markdown
> [!类型] 标题
内容
```

| 类型 | 使用场景 |
|------|----------|
| info | 一般信息 |
| warning | 警告提醒 |
| important | 重要内容 |
| tip | 技巧提示 |

### Frontmatter

```yaml
---
title: "论文标题"
tags: [CV, Generation]
date: 2026-02-02
status: reading
---
```

### Tags

```
#一级/二级/三级
#CV/Generation/Diffusion
```

### Embeds

```
![[笔记名]]
![[笔记名#标题]]
![[文件名.canvas]]
```

---

## Canvas (.canvas) 格式规范

参考 `json-canvas` 技能。

### 文件结构

```json
{
  "nodes": [],
  "edges": []
}
```

### 节点类型

| 类型 | 说明 | 用途 |
|------|------|------|
| text | 文本内容 | 标题、描述 |
| file | 文件引用 | 笔记、图片 |
| link | 外部链接 | URL |
| group | 容器 | 组织节点 |

### 颜色编码

| 颜色 | 代码 | 说明 |
|------|------|------|
| 红色 | "1" | 核心/重要 |
| 橙色 | "2" | 重要进展 |
| 黄色 | "3" | 扩展 |
| 绿色 | "4" | 应用 |

---

## Bases (.base) 格式规范

参考 `obsidian-bases` 技能。

### 视图类型

| 类型 | 说明 | 用途 |
|------|------|------|
| table | 表格视图 | 详细列表 |
| cards | 卡片视图 | 封面展示 |
| list | 列表视图 | 简洁列表 |

### 公式示例

```yaml
formulas:
  status_icon: 'if(status == "done", "✅", "📚")'
  days_ago: '((now() - date(date)) / 86400000).round(0)'
```

### 分组排序

```yaml
views:
  - type: table
    groupBy:
      property: status
    order:
      - file.name
      - date
```

---

## 参考

- **格式参考技能**：`skills/obsidian-markdown/SKILL.md`, `skills/json-canvas/SKILL.md`, `skills/obsidian-bases/SKILL.md`
- **原始参考项目**：`D:/work_project/my_project/Ref_pro/obsidian-skills/`
- **CLAUDE.md**：项目核心规则
