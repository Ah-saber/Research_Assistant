# Research Assistant 技能系统升级实施计划

**版本**: v1.0
**创建日期**: 2026-02-01
**状态**: 计划阶段

---

## 一、升级概述

### 1.1 升级目标

基于 `everything-claude-code` 参考项目，对 Research Assistant 的技能系统进行标准化升级：

1. **格式标准化**：统一的技能文件格式（YAML frontmatter + SKILL.md）
2. **插件配置**：创建 `plugin.json` 支持插件化分发
3. **快速参考**：在技能中添加 GOOD/BAD 对比示例和速查表
4. **Hooks 自动化**：实现自动化触发机制
5. **自我进化**：支持从会话中提取模式的能力

### 1.2 语言规范

- **编写语言**：简体中文
- **技能/命令名称**：英文（kebab-case）
- **具体内容**：中文

### 1.3 目标架构

```
Research_Assistant/
├── .claude-plugin/
│   ├── plugin.json          # 新建：插件清单
│   └── marketplace.json     # 新建：市场配置（可选）
├── skills/                  # 重构：扁平化 + 标准化
│   ├── note-analyze/        # 从 skills/notes/ 移动
│   │   └── SKILL.md         # 重命名：从 .skill.md
│   ├── note-standardize/
│   │   └── SKILL.md
│   ├── paper-notes/
│   │   └── SKILL.md
│   └── ...                  # 其他17个技能
├── commands/                # 新建：快捷命令
│   ├── search-paper.md
│   ├── standardize-notes.md
│   └── capture-idea.md
├── hooks/                   # 新建：自动化触发
│   └── hooks.json
└── rules/                   # 新建：模块化规则
    ├── agents.md
    ├── coding-style.md
    └── hooks.md
```

---

## 二、技能文件格式规范

### 2.1 标准 SKILL.md 格式

```markdown
---
name: skill-name
description: Brief description of what this skill does
version: 1.0.0
---

# 技能名称（中文）

简短描述（1-2句话）

## When to Activate（何时启用）

- 触发条件1
- 触发条件2
- 触发条件3

## 核心功能

### 功能1
- **用途**：说明
- **语法**：格式
- **场景**：使用场景

## GOOD vs BAD（对比示例）

### ✅ GOOD
```python
# 正确示例
```

### ❌ BAD
```python
# 错误示例
```

## 工作流程

### 步骤1：描述
[详细步骤]

## 快速参考表

| 场景 | 命令 | 说明 |
|------|------|------|
| 场景1 | 命令1 | 说明1 |
```

### 2.2 与现有格式的差异

| 项目 | 现有格式 | 新格式 |
|------|----------|--------|
| 文件名 | `xxx.skill.md` | `SKILL.md` |
| YAML frontmatter | 无 | 必需 |
| When to Activate | "触发词"章节 | "When to Activate"章节 |
| 对比示例 | 无 | GOOD/BAD对比 |
| 快速参考 | 无 | 速查表 |

---

## 三、plugin.json 配置

### 3.1 标准 plugin.json 格式

```json
{
  "name": "research-assistant",
  "version": "1.0.0",
  "description": "Personal academic assistant for computer vision scholars",
  "author": {
    "name": "Your Name"
  },
  "homepage": "https://github.com/yourusername/Research_Assistant",
  "repository": "https://github.com/yourusername/Research_Assistant",
  "license": "MIT",
  "keywords": ["research-assistant", "zotero", "obsidian", "academic"],
  "skills": ["./skills/"],
  "commands": ["./commands/"],
  "agents": []
}
```

### 3.2 关键约束（重要！）

参考 `PLUGIN_SCHEMA_NOTES.md`：

1. **version 字段必需**
2. **路径必须是数组**：`skills`、`commands` 必须是数组
3. **不添加 hooks 字段**：`hooks/hooks.json` 自动加载，手动添加会导致重复错误
4. **agents 必须显式枚举**：如果使用 agents，不能使用目录路径

---

## 四、分阶段实施计划

### 阶段1：基础架构（1天）

**目标**：建立标准化的目录结构和配置

**文件清单**：
- 新建：`.claude-plugin/plugin.json`
- 新建：`.claude-plugin/marketplace.json`（可选）
- 新建：`commands/.gitkeep`
- 新建：`hooks/.gitkeep`
- 新建：`hooks/hooks.json`
- 新建：`rules/.gitkeep`

---

### 阶段2：Notes Skills 标准化（2天）

**优先级**：P0（最高）

**技能清单**（5个）：
1. `note-analyze`
2. `note-organize`
3. `note-template`
4. `note-link`
5. `note-standardize`

---

### 阶段3：Reading Skills 标准化（1天）

**优先级**：P1

**技能清单**（4个）：
1. `paper-search`
2. `paper-summary`
3. `annotation-extract`
4. `paper-notes`

---

### 阶段4：Ideas + Visualization + Dashboard（1天）

**优先级**：P2

**技能清单**（9个）：
- Ideas（3个）：`idea-capture`, `idea-organize`, `idea-review`
- Visualization（3个）：`paper-graph`, `idea-map`, `knowledge-canvas`
- Dashboard（3个）：`paper-dashboard`, `idea-tracker`, `research-dashboard`

---

### 阶段5：Commands 完善 + 文档更新（1天）

**Commands 完整清单**：
1. `search-paper.md`
2. `create-paper-note.md`
3. `standardize-notes.md`
4. `analyze-notes.md`
5. `organize-notes.md`
6. `link-notes.md`
7. `capture-idea.md`
8. `review-ideas.md`
9. `organize-ideas.md`
10. `paper-dashboard.md`
11. `idea-dashboard.md`

---

### 阶段6：Rules 模块化（1天）

**新建 rules/ 目录文件**：
- `rules/agents.md`
- `rules/coding-style.md`
- `rules/hooks.md`
- `rules/workflow.md`
- `rules/zotero-integration.md`

---

### 阶段7：自我进化实现（2-3天）

参考 `continuous-learning-v2` 技能：
- 观察会话活动
- 提取可重用模式
- 生成 atomic instincts
- 聚类进化为 skills/commands

---

## 五、关键文件路径

### 5.1 需要修改的文件

| 文件 | 操作 | 说明 |
|------|------|------|
| `skills/notes/*.skill.md` | 移动+重命名 | 移至 skills/{name}/SKILL.md |
| `skills/reading/*.skill.md` | 移动+重命名 | 移至 skills/{name}/SKILL.md |
| `skills/ideas/*.skill.md` | 移动+重命名 | 移至 skills/{name}/SKILL.md |
| `skills/visualization/*.skill.md` | 移动+重命名 | 移至 skills/{name}/SKILL.md |
| `skills/dashboard/*.skill.md` | 移动+重命名 | 移至 skills/{name}/SKILL.md |
| `CLAUDE.md` | 修改 | 更新技能路径和说明 |
| `README.md` | 修改 | 更新项目说明 |

### 5.2 需要新建的文件

| 文件 | 说明 |
|------|------|
| `.claude-plugin/plugin.json` | 插件配置清单 |
| `.claude-plugin/marketplace.json` | 市场配置（可选）|
| `hooks/hooks.json` | Hooks 自动化配置 |
| `commands/*.md` | 命令文件（约11个）|
| `rules/*.md` | 模块化规则（约5个）|
| `skills/continuous-learning/SKILL.md` | 自我进化技能 |

---

## 六、验证标准

### 6.1 格式验证

- [ ] 所有技能文件名为 `SKILL.md`
- [ ] 所有技能包含 YAML frontmatter（name, description, version）
- [ ] 所有技能包含 "When to Activate" 章节
- [ ] 所有技能包含 GOOD/BAD 对比示例
- [ ] 所有技能末尾包含快速参考表

### 6.2 功能验证

- [ ] plugin.json 通过验证
- [ ] 命令可以正确触发：`/research-assistant:xxx`
- [ ] 技能可以自动匹配：自然语言描述
- [ ] Hooks 正确触发：PostToolWrite、PostToolEdit、SessionEnd

---

## 七、进度跟踪

**进展文档**：`PLAN/PRO_UPD.md`

各阶段完成后更新 `PRO_UPD.md`。
