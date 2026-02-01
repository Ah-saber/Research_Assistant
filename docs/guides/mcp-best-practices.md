# Zotero MCP 使用最佳实践

## 概述

本文档总结了在使用 Zotero MCP 工具时遇到的问题和解决方案，供开发Skills时参考。

---

## 常见问题

### 1. 全文超过Token限制

**问题表现**：
```
Error: result (122,415 characters) exceeds maximum allowed tokens
Output has been saved to: C:\Users\{用户}\.claude\projects\{项目ID}\tool-results\mcp-zotero-zotero_get_item_fulltext-{时间戳}.txt
```

**原因**：
- 论文全文通常超过100KB，超过单次返回的token限制
- 系统会自动将内容保存到本地文件

**解决方案**：

**方案1：分页读取（推荐）**
```python
# 使用Read工具分段读取
Read(file_path, offset=1, limit=500)    # 第1批
Read(file_path, offset=501, limit=500)  # 第2批
# 继续直到读取完整内容
```

**方案2：降级策略**
```python
# 如果全文无法读取，基于摘要生成
metadata = zotero_get_item_metadata(item_key)
if fulltext_exceeds_limit:
    content = metadata["abstract"]
    quality = "basic"  # 明确标注质量级别
```

**方案3：摘要优先**
```python
# 先尝试摘要，摘要足够则不读取全文
abstract = metadata["abstract"]
if len(abstract) > 500:  # 摘要足够详细
    use_abstract_instead()
```

---

### 2. Windows路径转义问题

**问题表现**：
```
cat: 'C:\Users\...\file.txt': No such file or directory
Read tool: File does not exist
```

**原因**：
- Windows路径使用反斜杠 `\`，在字符串中需要转义
- 不同工具对路径格式的处理方式不同

**解决方案**：

| 工具 | 正确格式 | 示例 |
|------|----------|------|
| **Bash** | 正斜杠 `/` | `"C:/Users/Ahs/file.txt"` |
| **Read** | 双反斜杠 `\\` | `"C:\\Users\\Ahs\\file.txt"` |
| **变量传递** | 避免直接使用 | 重新构建路径 |

**代码示例**：
```python
# 错误
path = "C:\Users\Ahs\file.txt"  # \U 会被解析为转义字符

# 正确
bash_path = "C:/Users/Ahs/file.txt"
read_path = "C:\\Users\\Ahs\\file.txt"
raw_path = r"C:\Users\Ahs\file.txt"  # 使用raw string
```

---

### 3. 论文无注释

**问题表现**：
```
No annotations found for item: [论文标题]
```

**原因**：
- 用户未在Zotero Reader中添加高亮或笔记
- PDF附件可能未关联或损坏

**解决方案**：
```python
# 1. 先检查是否有注释
result = zotero_get_annotations(item_key)
if "No annotations found" in result:
    # 2. 友好提示
    prompt("该论文暂无PDF注释，您可以：\n"
           "- 在Zotero Reader中添加高亮/笔记\n"
           "- 继续使用摘要创建笔记")
    # 3. 不阻塞流程，继续执行
    return None
```

---

### 4. 注释数据量过大

**问题表现**：
```
Error: result (605,527 characters) exceeds maximum allowed tokens
```

**原因**：
- `zotero_get_annotations()` 不带参数时返回所有注释
- 整个Zotero库的注释可能超过60万字符

**解决方案**：

**方案1：按论文筛选（推荐）**
```python
# 获取单篇论文的注释
zotero_get_annotations(item_key="THJPBR5X")
```

**方案2：使用limit**
```python
# 限制返回数量
zotero_get_annotations(limit=20)
```

**方案3：分批处理**
```python
# 按collection分批获取
collections = zotero_get_collections()
for col in collections:
    annotations = get_annotations_by_collection(col)
```

---

## 通用最佳实践

### 错误处理模式

```python
# 1. 优先使用元数据（总是成功）
metadata = zotero_get_item_metadata(item_key)
if not metadata:
    return error("论文不存在")

# 2. 尝试获取全文（可能超限）
try:
    fulltext = zotero_get_item_fulltext(item_key)
except TokenLimitError:
    # 降级到摘要
    fulltext = metadata.get("abstract", "")
    log("使用摘要替代全文")

# 3. 检查注释（可能为空）
annotations = zotero_get_annotations(item_key)
if "No annotations" in annotations:
    annotations = None

# 4. 生成内容
generate_note(metadata, fulltext, annotations)
```

### 质量标注

明确告知用户数据来源的质量：
- `full` - 完整全文
- `abstract` - 仅基于摘要
- `partial` - 部分全文（分页读取）

### 用户沟通

遇到限制时：
1. **明确说明问题**：告知用户具体限制
2. **提供替代方案**：给出可行的替代选项
3. **不阻塞流程**：尽可能继续完成核心功能

---

## 工具速查表

| 工具 | 用途 | 限制 | 建议 |
|------|------|------|------|
| `zotero_search_items` | 关键词搜索 | 适中 | 优先使用，返回元数据 |
| `zotero_semantic_search` | 语义搜索 | 适中 | 找相关论文的好方法 |
| `zotero_get_item_metadata` | 获取元数据 | 低 | **总是成功**，优先调用 |
| `zotero_get_item_fulltext` | 获取全文 | **高** | 可能超限，准备降级 |
| `zotero_get_annotations` | 获取注释 | **高** | 必须指定item_key |
| `zotero_get_collections` | 获取集合 | 低 | 获取目录结构 |

---

## 调试技巧

### 1. 查看保存的大文件
```bash
# 列出最近的tool-results
ls -la "C:/Users/Ahs/.claude/projects/D--work-project-my_project-Research-Assistant/e5dd60e9-3cc9-4bee-8c25-b88ebaf2e6fe/tool-results/"
```

### 2. 分段读取大文件
```bash
# 读取前N行
head -500 "file_path"

# 搜索特定内容
grep "keyword" "file_path"
```

### 3. 验证路径格式
```python
# 测试路径是否正确
import os
os.path.exists(path)  # 验证路径存在性
```

---

## 更新日志

| 日期 | 更新内容 |
|------|----------|
| 2026-01-26 | 初始版本，总结Phase 4测试问题 |
