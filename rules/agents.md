# Agents 规则

本文档说明 Agent 的定义、使用场景，以及 Research Assistant 项目的 Agent 策略。

---

## 什么是 Agent

Agent 是 Claude Code 中的高级自动化组件，用于处理复杂的多步骤任务。

**Agent vs Skill**：
- **Skill**：封装特定工作流，通过自然语言或命令触发
- **Agent**：自主决策，可以使用多个工具，具有更大的自主权

**参考项目**：`everything-claude-code` 使用了多个专业 agents（build-error-resolver, code-reviewer, go-reviewer 等）

---

## Research Assistant 的 Agent 策略

### 当前状态：不使用 Agents

本项目**当前不使用** Agents，原因：

1. **工作流特性**：本项目的主要功能是文献阅读、笔记整理、Idea 管理，这些都是明确的、结构化的任务
2. **Skills 已足够**：18 个自定义 Skills 已覆盖所有核心功能
3. **避免过度设计**：Agent 的自主性在本项目中不是必需的

**验证**：`.claude-plugin/plugin.json` 中未声明 `agents` 字段

---

## 将来如需使用 Agents

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

参考 `everything-claude-code` 的 Agent 设计：

1. **单一职责**：每个 Agent 专注一个领域
2. **明确边界**：清楚定义 Agent 的职责范围
3. **可组合**：Agents 之间可以协作
4. **可测试**：Agent 行为可验证

---

## 参考

- **参考项目**：`D:\work_project\my_project\Ref_pro\everything-claude-code\agents\`
- **Claude Code 文档**：https://code.claude.com/docs/en/agents
