# 代码风格规范

本文档定义 Research Assistant 项目的代码风格规范，参考 `everything-claude-code` 项目。

---

## 不可变性原则（CRITICAL）

### 只读数据源

以下数据源**必须**被视为只读：

| 数据源 | 访问方式 | 约束 |
|--------|----------|------|
| Zotero | MCP 工具 | 只读查询，不能修改 |
| PLAN/references/ | Read 工具 | 参考模板，不可修改 |
| 参考项目 | Read 工具 | 只读参考，不可修改 |

### 不可变模式

**✅ GOOD**：
```python
# 使用不可变操作
new_content = content + append_text  # 创建新对象
items = existing_items + [new_item]  # 列表拼接
```

**❌ BAD**：
```python
# 直接修改可能影响其他引用
content += append_text
items.append(new_item)  # 原地修改
```

---

## 文件组织规范

### 项目目录结构

```
Research_Assistant/
├── .claude-plugin/      # 插件配置
├── skills/              # 技能文件（扁平化）
├── commands/            # 命令文件
├── hooks/               # Hooks 配置
├── rules/               # 规则文档（本文件所在目录）
├── PLAN/                # 项目规划
│   └── references/      # 参考模板（只读）
└── scripts/             # 辅助脚本
```

### 技能文件结构

```
skills/{skill-name}/
└── SKILL.md
```

- 每个技能一个独立目录
- 文件名固定为 `SKILL.md`
- 包含 YAML frontmatter

---

## 代码风格

### Python

**命名规范**：
- 函数/变量：`snake_case`
- 类名：`PascalCase`
- 常量：`UPPER_SNAKE_CASE`

**示例**：
```python
def search_papers(query: str) -> list[dict]:
    """搜索论文"""
    MAX_RESULTS = 10
    results = []
    # ...
    return results
```

### Bash

**命名规范**：
- 函数：`snake_case`
- 变量：`snake_case`
- 常量：`UPPER_SNAKE_CASE`

**路径格式**：
```bash
# Bash 工具使用正斜杠
path="C:/Users/Ahs/Documents"

# Read 工具使用双反斜杠（在 Python 字符串中）
path="C:\\Users\\Ahs\\Documents"
```

### JSON

**格式规范**：
- 使用 2 空格缩进
- 字符串使用双引号
- 必需字段：`name`, `description`, `version`

---

## 错误处理规范

### 基本原则

1. **明确失败原因**：提供清晰的错误信息
2. **提供解决建议**：告诉用户如何修复
3. **保持操作幂等**：重试不应产生副作用

### ✅ GOOD

```python
try:
    result = mcp__zotero__zotero_get_item_fulltext(item_key=item_key)
except Exception as e:
    print(f"[Error] 无法获取论文全文: {e}")
    print(f"[Suggestion] 尝试使用摘要代替")
    result = metadata.get("abstract", "摘要不可用")
```

### ❌ BAD

```python
try:
    result = mcp__zotero__zotero_get_item_fulltext(item_key=item_key)
except:
    result = ""  # 静默失败
```

---

## 输入验证规范

### 系统边界验证

| 边界 | 验证内容 |
|------|----------|
| 用户输入 | 路径合法性、命令安全性 |
| MCP 工具调用 | 参数类型、必填字段 |
| 文件操作 | 路径存在性、权限 |

### ✅ GOOD

```python
# 验证路径
if not item_key:
    raise ValueError("[Error] item_key 是必需参数")

# 验证 MCP 工具返回
if not result.get("success", True):
    logger.warning(f"MCP 工具返回失败: {result}")
```

### ❌ BAD

```python
# 直接使用，未验证
result = some_tool(user_input)  # user_input 未验证
```

---

## 代码质量检查清单

在提交代码前，确认以下检查项：

### 格式检查
- [ ] YAML frontmatter 正确（name, description, version）
- [ ] 缩进一致（使用空格，不使用 Tab）
- [ ] 行尾无多余空格
- [ ] JSON 格式正确

### 内容检查
- [ ] 代码示例正确可运行
- [ ] GOOD/BAD 对比清晰
- [ ] 错误处理完整

### 安全检查
- [ ] 无硬编码敏感信息
- [ ] 路径操作经过验证
- [ ] 命令注入风险已检查

---

## 参考项目

- **参考项目**：`D:\work_project\my_project\Ref_pro\everything-claude-code\rules\coding-style.md`
