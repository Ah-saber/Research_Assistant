# Hooks 使用说明

本文档说明 Research Assistant 项目的 Hooks 机制和使用规范。

---

## 什么是 Hooks

Hooks 是 Claude Code 的自动化触发机制，可以在特定事件发生时执行自定义命令。

---

## Hooks 触发时机

| Hook 类型 | 触发时机 | 用途 |
|-----------|----------|------|
| PreToolUse | 工具执行前 | 检查、验证、阻止 |
| PostToolUse | 工具执行后 | 格式化、检查、日志 |
| PreCompact | 上下文压缩前 | 保存状态 |
| SessionStart | 会话开始 | 加载上下文 |
| Stop | 每次响应后 | 检查状态 |
| SessionEnd | 会话结束 | 持久化、评估 |

---

## Hooks 匹配规则

### Matcher 语法

```javascript
// 匹配特定工具
tool == "Bash"

// 匹配工具 + 输入模式
tool == "Bash" && tool_input.command matches "python"

// 匹配文件路径
tool_input.file_path matches "\\.md$"

// 组合条件
tool == "Edit" && tool_input.file_path matches "\\.md$" && tool_input.file_path matches "C:\\\\Note\\\\MyNote_Obs\\\\**"
```

### 正则表达式示例

| 模式 | 匹配内容 |
|------|----------|
| `\\\\.md$` | 以 .md 结尾 |
| `python.*test` | python 后跟 test |
| `C:\\\\\\\\Note\\\\\\\\MyNote_Obs\\\\\\\\**` | Obsidian Vault 路径 |

---

## Hooks 编写规范

### 基本结构

```json
{
  "hooks": {
    "HookType": [
      {
        "matcher": "条件表达式",
        "hooks": [
          {
            "type": "command",
            "command": "node -e \"...\""
          }
        ],
        "description": "说明"
      }
    ]
  }
}
```

### Command 类型

| 类型 | 说明 | 示例 |
|------|------|------|
| command | 执行 shell 命令 | `node -e "..."` |
| suggest | 建议操作（未来） | - |

### 可选参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| async | 异步执行 | false |
| timeout | 超时时间（秒） | 30 |

---

## Research Assistant 的 Hooks

当前配置的 Hooks（见 `hooks/hooks.json`）：

### PreToolUse
1. 警告创建随机 .md 文件
2. 提醒激活 Python 虚拟环境
3. 警告编辑关键配置文件

### PostToolUse
1. 检查 Wikilink 格式
2. 建议笔记标准化

### Stop
1. 记录响应完成

### SessionEnd
1. 持久化会话状态
2. 建议运行 /learn

---

## 常见场景示例

### 场景1：阻止危险操作

```json
{
  "matcher": "tool == \"Bash\" && tool_input.command matches \"rm -rf\"",
  "hooks": [
    {
      "type": "command",
      "command": "node -e \"console.error('[Hook] DANGEROUS: rm -rf command blocked')\""
    }
  ]
}
```

### 场景2：自动格式化

```json
{
  "matcher": "tool == \"Edit\" && tool_input.file_path matches \"\\\\.py$\"",
  "hooks": [
    {
      "type": "command",
      "command": "black --quiet \"{{tool_input.file_path}}\""
    }
  ]
}
```

### 场景3：检查约束

```json
{
  "matcher": "tool == \"Write\" && tool_input.file_path matches \"\\\\.md$\"",
  "hooks": [
    {
      "type": "command",
      "command": "node -e \"console.log('[Hook] Markdown file created')\""
    }
  ]
}
```

---

## 调试 Hooks

### 查看输出

Hook 的输出会显示在 Claude Code 控制台：
- `console.error()` → 红色警告
- `console.log()` → 普通日志

### 测试 Hook

1. 修改 `hooks/hooks.json`
2. 触发匹配条件
3. 检查输出

---

## 参考资源

- **Claude Code 文档**：https://code.claude.com/docs/en/hooks-guide
- **当前配置**：`hooks/hooks.json`
