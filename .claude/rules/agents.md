# Agents 规则

本文档说明 Agent 的定义、使用场景，以及 Research Assistant 项目的 Agent 策略。

---

## 什么是 Agent

Agent 是 Claude Code 中的高级自动化组件，用于处理复杂的多步骤任务。

**Agent vs Skill**：
- **Skill**：封装特定工作流，通过自然语言或命令触发
- **Agent**：自主决策，可以使用多个工具，具有更大的自主权

---

## Research Assistant 的 Agent 策略

### 当前状态：按需使用 Agents

本项目采用**选择性 Agents** 策略，为特定复杂场景创建专业 Agents：

1. **大量上下文场景**：需要处理多篇论文/笔记，用户只看结果
2. **多步骤协调**：需要调用多个 Skills 完成复杂任务
3. **自主决策**：需要根据分析结果动态调整策略

**Agent 与 Skill 的关系**：
- **Skill**：封装特定工作流，通过自然语言或命令触发
- **Agent**：明确声明并调用 Skill，获得专业能力，自主协调多步骤任务

**验证**：`.claude-plugin/plugin.json` 中声明了 4 个 Agents

---

## 已实现的 Agents

### 1. literature-synthesizer（文献综合分析器）

**文件**：`./agents/literature-synthesizer.md`

**职责**：分析多篇论文并生成全面的文献综述

**调用的 Skills**：
- paper-search（检索相关论文）
- paper-summary（获取论文摘要）
- paper-notes（创建论文笔记）
- annotation-extract（提取PDF注释）

**使用场景**：
- 用户请求文献综述或调查
- 比较多篇论文的方法
- 识别研究趋势和空白
- 大量文献阅读后生成摘要

---

### 2. note-organizer（笔记智能整理代理）

**文件**：`./agents/note-organizer.md`

**职责**：分析笔记语义关系，生成智能整理方案

**调用的 Skills**：
- note-analyze（分析笔记结构）
- note-organize（执行笔记整理）
- note-link（建立笔记链接）
- note-standardize（标准化笔记格式）

**使用场景**：
- 笔记智能整理
- 发现深层语义关联
- 建立笔记间链接
- 标准化笔记格式

---

### 3. research-note-generator（研究笔记生成器）

**文件**：`./agents/research-note-generator.md`

**职责**：为论文创建包含概率框架分析的完整笔记

**调用的 Skills**：
- paper-notes（创建论文笔记）
- note-template（创建笔记模板）
- obsidian-markdown（Markdown格式参考）

**使用场景**：
- 阅读论文后自动生成笔记
- 确保笔记符合人设要求的六段式结构
- 包含概率框架分析模块

---

### 4. note-visualizer（笔记可视化综合代理）

**文件**：`./agents/note-visualizer.md`

**职责**：阅读多篇笔记，生成可视化图谱和仪表盘

**调用的 Skills**：
- note-analyze, note-link（分析和链接）
- paper-graph, idea-map, knowledge-canvas（Canvas可视化）
- paper-dashboard, idea-tracker, research-dashboard（Bases仪表盘）
- json-canvas, obsidian-bases（格式参考）

**使用场景**：
- 多篇笔记的可视化处理
- 生成知识画布（Canvas）
- 创建进度追踪仪表盘
- 展示笔记间的语义关联

---

## 将来如需添加更多 Agents

如果将来需要添加 Agents，遵循以下规范：

### 1. 在 plugin.json 中显式枚举

```json
{
  "agents": [
    "./agents/paper-analyzer.md",
    "./agents/note-organizer.md"
  ]
}
```

❌ **错误**：不能使用目录路径 `"./agents/"`

### 2. Agent 命名规范

- 文件名：kebab-case（如 `paper-analyzer.md`）
- 描述：简明扼要，说明 Agent 的职责范围

### 3. Agent 适用场景

| 场景 | 适用性 | 说明 |
|------|--------|------|
| 文献批量处理 | ✅ | 批量分析多篇论文，需要自主决策 |
| 笔记智能整理 | ✅ | 分析笔记语义关系，自主决定整理策略 |
| Zotero 查询 | ❌ | 明确的单步任务，Skill 足够 |
| 格式标准化 | ❌ | 规则明确，Skill 足够 |
| Canvas 生成 | ❌ | 确定性的可视化任务，Skill 足够 |

### 4. Agent 设计原则

1. **单一职责**：每个 Agent 专注一个领域
2. **明确边界**：清楚定义 Agent 的职责范围
3. **可组合**：Agents 之间可以协作
4. **可测试**：Agent 行为可验证

---

## 参考资源

- **Claude Code 文档**：https://code.claude.com/docs/en/agents
- **已实现的 Agents**：`.claude/agents/` 目录
