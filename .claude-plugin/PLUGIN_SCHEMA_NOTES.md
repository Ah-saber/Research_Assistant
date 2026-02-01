# Plugin Schema 约束说明

本文档记录 `plugin.json` 的重要约束，参考 `everything-claude-code` 项目。

---

## 必需字段

### version（必需）
```json
{
  "version": "1.0.0"
}
```
- 缺少此字段会导致插件加载失败

---

## 路径配置

### skills 和 commands 必须是数组
```json
{
  "skills": ["./skills/"],     // ✅ 正确：数组格式
  "commands": ["./commands/"]  // ✅ 正确：数组格式
}
```

❌ **错误示例**：
```json
{
  "skills": "./skills/"        // ❌ 错误：字符串格式
}
```

---

## Hooks 配置

### 不添加 hooks 字段
`hooks/hooks.json` 会自动加载，无需在 `plugin.json` 中声明。

❌ **错误示例**：
```json
{
  "hooks": ["./hooks/"]        // ❌ 错误：会导致重复加载
}
```

---

## Agents 配置

### 本项目不使用 agents
本项目不需要 agents 功能，不添加此字段。

如果将来需要使用 agents，必须显式枚举每个 agent：

```json
{
  "agents": [                  // ✅ 正确：显式枚举
    "./agents/review.md",
    "./agents/plan.md"
  ]
}
```

❌ **错误示例**：
```json
{
  "agents": ["./agents/"]      // ❌ 错误：不能使用目录路径
}
```

---

## 完整示例

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
  "skills": ["./skills/", "./commands/"]
}
```

**注意**：没有 `hooks` 和 `agents` 字段
